from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse
import os


class HttpHandler(BaseHTTPRequestHandler):
    PAGE_MAPPING = {
        "/": "index.html",
        "/message": "message.html",
        "/message.html": "message.html",
    }

    STATIC_PATHS = {
        "/style.css": "style.css",
        "/logo.png": "logo.png",
    }

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        path_without_fragment = urllib.parse.urldefrag(pr_url.path).url

        # Отладочная информация
        print("Current Working Directory:", os.getcwd())

        if path_without_fragment in self.PAGE_MAPPING:
            file_path = self.PAGE_MAPPING[path_without_fragment]
            self.send_html_file(file_path)
        elif path_without_fragment in self.STATIC_PATHS:
            file_path = self.STATIC_PATHS[path_without_fragment]
            self.send_static_file(file_path)
        else:
            # Добавим отладочную информацию
            full_path = os.path.join(os.getcwd(), path_without_fragment.lstrip("/"))
            print("Full Path for 404 Error:", full_path)
            self.send_error(404, "File Not Found")

    def send_html_file(self, filename, status=200):
        full_path = os.path.join(os.path.dirname(__file__), filename.lstrip("/"))
        print(
            "Attempting to open HTML file:", full_path
        )  # Добавим эту строку для отладки
        if os.path.exists(full_path):
            self.send_response(status)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open(full_path, "rb") as fd:
                self.wfile.write(fd.read())
        else:
            print("HTML file not found:", full_path)  # Добавим эту строку для отладки
            self.send_error(404, "File Not Found")

    def send_static_file(self, filename, status=200):
        full_path = os.path.join(os.path.dirname(__file__), filename.lstrip("/"))
        print("Attempting to open file:", full_path)  # Добавим эту строку для отладки
        if os.path.exists(full_path):
            self.send_response(status)
        if filename.endswith(".css"):
            self.send_header("Content-type", "text/css")
        elif filename.endswith(".png"):
            self.send_header("Content-type", "image/png")
            self.end_headers()
            with open(full_path, "rb") as fd:
                self.wfile.write(fd.read())
        else:
            self.send_error(404, "File Not Found")


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ("", 3000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == "__main__":
    run()
