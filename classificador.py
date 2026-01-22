"""Classificador por regras com pesos para mensagens curtas."""

from __future__ import annotations

from dataclasses import dataclass
import re
import unicodedata
from typing import Dict, Iterable, List, Sequence, Tuple


# Extrai tokens simples apos normalizacao (minusculas e sem acentos).
PADRAO_TOKEN = re.compile(r"[a-z0-9]+")


@dataclass(frozen=True)
class ResultadoClassificacao:
    categoria: str
    palavras_chave: List[str]


@dataclass(frozen=True)
class RegraPalavraChave:
    categoria: str
    palavras_chave_token: Tuple[Tuple[str, int], ...]
    palavras_chave_frase: Tuple[Tuple[str, int], ...]


class ClassificadorPorRegras:
    def __init__(self, regras: Sequence[RegraPalavraChave]) -> None:
        self._regras = regras

    def classificar(self, texto: str) -> ResultadoClassificacao:
        texto_normalizado = normalizar_texto(texto)
        tokens = set(_tokenizar_normalizado(texto_normalizado))

        melhor_categoria = "outros"
        melhores_palavras_chave: List[str] = []
        melhor_pontuacao = 0

        # Soma pesos das palavras encontradas e escolhe a maior pontuacao.
        for regra in self._regras:
            palavras_encontradas: List[str] = []
            pontuacao = 0
            for frase, peso in regra.palavras_chave_frase:
                if frase in texto_normalizado:
                    palavras_encontradas.append(frase)
                    pontuacao += peso
            for token, peso in regra.palavras_chave_token:
                if token in tokens:
                    palavras_encontradas.append(token)
                    pontuacao += peso

            if pontuacao > melhor_pontuacao:
                melhor_pontuacao = pontuacao
                melhor_categoria = regra.categoria
                melhores_palavras_chave = palavras_encontradas

        return ResultadoClassificacao(
            categoria=melhor_categoria,
            palavras_chave=melhores_palavras_chave,
        )


def normalizar_texto(texto: str) -> str:
    # Remove acentos e normaliza para minusculas.
    normalizado = unicodedata.normalize("NFKD", texto)
    sem_acentos = "".join(
        caractere for caractere in normalizado if not unicodedata.combining(caractere)
    )
    return sem_acentos.lower()


def tokenizar(texto: str) -> List[str]:
    return _tokenizar_normalizado(normalizar_texto(texto))


def _tokenizar_normalizado(texto_normalizado: str) -> List[str]:
    return PADRAO_TOKEN.findall(texto_normalizado)


def _normalizar_palavras_chave(
    palavras_chave: Iterable[Tuple[str, int]],
) -> Tuple[Tuple[Tuple[str, int], ...], Tuple[Tuple[str, int], ...]]:
    palavras_token: List[Tuple[str, int]] = []
    palavras_frase: List[Tuple[str, int]] = []

    # Separa palavras unicas de frases com espacos.
    for palavra_chave, peso in palavras_chave:
        palavra_normalizada = normalizar_texto(palavra_chave)
        if " " in palavra_normalizada:
            palavras_frase.append((palavra_normalizada, peso))
        else:
            palavras_token.append((palavra_normalizada, peso))

    return tuple(palavras_token), tuple(palavras_frase)


def criar_classificador_padrao() -> ClassificadorPorRegras:
    regras: List[RegraPalavraChave] = []
    # Pesos simples (1 a 3) para resolver ambiguidades.
    palavras_por_categoria: Dict[str, Tuple[Tuple[str, int], ...]] = {
        "elogio": (
            ("obrigado", 2),
            ("obrigada", 2),
            ("otimo", 2),
            ("otima", 2),
            ("bom", 1),
            ("excelente", 3),
            ("parabens", 2),
            ("adorei", 2),
            ("amei", 2),
            ("show", 1),
        ),
        "reclamacao": (
            ("ruim", 2),
            ("horrivel", 3),
            ("pessimo", 3),
            ("problema", 2),
            ("problemas", 2),
            ("reclamar", 2),
            ("reclamacao", 2),
            ("demora", 1),
            ("erro", 2),
            ("nao funciona", 3),
            ("nao esta funcionando", 3),
            ("cobrado duas vezes", 3),
            ("quebrado", 2),
        ),
        "duvida": (
            ("como", 1),
            ("quando", 1),
            ("onde", 1),
            ("qual", 1),
            ("porque", 1),
            ("por que", 1),
            ("duvida", 2),
            ("ajuda", 1),
            ("pode", 1),
            ("posso", 1),
            ("consigo", 1),
        ),
        "financeiro": (
            ("preco", 2),
            ("valor", 2),
            ("pagamento", 3),
            ("cobranca", 2),
            ("cobrado", 1),
            ("boleto", 2),
            ("cartao", 2),
            ("pix", 2),
            ("reembolso", 2),
            ("assinatura", 2),
        ),
    }

    for categoria, palavras_chave in palavras_por_categoria.items():
        palavras_token, palavras_frase = _normalizar_palavras_chave(palavras_chave)
        regras.append(
            RegraPalavraChave(
                categoria=categoria,
                palavras_chave_token=palavras_token,
                palavras_chave_frase=palavras_frase,
            )
        )

    return ClassificadorPorRegras(regras)


CLASSIFICADOR_PADRAO = criar_classificador_padrao()
