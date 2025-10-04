import { BrowserRouter, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./context/AuthContext";
import Home from "./pages/Home";
import Upload from "./pages/Upload";
import Nav from "./components/Nav";
import QuizPage from "./pages/QuizPage";
import ResultsPage from "./pages/ResultsPage";
import Register from "./pages/Register";
import ForgotPassword from "./pages/ForgotPassword";

function App() {
  return (
    <div className="min-h-screen bg-gray-50 text-gray-900 font-sans">
      <BrowserRouter>
        <AuthProvider>
          <Nav />
          <main className="p-4">
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/upload" element={<Upload />} />
              <Route path="/quiz/:name" element={<QuizPage />} />
              <Route path="/results" element={<ResultsPage />} />
              <Route path="/register" element={<Register />} />
              <Route path="/forgot-password" element={<ForgotPassword />} />
            </Routes>
          </main>
        </AuthProvider>
      </BrowserRouter>
    </div>
  );
}

export default App;
