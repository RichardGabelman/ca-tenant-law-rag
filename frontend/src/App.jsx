import { useState } from "react";
import "./App.css";
import Header from "./components/Header.jsx";
import QueryInput from "./components/QueryInput.jsx";
import ResultsList from "./components/ResultsList.jsx";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

function App() {
  const [situation, setSituation] = useState("");
  const [results, setResults] = useState(null);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSubmit() {
    setLoading(true);
    setResults(null);

    try {
      const res = await fetch(`${API_URL}/query`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ situation }),
      });

      const data = await res.json();

      if (!res.ok) {
        throw new Error(data.detail || "Something went wrong.");
      }

      setResults(data.results);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <>
      <Header />
      <QueryInput
        situation={situation}
        setSituation={setSituation}
        onSubmit={handleSubmit}
        loading={loading}
      />
      <div aria-live="polite" aria-atomic="true">
        {error && <div className="error-msg">{error}</div>}
        {results && <ResultsList results={results} />}
      </div>
    </>
  );
}

export default App;
