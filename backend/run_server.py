import os
from waitress import serve
from backend.app import app, cleanup_old_audio

if __name__ == "__main__":
    cleanup_old_audio()
    port = int(os.environ.get("PORT", 5000))
    print(f"Server running on port {port}")
    serve(app, host="0.0.0.0", port=port, threads=4)