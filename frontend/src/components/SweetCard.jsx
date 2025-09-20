// frontend/src/components/SweetCard.jsx
import React from "react";

export default function SweetCard({ sweet, onPurchase, onDelete, onRestock, isAdmin }){
  return (
    <div className="card">
      <div className="sweet-name">{sweet.name}</div>
      <div className="small">{sweet.category} • ₹{Number(sweet.price).toFixed(2)}</div>
      <div className="small">Quantity: {sweet.quantity}</div>
      <div style={{marginTop:8, display:"flex", gap:8}}>
        <button disabled={sweet.quantity <= 0} onClick={()=>onPurchase(sweet.id)}>Purchase</button>
        {isAdmin ? <>
          <button onClick={()=>onRestock(sweet.id)}>Restock</button>
          <button onClick={()=>onDelete(sweet.id)}>Delete</button>
        </> : null}
      </div>
    </div>
  );
}
