const API_BASE = "/api";

function getToken() {
  return localStorage.getItem("jwt_token");
}

export function setToken(token) {
  localStorage.setItem("jwt_token", token);
}

export function clearToken() {
  localStorage.removeItem("jwt_token");
}

async function request(url, options = {}) {
  const { headers, ...rest } = options;
  const token = getToken();
  const res = await fetch(`${API_BASE}${url}`, {
    headers: {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...headers,
    },
    ...rest,
  });
  if (res.status === 204) return null;
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || data.detail || "请求失败");
  return data;
}

export const getPosts = () => request("/posts/");
export const getPost = (id) => request(`/posts/${id}/`);
export const addComment = (postId, content) =>
  request(`/posts/${postId}/comments/`, {
    method: "POST",
    body: JSON.stringify({ content }),
  });
export const deleteComment = (commentId) =>
  request(`/comments/${commentId}/delete/`, { method: "DELETE" });
export const login = (username, password) =>
  request("/login/", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
export const register = (username, password) =>
  request("/register/", {
    method: "POST",
    body: JSON.stringify({ username, password }),
  });
export const getMe = () => request("/me/");
export { getToken };
