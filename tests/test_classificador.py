import unittest

from classificador import criar_classificador_padrao


class TesteClassificadorPorRegras(unittest.TestCase):
    def setUp(self) -> None:
        self.classificador = criar_classificador_padrao()

    def test_classifica_elogio(self) -> None:
        resultado = self.classificador.classificar("Atendimento excelente, parabens")
        self.assertEqual(resultado.categoria, "elogio")

    def test_classifica_reclamacao(self) -> None:
        resultado = self.classificador.classificar("O app esta ruim e nao funciona")
        self.assertEqual(resultado.categoria, "reclamacao")

    def test_classifica_duvida(self) -> None:
        resultado = self.classificador.classificar("Como posso mudar minha senha?")
        self.assertEqual(resultado.categoria, "duvida")

    def test_classifica_financeiro(self) -> None:
        resultado = self.classificador.classificar("Qual o valor da assinatura e do boleto?")
        self.assertEqual(resultado.categoria, "financeiro")

    def test_classifica_outros(self) -> None:
        resultado = self.classificador.classificar("Mensagem neutra sem palavras chave")
        self.assertEqual(resultado.categoria, "outros")

    def test_desempate_por_peso_financeiro(self) -> None:
        resultado = self.classificador.classificar("Preciso de ajuda com pagamento")
        self.assertEqual(resultado.categoria, "financeiro")

    def test_classifica_com_acentos(self) -> None:
        texto = "Parab\u00e9ns, o atendimento foi \u00f3timo."
        resultado = self.classificador.classificar(texto)
        self.assertEqual(resultado.categoria, "elogio")

    def test_prioriza_financeiro_com_caixa_e_pontuacao(self) -> None:
        texto = "COMO FA\u00c7O O PAGAMENTO???"
        resultado = self.classificador.classificar(texto)
        self.assertEqual(resultado.categoria, "financeiro")

    def test_conflito_prioriza_reclamacao(self) -> None:
        texto = "O app nao funciona e fui cobrado duas vezes"
        resultado = self.classificador.classificar(texto)
        self.assertEqual(resultado.categoria, "reclamacao")

    def test_retorna_palavras_chave_encontradas(self) -> None:
        resultado = self.classificador.classificar("Qual o valor da assinatura mensal?")
        self.assertIn("valor", resultado.palavras_chave)
        self.assertIn("assinatura", resultado.palavras_chave)

    def test_classifica_exemplos_fornecidos(self) -> None:
        exemplos = [
            ("Qual o valor da assinatura mensal?", "financeiro"),
            ("Como faco para alterar meu plano?", "duvida"),
            ("Quando o pagamento e cobrado?", "financeiro"),
            ("O aplicativo nao esta funcionando desde ontem.", "reclamacao"),
            ("Fui cobrado duas vezes e ninguem responde.", "reclamacao"),
            ("Estou tendo problemas para acessar minha conta.", "reclamacao"),
            ("Gostei muito do atendimento, estao de parabens.", "elogio"),
            ("A experiencia com o sistema foi otima.", "elogio"),
            ("Oi", "outros"),
            ("Teste", "outros"),
        ]

        for texto, categoria_esperada in exemplos:
            with self.subTest(texto=texto):
                resultado = self.classificador.classificar(texto)
                self.assertEqual(resultado.categoria, categoria_esperada)


if __name__ == "__main__":
    unittest.main()
