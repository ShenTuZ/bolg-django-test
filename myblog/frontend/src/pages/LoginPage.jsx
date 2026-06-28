import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { login, setToken } from "../api";

export default function LoginPage({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const nav = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await login(username, password);
      setToken(data.access);
      onLogin({ username: data.username, is_staff: data.is_staff });
      nav("/");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="page auth-page">
      <form onSubmit={handleSubmit}>
        <h2>登录</h2>
        {error && <p className="error">{error}</p>}
        <input
          type="text"
          placeholder="用户名"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type="password"
          placeholder="密码"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type="submit">登录</button>
        <p className="switch">
          没有账号？<a href="/register">去注册</a>
        </p>
      </form>
    </div>
  );
}
