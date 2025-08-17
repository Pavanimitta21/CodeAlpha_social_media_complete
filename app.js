
document.addEventListener('DOMContentLoaded', () => {
  const status = document.getElementById('status');
  const registerForm = document.getElementById('register-form');
  const loginForm = document.getElementById('login-form');
  const composer = document.getElementById('composer');
  const btnPost = document.getElementById('btn-post');
  const btnLogout = document.getElementById('btn-logout');
  const feed = document.getElementById('feed');

  function showStatus(msg, ok=true) {
    status.textContent = msg;
    status.style.color = ok ? 'green' : 'red';
  }

  async function loadFeed() {
    const res = await fetch('/api/feed/');
    const data = await res.json();
    feed.innerHTML = '';
    data.forEach(p => {
      const d = document.createElement('div');
      d.className = 'post';
      d.innerHTML = `<div class="meta">@${p.user} · ${new Date(p.created_at).toLocaleString()} · ❤ ${p.likes} · 💬 ${p.commentsCount}</div>
                     <div>${p.content}</div>
                     <div class="actions">
                       <button data-id="${p.id}" class="like-btn">Like</button>
                       <input placeholder="Write a comment..." class="c-input" data-id="${p.id}">
                       <button class="c-btn" data-id="${p.id}">Comment</button>
                       <button class="view-comments" data-id="${p.id}">View</button>
                     </div>`;
      feed.appendChild(d);
    });
  }

  registerForm.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const username = document.getElementById('reg-username').value;
    const password = document.getElementById('reg-password').value;
    const res = await fetch('/api/register/', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({username,password})});
    const data = await res.json();
    if (!res.ok) { showStatus(data.error || 'Register failed', false); return; }
    showStatus('Registered. You can login.');
    registerForm.reset();
  });

  loginForm.addEventListener('submit', async (e)=>{
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const res = await fetch('/api/login/', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({username,password})});
    const data = await res.json();
    if (!res.ok) { showStatus(data.error || 'Login failed', false); return; }
    showStatus('Logged in');
    loginForm.reset();
    composer.style.display = 'block';
    loadFeed();
  });

  btnLogout.addEventListener('click', async ()=>{
    await fetch('/api/logout/');
    showStatus('Logged out');
    composer.style.display='none';
  });

  btnPost.addEventListener('click', async ()=>{
    const content = document.getElementById('post-content').value;
    const res = await fetch('/api/posts/', {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({content})});
    const data = await res.json();
    if (!res.ok) { showStatus(data.error || 'Post failed', false); return; }
    showStatus('Posted');
    document.getElementById('post-content').value = '';
    loadFeed();
  });

  feed.addEventListener('click', async (e)=>{
    const id = e.target.dataset.id;
    if (e.target.classList.contains('like-btn')) {
      const res = await fetch(`/api/posts/${id}/like/`, {method:'POST'});
      const data = await res.json();
      if (!res.ok) { showStatus(data.error||'Like failed', false); return; }
      showStatus(data.liked ? 'Liked' : 'Unliked');
      loadFeed();
    } else if (e.target.classList.contains('c-btn')) {
      const input = document.querySelector('.c-input[data-id="'+id+'"]');
      const content = input.value;
      const res = await fetch(`/api/posts/${id}/comments/`, {method:'POST', headers:{'Content-Type':'application/json'}, body: JSON.stringify({content})});
      const data = await res.json();
      if (!res.ok) { showStatus(data.error||'Comment failed', false); return; }
      showStatus('Comment added');
      input.value='';
    } else if (e.target.classList.contains('view-comments')) {
      const res = await fetch(`/api/posts/${id}/comments/`);
      const data = await res.json();
      if (!res.ok) { showStatus(data.error||'Could not load', false); return; }
      let txt = 'Comments:\n';
      data.forEach(c=> txt += `@${c.user}: ${c.content}\n`);
      alert(txt);
    }
  });

  loadFeed();
});
