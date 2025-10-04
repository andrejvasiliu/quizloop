import { useState } from "react";
import { Link } from "react-router-dom";
import { useAuth } from "@/context/AuthContext";
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

function Nav() {
  const { token, login, logout, error, clearError } = useAuth();
  const [open, setOpen] = useState(false);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();

    try {
      await login(username, password);
      setUsername("");
      setPassword("");
      setOpen(false);
    } catch (err: any) {
      console.error("Login error1:", err.response?.data || err.message);
    }
  };

  return (
    <nav className="flex items-center justify-between p-4 shadow-md">
      <div className="text-xl font-bold">
        <Link to="/">quizloop</Link>
      </div>

      <div className="hidden md:flex gap-4">
        {!token ? (
          <Dialog
            open={open}
            onOpenChange={(o) => {
              setOpen(o);
              if (!o) clearError();
            }}
          >
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
                    <Label htmlFor="username">Username</Label>
                    <Input
                      id="username"
                      name="username"
                      placeholder="Username"
                      value={username}
                      onChange={(e) => {
                        setUsername(e.target.value);
                        clearError();
                      }}
                    />
                  </div>
                  <div className="grid gap-3">
                    <Label htmlFor="password">Password</Label>
                    <Input
                      id="password"
                      name="password"
                      type="password"
                      placeholder="Password"
                      value={password}
                      onChange={(e) => {
                        setPassword(e.target.value);
                        clearError();
                      }}
                    />
                  </div>
                  {error && <p className="text-sm text-red-500">{error}</p>}
                </div>
                <div className="flex flex-col items-center space-y-4">
                  <Button asChild variant="link" onClick={() => setOpen(false)}>
                    <Link to="/forgot-password">Forgot password?</Link>
                  </Button>
                  <Button asChild variant="link" onClick={() => setOpen(false)}>
                    <Link to="/register">Sign Up</Link>
                  </Button>
                </div>
                <DialogFooter>
                  <Button type="submit">Log In</Button>
                </DialogFooter>
              </form>
            </DialogContent>
          </Dialog>
        ) : (
          <div>
            <Button asChild variant="ghost">
              <Link to="/upload">Upload</Link>
            </Button>

            <Button variant="ghost" onClick={logout}>
              Log Out
            </Button>
          </div>
        )}
      </div>
    </nav>
  );
}

export default Nav;
