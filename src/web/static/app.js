const result = document.getElementById('result');
const tokenField = document.getElementById('token');

const getToken = () => localStorage.getItem('access_token') || tokenField.value.trim();
const setToken = (token) => {
  tokenField.value = token;
  localStorage.setItem('access_token', token);
};

if (localStorage.getItem('access_token')) {
  tokenField.value = localStorage.getItem('access_token');
}

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

document.getElementById('create-item-form').addEventListener('submit', async (event) => {
  event.preventDefault();
  const form = new FormData(event.target);
  const payload = Object.fromEntries(form.entries());
  payload.count = Number(payload.count);
  payload.price = Number(payload.price);

  try {
    show(await api('/api/v1/users/items', {
      method: 'POST',
      body: JSON.stringify(payload),
    }, true));
  } catch (error) {
    show(error);
  }
});

document.getElementById('list-items').addEventListener('click', async () => {
  try {
    show(await api('/api/v1/users/items?limit=10&offset=0', {}, true));
  } catch (error) {
    show(error);
  }
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
    show(await api(`/api/v1/users/items/${id}`, {
      method: 'PUT',
      body: JSON.stringify(payload),
    }, true));
  } catch (error) {
    show(error);
  }
});

document.getElementById('delete-item').addEventListener('click', async () => {
  const id = document.getElementById('delete-item-id').value;
  if (!id) return show('Provide item ID');

  try {
    show(await api(`/api/v1/users/items/${id}`, { method: 'DELETE' }, true));
  } catch (error) {
    show(error);
  }
});
