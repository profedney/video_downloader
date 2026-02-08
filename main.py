import json
import os
import threading
import webbrowser
from http.server import SimpleHTTPRequestHandler, HTTPServer
from yt_dlp import YoutubeDL

PORT = 8765
BASE_DIR = os.path.dirname(os.path.abspath(__file__))


class APIHandler(SimpleHTTPRequestHandler):

    def do_POST(self):
        if self.path != "/api/baixar":
            self.send_error(404)
            return

        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode("utf-8"))

        url = data.get("url")
        resposta = baixar_video(url)

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"mensagem": resposta}).encode("utf-8"))


def baixar_video(url):
    pasta_download = os.path.join(os.path.expanduser("~"), "Downloads")

    opcoes = {
        "outtmpl": os.path.join(pasta_download, "%(title)s.%(ext)s"),
        "format": "best[ext=mp4]/best",
        "noplaylist": True,
        "quiet": True,
        "merge_output_format": None,
        "postprocessors": [],
    }

    try:
        with YoutubeDL(opcoes) as ydl:
            info = ydl.extract_info(url, download=True)
            titulo = info.get("title", "vídeo")
            formato = info.get("ext", "desconhecido")
        return f"✅ '{titulo}' baixado ({formato}) em: {pasta_download}"
    except Exception as e:
        return f"❌ Erro ao baixar: {str(e)}"


def iniciar_servidor():
    os.chdir(BASE_DIR)
    server = HTTPServer(("localhost", PORT), APIHandler)
    server.serve_forever()


if __name__ == "__main__":
    print("▶ Iniciando servidor local...")
    thread = threading.Thread(target=iniciar_servidor, daemon=True)
    thread.start()

    url = f"http://localhost:{PORT}/web/index.html"
    print(f"🌐 Abrindo navegador em {url}")
    webbrowser.open(url)

    thread.join()
