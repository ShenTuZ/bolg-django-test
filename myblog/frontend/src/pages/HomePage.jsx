import { useState, useEffect } from "react";
import { getPosts } from "../api";

export default function HomePage() {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    getPosts().then(setPosts).catch(console.error);
  }, []);

  return (
    <div className="page home-page">
      {posts.map((post) => (
        <article key={post.id} className="post-card">
          <h2>
            <a href={`/post/${post.id}`}>{post.title}</a>
          </h2>
          <div className="meta">
            <span>{post.author_name}</span>
            <span className="dot">·</span>
            <span>{post.category_name}</span>
            <span className="dot">·</span>
            <span>{post.created_at.slice(0, 10)}</span>
            <span className="dot">·</span>
            <span>{post.comment_count} 条评论</span>
          </div>
          <p className="excerpt">{post.content.slice(0, 200)}</p>
        </article>
      ))}
      {posts.length === 0 && <p className="empty">还没有文章</p>}
    </div>
  );
}
