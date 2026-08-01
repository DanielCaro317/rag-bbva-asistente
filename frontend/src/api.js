const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function sendMessage(question, sessionId) {
  const res = await fetch(`${API_URL}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question, session_id: sessionId }),
  });
  if (!res.ok) {
    let detail = `Error ${res.status}`;
    try {
      detail = (await res.json()).detail || detail;
    } catch {
      // la respuesta de error no traía JSON
    }
    throw new Error(detail);
  }
  return res.json();
}
