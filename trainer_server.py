#!/usr/bin/env python3
import http.server
import urllib.parse
import subprocess
import threading

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

        # On lance les deux commandes kubectl et on capture leurs sorties
        def run_cmd(cmd):
            try:
                out = subprocess.check_output(cmd, shell=True, text=True, timeout=5)
                return out.strip()
            except subprocess.CalledProcessError as e:
                return f"Error: {e}"
            except subprocess.TimeoutExpired:
                return "Timeout"

        pods = run_cmd("kubectl get pods -n mon-application")
        svcs = run_cmd("kubectl get svc -n mon-application")

        # Log dans la console (ou dans un fichier)
        print("\n--- Rapport d'un stagiaire ---")
        print(f"Payload du bouton : {data}")
        print("Pods (vus par le formateur) :")
        print(pods)
        print("Services (vus par le formateur) :")
        print(svcs)
        print("------------------------------\n")

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
            import time
            time.sleep(1)
    except KeyboardInterrupt:
        print("\nArrêt du serveur.")
