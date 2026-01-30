#!/usr/bin/env python3
import http.server
import urllib.parse
import threading
import time

HOST = "0.0.0.0"
PORT = 5000

class Handler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/report":
            self.send_response(404)
            self.end_headers()
            return

        query = urllib.parse.parse_qs(parsed.query)
        data = query.get("data", [""])[0]

        # Log dans la console (ou dans un fichier)
        print("\n--- Rapport reçu d'un stagiaire ---")
        if data:
            print(data)
        else:
            print("[Aucune donnée reçue]")
        print("-----------------------------------\n")

        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def serve():
    httpd = http.server.HTTPServer((HOST, PORT), Handler)
    print(f"Serveur formateur démarré sur http://{HOST}:{PORT}")
    httpd.serve_forever()

if __name__ == "__main__":
    threading.Thread(target=serve, daemon=True).start()
    # Le formateur peut garder le terminal ouvert pour voir les rapports
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nArrêt du serveur.")
