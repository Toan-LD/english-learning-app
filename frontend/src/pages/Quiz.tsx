import React, { useEffect, useState } from 'react';
import { quizAPI } from '../api/endpoints';
import { toast } from 'react-toastify';
import type { Quiz as QuizType, QuizSubmitResult } from '../types';

const Quiz: React.FC = () => {
  const [quizzes, setQuizzes] = useState<QuizType[]>([]);
  const [selectedQuiz, setSelectedQuiz] = useState<QuizType | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [startTime, setStartTime] = useState<number>(0);
  const [result, setResult] = useState<QuizSubmitResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [quizStarted, setQuizStarted] = useState(false);

  useEffect(() => {
    loadQuizzes();
  }, []);

  const loadQuizzes = async () => {
    setLoading(true);
    try {
      const response = await quizAPI.list();
      setQuizzes(response.data.results);
    } catch (error) {
      toast.error('Failed to load quizzes');
    }
    setLoading(false);
  };

  const startQuiz = async (quiz: QuizType) => {
    try {
      const response = await quizAPI.detail(quiz.id);
      setSelectedQuiz(response.data);
      setQuizStarted(true);
      setCurrentQuestionIndex(0);
      setAnswers({});
      setResult(null);
      setStartTime(Date.now());
      await quizAPI.start(quiz.id);
    } catch (error) {
      toast.error('Failed to start quiz');
    }
  };

  const handleAnswer = (questionId: number, answer: string) => {
    setAnswers({ ...answers, [questionId.toString()]: answer });
  };

  const handleSubmit = async () => {
    if (!selectedQuiz) return;

    const timeTaken = Math.floor((Date.now() - startTime) / 1000);
    try {
      const response = await quizAPI.submit(selectedQuiz.id, {
        answers,
        time_taken: timeTaken,
      });
      setResult(response.data);
      toast.success(
        response.data.passed
          ? `Congratulations! You passed with ${response.data.score}%!`
          : `Quiz completed. Score: ${response.data.score}%. Keep practicing!`
      );
    } catch (error) {
      toast.error('Failed to submit quiz');
    }
  };

  const resetQuiz = () => {
    setSelectedQuiz(null);
    setQuizStarted(false);
    setResult(null);
    setAnswers({});
    setCurrentQuestionIndex(0);
  };

  // Quiz Selection View
  if (!quizStarted) {
    return (
      <div className="space-y-6">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Quizzes</h1>
          <p className="text-gray-600 mt-1">Test your knowledge with interactive quizzes</p>
        </div>

        {loading ? (
          <div className="flex items-center justify-center h-64">
            <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {quizzes.map((quiz) => (
              <div key={quiz.id} className="card hover:shadow-lg transition">
                <div className="space-y-3">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-semibold px-2.5 py-1 rounded-full bg-purple-100 text-purple-800">
                      {quiz.quiz_type.replace('_', ' ')}
                    </span>
                    <span className="text-sm text-gray-500">
                      {quiz.question_count} questions
                    </span>
                  </div>
                  <h3 className="text-lg font-semibold text-gray-900">{quiz.title}</h3>
                  <p className="text-sm text-gray-600">{quiz.description}</p>
                  <div className="flex items-center space-x-4 text-sm text-gray-500">
                    <span>⏱ {Math.floor(quiz.time_limit / 60)} min</span>
                    <span>🎯 Pass: {quiz.passing_score}%</span>
                  </div>
                  <button
                    onClick={() => startQuiz(quiz)}
                    className="btn-primary w-full"
                  >
                    Start Quiz
                  </button>
                </div>
              </div>
            ))}
            {quizzes.length === 0 && (
              <div className="col-span-full text-center py-12 text-gray-500">
                No quizzes available. Check back later!
              </div>
            )}
          </div>
        )}
      </div>
    );
  }

  // Quiz Results View
  if (result) {
    return (
      <div className="max-w-3xl mx-auto space-y-6">
        <div className={`card text-center ${result.passed ? 'bg-green-50' : 'bg-red-50'}`}>
          <div className="text-6xl mb-4">{result.passed ? '🎉' : '📚'}</div>
          <h2 className="text-2xl font-bold text-gray-900">
            {result.passed ? 'Congratulations!' : 'Keep Practicing!'}
          </h2>
          <div className="mt-4 text-4xl font-bold text-primary-600">
            {result.score}%
          </div>
          <div className="mt-2 text-gray-600">
            {result.correct_answers} / {result.total_questions} correct
          </div>
          <div className="mt-2 text-sm text-gray-500">
            +{result.xp_earned} XP earned
          </div>
          <div className="mt-6 flex justify-center space-x-4">
            <button onClick={resetQuiz} className="btn-primary">
              Back to Quizzes
            </button>
            {selectedQuiz && (
              <button onClick={() => startQuiz(selectedQuiz)} className="btn-secondary">
                Try Again
              </button>
            )}
          </div>
        </div>

        {/* Question Review */}
        <div>
          <h3 className="text-xl font-bold text-gray-900 mb-4">Review Answers</h3>
          <div className="space-y-4">
            {result.questions_review.map((q, idx) => {
              const userAnswer = answers[q.id.toString()] || '';
              const isCorrect = userAnswer.toLowerCase().trim() === q.correct_answer?.toLowerCase().trim();
              return (
                <div key={q.id} className={`card ${isCorrect ? 'border-green-200' : 'border-red-200'}`}>
                  <div className="flex items-start space-x-3">
                    <span className="text-2xl">{isCorrect ? '✅' : '❌'}</span>
                    <div className="flex-1">
                      <p className="font-medium text-gray-900">
                        {idx + 1}. {q.question_text}
                      </p>
                      <p className="text-sm text-gray-600 mt-1">
                        Your answer: <span className={isCorrect ? 'text-green-600' : 'text-red-600'}>{userAnswer || 'No answer'}</span>
                      </p>
                      {!isCorrect && q.correct_answer && (
                        <p className="text-sm text-green-600 mt-1">
                          Correct: {q.correct_answer}
                        </p>
                      )}
                      {q.explanation && (
                        <p className="text-sm text-gray-500 mt-2 italic">{q.explanation}</p>
                      )}
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    );
  }

  // Quiz In Progress View
  const questions = selectedQuiz?.questions || [];
  const currentQuestion = questions[currentQuestionIndex];

  if (!currentQuestion) {
    return (
      <div className="text-center py-12">
        <p className="text-gray-500">Loading quiz...</p>
      </div>
    );
  }

  return (
    <div className="max-w-3xl mx-auto space-y-6">
      {/* Progress */}
      <div className="flex items-center justify-between">
        <h2 className="text-lg font-semibold text-gray-900">{selectedQuiz?.title}</h2>
        <span className="text-sm text-gray-500">
          Question {currentQuestionIndex + 1} of {questions.length}
        </span>
      </div>
      <div className="w-full bg-gray-200 rounded-full h-2">
        <div
          className="bg-primary-600 rounded-full h-2 transition-all"
          style={{ width: `${((currentQuestionIndex + 1) / questions.length) * 100}%` }}
        ></div>
      </div>

      {/* Question */}
      <div className="card">
        <h3 className="text-xl font-semibold text-gray-900 mb-6">
          {currentQuestion.question_text}
        </h3>

        {currentQuestion.question_type === 'multiple_choice' ? (
          <div className="space-y-3">
            {currentQuestion.options.map((option, idx) => (
              <button
                key={idx}
                onClick={() => handleAnswer(currentQuestion.id, option)}
                className={`w-full text-left p-4 rounded-lg border-2 transition ${
                  answers[currentQuestion.id.toString()] === option
                    ? 'border-primary-500 bg-primary-50'
                    : 'border-gray-200 hover:border-gray-300'
                }`}
              >
                <span className="font-medium">
                  {String.fromCharCode(65 + idx)}.
                </span>{' '}
                {option}
              </button>
            ))}
          </div>
        ) : (
          <div>
            <input
              type="text"
              value={answers[currentQuestion.id.toString()] || ''}
              onChange={(e) => handleAnswer(currentQuestion.id, e.target.value)}
              className="input-field"
              placeholder="Type your answer here..."
            />
          </div>
        )}
      </div>

      {/* Navigation */}
      <div className="flex justify-between">
        <button
          onClick={() => setCurrentQuestionIndex(Math.max(0, currentQuestionIndex - 1))}
          disabled={currentQuestionIndex === 0}
          className="btn-secondary disabled:opacity-50"
        >
          ← Previous
        </button>

        {currentQuestionIndex === questions.length - 1 ? (
          <button
            onClick={handleSubmit}
            disabled={!answers[currentQuestion.id.toString()]}
            className="btn-primary disabled:opacity-50"
          >
            Submit Quiz
          </button>
        ) : (
          <button
            onClick={() => setCurrentQuestionIndex(currentQuestionIndex + 1)}
            className="btn-primary"
          >
            Next →
          </button>
        )}
      </div>
    </div>
  );
};

export default Quiz;
