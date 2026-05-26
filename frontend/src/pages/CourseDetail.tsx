import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../store';
import { fetchCourseDetail, fetchCourseLessons } from '../store/coursesSlice';
import { enrollCourse } from '../store/progressSlice';
import { toast } from 'react-toastify';

const CourseDetail: React.FC = () => {
  const { slug } = useParams<{ slug: string }>();
  const dispatch = useAppDispatch();
  const { currentCourse, lessons, loading } = useAppSelector((state) => state.courses);
  const { progresses } = useAppSelector((state) => state.progress);
  const [enrolling, setEnrolling] = useState(false);

  useEffect(() => {
    if (slug) {
      dispatch(fetchCourseDetail(slug));
      dispatch(fetchCourseLessons(slug));
    }
  }, [dispatch, slug]);

  const progress = progresses.find((p) => p.course_slug === slug);
  const isEnrolled = !!progress;

  const handleEnroll = async () => {
    if (!currentCourse) return;
    setEnrolling(true);
    const result = await dispatch(enrollCourse(currentCourse.id));
    setEnrolling(false);
    if (enrollCourse.fulfilled.match(result)) {
      toast.success('Successfully enrolled in the course!');
    } else {
      toast.error('Failed to enroll. Please try again.');
    }
  };

  if (loading || !currentCourse) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="space-y-8">
      {/* Header */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-2xl p-8 text-white">
        <Link to="/courses" className="text-primary-200 hover:text-white text-sm mb-2 inline-block">
          ← Back to Courses
        </Link>
        <h1 className="text-3xl font-bold">{currentCourse.title}</h1>
        <p className="mt-2 text-primary-100">{currentCourse.description}</p>
        <div className="mt-4 flex items-center space-x-6 text-sm">
          <span className="bg-white/20 px-3 py-1 rounded-full">
            {currentCourse.difficulty}
          </span>
          <span>📚 {currentCourse.lesson_count || currentCourse.total_lessons} lessons</span>
          <span>⏱ {currentCourse.estimated_hours} hours</span>
        </div>

        {isEnrolled && progress && (
          <div className="mt-4">
            <div className="flex justify-between text-sm mb-1">
              <span>Progress</span>
              <span>{progress.progress_percentage}%</span>
            </div>
            <div className="w-full bg-white/20 rounded-full h-2">
              <div
                className="bg-white rounded-full h-2 transition-all"
                style={{ width: `${progress.progress_percentage}%` }}
              ></div>
            </div>
          </div>
        )}
      </div>

      {/* Enroll Button */}
      {!isEnrolled && (
        <div className="text-center">
          <button
            onClick={handleEnroll}
            disabled={enrolling}
            className="btn-primary text-lg px-8 py-3"
          >
            {enrolling ? 'Enrolling...' : 'Enroll in This Course'}
          </button>
        </div>
      )}

      {/* Lessons List */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Course Content</h2>
        <div className="space-y-3">
          {lessons.map((lesson) => (
            <div
              key={lesson.id}
              className={`card flex items-center justify-between ${
                !isEnrolled && !lesson.is_free ? 'opacity-60' : ''
              }`}
            >
              <div className="flex items-center space-x-4">
                <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
                  <span className="text-primary-700 font-bold">{lesson.order}</span>
                </div>
                <div>
                  <h3 className="font-semibold text-gray-900">{lesson.title}</h3>
                  <div className="flex items-center space-x-3 text-sm text-gray-500">
                    <span>
                      {lesson.lesson_type === 'reading' && '📖'}
                      {lesson.lesson_type === 'video' && '🎥'}
                      {lesson.lesson_type === 'quiz' && '📝'}
                      {lesson.lesson_type === 'practice' && '✏️'}
                      {' '}{lesson.lesson_type}
                    </span>
                    <span>⏱ {lesson.duration_minutes} min</span>
                    {lesson.is_free && (
                      <span className="bg-green-100 text-green-800 text-xs px-2 py-0.5 rounded-full">
                        Free
                      </span>
                    )}
                  </div>
                </div>
              </div>

              {(isEnrolled || lesson.is_free) ? (
                <Link
                  to={`/lessons/${lesson.id}`}
                  className="btn-primary text-sm"
                >
                  Start Lesson
                </Link>
              ) : (
                <span className="text-gray-400 text-sm">🔒 Enroll to access</span>
              )}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default CourseDetail;
