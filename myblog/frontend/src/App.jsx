import { useState, useEffect } from "react";
import { BrowserRouter, Routes, Route, Link, useNavigate } from "react-router-dom";
import { getMe, logout as apiLogout, fetchCsrf } from "./api";
import HomePage from "./pages/HomePage";
import PostPage from "./pages/PostPage";
import LoginPage from "./pages/LoginPage";
import RegisterPage from "./pages/RegisterPage";

function Navbar({ user, onLogout }) {
  const nav = useNavigate();
  return (
    <header className="navbar">
      <div className="inner">
        <Link to="/" className="logo">MyBlog</Link>
        <nav>
          {user ? (
            <>
              <span className="greeting">{user.username}</span>
              <button
                className="btn-link"
                onClick={async () => {
                  await apiLogout();
                  onLogout();
                  nav("/");
                }}
              >
                退出
              </button>
            </>
          ) : (
            <>
              <Link to="/login">登录</Link>
              <Link to="/register">注册</Link>
            </>
          )}
        </nav>
      </div>
    </header>
  );
}

export default function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchCsrf().then(() => getMe())
      .then((data) => setUser(data))
      .catch(() => setUser(null))
      .finally(() => setLoading(false));
  }, []);

  if (loading) return null;

  return (
    <BrowserRouter>
      <Routes>
        <Route
          path="*"
          element={
            <>
              <Navbar
                user={user}
                onLogout={() => setUser(null)}
              />
              <main>
                <Routes>
                  <Route path="/" element={<HomePage />} />
                  <Route
                    path="/post/:id"
                    element={<PostPage user={user} />}
                  />
                  <Route
                    path="/login"
                    element={<LoginPage onLogin={(u) => setUser(u)} />}
                  />
                  <Route
                    path="/register"
                    element={<RegisterPage onLogin={(u) => setUser(u)} />}
                  />
                </Routes>
              </main>
            </>
          }
        />
      </Routes>
    </BrowserRouter>
  );
}
