import { useEffect, useState } from "react";
import axios from "axios";
import { API_QUIZZES_URL } from "../config";
import { Link } from "react-router-dom";
import type { QuizListItem } from "../types/quiz_types";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";

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
    <>
      <h1>Welcome to the Home Page</h1>
      <h2>Available Quizzes:</h2>

      <div>
        {quizzes.map((quiz) => (
          <Card key={quiz.name}>
            <CardHeader>
              <CardTitle>{quiz.title}</CardTitle>
            </CardHeader>
            <CardContent>
              <Button asChild>
                <Link to={`/quiz/${quiz.name}`}>Start Quiz</Link>
              </Button>
            </CardContent>
          </Card>
        ))}
      </div>
    </>
  );
}

export default Home;
