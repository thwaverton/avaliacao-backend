# Avaliacao pratica - backend

API HTTP (estilo REST) para classificar mensagens curtas em categorias usando regras de palavras-chave com pesos. Feita para ser pequena, didatica e facil de testar.

## Requisitos

- Python 3.11+
- Somente Python stdlib (nenhuma dependencia externa)

Conferir a versao do Python:

```bash
python3 --version
```

## Como executar (tutorial passo a passo)

1) Abra o terminal na pasta do projeto e inicie o servidor (deixe este terminal aberto):

```bash
python3 servidor.py --host 127.0.0.1 --port 8000
```

O que esperar no terminal do servidor:

```
Servidor rodando em http://127.0.0.1:8000
```

2) Abra outro terminal para testar sem interromper o servidor. Verifique o status:

```bash
curl http://127.0.0.1:8000/
```

Resposta esperada:

```json
{"mensagem": "API de classificacao ativa.", "uso": "Envie POST /classificar com JSON {'texto': '...'}"}
```

3) Envie requisicoes de exemplo para cada categoria:

- Financeiro:

```bash
curl -X POST http://127.0.0.1:8000/classificar \
  -H "Content-Type: application/json" \
  -d '{"texto": "Qual o valor da assinatura mensal?"}'
```

Resposta esperada:

```json
{"categoria": "financeiro", "palavras_chave": ["valor", "assinatura"]}
```

- Duvida:

```bash
curl -X POST http://127.0.0.1:8000/classificar \
  -H "Content-Type: application/json" \
  -d '{"texto": "Como faco para alterar meu plano?"}'
```

Resposta esperada:

```json
{"categoria": "duvida", "palavras_chave": ["como"]}
```

- Reclamacao:

```bash
curl -X POST http://127.0.0.1:8000/classificar \
  -H "Content-Type: application/json" \
  -d '{"texto": "O aplicativo nao esta funcionando desde ontem."}'
```

Resposta esperada:

```json
{"categoria": "reclamacao", "palavras_chave": ["nao esta funcionando"]}
```

- Elogio:

```bash
curl -X POST http://127.0.0.1:8000/classificar \
  -H "Content-Type: application/json" \
  -d '{"texto": "A experiencia com o sistema foi otima."}'
```

Resposta esperada:

```json
{"categoria": "elogio", "palavras_chave": ["otima"]}
```

- Outros (fallback):

```bash
curl -X POST http://127.0.0.1:8000/classificar \
  -H "Content-Type: application/json" \
  -d '{"texto": "Teste"}'
```

Resposta esperada:

```json
{"categoria": "outros", "palavras_chave": []}
```

- Exemplo invalido (texto vazio):

```bash
curl -X POST http://127.0.0.1:8000/classificar \
  -H "Content-Type: application/json" \
  -d '{"texto": "   "}'
```

Resposta esperada (HTTP 400):

```json
{"erro": "texto_vazio", "detalhe": "texto nao pode ser vazio."}
```

No terminal do servidor, cada requisicao gera um log parecido com:

```
127.0.0.1 - - [data/hora] "POST /classificar HTTP/1.1" 200 -
```

4) Para encerrar o servidor, volte ao terminal onde ele esta rodando e use `Ctrl + C`. A mensagem esperada e `Encerrando servidor.`

## Contrato do endpoint

- `GET /` (healthcheck): status simples da API
- `POST /classificar`
  - Body JSON: `{"texto": "..."}`
  - Resposta: `{"categoria": "...", "palavras_chave": [...]}`

Validacao basica (HTTP 400 em caso de erro):
- `texto` precisa ser string
- `texto` nao pode ser vazio ou so espacos
- tamanho maximo: 500 caracteres

Codigos HTTP utilizados:
- `200` sucesso
- `400` erros de validacao (`texto_vazio`, `texto_invalido`, `texto_muito_longo`, `json_invalido`, `tamanho_conteudo_ausente`)
- `405` metodo nao permitido (ex.: GET em `/classificar`)
- `404` rota nao encontrada

## Erros comuns e o que significam

- `json_invalido`: corpo nao e JSON valido
- `texto_invalido`: campo `texto` nao e string
- `texto_vazio`: campo `texto` veio vazio
- `texto_muito_longo`: limite de 500 caracteres excedido
- `metodo_nao_permitido`: tentou `GET` em `/classificar`

## Categorias e regras

As categorias abaixo sao um exemplo e podem ser adaptadas ao dominio. Todas usam palavras-chave normalizadas (minusculas e sem acentos). Cada palavra tem peso (1 a 3); a pontuacao da categoria e a soma dos pesos encontrados; a maior pontuacao vence.

- `elogio`: obrigado, otimo, otima, excelente, parabens, amei...
- `reclamacao`: ruim, pessimo, problema, problemas, demora, "nao funciona", "nao esta funcionando", "cobrado duas vezes"...
- `duvida`: como, quando, onde, qual, ajuda, posso...
- `financeiro`: preco, valor, pagamento, cobranca, cobrado, boleto, cartao...
- `outros`: fallback quando nenhuma regra casa

## Testes

Rodar todos os testes (classificador + servidor):

```bash
python3 -m unittest discover -s tests
```

Rodar apenas os testes do servidor (validacao do endpoint):

```bash
python3 -m unittest tests/test_servidor.py
```

Saida esperada (resumo):

```
Ran 13 tests in ...
OK
```

## Estrutura dos arquivos

- `servidor.py`: servidor HTTP e validacao do request
- `classificador.py`: regras, pesos e logica de classificacao
- `tests/test_classificador.py`: testes unitarios do classificador
- `tests/test_servidor.py`: testes de validacao do endpoint HTTP

## Decisoes tecnicas

- Servidor HTTP direto com `http.server` para manter a solucao pequena e didatica
- Classificador por regras e pesos para previsibilidade e explicacao clara
- Normalizacao de texto para lidar com maiusculas e acentos

## Limitacoes

- Regras simples podem gerar falsos positivos/negativos
- Empates (mesma pontuacao) ainda seguem ordem fixa das categorias
- Nao ha persistencia nem autenticacao

## Possiveis extensoes

- Ajustar regras por dominio e refinar pesos
- Criar arquivo de configuracao (JSON) para regras e pesos (sem endpoint)
- (Opcional) Integrar modelo/LLM mantendo fallback por regras e explicabilidade

## Fontes

- Nenhuma fonte externa utilizada
