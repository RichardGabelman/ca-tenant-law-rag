import "./AnswerPanel.css";

export default function AnswerPanel({ answer, citedSections }) {
  return (
    <div className="answer-panel" role="region" aria-label="Answer">
      <div className="answer-panel-header">
        <span className="answer-label">Answer</span>
        {citedSections.length > 0 && (
          <div className="answer-citations" aria-label="Cited sections">
            {citedSections.map((sec) => (
              <span key={sec} className="answer-citation-badge">
                § {sec}
              </span>
            ))}
          </div>
        )}
      </div>
      <p className="answer-text">{answer}</p>
    </div>
  );
}