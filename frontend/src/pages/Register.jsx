import React, { useState } from "react";
import api from "../services/api";

export default function Register(){
  const [username,setUsername]=useState("");
  const [password,setPassword]=useState("");
  const [adminSecret,setAdminSecret]=useState("");
  const [msg,setMsg]=useState(null);

  async function submit(e){
    e.preventDefault();
    setMsg(null);
    try{
      const res = await api.register(username, password, adminSecret || undefined);
      setMsg("Registered. You can now login.");
    }catch(e){
      setMsg("Error: " + (e.data?.detail || e.data || "Registration failed"));
    }
  }

  return (
    <div className="card" style={{minWidth:320}}>
      <h3>Register</h3>
      <form onSubmit={submit}>
        <input placeholder="Username" value={username} onChange={e=>setUsername(e.target.value)} />
        <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)} />
        <input placeholder="Admin secret (optional)" value={adminSecret} onChange={e=>setAdminSecret(e.target.value)} />
        <button type="submit">Register</button>
      </form>
      {msg ? <div className="small">{msg}</div> : null}
    </div>
  );
}
