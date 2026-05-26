import React, { useEffect, useState, useCallback } from 'react';
import { useAppDispatch, useAppSelector } from '../store';
import { fetchRandomWords, markWordLearned } from '../store/vocabularySlice';
import { speak } from '../utils/speech';
import type { Word } from '../types';

const VocabularyFlashcard: React.FC = () => {
  const dispatch = useAppDispatch();
  const { flashcardWords, loading } = useAppSelector((state) => state.vocabulary);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [isFlipped, setIsFlipped] = useState(false);
  const [difficulty, setDifficulty] = useState<string>('');
  const [cardCount, setCardCount] = useState(10);

  const loadWords = useCallback(() => {
    dispatch(fetchRandomWords({
      count: cardCount,
      difficulty: difficulty || undefined,
    }));
    setCurrentIndex(0);
    setIsFlipped(false);
  }, [dispatch, cardCount, difficulty]);

  useEffect(() => {
    loadWords();
  }, [loadWords]);

  const currentWord: Word | undefined = flashcardWords[currentIndex];

  const handleNext = () => {
    setIsFlipped(false);
    setTimeout(() => {
      if (currentIndex < flashcardWords.length - 1) {
        setCurrentIndex(currentIndex + 1);
      } else {
        setCurrentIndex(0);
      }
    }, 100);
  };

  const handlePrev = () => {
    setIsFlipped(false);
    setTimeout(() => {
      if (currentIndex > 0) {
        setCurrentIndex(currentIndex - 1);
      } else {
        setCurrentIndex(flashcardWords.length - 1);
      }
    }, 100);
  };

  const handlePronounce = () => {
    if (currentWord) {
      speak(currentWord.word);
    }
  };

  const handleMarkLearned = async () => {
    if (currentWord) {
      await dispatch(markWordLearned(currentWord.id));
      handleNext();
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Vocabulary Flashcards</h1>
          <p className="text-gray-600 mt-1">Click the card to flip and reveal the definition</p>
        </div>
        <div className="flex items-center space-x-3">
          <select
            value={difficulty}
            onChange={(e) => setDifficulty(e.target.value)}
            className="input-field w-40"
          >
            <option value="">All Levels</option>
            <option value="basic">Basic</option>
            <option value="intermediate">Intermediate</option>
            <option value="advanced">Advanced</option>
          </select>
          <select
            value={cardCount}
            onChange={(e) => setCardCount(parseInt(e.target.value))}
            className="input-field w-28"
          >
            <option value={5}>5 cards</option>
            <option value={10}>10 cards</option>
            <option value={20}>20 cards</option>
          </select>
          <button onClick={loadWords} className="btn-primary">
            🔄 New Set
          </button>
        </div>
      </div>

      {loading ? (
        <div className="flex items-center justify-center h-64">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
        </div>
      ) : currentWord ? (
        <>
          {/* Progress */}
          <div className="text-center text-gray-500">
            Card {currentIndex + 1} of {flashcardWords.length}
          </div>
          <div className="w-full bg-gray-200 rounded-full h-2">
            <div
              className="bg-primary-600 rounded-full h-2 transition-all"
              style={{ width: `${((currentIndex + 1) / flashcardWords.length) * 100}%` }}
            ></div>
          </div>

          {/* Flashcard */}
          <div className="flex justify-center">
            <div
              className="flashcard-container w-full max-w-lg h-80 cursor-pointer"
              onClick={() => setIsFlipped(!isFlipped)}
            >
              <div className={`flashcard ${isFlipped ? 'flipped' : ''}`}>
                {/* Front */}
                <div className="flashcard-front bg-gradient-to-br from-primary-500 to-primary-700 rounded-2xl p-8 text-white">
                  <div className="text-center">
                    <div className="text-sm uppercase tracking-wide text-primary-200 mb-4">
                      {currentWord.part_of_speech}
                    </div>
                    <h2 className="text-4xl font-bold mb-4">{currentWord.word}</h2>
                    <p className="text-primary-100 text-lg mb-6">{currentWord.phonetic}</p>
                    <button
                      onClick={(e) => {
                        e.stopPropagation();
                        handlePronounce();
                      }}
                      className="bg-white/20 hover:bg-white/30 px-4 py-2 rounded-lg transition"
                    >
                      🔊 Pronounce
                    </button>
                  </div>
                </div>

                {/* Back */}
                <div className="flashcard-back bg-white rounded-2xl p-8 border-2 border-primary-200">
                  <div className="text-center h-full flex flex-col justify-center">
                    <h3 className="text-xl font-bold text-gray-900 mb-3">
                      {currentWord.word}
                    </h3>
                    <p className="text-gray-700 text-lg mb-4">
                      {currentWord.definition}
                    </p>
                    {currentWord.definition_vi && (
                      <p className="text-gray-500 italic mb-4">
                        🇻🇳 {currentWord.definition_vi}
                      </p>
                    )}
                    {currentWord.example_sentence && (
                      <div className="bg-gray-50 rounded-lg p-3 mt-2">
                        <p className="text-sm text-gray-600 italic">
                          "{currentWord.example_sentence}"
                        </p>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Controls */}
          <div className="flex justify-center items-center space-x-4">
            <button onClick={handlePrev} className="btn-secondary px-6">
              ← Previous
            </button>
            <button onClick={handleMarkLearned} className="btn-primary px-6">
              ✅ I Know This
            </button>
            <button onClick={handleNext} className="btn-secondary px-6">
              Next →
            </button>
          </div>
        </>
      ) : (
        <div className="text-center py-12 text-gray-500">
          <p className="text-lg">No flashcards loaded. Click "New Set" to start!</p>
        </div>
      )}
    </div>
  );
};

export default VocabularyFlashcard;
