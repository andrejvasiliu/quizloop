import { useEffect, useState } from "react";
import axios from "axios";
import { API_QUIZZES_URL } from "../config";
import { Link } from "react-router-dom";
import type { QuizListItem } from "../types/types";

function Home() {
  const [quizzes, setQuizzes] = useState<QuizListItem[]>([]);

  useEffect(() => {
    const fetchQuizzes = async () => {
      try {
        const response = await axios.get<{ quizzes: QuizListItem[] }>(
          `${API_QUIZZES_URL}`
        );
        setQuizzes(response.data.quizzes || []);
      } catch (error) {
        console.error("Error fetching quizzes:", error);
      }
    };
    fetchQuizzes();
  }, []);

  return (
    <div>
      <h1>Welcome to the Home Page</h1>
      <h2>Available Quizzes:</h2>
      <ul>
        {quizzes.map((quiz) => (
          <li key={quiz.name}>
            <Link
              to={`/quiz/${quiz.name}`}
              style={{ textDecoration: "none", color: "blue" }}
            >
              {quiz.title}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default Home;
