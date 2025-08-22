import { Link } from "react-router-dom";
import { Button } from "@/components/ui/button";

function Nav() {
  return (
    <nav className="flex items-center justify-between p-4 shadow-md">
      <div className="text-xl font-bold">
        <Link to="/">quizloop</Link>
      </div>
      <div className="hidden md:flex gap-4">
        <Button asChild variant="ghost">
          <Link to="/upload">Upload</Link>
        </Button>
      </div>
    </nav>
  );
}

export default Nav;
