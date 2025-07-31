import { Link } from "react-router-dom";
import "../styles/nav.css";

function Nav() {
  return (
    <nav className="navbar">
      <ul>
        <li>
          <Link to="/">Home</Link>
        </li>
        <li>
          <Link to="/upload">Upload</Link>
        </li>
      </ul>
    </nav>
  );
}

export default Nav;