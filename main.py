import webview
import os
from yt_dlp import YoutubeDL

class API:
    def baixar_video(self, url):
        """Baixa o melhor formato disponível (sem ffmpeg)."""
        pasta_download = os.path.join(os.path.expanduser("~"), "Downloads")

        opcoes = {
            'outtmpl': os.path.join(pasta_download, '%(title)s.%(ext)s'),
            'format': 'best[ext=mp4]/best',
            'noplaylist': True,
            'quiet': True,
            'merge_output_format': None,
            'postprocessors': [],
        }

        try:
            with YoutubeDL(opcoes) as ydl:
                info = ydl.extract_info(url, download=True)
                titulo = info.get('title', 'vídeo')
                formato = info.get('ext', 'desconhecido')
            return f"✅ '{titulo}' baixado ({formato}) em: {pasta_download}"
        except Exception as e:
            return f"❌ Erro ao baixar: {str(e)}"

if __name__ == '__main__':
    caminho_html = os.path.abspath('web/index.html')
    api = API()
    janela = webview.create_window(
        "YouTube Downloader",
        url=f'file:///{caminho_html}',
        js_api=api,
        width=500,
        height=400,
        resizable=False
    )
    webview.start(debug=False)
