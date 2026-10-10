# backend/security.py
"""
Basic protection for a private beta:
1. APP_KEY: if set in .env, every request must send the header  X-App-Key: <key>
   (keeps random scanners and strangers off your server).
2. Rate limit: each IP can start only a few AI requests per minute, so one
   person (or a bug) cannot use up your whole Groq quota.

This is NOT a replacement for real user accounts. Anyone who extracts the key
from the app can still use it. Real login is the next step before going public.

Use it in app.py, right after  app = Flask(__name__):
    from backend.security import install_security
    install_security(app)
"""
import hmac
import os
import threading
import time
from collections import defaultdict, deque

from flask import jsonify, request

AI_PREFIXES = (
    "/lesson", "/teach", "/book", "/scan", "/text",
    "/audio/read", "/pronunciation",
)

_hits = defaultdict(deque)
_lock = threading.Lock()


def install_security(app):
    app_key = os.getenv("APP_KEY", "")
    limit = int(os.getenv("RATE_LIMIT_PER_MIN", "40"))

    @app.before_request
    def guard():
        if request.method == "OPTIONS":
            return None

        path = request.path

        # The home check and the audio files (played by the browser, which
        # cannot send custom headers) stay open.
        if path == "/" or path.startswith("/data/audio/"):
            return None

        if app_key and not hmac.compare_digest(
            request.headers.get("X-App-Key", ""), app_key
        ):
            return jsonify({"error": "Unauthorized"}), 401

        if request.method == "POST" and path.startswith(AI_PREFIXES):
            ip = (
                request.headers.get("CF-Connecting-IP")
                or request.remote_addr
                or "unknown"
            )
            now = time.time()

            with _lock:
                recent = _hits[ip]

                while recent and now - recent[0] > 60:
                    recent.popleft()

                if len(recent) >= limit:
                    return jsonify({
                        "error": "Too many requests. Please wait a minute and try again."
                    }), 429

                recent.append(now)

        return None