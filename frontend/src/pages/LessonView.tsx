import React, { useEffect, useState } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { useAppDispatch, useAppSelector } from '../store';
import { fetchLessonDetail } from '../store/coursesSlice';
import { speak } from '../utils/speech';

const LessonView: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const dispatch = useAppDispatch();
  const navigate = useNavigate();
  const { currentLesson } = useAppSelector((state) => state.courses);
  const [readAloud, setReadAloud] = useState(false);

  useEffect(() => {
    if (id) {
      dispatch(fetchLessonDetail(parseInt(id)));
    }
  }, [dispatch, id]);

  const handleReadAloud = () => {
    if (!currentLesson) return;
    if (readAloud) {
      window.speechSynthesis.cancel();
      setReadAloud(false);
    } else {
      const textContent = currentLesson.content.replace(/<[^>]*>/g, '');
      speak(textContent);
      setReadAloud(true);
    }
  };

  if (!currentLesson) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto space-y-6">
      {/* Header */}
      <div className="flex items-center justify-between">
        <button
          onClick={() => navigate(-1)}
          className="text-gray-600 hover:text-gray-900 text-sm"
        >
          ← Back to Course
        </button>
        <div className="flex items-center space-x-3">
          <button
            onClick={handleReadAloud}
            className={`px-4 py-2 rounded-lg text-sm font-medium transition ${
              readAloud
                ? 'bg-red-100 text-red-700 hover:bg-red-200'
                : 'bg-blue-100 text-blue-700 hover:bg-blue-200'
            }`}
          >
            {readAloud ? '⏹ Stop' : '🔊 Read Aloud'}
          </button>
        </div>
      </div>

      {/* Lesson Content */}
      <div className="card">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-10 h-10 bg-primary-100 rounded-lg flex items-center justify-center">
            <span className="text-primary-700 font-bold">{currentLesson.order}</span>
          </div>
          <div>
            <h1 className="text-2xl font-bold text-gray-900">{currentLesson.title}</h1>
            <div className="flex items-center space-x-3 text-sm text-gray-500">
              <span>
                {currentLesson.lesson_type === 'reading' && '📖 Reading'}
                {currentLesson.lesson_type === 'video' && '🎥 Video'}
                {currentLesson.lesson_type === 'quiz' && '📝 Quiz'}
                {currentLesson.lesson_type === 'practice' && '✏️ Practice'}
              </span>
              <span>⏱ {currentLesson.duration_minutes} minutes</span>
            </div>
          </div>
        </div>

        {/* Video URL if available */}
        {currentLesson.video_url && (
          <div className="mb-6 aspect-video bg-gray-900 rounded-lg overflow-hidden">
            <iframe
              src={currentLesson.video_url}
              className="w-full h-full"
              allowFullScreen
              title={currentLesson.title}
            ></iframe>
          </div>
        )}

        {/* Lesson content */}
        <div
          className="prose prose-lg max-w-none"
          dangerouslySetInnerHTML={{ __html: currentLesson.content }}
        />
      </div>

      {/* Mark as Complete */}
      <div className="flex justify-center">
        <button
          onClick={() => {
            navigate(-1);
          }}
          className="btn-primary text-lg px-8 py-3"
        >
          ✅ Complete Lesson
        </button>
      </div>
    </div>
  );
};

export default LessonView;
