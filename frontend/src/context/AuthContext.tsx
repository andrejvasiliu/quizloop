import { createContext, useContext, useState, type ReactNode } from "react";
import axios from "axios";
import {
  API_LOGIN_URL,
  API_REGISTER_URL,
  API_ME_URL,
  //   API_LOGOUT_URL,
} from "../config";
import type {
  AuthContextType,
  AuthResponse,
  AuthMeResponse,
} from "@/types/auth_types";

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [token, setToken] = useState<string | null>(null);
  const [user, setUser] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);

  const login = async (username: string, password: string) => {
    try {
      const res = await axios.post<AuthResponse>(
        API_LOGIN_URL,
        { username, password },
        { withCredentials: true }
      );

      setToken(res.data.access_token);
      setUser(res.data.username);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.error || "Login failed");
    }
  };

  const register = async (
    username: string,
    email: string,
    password: string
  ) => {
    try {
      const res = await axios.post<AuthResponse>(
        API_REGISTER_URL,
        { username, email, password },
        { withCredentials: true }
      );
      setToken(res.data.access_token);
      setUser(res.data.username);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.error || "Registration failed");
    }
  };

  const me = async () => {
    try {
      if (!token) {
        throw new Error("No token available");
      }

      const res = await axios.get<AuthMeResponse>(API_ME_URL, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
        withCredentials: true,
      });

      setUser(res.data.username);
      setError(null);
    } catch (err: any) {
      setError(err.response?.data?.error || "Failed to fetch user");
    }
  };

  const logout = () => {
    setToken(null);
    setUser(null);
    setError(null);
  };

  const clearError = () => setError(null);

  return (
    <AuthContext.Provider
      value={{ token, login, register, me, logout, user, error, clearError }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
