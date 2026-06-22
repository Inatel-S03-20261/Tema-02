from abc import ABC, abstractmethod
from typing import List
from .trocas_entity import TrocaEntity
from .interface import InterfaceCartasService, InterfaceCartasRepository

# ==========================================
#      PADRÃO COMPORTAMENTAL: STRATEGY
# ==========================================

class TrocaValidacao(ABC):
    @abstractmethod
    def validar(self, dados_troca: TrocaEntity, repo: InterfaceCartasRepository) -> tuple[bool, str]:
        pass

class ValidarQuantidade(TrocaValidacao):
    def validar(self, dados_troca: TrocaEntity, repo: InterfaceCartasRepository) -> tuple[bool, str]:
        if len(dados_troca.idsPokemonsEnviados) != len(dados_troca.idsPokemonsRecebidos):
            return False, "A troca exige quantias iguais de Pokémons de ambos os lados."
        return True, ""

class ValidarJogadoresDistintos(TrocaValidacao):
    def validar(self, dados_troca: TrocaEntity, repo: InterfaceCartasRepository) -> tuple[bool, str]:
        if dados_troca.idJogadorOrigem == dados_troca.idJogadorDestino:
            return False, "Troca rejeitada: Um jogador não pode trocar cartas consigo mesmo."
        return True, ""

class ValidarExistenciaJogadores(TrocaValidacao):
    def validar(self, dados_troca: TrocaEntity, repo: InterfaceCartasRepository) -> tuple[bool, str]:
        if not repo.validarJogador(dados_troca.idJogadorOrigem):
            return False, f"Jogador origem (ID {dados_troca.idJogadorOrigem}) não existe."
        if not repo.validarJogador(dados_troca.idJogadorDestino):
            return False, f"Jogador destino (ID {dados_troca.idJogadorDestino}) não existe."
        return True, ""

class ValidarPosseCartas(TrocaValidacao):
    def validar(self, dados_troca: TrocaEntity, repo: InterfaceCartasRepository) -> tuple[bool, str]:
        cartas_origem = repo.consultarCartas(dados_troca.idJogadorOrigem)
        cartas_destino = repo.consultarCartas(dados_troca.idJogadorDestino)

        if not set(dados_troca.idsPokemonsEnviados).issubset(set(cartas_origem)):
            return False, f"O jogador origem não possui todas as cartas que está oferecendo."
        if not set(dados_troca.idsPokemonsRecebidos).issubset(set(cartas_destino)):
            return False, f"O jogador destino não possui todas as cartas que estão sendo pedidas."
        return True, ""

class ValidarCartasDuplicadas(TrocaValidacao):
    def validar(self, dados_troca: TrocaEntity, repo: InterfaceCartasRepository) -> tuple[bool, str]:
        cartas_origem = repo.consultarCartas(dados_troca.idJogadorOrigem)
        cartas_destino = repo.consultarCartas(dados_troca.idJogadorDestino)

        futuro_deck_origem = cartas_origem.copy()
        for carta in dados_troca.idsPokemonsEnviados:
            if carta in futuro_deck_origem: futuro_deck_origem.remove(carta)
        futuro_deck_origem.extend(dados_troca.idsPokemonsRecebidos)

        futuro_deck_destino = cartas_destino.copy()
        for carta in dados_troca.idsPokemonsRecebidos:
            if carta in futuro_deck_destino: futuro_deck_destino.remove(carta)
        futuro_deck_destino.extend(dados_troca.idsPokemonsEnviados)

        if len(futuro_deck_origem) != len(set(futuro_deck_origem)):
            return False, f"Troca rejeitada: Resultaria em Pokémons repetidos para o jogador {dados_troca.idJogadorOrigem}."
        
        if len(futuro_deck_destino) != len(set(futuro_deck_destino)):
            return False, f"Troca rejeitada: Resultaria em Pokémons repetidos para o jogador {dados_troca.idJogadorDestino}."

        return True, ""


class CartasService(InterfaceCartasService):
    def __init__(self, repository: InterfaceCartasRepository):
        self.repository = repository
        
        self.validacoes_troca: List[TrocaValidacao] = [
            ValidarJogadoresDistintos(),
            ValidarQuantidade(),
            ValidarExistenciaJogadores(),
            ValidarPosseCartas(),
            ValidarCartasDuplicadas()
        ]

    def consultarCartas(self, idJogador: int) -> List[int]:
        return self.repository.consultarCartas(idJogador)

    def requisicaoTroca(self, dadosTroca: TrocaEntity) -> bool:
        for validacao in self.validacoes_troca:
            sucesso, mensagem_erro = validacao.validar(dadosTroca, self.repository)
            if not sucesso:
                print(f"❌ [Troca Rejeitada] {mensagem_erro}")
                return False

        try:
            self.repository.removerCartas(dadosTroca.idJogadorOrigem, dadosTroca.idsPokemonsEnviados)
            self.repository.adicionarCartas(dadosTroca.idJogadorDestino, dadosTroca.idsPokemonsEnviados)

            self.repository.removerCartas(dadosTroca.idJogadorDestino, dadosTroca.idsPokemonsRecebidos)
            self.repository.adicionarCartas(dadosTroca.idJogadorOrigem, dadosTroca.idsPokemonsRecebidos)

            print("✅ [Troca Efetivada] Transação concluída com sucesso!")
            return True
        except Exception as e:
            print(f"❌ [Erro] Falha ao processar a troca no banco de dados: {e}")
            return False