export interface QuizQuestion {
  question: string;
  options: string[];
  answer_index: number;
}

export interface Quiz {
  title: string;
  questions: QuizQuestion[];
}

export interface QuizListItem {
  title: string;
  name: string; // filename without .json
}

export interface ResultsState {
  quizTitle: string;
  questions: QuizQuestion[];
  answers: number[];
}
