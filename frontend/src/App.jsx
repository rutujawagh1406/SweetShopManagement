// frontend/src/App.jsx
import React, { useState, useEffect } from "react";
import Login from "./pages/Login";
import Register from "./pages/Register";
import SweetsList from "./pages/SweetsList";
import AdminPanel from "./pages/AdminPanel";
import api from "./services/api";

export default function App(){
  const [token, setToken] = useState(localStorage.getItem("token"));
  const [user, setUser] = useState(JSON.parse(localStorage.getItem("user")) || null);

  useEffect(()=> {
    if(token) api.setToken(token);
  }, [token]);

  function handleLogin(loginResponse){
    // loginResponse is the full response from backend: { access_token, username, is_admin, token_type }
    const t = loginResponse.access_token;
    const userInfo = { username: loginResponse.username, is_admin: loginResponse.is_admin };
    setToken(t);
    setUser(userInfo);
    localStorage.setItem("token", t);
    localStorage.setItem("user", JSON.stringify(userInfo));
    api.setToken(t);
  }

  function handleLogout(){
    setToken(null);
    setUser(null);
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    api.setToken(null);
  }

  return (
    <div className="container">
      <header>
        <h1>Sweet Shop</h1>
        {token ? (
          <div>
            <span>Hi, {user?.username} {user?.is_admin ? "(Admin)" : ""}</span>
            <button onClick={handleLogout}>Logout</button>
          </div>
        ) : null}
      </header>

      <main>
        {!token ? (
          <div className="auth-grid">
            <Login onLogin={handleLogin} />
            <Register />
          </div>
        ) : (
          <>
            <SweetsList isAdmin={user?.is_admin} />
            {user?.is_admin ? <AdminPanel /> : null}
          </>
        )}
      </main>
    </div>
  );
}
