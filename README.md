# Avaliacao pratica - backend

Este projeto cria uma API REST simples para classificar mensagens curtas em categorias.
Ele foi feito para ser pequeno, facil de entender e rapido de testar.

## Para quem e este README

Se voce nunca testou uma API antes, siga o passo a passo abaixo.
Nao precisa instalar nada alem do Python.

## O que este projeto faz

- Recebe um texto curto em JSON.
- Aplica regras simples de palavras-chave com pesos.
- Devolve a categoria encontrada.

Exemplo de categoria: `elogio`, `reclamacao`, `duvida`, `financeiro`.

## Requisitos

- Python 3.11+ instalado.
- Nenhuma dependencia externa.

Para conferir a versao do Python:

```bash
python3 --version
```

## Como executar (passo a passo)

1) Abra o terminal na pasta do projeto.

2) Inicie o servidor:

```bash
python3 servidor.py --host 127.0.0.1 --port 8000
```

Voce deve ver algo parecido com:

```
Servidor rodando em http://127.0.0.1:8000
```

3) (Opcional) Verifique se o servidor esta vivo acessando a raiz:

```bash
curl http://127.0.0.1:8000/
```

Resposta esperada:

```json
{"mensagem": "API de classificacao ativa.", "uso": "Envie POST /classificar com JSON {'texto': '...'}"}
```

4) Envie uma requisicao para classificar um texto:

```bash
curl -X POST http://127.0.0.1:8000/classificar \
  -H "Content-Type: application/json" \
  -d '{"texto": "Qual o valor da assinatura?"}'
```

Resposta esperada:

```json
{"categoria": "financeiro", "palavras_chave": ["valor", "assinatura"]}
```

5) Para encerrar o servidor, use `Ctrl + C` no terminal.

## Importante sobre o endpoint

- A rota `/classificar` aceita somente `POST`.
- Se tentar `GET /classificar` no navegador, o servidor responde `405`.
- A rota `/` existe apenas para informar que a API esta ativa.

## Contrato do endpoint (resumo)

- `POST /classificar`
- Body JSON: `{"texto": "..."}`
- Resposta: `{"categoria": "...", "palavras_chave": [...]}`

Validacao basica:
- `texto` precisa ser string.
- `texto` nao pode ser vazio.
- tamanho maximo: 500 caracteres.

## Erros comuns e como entender

- `json_invalido`: o corpo nao e um JSON valido.
- `texto_invalido`: o campo `texto` nao e string.
- `texto_vazio`: o campo `texto` veio vazio.
- `texto_muito_longo`: o texto passou do limite.
- `metodo_nao_permitido`: voce tentou `GET` em `/classificar`.

## Categorias e regras

As categorias sao baseadas em palavras-chave com normalizacao simples (minusculas e sem acentos).
Cada palavra possui um peso (1 a 3). A pontuacao da categoria e a soma dos pesos encontrados.
A maior pontuacao vence.

- `elogio`: obrigado, otimo, excelente, parabens, amei...
- `reclamacao`: ruim, pessimo, problema, demora, "nao funciona"...
- `duvida`: como, quando, onde, qual, ajuda, posso...
- `financeiro`: preco, valor, pagamento, cobranca, boleto, cartao...
- `outros`: fallback quando nenhuma regra casa.

## Testes (opcional)

Os testes conferem se as regras estao funcionando.

```bash
python3 -m unittest discover -s tests
```

## Estrutura dos arquivos

- `servidor.py`: servidor HTTP e validacao do request.
- `classificador.py`: regras e logica de classificacao.
- `tests/test_classificador.py`: testes do classificador.

## Decisoes tecnicas

- Servidor HTTP direto com `http.server` para manter a solucao pequena e didatica.
- Classificador por regras para garantir previsibilidade e facilitar explicacao.
- Normalizacao de texto para reduzir variacao de maiusculas e acentos.

## Limitacoes

- As regras sao simples e podem gerar falsos positivos/negativos.
- Empates sao resolvidos pela ordem das regras.
- Nao ha persistencia nem autenticacao.

## Possiveis extensoes

- Ajustar regras por dominio e refinar pesos.
- Criar arquivo de configuracao (JSON) para regras e pesos, sem endpoint.
- Substituir por modelo de ML ou LLM com explicacao de resultados.

## Fontes

- Nenhuma fonte externa utilizada.
