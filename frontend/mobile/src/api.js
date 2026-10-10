// mobile/src/api.js

// Starts from the address baked in at build time (eas.json -> EXPO_PUBLIC_API_URL).
// setBase() can still override it, for example from a screen where the user types an address.
let BASE = (process.env.EXPO_PUBLIC_API_URL || "").trim().replace(/\/+$/, "");
export const setBase = (u) => {
  BASE = u.trim().replace(/\/+$/, "");
};

// Must be exactly the same text as APP_KEY in your backend .env file.
// If APP_KEY is empty in .env, this value is ignored by the server.
const KEY = process.env.EXPO_PUBLIC_APP_KEY || "";

// timeoutMs: lessons can take longer than 60 seconds (the AI explains every
// sentence). The old fixed 60 s cancelled them and Library/Scan hid the error.
export async function call(path, opts = {}, timeoutMs = 60000) {
  const ctrl = new AbortController();
  const timer = setTimeout(() => ctrl.abort(), timeoutMs);
  try {
    const r = await fetch(BASE + path, {
      ...opts,
      headers: { ...(opts.headers || {}), "X-App-Key": KEY },
      signal: ctrl.signal,
    });
    const j = await r.json().catch(() => ({}));
    if (!r.ok) throw new Error(j.error || "Server error " + r.status);
    return j;
  } catch (e) {
    const canceled =
      e.name === "AbortError" ||
      /FetchRequestCanceledException|request has been canceled/i.test(
        e.message || "",
      );

    if (e.message === "Network request failed") {
      throw new Error(
        "Can't reach the server at " +
          BASE +
          ". Check the address, that the backend is running, and that you have an internet connection.",
      );
    }
    if (canceled) {
      const err = new Error(
        "This is taking too long. Check your connection and try again.",
      );
      err.isCanceled = true;
      throw err;
    }
    throw e;
  } finally {
    clearTimeout(timer);
  }
}

const json = (method) => (p, b, ms) =>
  call(
    p,
    {
      method,
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(b),
    },
    ms,
  );

export const get = (p, ms) => call(p, {}, ms);
export const post = json("POST");
export const put = json("PUT");
export const upload = (p, form, ms = 180000) =>
  call(p, { method: "POST", body: form }, ms);

export const audioUrl = (a) => {
  const s = typeof a === "string" ? a : a?.url || a?.path || a?.file || "";
  if (!s) return null;
  return s.startsWith("http") ? s : BASE + "/" + s.replace(/^\/+/, "");
};

// Turns any lesson JSON from the backend into readable text.
export const flatten = (o) => {
  if (o == null) return "";
  if (typeof o === "string" || typeof o === "number") return String(o);
  if (Array.isArray(o)) return o.map(flatten).filter(Boolean).join("\n");
  return Object.entries(o)
    .map(([k, v]) => {
      const t = flatten(v);
      return t
        ? typeof v === "object"
          ? k.replace(/_/g, " ").toUpperCase() + "\n" + t
          : t
        : "";
    })
    .filter(Boolean)
    .join("\n\n");
};
