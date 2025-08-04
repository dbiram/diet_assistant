import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { Button } from "../components/ui/button";

export default function NavBar() {
  const { token, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/");
  };

  return (
    <nav className="bg-white border-b p-4 flex justify-between items-center">
        {token && (<>
      <div className="space-x-4">
        <Link to="/chat" className="text-sm font-medium text-green-600 hover:underline">
          Chat
        </Link>
        <Link to="/profile" className="text-sm font-medium text-green-600 hover:underline">
          Profile
        </Link>
      </div>
        <Button variant="outline" size="sm" onClick={handleLogout}>
          Logout
        </Button>
      </>)}
      {!token && (
        <div className="space-x-4">
          <Link to="/" className="text-sm font-medium text-green-600 hover:underline">
            Login
          </Link>
          <Link to="/register" className="text-sm font-medium text-green-600 hover:underline">
            Register
          </Link>
        </div>
      )}
    </nav>
  );
}
