// frontend/web/src/hooks/useTheme.js
import { useEffect, useState, useCallback } from "react";

// Scoped for now to whichever component calls it (the Lesson page).
// Safe to lift to an app-wide ThemeProvider later — same API, same
// storage key — once the --ink/--paper token collision elsewhere in
// globals.css is sorted out.

const STORAGE_KEY = "lingua_theme";

function getSystemTheme() {
  if (typeof window === "undefined" || !window.matchMedia) return "dark";
  return window.matchMedia("(prefers-color-scheme: light)").matches
    ? "light"
    : "dark";
}

export function useTheme() {
  const [theme, setTheme] = useState(() => {
    const saved =
      typeof window !== "undefined" ? localStorage.getItem(STORAGE_KEY) : null;
    return saved === "light" || saved === "dark" ? saved : getSystemTheme();
  });

  // If the person never made an explicit choice, keep following the
  // system setting live (e.g. their OS switches to dark mode at night).
  // Once they tap the toggle, that choice sticks and we stop listening.
  useEffect(() => {
    if (localStorage.getItem(STORAGE_KEY)) return;
    if (!window.matchMedia) return;

    const mql = window.matchMedia("(prefers-color-scheme: light)");
    const handler = (e) => setTheme(e.matches ? "light" : "dark");

    mql.addEventListener?.("change", handler);
    return () => mql.removeEventListener?.("change", handler);
  }, []);

  const toggleTheme = useCallback(() => {
    setTheme((prev) => {
      const next = prev === "light" ? "dark" : "light";
      localStorage.setItem(STORAGE_KEY, next);
      return next;
    });
  }, []);

  return [theme, toggleTheme];
}
