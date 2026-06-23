import "./QueryInput.css";

const EXAMPLE_PROMPTS = [
  "My landlord hasn't returned my security deposit after 45 days",
  "My heater has been broken for weeks and my landlord won't fix it",
  "My landlord wants to enter my apartment tomorrow with no notice",
  "My landlord raised my rent by 15% with no warning",
];

export default function QueryInput({
  situation,
  setSituation,
  onSubmit,
  loading,
}) {
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
        <button className="submit-btn" onClick={onSubmit} disabled={loading}>
          {loading ? "Thinking..." : "Ask"}
        </button>
      </div>
      <div className="example-prompts">
        {EXAMPLE_PROMPTS.map((prompt) => (
          <button
            key={prompt}
            className="prompt-btn"
            onClick={() => setSituation(prompt)}
          >
            {prompt}
          </button>
        ))}
      </div>
    </section>
  );
}
