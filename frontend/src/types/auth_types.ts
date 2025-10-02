export interface AuthContextType {
  token: string | null;
  login: (username: string, password: string) => Promise<void>;
  register: (
    username: string,
    email: string,
    password: string
  ) => Promise<void>;
  me: () => Promise<void>;
  logout: () => void;
  user: string | null;
  error: string | null;
  clearError: () => void;
}

export interface AuthResponse {
  access_token: string;
  username: string;
  message?: string;
}

export interface AuthMeResponse {
  username: string;
  message?: string;
}
