import { useState } from "react";
import axios from "axios";

const WEBSITES = [
  { value: "fo1.altius.finance", label: "FO1 (fo1.altius.finance)" },
  { value: "fo2.altius.finance", label: "FO2 (fo2.altius.finance)" },
];

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export default function App() {
  const [website, setWebsite] = useState(WEBSITES[0].value);
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [result, setResult] = useState(null); // { website, token, deals }

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");
    setResult(null);
    setLoading(true);

    try {
      const response = await axios.post(`${API_BASE_URL}/get_data`, {
        website,
        username,
        password,
      });

      setResult(response.data);
    } catch (err) {
      if (err.response) {
        // שגיאה מהשרת
        setError(
          err.response.data?.detail ||
            `Request failed with status ${err.response.status}`
        );
      } else {
        setError("Failed to reach the server. Is the backend running?");
      }
    } finally {
      setLoading(false);
    }
  };

  const handleWebsiteChange = (e) => {
    setWebsite(e.target.value);
    // לא מאפס אוטומטית את ה-username/password – שתרגיש "אקסטרה" אנושי
  };

  return (
    <div style={styles.page}>
      <div style={styles.card}>
        <h1 style={styles.title}>Site Crawler Login</h1>
        <p style={styles.subtitle}>
          Choose a website, enter credentials, and fetch available deals.
        </p>

        <form onSubmit={handleSubmit} style={styles.form}>
          {/* Website select */}
          <div style={styles.field}>
            <label style={styles.label}>Website</label>
            <select
              value={website}
              onChange={handleWebsiteChange}
              style={styles.input}
            >
              {WEBSITES.map((w) => (
                <option key={w.value} value={w.value}>
                  {w.label}
                </option>
              ))}
            </select>
          </div>

          {/* Username */}
          <div style={styles.field}>
            <label style={styles.label}>Username (email)</label>
            <input
              type="email"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              style={styles.input}
              placeholder="aaaaa@whatever.com"
              required
            />
          </div>

          {/* Password */}
          <div style={styles.field}>
            <label style={styles.label}>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              style={styles.input}
              required
            />
          </div>

          <button type="submit" style={styles.button} disabled={loading}>
            {loading ? "Logging in..." : "Send"}
          </button>
        </form>

        {/* Error */}
        {error && <div style={styles.error}>{error}</div>}

        {/* Result */}
        {result && (
          <div style={styles.resultBox}>
            <h2 style={styles.resultTitle}>Server Response</h2>

            <div style={styles.resultSection}>
              <strong>Website:</strong> {result.website}
            </div>

            {/* אם ה-API שלך מחזיר token */}
            {result.token && (
              <div style={styles.resultSection}>
                <strong>Token:</strong>
                <div style={styles.tokenBox}>{result.token}</div>
              </div>
            )}

            <div style={styles.resultSection}>
              <strong>Deals:</strong>
              {(!result.deals || result.deals.length === 0) && (
                <div style={{ marginTop: 4 }}>No deals found.</div>
              )}
              {result.deals && result.deals.length > 0 && (
                <ul style={styles.dealsList}>
                  {result.deals.map((deal) => (
                    <li key={deal.id} style={styles.dealItem}>
                      <div style={styles.dealTitle}>{deal.title}</div>
                      <div style={styles.dealMeta}>
                        {deal.asset_class && (
                          <span>Asset class: {deal.asset_class}</span>
                        )}
                        {deal.status && (
                          <span style={{ marginLeft: 8 }}>
                            Status: {deal.status}
                          </span>
                        )}
                        {deal.currency && (
                          <span style={{ marginLeft: 8 }}>
                            Currency: {deal.currency}
                          </span>
                        )}
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

const styles = {
  page: {
    minHeight: "100vh",
    display: "flex",
    justifyContent: "center",
    alignItems: "flex-start",
    padding: "40px 16px",
    background: "#0f172a",
    color: "#e5e7eb",
    fontFamily: "system-ui, -apple-system, BlinkMacSystemFont, sans-serif",
  },
  card: {
    width: "100%",
    maxWidth: 600,
    background: "#020617",
    borderRadius: 12,
    padding: 24,
    boxShadow: "0 20px 40px rgba(0,0,0,0.35)",
    border: "1px solid rgba(148,163,184,0.3)",
  },
  title: {
    fontSize: 24,
    marginBottom: 4,
  },
  subtitle: {
    fontSize: 14,
    color: "#94a3b8",
    marginBottom: 24,
  },
  form: {
    display: "flex",
    flexDirection: "column",
    gap: 16,
    marginBottom: 24,
  },
  field: {
    display: "flex",
    flexDirection: "column",
    gap: 4,
  },
  label: {
    fontSize: 13,
    color: "#cbd5f5",
  },
  input: {
    padding: "8px 10px",
    borderRadius: 8,
    border: "1px solid #1f2937",
    background: "#020617",
    color: "#e5e7eb",
    fontSize: 14,
    outline: "none",
  },
  button: {
    marginTop: 8,
    padding: "10px 14px",
    borderRadius: 999,
    border: "none",
    background:
      "linear-gradient(to right, rgb(56,189,248), rgb(129,140,248))",
    color: "#0b1120",
    fontWeight: 600,
    cursor: "pointer",
  },
  error: {
    marginTop: 12,
    padding: 10,
    borderRadius: 8,
    background: "rgba(239,68,68,0.1)",
    color: "#fecaca",
    fontSize: 14,
  },
  resultBox: {
    marginTop: 16,
    padding: 16,
    borderRadius: 8,
    background: "#020617",
    border: "1px solid rgba(148,163,184,0.4)",
  },
  resultTitle: {
    fontSize: 16,
    marginBottom: 8,
  },
  resultSection: {
    marginTop: 8,
    fontSize: 14,
  },
  tokenBox: {
    marginTop: 4,
    padding: 8,
    borderRadius: 6,
    background: "#020617",
    fontSize: 12,
    wordBreak: "break-all",
    border: "1px dashed rgba(148,163,184,0.4)",
  },
  dealsList: {
    listStyle: "none",
    padding: 0,
    marginTop: 8,
  },
  dealItem: {
    padding: 8,
    borderRadius: 6,
    background: "#020617",
    border: "1px solid rgba(51,65,85,0.8)",
    marginBottom: 6,
  },
  dealTitle: {
    fontWeight: 600,
    fontSize: 14,
  },
  dealMeta: {
    marginTop: 2,
    fontSize: 12,
    color: "#94a3b8",
  },
};