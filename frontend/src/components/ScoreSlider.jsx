import "./ScoreSlider.css";

export default function ScoreSlider({ minScore, setMinScore }) {
  return (
    <div className="score-slider">
      <div className="score-slider-header">
        <label htmlFor="min-score" className="score-slider-label">
          Minimum match score
        </label>
        <span className="score-slider-value">
          {Math.round(minScore * 100)}%
        </span>
      </div>
      <input
        id="min-score"
        type="range"
        min="0"
        max="100"
        step="1"
        value={Math.round(minScore * 100)}
        onChange={(e) => setMinScore(e.target.value / 100)}
        className="score-range"
        aria-label="Minimum match score"
      />
      <div className="score-slider-hints">
        <span>0% - show everything</span>
        <span>100% - exact matches only</span>
      </div>
    </div>
  );
}
