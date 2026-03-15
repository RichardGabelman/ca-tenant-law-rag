import ResultCard from "./ResultCard";
import "./ResultsList.css";

export default function ResultsList({ results }) {
  return (
    <>
      <div className="results-header">
        <span className="results-count">
          {results.length} section{results.length !== 1 ? "s" : ""} found
        </span>
      </div>
      <div className="results-list">
        {results.map((result) => (
          <ResultCard key={result.section_num} result={result} />
        ))}
      </div>
    </>
  );
}
