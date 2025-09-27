import { useState } from "react";
import axios from "axios";
import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import { Input } from "@/components/ui/input";
import { API_LOGIN_URL } from "../config";

function Nav() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    try {
      const res = await axios.post(
        API_LOGIN_URL,
        { username, password },
        { withCredentials: true }
      );

      console.log("Login success:", res.data);
    } catch (err: any) {
      console.error("Login error:", err.response?.data || err.message);
      setError(err.response?.data?.error || "Something went wrong");
    }
  };

  return (
    <nav className="flex items-center justify-between p-4 shadow-md">
      <div className="text-xl font-bold">
        <Link to="/">quizloop</Link>
      </div>
      <div className="hidden md:flex gap-4">
        <Button asChild variant="ghost">
          <Link to="/upload">Upload</Link>
        </Button>
        <Dialog>
          <DialogTrigger asChild>
            <Button variant="ghost">Log In</Button>
          </DialogTrigger>
          <DialogContent className="sm:max-w-[425px]">
            <form onSubmit={handleAuth} className="grid gap-4">
              <DialogHeader>
                <DialogTitle className="mb-4">Log In</DialogTitle>
              </DialogHeader>
              <div className="grid gap-4">
                <div className="grid gap-3">
                  <Label htmlFor="username-1">Username</Label>
                  <Input
                    id="username-1"
                    name="username"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                  />
                </div>
                <div className="grid gap-3">
                  <Label htmlFor="password-1">Password</Label>
                  <Input
                    id="password-1"
                    name="password"
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                  />
                </div>
                {error && <p className="text-sm text-red-500">{error}</p>}
              </div>
              <div className="flex flex-col items-center space-y-4">
                <Button asChild variant="link">
                  <Link to="#">Forgot password?</Link>
                </Button>
                <Button variant="link">
                  <Link to="#">Sign Up</Link>
                </Button>
              </div>
              <DialogFooter>
                <Button type="submit">Log In</Button>
              </DialogFooter>
            </form>
          </DialogContent>
        </Dialog>
      </div>
    </nav>
  );
}

export default Nav;
