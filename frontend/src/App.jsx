import { useState } from "react";

import { sendMessage, getMetrics } from "./api";

function newSessionId() {
  return "web-" + Math.random().toString(36).slice(2, 10);
}

function MetricsPanel({ data, error }) {
  if (error) return <div className="error">{error}</div>;
  if (!data) return <p className="empty">Cargando métricas…</p>;

  const items = [
    ["Sesiones", data.total_sessions],
    ["Mensajes", data.total_messages],
    ["Preguntas", data.total_questions],
    ["Respuestas", data.total_answers],
    ["Prom. msgs/sesión", data.avg_messages_per_session],
    ['Tasa "no sé"', data.grounding_no_answer_rate],
    ["Latencia media (ms)", data.avg_latency_ms],
    ["Latencia máx (ms)", data.max_latency_ms],
  ];

  return (
    <div className="metrics">
      <div className="metrics-grid">
        {items.map(([label, value]) => (
          <div key={label} className="metric">
            <span className="metric-value">{value}</span>
            <span className="metric-label">{label}</span>
          </div>
        ))}
      </div>
    </div>
  );
}

export default function App() {
  const [sessionId] = useState(newSessionId);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [view, setView] = useState("chat");
  const [metrics, setMetrics] = useState(null);
  const [metricsError, setMetricsError] = useState(null);

  async function openMetrics() {
    setView("metrics");
    setMetrics(null);
    setMetricsError(null);
    try {
      setMetrics(await getMetrics());
    } catch (err) {
      setMetricsError(err.message);
    }
  }

  async function handleSend(e) {
    e.preventDefault();
    const question = input.trim();
    if (!question || loading) return;

    setMessages((prev) => [...prev, { role: "user", content: question }]);
    setInput("");
    setLoading(true);
    setError(null);

    try {
      const data = await sendMessage(question, sessionId);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.answer, sources: data.sources },
      ]);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app">
      <header className="header">
        <h1>Asistente RAG · Banca</h1>
        <div className="header-actions">
          <span className="session">sesión {sessionId}</span>
          <button
            className={`tab ${view === "chat" ? "active" : ""}`}
            onClick={() => setView("chat")}
          >
            Chat
          </button>
          <button
            className={`tab ${view === "metrics" ? "active" : ""}`}
            onClick={openMetrics}
          >
            Métricas
          </button>
        </div>
      </header>

      {view === "metrics" ? (
        <MetricsPanel data={metrics} error={metricsError} />
      ) : (
        <>
          <div className="chat">
            {messages.length === 0 && (
              <p className="empty">Pregunta sobre los productos del banco.</p>
            )}
            {messages.map((m, i) => (
              <div key={i} className={`msg ${m.role}`}>
                <div className="bubble">{m.content}</div>
                {m.sources && m.sources.length > 0 && (
                  <div className="sources">
                    {m.sources.map((s) => (
                      <span key={s} className="source">{s}</span>
                    ))}
                  </div>
                )}
              </div>
            ))}
            {loading && (
              <div className="msg assistant">
                <div className="bubble">…</div>
              </div>
            )}
          </div>

          {error && <div className="error">{error}</div>}

          <form className="composer" onSubmit={handleSend}>
            <input
              value={input}
              onChange={(e) => setInput(e.target.value)}
              placeholder="Escribe tu pregunta…"
              disabled={loading}
            />
            <button type="submit" disabled={loading || !input.trim()}>
              Enviar
            </button>
          </form>
        </>
      )}
    </div>
  );
}
