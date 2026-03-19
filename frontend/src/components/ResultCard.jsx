import { useState } from "react";
import "./ResultCard.css";

const PREVIEW_SIZE = 550

export default function ResultCard({ result, viewMode }) {
  const [expanded, setExpanded] = useState(false);

  const isSummary = viewMode === "summary";
  const displayText = isSummary ? result.summary : result.raw_text;
  const preview = displayText.slice(0, PREVIEW_SIZE);
  const isLong = displayText.length > PREVIEW_SIZE;

  return (
    <div className="result-card">
      <div className="card-header">
        <h2 className="section-badge">
          <span>§</span>
          <span className="section-num">{result.section_num}</span>
        </h2>
        <a
          href={result.citation_url}
          className="citation-link"
          target="_blank"
          rel="noopener noreferrer"
          aria-label={`View § ${result.section_num} on leginfo.legislature.ca.gov`}
        >
          leginfo.legislature.ca.gov ↗
        </a>
      </div>
      <div className="card-body">
        <p className={isSummary ? "summary-text" : "raw-text"}>
          {expanded || !isLong ? displayText : preview + "..."}
        </p>
        {isLong && (
          <button
            className="expand-btn"
            onClick={() => setExpanded((e) => !e)}
            aria-label={
              expanded
                ? `Show less of § ${result.section_num}`
                : `Read full text of § ${result.section_num}`
            }
          >
            {expanded ? "Show less" : "Read more"}
          </button>
        )}
      </div>
    </div>
  );
}
