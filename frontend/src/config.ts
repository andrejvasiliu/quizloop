const BASE = import.meta.env.VITE_API_BASE_URL;

export const API = {
  base: BASE,
  quizzes: `${BASE}/quizzes`,
  quiz: `${BASE}/quiz`,
  upload: `${BASE}/upload`,
  auth: {
    register: `${BASE}/register`,
    login: `${BASE}/login`,
    logout: `${BASE}/logout`,
    me: `${BASE}/me`,
  },
};