import { useState } from "react";
import { useNavigate } from "react-router-dom";
import { register, setToken } from "../api";

export default function RegisterPage({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const nav = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const data = await register(username, password);
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
        <h2>注册</h2>
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
        <button type="submit">注册</button>
        <p className="switch">
          已有账号？<a href="/login">去登录</a>
        </p>
      </form>
    </div>
  );
}
