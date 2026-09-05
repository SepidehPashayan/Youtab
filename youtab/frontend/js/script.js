
const API_BASE = '';
let MODELS = {};       
let currentModel = 'kourosh';

async function loadCarsFromServer() {
  try {
    const res = await fetch(`${API_BASE}/api/cars`);
    if (!res.ok) throw new Error('failed to load cars');
    const cars = await res.json();

    cars.forEach(car => {
      const defaultColor = car.colors.find(c => c.is_default) || car.colors[0];
      MODELS[car.key] = {
        id: car.id,
        name: car.name,
        price: Number(car.base_price),
        priceLabel: Number(car.base_price).toLocaleString('en-US') + ' Toman',
        color: defaultColor ? defaultColor.name : '',
        img: defaultColor ? defaultColor.image_path : '',
        colors: car.colors,
      };
    });
  } catch (err) {
    console.error('Could not load car data from the server:', err);
  }
}

document.querySelectorAll('.swatches').forEach(group => {
  group.addEventListener('click', (e) => {
    const sw = e.target.closest('.swatch');
    if (!sw) return;

    group.querySelectorAll('.swatch').forEach(s => s.classList.remove('active'));
    sw.classList.add('active');

    const targetId = group.dataset.target;
    document.getElementById(targetId).src = sw.dataset.src;

    const modelKey = targetId.includes('kourosh') ? 'kourosh' : 'ario';
    if (MODELS[modelKey]) {
      MODELS[modelKey].img = sw.dataset.src;
      MODELS[modelKey].color = sw.dataset.name;
    }
  });
});


function selectForConfig(modelKey) {
  currentModel = modelKey;
  const m = MODELS[modelKey];
  if (!m) return;
  document.getElementById('config-img').src = m.img;
  document.getElementById('config-name').textContent = m.name;
  document.getElementById('config-color').textContent = m.color;
  document.getElementById('config-price').textContent = m.priceLabel;
  document.getElementById('configure').scrollIntoView({ behavior: 'smooth' });
}

function goCheckout() {
  const m = MODELS[currentModel];
  if (m) {
    document.getElementById('pay-amount').textContent = '(' + m.priceLabel + ')';
  }
  document.getElementById('checkout').scrollIntoView({ behavior: 'smooth' });
  renderCheckoutAuthState();
}

function getToken() { return localStorage.getItem('youtab_token'); }
function getStoredUser() {
  const raw = localStorage.getItem('youtab_user');
  return raw ? JSON.parse(raw) : null;
}
function setSession(token, user) {
  localStorage.setItem('youtab_token', token);
  localStorage.setItem('youtab_user', JSON.stringify(user));
}
function clearSession() {
  localStorage.removeItem('youtab_token');
  localStorage.removeItem('youtab_user');
}

function handleNavAuthClick(e) {
  e.preventDefault();
  if (getToken()) {
    clearSession();
    renderNavAuthState();
    renderCheckoutAuthState();
  } else {
    openAuthModal();
  }
  return false;
}

function renderNavAuthState() {
  const btn = document.getElementById('navAuthBtn');
  const ordersBtn = document.getElementById('navOrdersBtn');
  const user = getStoredUser();
  if (user && getToken()) {
    btn.innerHTML = `<img src="icon/man.png" alt="">${user.full_name.split(' ')[0]} · Sign Out`;
    ordersBtn.style.display = 'flex';
  } else {
    btn.innerHTML = `<img src="icon/man.png" alt="">Sign In`;
    ordersBtn.style.display = 'none';
  }
}

function renderCheckoutAuthState() {
  const user = getStoredUser();
  const signedOutBox = document.getElementById('checkout-signed-out');
  const form = document.getElementById('checkout-form');
  if (user && getToken()) {
    signedOutBox.style.display = 'none';
    form.style.display = 'block';
    document.getElementById('coFullName').value = user.full_name;
    document.getElementById('coPhone').value = user.phone_number;
    document.getElementById('coNational').value = user.national_id;
  } else {
    signedOutBox.style.display = 'block';
    form.style.display = 'none';
  }
}

function openAuthModal() {
  document.getElementById('authOverlay').classList.add('show');
  document.getElementById('authError').textContent = '';
}
function closeAuthModal() {
  document.getElementById('authOverlay').classList.remove('show');
}
function switchAuthTab(tab) {
  document.querySelectorAll('.modal-tab').forEach(t => t.classList.toggle('active', t.dataset.tab === tab));
  document.getElementById('loginForm').classList.toggle('active', tab === 'login');
  document.getElementById('registerForm').classList.toggle('active', tab === 'register');
  document.getElementById('authError').textContent = '';
}

function handleOrdersClick(e) {
  e.preventDefault();
  openOrdersModal();
  return false;
}

function openOrdersModal() {
  document.getElementById('ordersOverlay').classList.add('show');
  loadMyOrders();
}
function closeOrdersModal() {
  document.getElementById('ordersOverlay').classList.remove('show');
}

async function loadMyOrders() {
  const list = document.getElementById('ordersList');
  list.innerHTML = '<div class="order-empty">Loading…</div>';

  const token = getToken();
  if (!token) {
    list.innerHTML = '<div class="order-empty">Sign in to see your orders.</div>';
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/orders/me`, {
      headers: { 'Authorization': `Bearer ${token}` },
    });
    if (!res.ok) {
      list.innerHTML = '<div class="order-empty">Could not load your orders.</div>';
      return;
    }
    const orders = await res.json();
    if (orders.length === 0) {
      list.innerHTML = '<div class="order-empty">You have no orders yet.</div>';
      return;
    }

    list.innerHTML = orders.map(o => {
      const carLabel = Object.values(MODELS).find(m => m.id === o.car_model_id)?.name || `Model #${o.car_model_id}`;
      const date = new Date(o.created_at).toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
      const priceLabel = Number(o.total_price).toLocaleString('en-US') + ' Toman';
      return `
        <div class="order-card">
          <div class="order-main">
            <b>${carLabel} — ${o.color_name}</b>
            <span>${date} · ${o.delivery_address} · ${o.status}</span>
          </div>
          <div class="order-price">${priceLabel}</div>
        </div>`;
    }).join('');
  } catch (err) {
    list.innerHTML = '<div class="order-empty">Could not reach the server.</div>';
  }
}

async function handleLogin(e) {
  e.preventDefault();
  const phone_number = document.getElementById('loginPhone').value.trim();
  const password = document.getElementById('loginPassword').value;
  const errBox = document.getElementById('authError');
  errBox.textContent = '';

  try {
    const res = await fetch(`${API_BASE}/api/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ phone_number, password }),
    });
    const data = await res.json();
    if (!res.ok) {
      errBox.textContent = data.detail || 'Sign in failed.';
      return false;
    }
    setSession(data.access_token, data.user);
    renderNavAuthState();
    renderCheckoutAuthState();
    closeAuthModal();
  } catch (err) {
    errBox.textContent = 'Could not reach the server. Is the backend running?';
  }
  return false;
}

async function handleRegister(e) {
  e.preventDefault();
  const full_name = document.getElementById('regName').value.trim();
  const phone_number = document.getElementById('regPhone').value.trim();
  const national_id = document.getElementById('regNational').value.trim();
  const password = document.getElementById('regPassword').value;
  const errBox = document.getElementById('authError');
  errBox.textContent = '';

  try {
    const res = await fetch(`${API_BASE}/api/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ full_name, phone_number, national_id, password }),
    });
    const data = await res.json();
    if (!res.ok) {
      errBox.textContent = data.detail || 'Registration failed.';
      return false;
    }
    setSession(data.access_token, data.user);
    renderNavAuthState();
    renderCheckoutAuthState();
    closeAuthModal();
  } catch (err) {
    errBox.textContent = 'Could not reach the server. Is the backend running?';
  }
  return false;
}

async function fakePay() {
  const errBox = document.getElementById('checkoutError');
  errBox.textContent = '';

  const token = getToken();
  if (!token) {
    openAuthModal();
    return;
  }

  const address = document.getElementById('coAddress').value.trim();
  if (!address) {
    errBox.textContent = 'Please enter a delivery address.';
    return;
  }

  const m = MODELS[currentModel];
  if (!m) {
    errBox.textContent = 'Car data has not loaded from the server yet — try again in a moment.';
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/api/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`,
      },
      body: JSON.stringify({
        car_key: currentModel,
        color_name: m.color,
        delivery_address: address,
      }),
    });
    const data = await res.json();
    if (!res.ok) {
      errBox.textContent = data.detail || 'Could not place the order.';
      return;
    }
    document.getElementById('checkout-form').style.display = 'none';
    document.getElementById('success-box').classList.add('show');
  } catch (err) {
    errBox.textContent = 'Could not reach the server. Is the backend running?';
  }
}

window.addEventListener('DOMContentLoaded', async () => {
  await loadCarsFromServer();
  renderNavAuthState();
  renderCheckoutAuthState();

  const tl = gsap.timeline();
  tl.to('#speedCar', { left: '115%', duration: 1.1, ease: 'power2.in' }, 0)
    .to('#trail', { opacity: 1, left: '110%', duration: 1.0, ease: 'power2.in' }, 0.05)
    .to('#trail', { opacity: 0, duration: .3 }, 0.9)
    .to('#wordmark', { opacity: 1, y: 0, duration: .7, ease: 'power2.out' }, 0.9)
    .to('#scrollCue', { opacity: 1, duration: .5 }, '-=.2');
});
