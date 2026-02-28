const result = document.getElementById('result');
const pageContent = document.getElementById('page-content');

const PROJECT_BACKGROUND_GIF = '/images/background.gif';
const BACKGROUND_FALLBACK_GIF = '/static/background.gif';

const resolveBackground = (primary, fallback) => new Promise((resolve) => {
  const image = new Image();
  image.onload = () => resolve(primary);
  image.onerror = () => resolve(fallback);
  image.src = primary;
});

resolveBackground(PROJECT_BACKGROUND_GIF, BACKGROUND_FALLBACK_GIF).then((imagePath) => {
  document.body.style.setProperty('--app-background-image', `url("${imagePath}")`);
});

const state = {
  token: localStorage.getItem('access_token') || '',
  page: 'intro',
};

const getToken = () => state.token.trim();
const setToken = (token) => {
  state.token = token;
  localStorage.setItem('access_token', token);
};

const show = (data) => {
  result.textContent = typeof data === 'string' ? data : JSON.stringify(data, null, 2);
};

const api = async (path, options = {}, auth = false) => {
  const headers = { 'Content-Type': 'application/json', ...(options.headers || {}) };
  if (auth) {
    headers.Authorization = `Bearer ${getToken()}`;
  }

  const response = await fetch(path, { ...options, headers });
  const contentType = response.headers.get('content-type') || '';
  const payload = contentType.includes('application/json') ? await response.json() : await response.text();
  if (!response.ok) throw payload;
  return payload;
};

const dockTemplate = () => `
  <div class="edge-hotspot" id="edge-hotspot" aria-hidden="true"></div>
  <aside class="side-dock" id="side-dock">
    <button class="dock-link" type="button" data-page="intro">Intro</button>
    <button class="dock-link" type="button" data-page="catalog">Catalog</button>
    <button class="dock-link" type="button" data-page="profile">Profile</button>
  </aside>
`;

const pages = {
  intro: () => `
    <section class="card intro-card page-view">
      <h2>Intro</h2>
      <p>Добро пожаловать в мини-приложение. Это отдельная страница Intro.</p>
      <p class="muted">Наведите курсор на правую полосу экрана — появится меню перехода между страницами.</p>
      <p class="muted">Фон берётся из <code>src/images/background.gif</code> (fallback: <code>src/web/static/background.gif</code>).</p>
    </section>
  `,
  catalog: () => `
    <section class="card page-view">
      <h2>Catalog</h2>
      <form id="create-item-form" class="grid four">
        <input name="name" placeholder="Name" required />
        <select name="category" required>
          <option value="home">home</option>
          <option value="school">school</option>
          <option value="college">college</option>
        </select>
        <input type="number" name="count" placeholder="Count" min="0" required />
        <input type="number" name="price" placeholder="Price" min="1" required />
        <button class="pulse-button" type="submit">Create item</button>
      </form>

      <div class="grid three actions">
        <button class="pulse-button" id="list-items" type="button">List items</button>
        <input id="item-id" type="number" placeholder="Item ID" min="1" />
        <button class="pulse-button" id="get-item" type="button">Get item by ID</button>
      </div>

      <form id="update-item-form" class="grid four">
        <input name="id" type="number" placeholder="Item ID" min="1" required />
        <input name="name" placeholder="New name" required />
        <select name="category" required>
          <option value="home">home</option>
          <option value="school">school</option>
          <option value="college">college</option>
        </select>
        <input type="number" name="count" placeholder="Count" min="0" required />
        <input type="number" name="price" placeholder="Price" min="1" required />
        <button class="pulse-button" type="submit">Update item</button>
      </form>

      <div class="grid three actions">
        <input id="delete-item-id" type="number" placeholder="Item ID for delete" min="1" />
        <button class="pulse-button" id="delete-item" type="button">Delete item</button>
      </div>

      <section class="catalog-list">
        <h3>Items in catalog</h3>
        <div id="catalog-items" class="items-grid"></div>
      </section>
    </section>
  `,
  profile: () => `
    <section class="card page-view">
      <h2>Profile</h2>
      <div class="grid two">
        <form id="register-form">
          <h3>Register</h3>
          <input name="username" placeholder="Username" required />
          <input type="email" name="email" placeholder="Email" required />
          <input type="password" name="password" placeholder="Password" required />
          <button class="pulse-button" type="submit">Register</button>
        </form>

        <form id="login-form">
          <h3>Login</h3>
          <input name="username" placeholder="Username" required />
          <input type="password" name="password" placeholder="Password" required />
          <button class="pulse-button" type="submit">Login</button>
        </form>
      </div>

      <div class="token-box">
        <label for="token">Access token</label>
        <textarea id="token" rows="3" placeholder="Token appears here after login">${state.token}</textarea>
        <div class="token-actions">
          <button class="pulse-button" id="save-token" type="button">Save token</button>
          <button class="pulse-button" id="me-button" type="button">Get /me</button>
        </div>
      </div>
    </section>
  `,
};


const normalizeItemsPayload = (payload) => {
  if (Array.isArray(payload)) return payload;
  if (Array.isArray(payload?.items)) return payload.items;
  if (Array.isArray(payload?.data)) return payload.data;
  return [];
};

const renderCatalogItems = (payload) => {
  const container = document.getElementById('catalog-items');
  if (!container) return;

  const items = normalizeItemsPayload(payload);
  if (!items.length) {
    container.innerHTML = '<p class="muted">No items yet.</p>';
    return;
  }

  container.innerHTML = items.map((item) => `
    <article class="item-card">
      <strong>#${item.id ?? '-'} · ${item.name ?? 'Unnamed'}</strong>
      <span>Category: ${item.category ?? '-'}</span>
      <span>Count: ${item.count ?? 0}</span>
      <span>Price: ${item.price ?? 0}</span>
    </article>
  `).join('');
};

const refreshCatalogItems = async () => {
  if (!getToken()) {
    renderCatalogItems([]);
    show('Login first to load catalog items.');
    return;
  }

  try {
    const payload = await api('/api/v1/users/items?limit=50&offset=0', {}, true);
    renderCatalogItems(payload);
    show(payload);
  } catch (error) {
    show(error);
  }
};

const attachCatalogEvents = () => {
  document.getElementById('create-item-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = new FormData(event.target);
    const payload = Object.fromEntries(form.entries());
    payload.count = Number(payload.count);
    payload.price = Number(payload.price);

    try {
      const response = await api('/api/v1/users/items', {
        method: 'POST',
        body: JSON.stringify(payload),
      }, true);
      show(response);
      await refreshCatalogItems();
    } catch (error) {
      show(error);
    }
  });

  document.getElementById('list-items').addEventListener('click', async () => {
    await refreshCatalogItems();
  });

  document.getElementById('get-item').addEventListener('click', async () => {
    const id = document.getElementById('item-id').value;
    if (!id) return show('Provide item ID');

    try {
      show(await api(`/api/v1/users/items/${id}`, {}, true));
    } catch (error) {
      show(error);
    }
  });

  document.getElementById('update-item-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = Object.fromEntries(new FormData(event.target).entries());
    const id = form.id;
    const payload = {
      name: form.name,
      category: form.category,
      count: Number(form.count),
      price: Number(form.price),
    };

    try {
      const response = await api(`/api/v1/users/items/${id}`, {
        method: 'PUT',
        body: JSON.stringify(payload),
      }, true);
      show(response);
      await refreshCatalogItems();
    } catch (error) {
      show(error);
    }
  });

  document.getElementById('delete-item').addEventListener('click', async () => {
    const id = document.getElementById('delete-item-id').value;
    if (!id) return show('Provide item ID');

    try {
      const response = await api(`/api/v1/users/items/${id}`, { method: 'DELETE' }, true);
      show(response);
      await refreshCatalogItems();
    } catch (error) {
      show(error);
    }
  });
};

const attachProfileEvents = () => {
  const tokenField = document.getElementById('token');

  document.getElementById('save-token').addEventListener('click', () => {
    setToken(tokenField.value.trim());
    show('Token saved');
  });

  document.getElementById('register-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = new FormData(event.target);
    try {
      const payload = Object.fromEntries(form.entries());
      const data = await api('/api/v1/users/auth/register', {
        method: 'POST',
        body: JSON.stringify(payload),
      });
      show(data);
    } catch (error) {
      show(error);
    }
  });

  document.getElementById('login-form').addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = new FormData(event.target);
    const body = new URLSearchParams(form).toString();
    try {
      const data = await fetch('/api/v1/users/auth/login', {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body,
      }).then(async (res) => {
        const json = await res.json();
        if (!res.ok) throw json;
        return json;
      });

      setToken(data.access_token);
      tokenField.value = data.access_token;
      show(data);
    } catch (error) {
      show(error);
    }
  });

  document.getElementById('me-button').addEventListener('click', async () => {
    try {
      show(await api('/api/v1/users/auth/me', {}, true));
    } catch (error) {
      show(error);
    }
  });
};

const renderPage = (pageName) => {
  state.page = pages[pageName] ? pageName : 'intro';
  pageContent.innerHTML = `${pages[state.page]()}${dockTemplate()}`;

  if (state.page === 'catalog') {
    attachCatalogEvents();
    refreshCatalogItems();
  }
  if (state.page === 'profile') attachProfileEvents();

  const dock = document.getElementById('side-dock');
  const hotspot = document.getElementById('edge-hotspot');

  const openDock = () => dock.classList.add('visible');
  const hideDock = () => dock.classList.remove('visible');

  hotspot.addEventListener('mouseenter', openDock);
  hotspot.addEventListener('mouseleave', hideDock);
  dock.addEventListener('mouseenter', openDock);
  dock.addEventListener('mouseleave', hideDock);

  dock.addEventListener('click', (event) => {
    const button = event.target.closest('[data-page]');
    if (!button) return;
    renderPage(button.dataset.page);
  });
};

renderPage('intro');
show('Hover over right border strip to open Intro/Catalog/Profile menu.');
