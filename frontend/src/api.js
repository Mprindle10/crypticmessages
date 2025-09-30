// API utility for connecting frontend to FastAPI backend
const API_BASE = "http://localhost:8000";

export async function subscribe(email, paymentMethodId) {
  const res = await fetch(`${API_BASE}/subscribe`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, payment_method_id: paymentMethodId })
  });
  return res.json();
}
