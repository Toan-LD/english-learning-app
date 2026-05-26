import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../store';
import { fetchStats } from '../store/progressSlice';
import { fetchProfile } from '../store/authSlice';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from 'recharts';

const Dashboard: React.FC = () => {
  const dispatch = useAppDispatch();
  const { user } = useAppSelector((state) => state.auth);
  const { stats, loading } = useAppSelector((state) => state.progress);

  useEffect(() => {
    dispatch(fetchStats());
    dispatch(fetchProfile());
  }, [dispatch]);

  const weeklyData = stats?.weekly_activity?.map((day) => ({
    date: new Date(day.date).toLocaleDateString('en-US', { weekday: 'short' }),
    minutes: day.minutes_studied,
    words: day.words_learned,
    xp: day.xp_earned,
  })) || [];

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-primary-600 to-primary-700 rounded-2xl p-8 text-white">
        <h1 className="text-3xl font-bold">
          Welcome back, {user?.first_name || 'Learner'}! 👋
        </h1>
        <p className="mt-2 text-primary-100">
          Continue your English learning journey. You're doing great!
        </p>
        <div className="mt-4 flex items-center space-x-6">
          <div className="bg-white/20 rounded-xl px-4 py-2">
            <div className="text-2xl font-bold">{user?.total_xp || 0}</div>
            <div className="text-xs text-primary-100">Total XP</div>
          </div>
          <div className="bg-white/20 rounded-xl px-4 py-2">
            <div className="text-2xl font-bold">🔥 {user?.streak_days || 0}</div>
            <div className="text-xs text-primary-100">Day Streak</div>
          </div>
          <div className="bg-white/20 rounded-xl px-4 py-2">
            <div className="text-2xl font-bold">{stats?.total_words_learned || 0}</div>
            <div className="text-xs text-primary-100">Words Learned</div>
          </div>
        </div>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-blue-100 rounded-xl flex items-center justify-center">
              <span className="text-2xl">📚</span>
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">
                {stats?.total_courses_enrolled || 0}
              </div>
              <div className="text-sm text-gray-500">Courses Enrolled</div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-green-100 rounded-xl flex items-center justify-center">
              <span className="text-2xl">✅</span>
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">
                {stats?.courses_completed || 0}
              </div>
              <div className="text-sm text-gray-500">Courses Completed</div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-purple-100 rounded-xl flex items-center justify-center">
              <span className="text-2xl">📝</span>
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">
                {stats?.total_quizzes_taken || 0}
              </div>
              <div className="text-sm text-gray-500">Quizzes Taken</div>
            </div>
          </div>
        </div>

        <div className="card">
          <div className="flex items-center space-x-3">
            <div className="w-12 h-12 bg-yellow-100 rounded-xl flex items-center justify-center">
              <span className="text-2xl">⭐</span>
            </div>
            <div>
              <div className="text-2xl font-bold text-gray-900">
                {stats?.average_quiz_score || 0}%
              </div>
              <div className="text-sm text-gray-500">Avg Quiz Score</div>
            </div>
          </div>
        </div>
      </div>

      {/* Chart and Quick Actions */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Weekly Activity</h2>
          {loading ? (
            <div className="h-64 flex items-center justify-center text-gray-500">
              Loading chart...
            </div>
          ) : weeklyData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={weeklyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="date" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="minutes" fill="#3b82f6" name="Minutes" radius={[4, 4, 0, 0]} />
                <Bar dataKey="xp" fill="#8b5cf6" name="XP" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : (
            <div className="h-64 flex items-center justify-center text-gray-500">
              No activity data yet. Start learning to see your progress!
            </div>
          )}
        </div>

        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="space-y-3">
            <Link
              to="/courses"
              className="flex items-center space-x-3 p-3 rounded-lg bg-blue-50 hover:bg-blue-100 transition"
            >
              <span className="text-2xl">📚</span>
              <div>
                <div className="font-medium text-gray-900">Browse Courses</div>
                <div className="text-sm text-gray-500">Find your next lesson</div>
              </div>
            </Link>
            <Link
              to="/vocabulary"
              className="flex items-center space-x-3 p-3 rounded-lg bg-green-50 hover:bg-green-100 transition"
            >
              <span className="text-2xl">🔤</span>
              <div>
                <div className="font-medium text-gray-900">Practice Vocabulary</div>
                <div className="text-sm text-gray-500">Flashcard review</div>
              </div>
            </Link>
            <Link
              to="/quiz"
              className="flex items-center space-x-3 p-3 rounded-lg bg-purple-50 hover:bg-purple-100 transition"
            >
              <span className="text-2xl">🎯</span>
              <div>
                <div className="font-medium text-gray-900">Take a Quiz</div>
                <div className="text-sm text-gray-500">Test your knowledge</div>
              </div>
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
