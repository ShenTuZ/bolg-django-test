const API_BASE = "/api";

function getCSRFToken() {
  const match = document.cookie.match(/csrftoken=([^;]+)/);
  return match ? decodeURIComponent(match[1]) : "";
}

async function request(url, options = {}) {
  const { headers, ...rest } = options;
  const isUnsafe = options.method && !["GET", "HEAD"].includes(options.method);
  const res = await fetch(`${API_BASE}${url}`, {
    credentials: "include",
    headers: {
      "Content-Type": "application/json",
      ...(isUnsafe ? { "X-CSRFToken": getCSRFToken() } : {}),
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
export const logout = () => request("/logout/", { method: "POST" });
export const getMe = () => request("/me/");
export const fetchCsrf = () => request("/csrf/");
