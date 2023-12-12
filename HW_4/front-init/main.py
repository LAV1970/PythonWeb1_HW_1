from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse


class HttpHandler(BaseHTTPRequestHandler):
    PAGE_MAPPING = {
        "/": "index.html",
        "/message": "message.html",
    }

    def do_GET(self):
        pr_url = urllib.parse.urlparse(self.path)
        file_path = self.PAGE_MAPPING.get(pr_url.path, "error.html")

        self.send_html_file(file_path)

    def send_html_file(self, filename, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        with open(filename, "rb") as fd:
            self.wfile.write(fd.read())


def run(server_class=HTTPServer, handler_class=HttpHandler):
    server_address = ("", 8000)
    http = server_class(server_address, handler_class)
    try:
        http.serve_forever()
    except KeyboardInterrupt:
        http.server_close()


if __name__ == "__main__":
    run()
