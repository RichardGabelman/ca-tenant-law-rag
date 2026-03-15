import "./ResultCard.css";

export default function ResultCard({ result }) {
  <div className="result-card">
    <div className="card-header">
      <span className="section-badge">§ {result.section_num}</span>
      <a
        href={result.citation_url}
        className="citation-link"
        target="_blank"
        rel="noopener noreferrer"
      >
        leginfo.legislature.ca.gov ↗
      </a>
    </div>
    <div className="card-body">
      <p className="raw-text">
        {result.raw_text}
      </p>
    </div>
  </div>;
}
