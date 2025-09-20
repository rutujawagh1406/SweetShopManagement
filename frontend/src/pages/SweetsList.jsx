// frontend/src/pages/SweetsList.jsx
import React, { useState, useEffect } from "react";
import api from "../services/api";
import SweetCard from "../components/SweetCard";

export default function SweetsList({ isAdmin=false }){
  const [sweets, setSweets] = useState([]);
  const [err, setErr] = useState(null);

  async function load(){
    try{
      const data = await api.listSweets();
      setSweets(data);
    }catch(e){
      setErr(e.data || "Failed to load");
    }
  }

  useEffect(()=>{ load(); }, []);

  async function handlePurchase(id){
    try{
      await api.purchase(id, 1);
      await load();
    }catch(e){
      alert("Purchase failed: " + (e.data?.detail || e.data || e));
    }
  }

  async function handleDelete(id){
    if(!confirm("Delete this sweet?")) return;
    try{
      await api.deleteSweet(id);
      await load();
    }catch(e){
      alert("Delete failed: " + (e.data?.detail || e.data || e));
    }
  }

  async function handleRestock(id){
    const qty = parseInt(prompt("Quantity to restock", "5"), 10);
    if(!qty) return;
    try{
      await api.restock(id, qty);
      await load();
    }catch(e){
      alert("Restock failed: " + (e.data?.detail || e.data || e));
    }
  }

  return (
    <div>
      <h2>Available Sweets</h2>
      {err ? <div className="small" style={{color:"red"}}>{err}</div> : null}
      <div className="sweets-grid">
        {sweets.map(s => (
          <SweetCard
            key={s.id}
            sweet={s}
            onPurchase={handlePurchase}
            onDelete={handleDelete}
            onRestock={handleRestock}
            isAdmin={isAdmin}
          />
        ))}
      </div>
    </div>
  );
}
