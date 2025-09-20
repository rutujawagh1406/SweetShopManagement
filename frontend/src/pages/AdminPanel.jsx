import React, { useState } from "react";
import api from "../services/api";

export default function AdminPanel(){
  const [name,setName]=useState("");
  const [category,setCategory]=useState("");
  const [price,setPrice]=useState("");
  const [qty,setQty]=useState(0);
  const [msg,setMsg]=useState(null);

  async function submit(e){
    e.preventDefault();
    setMsg(null);
    try{
      await api.addSweet({ name, category, price: Number(price), quantity: Number(qty) });
      setMsg("Added");
      setName(""); setCategory(""); setPrice(""); setQty(0);
    }catch(e){
      setMsg("Error: " + (e.data?.detail || e.data || "Failed"));
    }
  }

  return (
    <div style={{marginTop:20}} className="card">
      <h3>Admin Panel</h3>
      <form onSubmit={submit}>
        <input placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
        <input placeholder="Category" value={category} onChange={e=>setCategory(e.target.value)} />
        <input placeholder="Price" value={price} onChange={e=>setPrice(e.target.value)} />
        <input placeholder="Quantity" value={qty} onChange={e=>setQty(e.target.value)} type="number" />
        <button type="submit">Add Sweet</button>
      </form>
      {msg ? <div className="small">{msg}</div> : null}
    </div>
  );
}
