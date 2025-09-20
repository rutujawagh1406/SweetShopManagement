// frontend/src/services/api.js
const BASE = import.meta.env.VITE_API_BASE_URL || "http://127.0.0.1:8000";

let token = null;
function setToken(t){ token = t; }

async function request(path, { method="GET", body } = {}) {
  const headers = {"Content-Type":"application/json"};
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const res = await fetch(BASE + path, {
    method,
    headers,
    body: body ? JSON.stringify(body) : undefined
  });
  const text = await res.text();
  let data;
  try { data = text ? JSON.parse(text) : null; } catch(e) { data = text; }
  if (!res.ok) throw { status: res.status, data };
  return data;
}

export default {
  setToken,
  register: (username, password, admin_secret) => request("/api/auth/register", {method:"POST", body:{username, password, admin_secret}}),
  login: (username, password) => request("/api/auth/login", {method:"POST", body:{username, password}}),
  listSweets: () => request("/api/sweets"),
  addSweet: (payload) => request("/api/sweets", {method:"POST", body: payload}),
  purchase: (id, qty=1) => request(`/api/sweets/${id}/purchase`, {method:"POST", body:{quantity: qty}}),
  restock: (id, qty=1) => request(`/api/sweets/${id}/restock`, {method:"POST", body:{quantity: qty}}),
  update: (id, payload) => request(`/api/sweets/${id}`, {method:"PUT", body: payload}),
  deleteSweet: (id) => request(`/api/sweets/${id}`, {method:"DELETE"})
};
