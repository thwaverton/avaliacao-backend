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

    def test_peso_financeiro_em_duvida(self) -> None:
        resultado = self.classificador.classificar("Como faco o pagamento?")
        self.assertEqual(resultado.categoria, "financeiro")


if __name__ == "__main__":
    unittest.main()
