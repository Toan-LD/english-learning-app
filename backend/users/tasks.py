"""
Celery tasks for the users app.
"""
import logging
from celery import shared_task
from django.utils import timezone

logger = logging.getLogger(__name__)


@shared_task(bind=True, max_retries=3)
def send_daily_learning_reminder(self):
    """Send daily learning reminders to active users."""
    from .models import User

    today = timezone.now().date()
    users = User.objects.filter(
        is_active=True,
        is_notification_enabled=True,
    )

    notified_count = 0
    for user in users:
        if user.last_active_date and user.last_active_date < today:
            days_inactive = (today - user.last_active_date).days
            if days_inactive >= 1:
                logger.info(
                    f"Reminder for {user.email}: "
                    f"inactive for {days_inactive} day(s)"
                )
                notified_count += 1

    logger.info(f"Daily reminder task completed. Notified {notified_count} users.")
    return {'notified_count': notified_count}


@shared_task
def update_user_streak(user_id: int):
    """Update user streak based on daily activity."""
    from .models import User

    try:
        user = User.objects.get(id=user_id)
        today = timezone.now().date()

        if user.last_active_date == today:
            return {'message': 'Already active today'}

        if user.last_active_date and (today - user.last_active_date).days == 1:
            user.streak_days += 1
        else:
            user.streak_days = 1

        user.last_active_date = today
        user.save(update_fields=['streak_days', 'last_active_date'])
        return {'streak_days': user.streak_days}

    except User.DoesNotExist:
        logger.error(f"User with id {user_id} not found")
        return {'error': 'User not found'}
