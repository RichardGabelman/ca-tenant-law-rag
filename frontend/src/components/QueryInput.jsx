import "./QueryInput.css";

export default function QueryInput({ situation, setSituation, onSubmit }) {
  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      onSubmit();
    }
  }

  return (
    <section className="input-section">
      <label className="input-label" htmlFor="situation">
        Describe your situation
      </label>
      <textarea
        id="situation"
        className="situation-input"
        placeholder="e.g. My landlord hasn't returned my security deposit after 60 days..."
        value={situation}
        onChange={(e) => setSituation(e.target.value)}
        onKeyDown={handleKeyDown}
      />
      <div className="input-footer">
        <p className="disclaimer">
          Covers California Civil Code §§ 1940–1954. Local ordinances may
          provide additional protections. Shift + ↵ for a new line.
        </p>
        <button className="submit-btn" onClick={onSubmit}>
          Find relevant law
        </button>
      </div>
    </section>
  );
}
