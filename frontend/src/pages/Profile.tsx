import React, { useState, useEffect } from 'react';
import { useAppDispatch, useAppSelector } from '../store';
import { updateProfile, fetchProfile } from '../store/authSlice';
import { fetchStats, fetchProgresses } from '../store/progressSlice';
import { toast } from 'react-toastify';
import type { LearningLevel } from '../types';

const Profile: React.FC = () => {
  const dispatch = useAppDispatch();
  const { user } = useAppSelector((state) => state.auth);
  const { progresses } = useAppSelector((state) => state.progress);
  const [editing, setEditing] = useState(false);
  const [formData, setFormData] = useState({
    first_name: user?.first_name || '',
    last_name: user?.last_name || '',
    bio: user?.bio || '',
    daily_goal: user?.daily_goal || 30,
    learning_level: user?.learning_level || 'beginner' as LearningLevel,
  });

  useEffect(() => {
    dispatch(fetchProfile());
    dispatch(fetchStats());
    dispatch(fetchProgresses());
  }, [dispatch]);

  useEffect(() => {
    if (user) {
      setFormData({
        first_name: user.first_name,
        last_name: user.last_name,
        bio: user.bio,
        daily_goal: user.daily_goal,
        learning_level: user.learning_level,
      });
    }
  }, [user]);

  const handleSave = async () => {
    const result = await dispatch(updateProfile(formData));
    if (updateProfile.fulfilled.match(result)) {
      toast.success('Profile updated successfully!');
      setEditing(false);
    } else {
      toast.error('Failed to update profile');
    }
  };

  return (
    <div className="max-w-4xl mx-auto space-y-8">
      <h1 className="text-3xl font-bold text-gray-900">My Profile</h1>

      {/* Profile Card */}
      <div className="card">
        <div className="flex items-center space-x-6 mb-6">
          <div className="w-20 h-20 bg-gradient-to-br from-primary-400 to-primary-600 rounded-full flex items-center justify-center">
            <span className="text-white text-3xl font-bold">
              {user?.first_name?.[0]}{user?.last_name?.[0]}
            </span>
          </div>
          <div>
            <h2 className="text-2xl font-bold text-gray-900">
              {user?.first_name} {user?.last_name}
            </h2>
            <p className="text-gray-500">{user?.email}</p>
            <p className="text-sm text-gray-400">@{user?.username}</p>
          </div>
          <button
            onClick={() => setEditing(!editing)}
            className="ml-auto btn-secondary"
          >
            {editing ? 'Cancel' : '✏️ Edit Profile'}
          </button>
        </div>

        {editing ? (
          <div className="space-y-4 border-t pt-6">
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">First Name</label>
                <input
                  type="text"
                  value={formData.first_name}
                  onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                  className="input-field"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Last Name</label>
                <input
                  type="text"
                  value={formData.last_name}
                  onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                  className="input-field"
                />
              </div>
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-1">Bio</label>
              <textarea
                value={formData.bio}
                onChange={(e) => setFormData({ ...formData, bio: e.target.value })}
                className="input-field"
                rows={3}
              />
            </div>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Learning Level</label>
                <select
                  value={formData.learning_level}
                  onChange={(e) => setFormData({ ...formData, learning_level: e.target.value as LearningLevel })}
                  className="input-field"
                >
                  <option value="beginner">Beginner</option>
                  <option value="intermediate">Intermediate</option>
                  <option value="advanced">Advanced</option>
                  <option value="proficient">Proficient</option>
                </select>
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">Daily Goal (minutes)</label>
                <input
                  type="number"
                  value={formData.daily_goal}
                  onChange={(e) => setFormData({ ...formData, daily_goal: parseInt(e.target.value) })}
                  className="input-field"
                  min={5}
                  max={120}
                />
              </div>
            </div>
            <button onClick={handleSave} className="btn-primary">
              💾 Save Changes
            </button>
          </div>
        ) : (
          <div className="border-t pt-6 space-y-4">
            {user?.bio && (
              <div>
                <span className="text-sm font-medium text-gray-500">Bio</span>
                <p className="text-gray-700">{user.bio}</p>
              </div>
            )}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              <div className="bg-blue-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-blue-700">{user?.total_xp || 0}</div>
                <div className="text-sm text-blue-600">Total XP</div>
              </div>
              <div className="bg-orange-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-orange-700">🔥 {user?.streak_days || 0}</div>
                <div className="text-sm text-orange-600">Day Streak</div>
              </div>
              <div className="bg-green-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-green-700">{user?.words_learned || 0}</div>
                <div className="text-sm text-green-600">Words Learned</div>
              </div>
              <div className="bg-purple-50 rounded-lg p-4 text-center">
                <div className="text-2xl font-bold text-purple-700">{user?.courses_enrolled || 0}</div>
                <div className="text-sm text-purple-600">Courses</div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Enrolled Courses */}
      <div className="card">
        <h2 className="text-xl font-bold text-gray-900 mb-4">My Courses</h2>
        {progresses.length > 0 ? (
          <div className="space-y-4">
            {progresses.map((p) => (
              <div key={p.id} className="flex items-center justify-between p-4 bg-gray-50 rounded-lg">
                <div>
                  <h3 className="font-semibold text-gray-900">{p.course_title}</h3>
                  <p className="text-sm text-gray-500">
                    {p.completed_lesson_count}/{p.total_lessons} lessons • {p.total_time_spent} min
                  </p>
                </div>
                <div className="w-32">
                  <div className="flex justify-between text-xs text-gray-500 mb-1">
                    <span>{p.progress_percentage}%</span>
                  </div>
                  <div className="w-full bg-gray-200 rounded-full h-2">
                    <div
                      className="bg-primary-600 rounded-full h-2"
                      style={{ width: `${p.progress_percentage}%` }}
                    ></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        ) : (
          <p className="text-gray-500">You haven't enrolled in any courses yet.</p>
        )}
      </div>
    </div>
  );
};

export default Profile;
