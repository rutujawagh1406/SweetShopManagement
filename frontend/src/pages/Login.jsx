// frontend/src/pages/Login.jsx
import React, { useState } from "react";
import api from "../services/api";

export default function Login({ onLogin }){
  const [username,setUsername] = useState("");
  const [password,setPassword] = useState("");
  const [err,setErr] = useState(null);

  async function submit(e){
    e.preventDefault();
    setErr(null);
    try{
      const res = await api.login(username, password);
      // res: { access_token, token_type, username, is_admin }
      onLogin(res);
    }catch(e){
      setErr(e.data?.detail || e.data || "Login failed");
    }
  }

  return (
    <div className="card" style={{minWidth:320}}>
      <h3>Login</h3>
      <form onSubmit={submit}>
        <input placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <button type="submit">Login</button>
        {err ? <div className="small" style={{color:"red"}}>{String(err)}</div> : null}
      </form>
    </div>
  );
}
