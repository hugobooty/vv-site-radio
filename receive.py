"""Tiny local receiver: the site page POSTs a mono 16-bit WAV, this converts it to MP3 with ffmpeg into OUT.
Only listens on 127.0.0.1. Usage: py -3.13 receive.py <out_dir> [port]"""
import sys, os, re, subprocess, tempfile
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs

OUT = sys.argv[1]; PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 8799
os.makedirs(OUT, exist_ok=True)

class H(BaseHTTPRequestHandler):
    def cors(self):
        self.send_header("Access-Control-Allow-Origin", "http://127.0.0.1:8792")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
    def do_OPTIONS(self):
        self.send_response(204); self.cors(); self.end_headers()
    def do_POST(self):
        name = parse_qs(urlparse(self.path).query).get("name", ["song"])[0]
        name = re.sub(r"[^A-Za-z0-9 ()._-]", "", name)[:80] or "song"
        data = self.rfile.read(int(self.headers["Content-Length"]))
        with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f: f.write(data); wav = f.name
        mp3 = os.path.join(OUT, name + ".mp3")
        r = subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", wav, "-codec:a", "libmp3lame", "-b:a", "192k",
                            "-metadata", f"title={name[3:]}", "-metadata", "artist=Vulpine Valley", "-metadata", "album=site radio", mp3],
                           capture_output=True, text=True)
        os.remove(wav)
        ok = r.returncode == 0
        self.send_response(200 if ok else 500); self.cors(); self.end_headers()
        self.wfile.write((mp3 if ok else r.stderr).encode())
    def log_message(self, *a): pass

HTTPServer(("127.0.0.1", PORT), H).serve_forever()
