// API 주소
const API_URL = '/api';

// 날짜 형식 변환 함수
function formatDate(dateString) {
  const date = new Date(dateString);
  return `${date.getFullYear()}년 ${date.getMonth() + 1}월 ${date.getDate()}일 ${date.getHours()}:${date.getMinutes()}`;
}

// 에러 컴포넌트
const ErrorMessage = ({ message }) => {
  return message ? <div className="error">{message}</div> : null;
};

// 로딩 컴포넌트
const Loading = () => {
  return <div className="loading">로딩 중...</div>;
};

// 댓글 컴포넌트
const Comment = ({ comment, postId, onDelete, currentUser }) => {
  const [isEditing, setIsEditing] = React.useState(false);
  const [newContent, setNewContent] = React.useState(comment.content);

  const handleEdit = async () => {
    try {
      const response = await fetch(`${API_URL}/posts/${postId}/comments/${comment.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: newContent })
      });
      
      if (!response.ok) throw new Error('댓글 수정에 실패했습니다.');
      
      setIsEditing(false);
      // 상위 컴포넌트에서 댓글 목록 새로고침을 처리합니다
    } catch (error) {
      console.error('댓글 수정 오류:', error);
    }
  };

  return (
    <div className="comment">
      <div className="comment-header">
        <span className="comment-username">{comment.userName}</span>
        <span className="comment-date">{formatDate(comment.createdAt)}</span>
      </div>
      
      {isEditing ? (
        <div className="edit-form">
          <input
            type="text"
            value={newContent}
            onChange={(e) => setNewContent(e.target.value)}
          />
          <button className="button" onClick={handleEdit}>저장</button>
          <button className="button" onClick={() => setIsEditing(false)}>취소</button>
        </div>
      ) : (
        <>
          <p>{comment.content}</p>
          {currentUser === comment.userName && (
            <div>
              <button className="button" onClick={() => setIsEditing(true)}>수정</button>
              <button className="button delete" onClick={() => onDelete(comment.id)}>삭제</button>
            </div>
          )}
        </>
      )}
    </div>
  );
};

// 포스트 컴포넌트
const Post = ({ post, onDelete, onUpdate, currentUser }) => {
  const [comments, setComments] = React.useState([]);
  const [showComments, setShowComments] = React.useState(false);
  const [newComment, setNewComment] = React.useState('');
  const [isEditing, setIsEditing] = React.useState(false);
  const [newContent, setNewContent] = React.useState(post.content);
  const [liked, setLiked] = React.useState(false);
  const [error, setError] = React.useState('');
  const [loadingComments, setLoadingComments] = React.useState(false);

  // 댓글 불러오기
  const fetchComments = async () => {
    if (!showComments) return;
    
    setLoadingComments(true);
    try {
      const response = await fetch(`${API_URL}/posts/${post.id}/comments`);
      if (!response.ok) throw new Error('댓글을 불러오는데 실패했습니다.');
      
      const data = await response.json();
      setComments(data);
    } catch (error) {
      console.error('댓글 불러오기 오류:', error);
      setError('댓글을 불러오는데 실패했습니다.');
    } finally {
      setLoadingComments(false);
    }
  };

  // 댓글 표시 토글 시 댓글 로딩
  React.useEffect(() => {
    fetchComments();
  }, [showComments]);

  // 새 댓글 작성
  const handleCommentSubmit = async (e) => {
    e.preventDefault();
    if (!newComment.trim()) return;
    
    try {
      const response = await fetch(`${API_URL}/posts/${post.id}/comments`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userName: currentUser, content: newComment })
      });
      
      if (!response.ok) throw new Error('댓글 작성에 실패했습니다.');
      
      const data = await response.json();
      setComments([...comments, data]);
      setNewComment('');
      // 댓글 카운트는 백엔드에서 자동으로 증가하므로 포스트 새로고침이 필요합니다
      onUpdate();
    } catch (error) {
      console.error('댓글 작성 오류:', error);
      setError('댓글 작성에 실패했습니다.');
    }
  };

  // 댓글 삭제
  const handleCommentDelete = async (commentId) => {
    try {
      const response = await fetch(`${API_URL}/posts/${post.id}/comments/${commentId}`, {
        method: 'DELETE'
      });
      
      if (!response.ok) throw new Error('댓글 삭제에 실패했습니다.');
      
      setComments(comments.filter(c => c.id !== commentId));
      onUpdate(); // 댓글 카운트 업데이트를 위해 포스트 새로고침
    } catch (error) {
      console.error('댓글 삭제 오류:', error);
      setError('댓글 삭제에 실패했습니다.');
    }
  };

  // 포스트 수정
  const handleEdit = async () => {
    try {
      const response = await fetch(`${API_URL}/posts/${post.id}`, {
        method: 'PATCH',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ content: newContent })
      });
      
      if (!response.ok) throw new Error('포스트 수정에 실패했습니다.');
      
      const updatedPost = await response.json();
      onUpdate(updatedPost);
      setIsEditing(false);
    } catch (error) {
      console.error('포스트 수정 오류:', error);
      setError('포스트 수정에 실패했습니다.');
    }
  };

  // 좋아요 토글
  const toggleLike = async () => {
    try {
      if (liked) {
        // 좋아요 취소
        const response = await fetch(`${API_URL}/posts/${post.id}/likes`, {
          method: 'DELETE',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userName: currentUser })
        });
        
        if (!response.ok) throw new Error('좋아요 취소에 실패했습니다.');
        
        setLiked(false);
      } else {
        // 좋아요 추가
        const response = await fetch(`${API_URL}/posts/${post.id}/likes`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ userName: currentUser })
        });
        
        if (!response.ok) throw new Error('좋아요에 실패했습니다.');
        
        setLiked(true);
      }
      onUpdate(); // 좋아요 카운트 업데이트를 위해 포스트 새로고침
    } catch (error) {
      console.error('좋아요 오류:', error);
      setError('좋아요 처리에 실패했습니다.');
    }
  };

  return (
    <div className="post">
      <div className="post-header">
        <span className="post-username">{post.userName}</span>
        <span className="post-date">{formatDate(post.createdAt)}</span>
      </div>
      
      {isEditing ? (
        <div className="edit-form">
          <textarea
            value={newContent}
            onChange={(e) => setNewContent(e.target.value)}
          />
          <button className="button" onClick={handleEdit}>저장</button>
          <button className="button" onClick={() => setIsEditing(false)}>취소</button>
        </div>
      ) : (
        <div className="post-content">{post.content}</div>
      )}
      
      <ErrorMessage message={error} />
      
      <div className="post-actions">
        <div>
          <button className="like-button" onClick={toggleLike}>
            {liked ? '❤️' : '🤍'} {post.likeCount}
          </button>
          <button className="button" onClick={() => setShowComments(!showComments)}>
            댓글 {post.commentCount}개 {showComments ? '숨기기' : '보기'}
          </button>
        </div>
        
        {currentUser === post.userName && (
          <div>
            <button className="button" onClick={() => setIsEditing(true)}>수정</button>
            <button className="button delete" onClick={() => onDelete(post.id)}>삭제</button>
          </div>
        )}
      </div>
      
      {showComments && (
        <div className="comments">
          {loadingComments ? (
            <Loading />
          ) : (
            <>
              {comments.map(comment => (
                <Comment
                  key={comment.id}
                  comment={comment}
                  postId={post.id}
                  onDelete={handleCommentDelete}
                  currentUser={currentUser}
                />
              ))}
              
              <form className="comment-form" onSubmit={handleCommentSubmit}>
                <input
                  type="text"
                  placeholder="댓글을 입력하세요"
                  value={newComment}
                  onChange={(e) => setNewComment(e.target.value)}
                />
                <button className="button" type="submit">댓글 작성</button>
              </form>
            </>
          )}
        </div>
      )}
    </div>
  );
};

// 메인 앱 컴포넌트
const App = () => {
  const [posts, setPosts] = React.useState([]);
  const [userName, setUserName] = React.useState('');
  const [content, setContent] = React.useState('');
  const [isLoggedIn, setIsLoggedIn] = React.useState(false);
  const [loading, setLoading] = React.useState(true);
  const [error, setError] = React.useState('');

  // 포스트 로딩
  const fetchPosts = async () => {
    setLoading(true);
    try {
      const response = await fetch(`${API_URL}/posts`);
      if (!response.ok) throw new Error('포스트를 불러오는데 실패했습니다.');
      
      const data = await response.json();
      setPosts(data);
    } catch (error) {
      console.error('포스트 불러오기 오류:', error);
      setError('포스트를 불러오는데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  // 컴포넌트 마운트 시 포스트 로딩
  React.useEffect(() => {
    fetchPosts();
  }, []);

  // 로그인 처리
  const handleLogin = (e) => {
    e.preventDefault();
    if (userName.trim()) {
      setIsLoggedIn(true);
      localStorage.setItem('userName', userName);
    }
  };

  // 로컬 스토리지에서 사용자 이름 로드
  React.useEffect(() => {
    const savedUserName = localStorage.getItem('userName');
    if (savedUserName) {
      setUserName(savedUserName);
      setIsLoggedIn(true);
    }
  }, []);

  // 로그아웃 처리
  const handleLogout = () => {
    setIsLoggedIn(false);
    localStorage.removeItem('userName');
  };

  // 새 포스트 작성
  const handlePostSubmit = async (e) => {
    e.preventDefault();
    if (!content.trim()) return;
    
    try {
      const response = await fetch(`${API_URL}/posts`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ userName, content })
      });
      
      if (!response.ok) throw new Error('포스트 작성에 실패했습니다.');
      
      const newPost = await response.json();
      setPosts([newPost, ...posts]);
      setContent('');
    } catch (error) {
      console.error('포스트 작성 오류:', error);
      setError('포스트 작성에 실패했습니다.');
    }
  };

  // 포스트 삭제
  const handlePostDelete = async (postId) => {
    try {
      const response = await fetch(`${API_URL}/posts/${postId}`, {
        method: 'DELETE'
      });
      
      if (!response.ok) throw new Error('포스트 삭제에 실패했습니다.');
      
      setPosts(posts.filter(post => post.id !== postId));
    } catch (error) {
      console.error('포스트 삭제 오류:', error);
      setError('포스트 삭제에 실패했습니다.');
    }
  };

  // 포스트 업데이트 (수정 또는 댓글/좋아요 카운트 변경 시)
  const handlePostUpdate = async (updatedPost) => {
    if (updatedPost) {
      // 수정된 포스트가 전달된 경우
      setPosts(posts.map(post => post.id === updatedPost.id ? updatedPost : post));
    } else {
      // 새로고침이 필요한 경우
      fetchPosts();
    }
  };

  // 로그인 화면
  if (!isLoggedIn) {
    return (
      <div className="container">
        <div className="header">
          <h1>간단한 SNS</h1>
        </div>
        
        <div className="post-form">
          <h2>로그인</h2>
          <form onSubmit={handleLogin}>
            <input
              type="text"
              placeholder="사용자 이름을 입력하세요"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              required
            />
            <button className="button" type="submit">로그인</button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="container">
      <div className="header">
        <h1>간단한 SNS</h1>
        <div>
          <span>안녕하세요, {userName}님!</span>
          <button className="button" onClick={handleLogout}>로그아웃</button>
        </div>
      </div>
      
      <div className="post-form">
        <h2>새 포스트 작성</h2>
        <ErrorMessage message={error} />
        <form onSubmit={handlePostSubmit}>
          <textarea
            placeholder="무슨 일이 있었나요?"
            value={content}
            onChange={(e) => setContent(e.target.value)}
            required
          />
          <button className="button" type="submit">게시</button>
        </form>
      </div>
      
      <div className="post-list">
        <h2>최근 포스트</h2>
        {loading ? (
          <Loading />
        ) : (
          <>
            {posts.length === 0 ? (
              <p>포스트가 없습니다. 첫 포스트를 작성해보세요!</p>
            ) : (
              posts.map(post => (
                <Post
                  key={post.id}
                  post={post}
                  onDelete={handlePostDelete}
                  onUpdate={handlePostUpdate}
                  currentUser={userName}
                />
              ))
            )}
          </>
        )}
      </div>
    </div>
  );
};

// 앱 렌더링
ReactDOM.render(<App />, document.getElementById('app')); 