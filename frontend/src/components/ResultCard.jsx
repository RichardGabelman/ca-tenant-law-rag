import "./ResultCard.css";

export default function ResultCard({ result }) {
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
        <p className="raw-text">{result.raw_text}</p>
      </div>
    </div>
  );
}
