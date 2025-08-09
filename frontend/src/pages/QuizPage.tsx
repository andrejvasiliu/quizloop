import { useParams, useNavigate } from "react-router-dom";
import { useEffect, useState } from "react";
import axios from "axios";
import { API_QUIZ_URL } from "../config";
import type { Quiz } from "../types/types";

function QuizPage() {
  const { name } = useParams<{ name: string }>();
  const navigate = useNavigate();
  const [quiz, setQuiz] = useState<Quiz | null>(null);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState<number | null>(null);
  const [answers, setAnswers] = useState<number[]>([]);

  useEffect(() => {
    const fetchQuiz = async () => {
      try {
        const response = await axios.post<{ quiz: Quiz }>(
          `${API_QUIZ_URL}/${name}`
        );
        setQuiz(response.data.quiz);
      } catch (error) {
        console.error("Error loading quiz:", error);
      }
    };
    fetchQuiz();
  }, [name]);

  if (!quiz) return <div>Loading...</div>;

  const currentQuestion = quiz.questions[currentQuestionIndex];

  const handleConfirm = () => {
    if (selectedOption === null) return; // can't confirm without selecting
    const updatedAnswers = [...answers];
    updatedAnswers[currentQuestionIndex] = selectedOption;
    setAnswers(updatedAnswers);
    setSelectedOption(null); // reset for next question

    if (currentQuestionIndex + 1 < quiz.questions.length) {
      setCurrentQuestionIndex((prev) => prev + 1);
    } else {
      // quiz finished then go to results page
      navigate(`/results`, {
        state: {
          quizTitle: quiz.title,
          questions: quiz.questions,
          answers: updatedAnswers,
        },
      });
    }
  };

  return (
    <div>
      <h1>{quiz.title}</h1>
      <h2>
        Question {currentQuestionIndex + 1} of {quiz.questions.length}
      </h2>
      <p>{currentQuestion.question}</p>
      <ul>
        {currentQuestion.options.map((opt, i) => (
          <li key={i}>
            <label style={{ cursor: "pointer" }}>
              <input
                type="radio"
                name="option"
                checked={selectedOption === i}
                onChange={() => setSelectedOption(i)}
              />
              {opt}
            </label>
          </li>
        ))}
      </ul>
      <button onClick={handleConfirm} disabled={selectedOption === null}>
        {currentQuestionIndex + 1 === quiz.questions.length
          ? "Finish Quiz"
          : "Next Question"}
      </button>
    </div>
  );
}

export default QuizPage;
