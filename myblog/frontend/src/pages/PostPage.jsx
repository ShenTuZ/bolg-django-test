import { useState, useEffect } from "react";
import { useParams } from "react-router-dom";
import { getPost, addComment, deleteComment } from "../api";

export default function PostPage({ user, onRefreshUser }) {
  const { id } = useParams();
  const [post, setPost] = useState(null);
  const [text, setText] = useState("");

  useEffect(() => {
    getPost(id).then(setPost).catch(console.error);
  }, [id]);

  const handleComment = async (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    await addComment(id, text);
    setText("");
    const updated = await getPost(id);
    setPost(updated);
  };

  const handleDelete = async (commentId) => {
    if (!confirm("确定删除？")) return;
    await deleteComment(commentId);
    const updated = await getPost(id);
    setPost(updated);
  };

  if (!post) return <div className="page"><p className="empty">加载中...</p></div>;

  return (
    <div className="page post-page">
      <article className="post-card">
        <h1>{post.title}</h1>
        <div className="meta">
          <span>{post.author_name}</span>
          <span className="dot">·</span>
          <span>{post.category_name}</span>
          <span className="dot">·</span>
          <span>{post.created_at.slice(0, 10)}</span>
          <span className="dot">·</span>
          <span>{post.comments.length} 条评论</span>
        </div>
        <div className="content">{post.content}</div>
      </article>

      <section className="comments">
        <h3>评论</h3>
        {post.comments.length === 0 && <p className="empty">还没有评论</p>}
        {post.comments.map((c) => (
          <div key={c.id} className="comment">
            <div className="comment-header">
              <strong>{c.author_name}</strong>
              <span className="time">{c.created_at.slice(0, 16).replace("T", " ")}</span>
              {user && user.is_staff && (
                <button className="btn-delete" onClick={() => handleDelete(c.id)}>
                  删除
                </button>
              )}
            </div>
            <p>{c.content}</p>
          </div>
        ))}

        {user ? (
          <form className="comment-form" onSubmit={handleComment}>
            <textarea
              rows="3"
              placeholder={`${user.username}，说点什么...`}
              value={text}
              onChange={(e) => setText(e.target.value)}
            />
            <button type="submit">发表评论</button>
          </form>
        ) : (
          <p className="login-hint">
            <a href="/login">登录</a>后可以发表评论
          </p>
        )}
      </section>
    </div>
  );
}
