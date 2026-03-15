import { useState } from "react";
import "./App.css";
import Header from "./components/Header.jsx";
import QueryInput from "./components/QueryInput.jsx";
import ResultsList from "./components/ResultsList.jsx";

function App() {
  const [situation, setSituation] = useState("");
  const [results, setResults] = useState(null);

  async function handleSubmit() {
    setResults([
      {
        section_num: 67,
        citation_url: "google.com",
        raw_text: "raw legislation text",
      },
      {
        section_num: 68,
        citation_url: "google.com",
        raw_text: "raw legislation text two",
      },
    ]);
    console.log("submitted! (placeholder)");
  }

  return (
    <>
      <Header />
      <QueryInput
        situation={situation}
        setSituation={setSituation}
        onSubmit={handleSubmit}
      />
      <div aria-live="polite" aria-atomic="true">
        {results && <ResultsList results={results} />}
      </div>
    </>
  );
}

export default App;
