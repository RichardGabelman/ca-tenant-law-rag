import { useState } from "react";
import ResultCard from "./ResultCard";
import "./ResultsList.css";

export default function ResultsList({ results, citedSections }) {
  const [viewMode, setViewMode] = useState("summary");
  const citedSet = new Set(citedSections);

  return (
    <>
      <div className="results-header">
        <span className="results-count">
          {results.length} source{results.length !== 1 ? "s" : ""}
        </span>
        <div className="toggle-group" role="group" aria-label="View mode">
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
      {results.length === 0 ? (
        <p className="no-results">
          No sections found — try reducing the minimum match score.
        </p>
      ) : (
        <div className="results-list">
          {results.map((result) => (
            <ResultCard
              key={result.section_num}
              result={result}
              viewMode={viewMode}
              cited={citedSet.has(result.section_num)}
            />
          ))}
        </div>
      )}
    </>
  );
}
