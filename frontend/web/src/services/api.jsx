// frontend/web/src/services/api.jsx
import axios from "axios";

const api = axios.create({
  // Change this in the web .env file when your server is not on this computer.
  baseURL: import.meta.env.VITE_API_URL || "http://127.0.0.1:5000",
  // Without a limit, a stuck request waits forever. Lesson pages set their
  // own longer limits where they need them.
  timeout: 60000,
  headers: {
    "Content-Type": "application/json",
  },
});

// Same text as APP_KEY in the backend .env. Leave it unset to skip the check.
// Same text as APP_KEY in the backend .env. Leave it unset to skip the check.
const appKey = import.meta.env.VITE_APP_KEY;

if (appKey) {
  api.defaults.headers.common["X-App-Key"] = appKey;
}

export default api;