# run_server.py  (project root)  ->  python run_server.py
# Flask's built-in server is only for development. Waitress is a real
# production server and works on Windows, Mac and Linux.
from waitress import serve

from backend.app import app, cleanup_old_audio

if __name__ == "__main__":
    cleanup_old_audio()
    print("Lingua AI running on http://0.0.0.0:5000")
    serve(app, host="0.0.0.0", port=5000, threads=8)