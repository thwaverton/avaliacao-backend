import json
import threading
import unittest
from http.client import HTTPConnection
from http.server import HTTPServer

from servidor import ManipuladorClassificacao


class ManipuladorSilencioso(ManipuladorClassificacao):
    def log_message(self, formato: str, *args: object) -> None:
        return


class TesteServidorAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.servidor = HTTPServer(("127.0.0.1", 0), ManipuladorSilencioso)
        cls.porta = cls.servidor.server_address[1]
        cls.thread = threading.Thread(target=cls.servidor.serve_forever, daemon=True)
        cls.thread.start()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.servidor.shutdown()
        cls.servidor.server_close()
        cls.thread.join(timeout=1)

    def _post_json(self, corpo: dict) -> tuple[int, dict]:
        conexao = HTTPConnection("127.0.0.1", self.porta, timeout=2)
        cabecalhos = {"Content-Type": "application/json"}
        corpo_json = json.dumps(corpo)
        conexao.request("POST", "/classificar", body=corpo_json, headers=cabecalhos)
        resposta = conexao.getresponse()
        dados = resposta.read().decode("utf-8")
        conexao.close()
        return resposta.status, json.loads(dados)

    def test_rejeita_texto_vazio(self) -> None:
        status, resposta = self._post_json({"texto": "   "})
        self.assertEqual(status, 400)
        self.assertEqual(resposta.get("erro"), "texto_vazio")

    def test_rejeita_texto_nao_string(self) -> None:
        status, resposta = self._post_json({"texto": 123})
        self.assertEqual(status, 400)
        self.assertEqual(resposta.get("erro"), "texto_invalido")


if __name__ == "__main__":
    unittest.main()
