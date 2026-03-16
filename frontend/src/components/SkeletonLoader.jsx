import "./SkeletonLoader.css";

export default function SkeletonLoader() {
  return (
    <div className="loading-state">
      <div className="skeleton-card">
        <div className="skeleton-card-header">
          <div
            className="skeleton"
            style={{ height: "24px", width: "80px", borderRadius: "4px" }}
          ></div>
          <div
            className="skeleton"
            style={{ height: "14px", width: "180px" }}
          ></div>
        </div>
        <div className="skeleton-card-body">
          {Array.from({ length: 8 }).map((_, j) => (
            <div
              key={j}
              className="skeleton"
              style={{
                height: "12px",
                width: `${85 + Math.floor((j * 37) % 15)}%`,
              }}
            />
          ))}
        </div>
      </div>
    </div>
  );
}
