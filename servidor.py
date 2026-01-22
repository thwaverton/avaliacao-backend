"""Servidor HTTP minimalista para classificar mensagens."""

from __future__ import annotations

import argparse
import json
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from typing import Any, Dict, Optional, Tuple

from classificador import CLASSIFICADOR_PADRAO, ResultadoClassificacao


TAMANHO_MAXIMO_TEXTO = 500


class ManipuladorClassificacao(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        # Verificacao simples para indicar que a API esta ativa.
        if self.path == "/":
            self._enviar_json(
                HTTPStatus.OK,
                {
                    "mensagem": "API de classificacao ativa.",
                    "uso": "Envie POST /classificar com JSON {'texto': '...'}",
                },
            )
            return

        if self.path == "/classificar":
            # Metodo nao permitido para esta rota.
            self._enviar_json_com_cabecalhos(
                HTTPStatus.METHOD_NOT_ALLOWED,
                {
                    "erro": "metodo_nao_permitido",
                    "detalhe": "Use POST /classificar com JSON.",
                },
                {"Allow": "POST"},
            )
            return

        if self.path == "/favicon.ico":
            self._enviar_vazio(HTTPStatus.NO_CONTENT)
            return

        self._enviar_json(HTTPStatus.NOT_FOUND, {"erro": "rota_nao_encontrada"})

    def do_POST(self) -> None:
        if self.path != "/classificar":
            self._enviar_json(HTTPStatus.NOT_FOUND, {"erro": "rota_nao_encontrada"})
            return

        # Valida JSON e campos basicos antes de classificar.
        corpo, resposta_erro = self._ler_corpo_json()
        if resposta_erro is not None:
            self._enviar_json(HTTPStatus.BAD_REQUEST, resposta_erro)
            return

        if not isinstance(corpo, dict):
            self._enviar_json(
                HTTPStatus.BAD_REQUEST,
                {"erro": "corpo_invalido", "detalhe": "JSON deve ser um objeto."},
            )
            return

        texto = corpo.get("texto")
        if not isinstance(texto, str):
            self._enviar_json(
                HTTPStatus.BAD_REQUEST,
                {"erro": "texto_invalido", "detalhe": "texto deve ser string."},
            )
            return

        texto_limpo = texto.strip()
        if not texto_limpo:
            self._enviar_json(
                HTTPStatus.BAD_REQUEST,
                {"erro": "texto_vazio", "detalhe": "texto nao pode ser vazio."},
            )
            return

        if len(texto_limpo) > TAMANHO_MAXIMO_TEXTO:
            self._enviar_json(
                HTTPStatus.BAD_REQUEST,
                {
                    "erro": "texto_muito_longo",
                    "detalhe": f"texto deve ter no maximo {TAMANHO_MAXIMO_TEXTO} caracteres.",
                },
            )
            return

        resultado = CLASSIFICADOR_PADRAO.classificar(texto_limpo)
        resposta = _montar_resposta(resultado)
        self._enviar_json(HTTPStatus.OK, resposta)

    def _ler_corpo_json(self) -> Tuple[Optional[Any], Optional[Dict[str, str]]]:
        # Le o corpo da requisicao e tenta converter para JSON valido.
        tamanho_conteudo = self.headers.get("Content-Length")
        if tamanho_conteudo is None:
            return None, {
                "erro": "tamanho_conteudo_ausente",
                "detalhe": "cabecalho Content-Length ausente.",
            }

        try:
            comprimento = int(tamanho_conteudo)
        except ValueError:
            return None, {"erro": "tamanho_conteudo_invalido"}

        if comprimento <= 0:
            return None, {"erro": "corpo_vazio"}

        corpo_bruto = self.rfile.read(comprimento)
        try:
            corpo_texto = corpo_bruto.decode("utf-8")
        except UnicodeDecodeError:
            return None, {
                "erro": "codificacao_invalida",
                "detalhe": "esperado UTF-8.",
            }

        try:
            corpo = json.loads(corpo_texto)
        except json.JSONDecodeError:
            return None, {"erro": "json_invalido"}

        return corpo, None

    def _enviar_json(self, status: HTTPStatus, carga: Dict[str, Any]) -> None:
        resposta_bytes = json.dumps(carga).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resposta_bytes)))
        self.end_headers()
        self.wfile.write(resposta_bytes)

    def _enviar_json_com_cabecalhos(
        self,
        status: HTTPStatus,
        carga: Dict[str, Any],
        cabecalhos: Dict[str, str],
    ) -> None:
        # Envia JSON com cabecalhos extras (ex.: Allow).
        resposta_bytes = json.dumps(carga).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(resposta_bytes)))
        for nome, valor in cabecalhos.items():
            self.send_header(nome, valor)
        self.end_headers()
        self.wfile.write(resposta_bytes)

    def _enviar_vazio(self, status: HTTPStatus) -> None:
        self.send_response(status)
        self.send_header("Content-Length", "0")
        self.end_headers()


def _montar_resposta(resultado: ResultadoClassificacao) -> Dict[str, Any]:
    return {
        "categoria": resultado.categoria,
        "palavras_chave": resultado.palavras_chave,
    }


def analisar_argumentos() -> argparse.Namespace:
    analisador = argparse.ArgumentParser(
        description="API de classificacao de texto por regras"
    )
    analisador.add_argument("--host", default="0.0.0.0", help="Host do servidor")
    analisador.add_argument("--port", type=int, default=8000, help="Porta do servidor")
    return analisador.parse_args()


def executar_servidor(host: str, port: int) -> None:
    servidor = HTTPServer((host, port), ManipuladorClassificacao)
    print(f"Servidor rodando em http://{host}:{port}")
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrando servidor.")
    finally:
        servidor.server_close()


if __name__ == "__main__":
    argumentos = analisar_argumentos()
    executar_servidor(argumentos.host, argumentos.port)
