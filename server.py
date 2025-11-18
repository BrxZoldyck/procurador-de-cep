import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse
from validar_cep import validar_cep

class MeuServidor(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

        caminho = urlparse(self.path).path

        if caminho.startswith("/validar/"):
            cep = caminho.replace("/validar/", "")
            resultado = validar_cep(cep)
            self.wfile.write(json.dumps(resultado).encode())
        else:
            self.wfile.write(json.dumps({"erro": "Rota inválida"}).encode())

def rodar():
    porta = 5000
    server = HTTPServer(("0.0.0.0", porta), MeuServidor)
    print(f"Servidor rodando em http://127.0.0.1:{porta}")
    server.serve_forever()

if __name__ == "__main__":
    rodar()
