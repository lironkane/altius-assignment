import { useState, useRef } from "react";
import axios from "axios";

const WEBSITES = [
  { value: "fo1.altius.finance", label: "FO1 – fo1.altius.finance" },
  { value: "fo2.altius.finance", label: "FO2 – fo2.altius.finance" },
];

const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function App() {
  const [website, setWebsite] = useState(WEBSITES[0].value);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [response, setResponse] = useState(null);

  const passwordRef = useRef(null);

  const submit = async (e) => {
    e.preventDefault();
    setError(null);
    setResponse(null);
    setLoading(true);

    try {
      const res = await axios.post(`${API_BASE_URL}/get_data`, {
        website,
        username,
        password,
      });

      setResponse(res.data);
    } catch (err) {
      if (err.response) {
        const status = err.response.status;

        if (status === 401) {
          setError("Invalid username or password. Please try again.");
          setPassword("");
          setTimeout(() => passwordRef.current?.focus(), 0);
          return;
        }

        setError(
          err.response.data?.detail ||
            `Request failed (status ${status})`
        );
      } else {
        setError("Backend is unreachable. Is the server running?");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>Site Crawler</h1>
        <p style={styles.subtitle}>
          Choose a website, log in, and view available deals
        </p>

        <form onSubmit={submit} style={styles.form}>
          <label style={styles.label}>
            Website
            <select
              value={website}
              onChange={(e) => setWebsite(e.target.value)}
              style={styles.input}
            >
              {WEBSITES.map((w) => (
                <option key={w.value} value={w.value}>
                  {w.label}
                </option>
              ))}
            </select>
          </label>

          <label style={styles.label}>
            Username (email)
            <input
              type="email"
              value={username}
              required
              onChange={(e) => setUsername(e.target.value)}
              style={styles.input}
              placeholder="user@whatever.com"
            />
          </label>

          <label style={styles.label}>
            Password
            <input
              ref={passwordRef}
              type="password"
              value={password}
              required
              onChange={(e) => setPassword(e.target.value)}
              style={styles.input}
            />
          </label>

          <button type="submit" disabled={loading} style={styles.button}>
            {loading ? "Logging in…" : "Login"}
          </button>
        </form>

        {error && <div style={styles.error}>{error}</div>}

        {response && (
          <div style={styles.result}>
            <h2>Deals</h2>

            {response.deals.length === 0 && <p>No deals found.</p>}

            <ul style={styles.deals}>
              {response.deals.map((deal) => (
                <li key={deal.id} style={styles.deal}>
                  <strong>{deal.title}</strong>
                  <div style={styles.meta}>
                    {deal.asset_class && <span>{deal.asset_class}</span>}
                    {deal.status && <span> · {deal.status}</span>}
                    {deal.currency && <span> · {deal.currency}</span>}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "#0f172a",
    display: "flex",
    justifyContent: "center",
    alignItems: "flex-start",
    paddingTop: 40,
    fontFamily: "system-ui",
    color: "#e5e7eb",
  },
  card: {
    width: "100%",
    maxWidth: 520,
    background: "#020617",
    borderRadius: 12,
    padding: 24,
    border: "1px solid #1e293b",
  },
  title: { margin: 0 },
  subtitle: { color: "#94a3b8", marginBottom: 24 },
  form: { display: "flex", flexDirection: "column", gap: 14 },
  label: { fontSize: 14, display: "flex", flexDirection: "column", gap: 4 },
  input: {
    padding: 8,
    borderRadius: 6,
    background: "#020617",
    color: "#e5e7eb",
    border: "1px solid #334155",
  },
  button: {
    marginTop: 10,
    padding: 10,
    borderRadius: 999,
    border: "none",
    background: "linear-gradient(to right,#38bdf8,#818cf8)",
    color: "#020617",
    fontWeight: 600,
    cursor: "pointer",
  },
  error: {
    marginTop: 16,
    padding: 10,
    background: "rgba(239,68,68,0.15)",
    borderRadius: 6,
    color: "#fecaca",
  },
  result: { marginTop: 24 },
  deals: { listStyle: "none", padding: 0 },
  deal: {
    padding: 10,
    marginBottom: 8,
    border: "1px solid #334155",
    borderRadius: 6,
  },
  meta: { fontSize: 12, color: "#94a3b8" },
};