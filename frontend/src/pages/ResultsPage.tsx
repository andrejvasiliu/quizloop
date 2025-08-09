import { useLocation, useNavigate } from "react-router-dom";
import type { ResultsState } from "../types/types";

function ResultsPage() {
  const location = useLocation();
  const navigate = useNavigate();
  const state = location.state as ResultsState;

  if (!state) {
    return <div>No results found. Please take a quiz first.</div>;
  }

  const { quizTitle, questions, answers } = state;

  const score = answers.reduce((acc, answerIndex, i) => {
    return acc + (answerIndex === questions[i].answer_index ? 1 : 0);
  }, 0);

  return (
    <div>
      <h1>{quizTitle} – Results</h1>
      <p>
        You scored {score} out of {questions.length}
      </p>

      <h2>Review</h2>
      <ol>
        {questions.map((q, i) => {
          const correctIndex = q.answer_index;
          const userIndex = answers[i];
          return (
            <li key={i}>
              <p>{q.question}</p>
              <p>
                Your answer: {q.options[userIndex]}{" "}
                {userIndex === correctIndex ? "✅" : "❌"}
              </p>
              {userIndex !== correctIndex && (
                <p>Correct answer: {q.options[correctIndex]}</p>
              )}
            </li>
          );
        })}
      </ol>

      <button onClick={() => navigate("/")}>Back to Home</button>
    </div>
  );
}

export default ResultsPage;
