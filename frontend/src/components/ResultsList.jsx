import { useState } from "react";
import ResultCard from "./ResultCard";
import "./ResultsList.css";

export default function ResultsList({ results }) {
  const [viewMode, setViewMode] = useState("summary");

  return (
    <>
      <div className="results-header">
        <span className="results-count">
          {results.length} section{results.length !== 1 ? "s" : ""} found
        </span>
        <div className="toggle-group" role="group" aria-label="View mdoe">
          <button
            className={`toggle-btn ${viewMode === "summary" ? "active" : ""}`}
            aria-pressed={viewMode === "summary"}
            onClick={() => setViewMode("summary")}
          >
            Summary
          </button>
          <button
            className={`toggle-btn ${viewMode === "raw" ? "active" : ""}`}
            aria-pressed={viewMode === "raw"}
            onClick={() => setViewMode("raw")}
          >
            Raw text
          </button>
        </div>
      </div>
      <div className="results-list">
        {results.map((result) => (
          <ResultCard
            key={result.section_num}
            result={result}
            viewMode={viewMode}
          />
        ))}
      </div>
    </>
  );
}
