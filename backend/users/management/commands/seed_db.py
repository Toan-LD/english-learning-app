"""
Management command to seed the database with sample data.
"""
from django.core.management.base import BaseCommand
from vocabulary.models import Word
from courses.models import Course, Lesson
from quiz.models import Quiz, Question
from seed_data.seed_words import SEED_WORDS
from seed_data.seed_courses import SEED_COURSES


class Command(BaseCommand):
    help = 'Seed the database with sample words, courses, and quizzes'

    def handle(self, *args, **options):
        self.stdout.write('Seeding database...')

        # Seed words
        self._seed_words()

        # Seed courses and lessons
        self._seed_courses()

        # Seed quizzes
        self._seed_quizzes()

        self.stdout.write(self.style.SUCCESS('Database seeded successfully!'))

    def _seed_words(self):
        """Seed 50 vocabulary words."""
        created_count = 0
        for word_data in SEED_WORDS:
            word, created = Word.objects.get_or_create(
                word=word_data['word'],
                defaults={
                    'phonetic': word_data['phonetic'],
                    'part_of_speech': word_data['part_of_speech'],
                    'definition': word_data['definition'],
                    'definition_vi': word_data['definition_vi'],
                    'example_sentence': word_data['example_sentence'],
                    'example_sentence_vi': word_data['example_sentence_vi'],
                    'synonym': word_data['synonym'],
                    'antonym': word_data['antonym'],
                    'difficulty': word_data['difficulty'],
                }
            )
            if created:
                created_count += 1
        self.stdout.write(f'  Created {created_count} words (total: {len(SEED_WORDS)})')

    def _seed_courses(self):
        """Seed 3 courses with 5 lessons each."""
        for course_data in SEED_COURSES:
            lessons_data = course_data.pop('lessons')
            course, created = Course.objects.get_or_create(
                slug=course_data['slug'],
                defaults={
                    'title': course_data['title'],
                    'description': course_data['description'],
                    'difficulty': course_data['difficulty'],
                    'estimated_hours': course_data['estimated_hours'],
                    'total_lessons': len(lessons_data),
                }
            )
            if created:
                for lesson_data in lessons_data:
                    Lesson.objects.get_or_create(
                        course=course,
                        slug=lesson_data['slug'],
                        defaults={
                            'title': lesson_data['title'],
                            'content': lesson_data['content'],
                            'lesson_type': lesson_data['lesson_type'],
                            'order': lesson_data['order'],
                            'duration_minutes': lesson_data['duration_minutes'],
                            'is_free': lesson_data['is_free'],
                        }
                    )
                self.stdout.write(f'  Created course: {course.title} with {len(lessons_data)} lessons')
            else:
                self.stdout.write(f'  Course already exists: {course.title}')

    def _seed_quizzes(self):
        """Seed quizzes for each course."""
        words = list(Word.objects.all()[:20])
        if len(words) < 10:
            self.stdout.write('  Not enough words to create quizzes')
            return

        for course_data in SEED_COURSES:
            try:
                course = Course.objects.get(slug=course_data['slug'])
            except Course.DoesNotExist:
                continue

            quiz, created = Quiz.objects.get_or_create(
                title=f"{course.title} - Quiz",
                defaults={
                    'description': f"Test your knowledge from {course.title}",
                    'quiz_type': 'multiple_choice',
                    'time_limit': 300,
                    'passing_score': 70,
                }
            )

            if created:
                # Create 5 questions for each quiz
                for i, word in enumerate(words[:5]):
                    options = [
                        word.definition,
                        words[(i + 1) % len(words)].definition,
                        words[(i + 2) % len(words)].definition,
                        words[(i + 3) % len(words)].definition,
                    ]
                    Question.objects.create(
                        quiz=quiz,
                        word=word,
                        question_text=f"What is the definition of '{word.word}'?",
                        question_type='multiple_choice',
                        correct_answer=word.definition,
                        options=options,
                        points=1,
                        order=i + 1,
                        explanation=f"The word '{word.word}' means: {word.definition}",
                    )
                self.stdout.write(f'  Created quiz for: {course.title}')
