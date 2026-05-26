import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../store';
import { fetchCourses } from '../store/coursesSlice';

const difficultyColors: Record<string, string> = {
  beginner: 'bg-green-100 text-green-800',
  intermediate: 'bg-yellow-100 text-yellow-800',
  advanced: 'bg-red-100 text-red-800',
};

const CourseList: React.FC = () => {
  const dispatch = useAppDispatch();
  const { courses, loading, error } = useAppSelector((state) => state.courses);

  useEffect(() => {
    dispatch(fetchCourses(undefined));
  }, [dispatch]);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-center py-12">
        <p className="text-red-600">{error}</p>
      </div>
    );
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Courses</h1>
        <p className="text-gray-600 mt-1">
          Choose a course that matches your level and start learning
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {courses.map((course) => (
          <Link
            key={course.id}
            to={`/courses/${course.slug}`}
            className="card hover:shadow-lg transition-shadow duration-200 group"
          >
            <div className="aspect-video bg-gradient-to-br from-primary-100 to-primary-200 rounded-lg mb-4 flex items-center justify-center">
              <span className="text-5xl">
                {course.difficulty === 'beginner' && '📗'}
                {course.difficulty === 'intermediate' && '📙'}
                {course.difficulty === 'advanced' && '📕'}
              </span>
            </div>

            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span
                  className={`text-xs font-semibold px-2.5 py-1 rounded-full ${
                    difficultyColors[course.difficulty] || 'bg-gray-100 text-gray-800'
                  }`}
                >
                  {course.difficulty}
                </span>
                <span className="text-sm text-gray-500">
                  {course.lesson_count || course.total_lessons} lessons
                </span>
              </div>

              <h3 className="text-lg font-semibold text-gray-900 group-hover:text-primary-600 transition">
                {course.title}
              </h3>

              <p className="text-sm text-gray-600 line-clamp-2">
                {course.description}
              </p>

              <div className="flex items-center text-sm text-gray-500 pt-2">
                <span>⏱ {course.estimated_hours} hours</span>
              </div>
            </div>
          </Link>
        ))}
      </div>

      {courses.length === 0 && (
        <div className="text-center py-12">
          <p className="text-gray-500 text-lg">No courses available yet.</p>
        </div>
      )}
    </div>
  );
};

export default CourseList;
