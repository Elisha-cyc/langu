// frontend/web/src/components/common/Loader.jsx
import "./loader.css";

const DEFAULT_CHARACTERS = ["A", "あ", "中", "가", "ب"];

/**
 * Reusable full-page loading animation.
 *
 * Usage (replaces the old plain <div className="loading">...</div>):
 *
 *   if (loading) {
 *     return <Loader label="Preparing your lesson..." />;
 *   }
 *
 * The animation itself has no timers or network awareness — it simply
 * renders for as long as the parent's `loading` state is true, and
 * unmounts the instant that state flips to false. So on a fast
 * connection it may barely flash, and on a slow one it will keep
 * spinning until the request resolves — exactly matching real network
 * conditions with zero extra wiring.
 */
export default function Loader({ label = "Loading...", characters = DEFAULT_CHARACTERS }) {
  return (
    <div className="app-loader">
      <div className="app-loader-orbit">
        <div className="app-loader-core">📖</div>

        <div className="app-loader-ring">
          {characters.map((char, index) => {
            const angle = (360 / characters.length) * index;

            return (
              <div
                key={char + index}
                className="app-loader-item"
                style={{ transform: `rotate(${angle}deg)` }}
              >
                <span className="app-loader-char">{char}</span>
              </div>
            );
          })}
        </div>
      </div>

      <p className="app-loader-label">{label}</p>
    </div>
  );
}
