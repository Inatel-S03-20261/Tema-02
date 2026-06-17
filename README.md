# 🎴 Distribuição de Cartas Pokémon

Aplicação responsável por gerenciar a distribuição de Pokémons para jogadores recém cadastrados, utilizando dados da **PokéAPI**.
###### Feito por Fernando Puebla Stein, Mauro Iwama, Rafael Braga Santos e Ramirez Wallace Villela Santos da Silva

<img width="2816" height="1536" alt="Gemini_Generated_Image_q9p8ivq9p8ivq9p8" src="https://github.com/user-attachments/assets/1c07e9c4-eda8-4c2b-bc31-94c216957366" />

---

## 📌 Descrição

Esta aplicação realiza automaticamente a atribuição de **cinco Pokémons aleatórios** para cada jogador no momento do cadastro.

Os dados são obtidos dinamicamente da PokéAPI e armazenados para permitir consulta posterior por outras aplicações.

A versão atual integra uma arquitetura de **microsserviços com mensageria assíncrona (MOM)**, aplicando padrões de projeto e princípios SOLID para garantir robustez, extensibilidade e desacoplamento entre os módulos.

---

## ⚙️ Funcionalidades

- 🎲 Geração aleatória de Pokémons via PokéAPI  
- 🧩 Distribuição automática de 5 Pokémons por jogador  
- 🚫 Garantia de **não repetição de Pokémons por jogador**  
- 🔁 Permite repetição de Pokémons entre jogadores diferentes  
- 📡 Disponibilização de dados para consulta externa (API)
- 🔄 Troca de cartas entre jogadores com validações de negócio
- ♻️ Cache inteligente da PokéAPI com fallback offline (24h)
- 🌐 Interface web estilo Pokédex para operação manual

---

## 🔗 Integração

A aplicação utiliza a API pública:

- 🌐 https://pokeapi.co/
- Link do video: https://drive.google.com/drive/folders/1vhd801y_KEQEN1ixP0-H_R89QsO56pqX?usp=drive_link
- 🌐 Interface para teste: https://pokemon-card-dealer.onrender.com/
  
  ###### Worker (deve ser executado antes da interface): https://clone-test-tema-02.onrender.com/

---

## 🏗️ Arquitetura do Sistema

O sistema é composto por **dois processos independentes** que se comunicam exclusivamente via broker MQTT

### Fluxo — Criação de Jogador

```
Browser → POST /jogador → main.py → produtor.criar_jogador()
        → publica {"id_jogador": X} em pokemon/jogadores/criado
        → HiveMQ → worker.py recebe
        → DistribuicaoController.on_jogador_criado()
        → DistribuicaoService.distribuirCartas(X)
        → PokeApiSmartProxy.sortear_ids_iniciais(5)
        → CartasRepository.adicionarCartas(X, [ids])
        → Firebase Firestore persiste o deck
```

### Fluxo — Troca de Cartas

```
Browser → POST /trocas → main.py → produtor.simular_troca()
        → publica TrocaEntity em pokemon/trocas/solicitada
        → HiveMQ → worker.py recebe
        → CartasConsumerController.on_troca_solicitada()
        → CartasService.requisicaoTroca(TrocaEntity)
        → [5 validações Strategy em cadeia]
        → CartasRepository: remove + adiciona cartas de ambos os lados
        → Firebase Firestore atualiza os dois decks
```

---

## 📨 MOM — Middleware Orientado a Mensagens
###### Como as demais aplicações ainda não tinham definido protocolo de comunicação até o fechamento desta versão, optamos por implementar um broker MQTT próprio para simular a intercomunicação entre os serviços, garantindo que nossa entrega fosse independente e funcional dentro do prazo.

O sistema usa **MQTT sobre TLS** com o broker **HiveMQ Cloud** como middleware de comunicação assíncrona entre o API Gateway e o Worker.

O API Gateway (`main.py`) e o Worker (`worker.py`) são processos **completamente desacoplados**: o gateway publica um evento e retorna imediatamente, sem esperar pelo processamento. O worker consome as mensagens de forma independente, garantindo:

- **Desacoplamento temporal** — produtor e consumidor não precisam estar ativos ao mesmo tempo  
- **Resiliência** — mensagens com QoS 1 são entregues pelo menos uma vez, mesmo com reconexões  
- **Escalabilidade** — múltiplos workers podem subscrever o mesmo tópico simultaneamente

### Tópicos MQTT

| Tópico | Publicado por | Consumido por | Payload |
|---|---|---|---|
| `pokemon/jogadores/criado` | `produtor.criar_jogador()` | `DistribuicaoController` | `{"id_jogador": int}` |
| `pokemon/trocas/solicitada` | `produtor.simular_troca()` | `CartasConsumerController` | `{"idJogadorOrigem": int, "idJogadorDestino": int, "idsPokemonsEnviados": [int], "idsPokemonsRecebidos": [int]}` |

---

## 📁 Estrutura de Pastas

```
Codigos/
├── main.py                          # API Gateway FastAPI (Processo 1)
├── worker.py                        # MQTT Listener (Processo 2)
├── produtor.py                      # Publicador MQTT (usado pelo main.py)
├── index.html                       # Interface Pokédex (SPA)
├── requirements.txt                 # Dependências Python
├── .gitignore                       # Ignora .env e firebase-adminsdk.json
│
├── shared/
│   └── database.py                  # Singleton de conexão com Firebase
│
├── DeckService/
│   ├── interface.py                 # Interfaces abstratas do módulo
│   ├── trocas_entity.py             # DTO TrocaEntity
│   ├── repository.py                # CartasRepository (Firebase Firestore)
│   ├── services.py                  # CartasService + 5 Strategy de validação
│   └── controllers/
│       ├── api.py                   # CartasApiController (FastAPI router)
│       └── consumer.py              # CartasConsumerController (MQTT handler)
│
└── DistribuicaoService/
    ├── interface.py                 # Interfaces abstratas do módulo
    ├── pokeapi_client.py            # PokeApiClient (padrão Adapter)
    ├── proxy.py                     # PokeApiSmartProxy (padrão Proxy + cache)
    ├── services.py                  # DistribuicaoService
    └── controllers.py               # DistribuicaoController (MQTT handler)
```

---

## 🧩 Design Patterns Implementados

### 1. Singleton — `shared/database.py`

**Categoria:** Criacional

**Problema resolvido:** Evitar múltiplas inicializações do Firebase Admin SDK, que lança exceção se chamado mais de uma vez por processo.

```python
class Database:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Database, cls).__new__(cls)
            cred = credentials.Certificate(path)
            firebase_admin.initialize_app(cred)
            cls._instance.db = firestore.client()
        return cls._instance
```

Qualquer chamada `Database()` em qualquer parte do código retorna sempre a mesma instância já conectada ao Firestore.

---

### 2. Proxy — `DistribuicaoService/proxy.py`

**Categoria:** Estrutural

**Problema resolvido:** Evitar uma requisição HTTP real à PokéAPI a cada novo jogador cadastrado. O `PokeApiSmartProxy` implementa a mesma interface do Adapter e adiciona cache de 24 horas e fallback offline.

```python
class PokeApiSmartProxy(InterfaceSorteadorPokemons):
    _TEMPO_EXPIRACAO_CACHE = 86400  # 24 horas
    _FALLBACK = 1025                # constante offline

    def sortear_ids_iniciais(self, quantidade: int = 5) -> List[int]:
        agora = time.time()
        if self._cache_total_pokemons and (agora - self._ultima_atualizacao) < self._TEMPO_EXPIRACAO_CACHE:
            total = self._cache_total_pokemons          # usa cache
        else:
            try:
                total = self._pokeapi_adapter.obter_quantidade_total_pokemons()
                self._cache_total_pokemons = total      # atualiza cache
                self._ultima_atualizacao = agora
            except Exception:
                total = self._cache_total_pokemons or self._FALLBACK  # fallback offline
        return random.sample(range(1, total + 1), quantidade)
```

---

### 3. Strategy — `DeckService/services.py`

**Categoria:** Comportamental

**Problema resolvido:** A validação de uma troca envolve 5 regras de negócio distintas. O padrão Strategy isola cada regra em uma classe própria, permitindo adicionar ou remover validações sem alterar o `CartasService`.

```python
class TrocaValidacao(ABC):
    @abstractmethod
    def validar(self, dados_troca: TrocaEntity, repo: InterfaceCartasRepository) -> tuple[bool, str]:
        pass

# Estratégias concretas:
class ValidarJogadoresDistintos(TrocaValidacao): ...  # jogador não troca consigo mesmo
class ValidarQuantidade(TrocaValidacao): ...           # quantidades iguais dos dois lados
class ValidarExistenciaJogadores(TrocaValidacao): ...  # ambos existem no banco
class ValidarPosseCartas(TrocaValidacao): ...          # cada um possui o que oferece
class ValidarCartasDuplicadas(TrocaValidacao): ...     # troca não gera cartas repetidas

class CartasService(InterfaceCartasService):
    def __init__(self, repository):
        self.validacoes_troca: List[TrocaValidacao] = [
            ValidarJogadoresDistintos(),
            ValidarQuantidade(),
            ValidarExistenciaJogadores(),
            ValidarPosseCartas(),
            ValidarCartasDuplicadas(),
        ]

    def requisicaoTroca(self, dadosTroca: TrocaEntity) -> bool:
        for validacao in self.validacoes_troca:
            sucesso, msg = validacao.validar(dadosTroca, self.repository)
            if not sucesso:
                return False
        # executa a troca no banco...
```

---

## ✅ Princípios SOLID Aplicados

| Princípio | Como foi aplicado |
|---|---|
| **S** — Single Responsibility | Cada classe tem uma única responsabilidade: `CartasRepository` só persiste dados, `CartasService` só orquestra regras, `PokeApiClient` só adapta a API externa, cada `TrocaValidacao` aplica uma única regra |
| **O** — Open/Closed | `CartasService` está aberto para extensão (novas validações = novas classes) e fechado para modificação (o loop de validação nunca muda) |
| **L** — Liskov Substitution | `PokeApiClient` e `PokeApiSmartProxy` são intercambiáveis via `InterfaceSorteadorPokemons` sem alterar o `DistribuicaoService` |
| **I** — Interface Segregation | Interfaces segregadas por responsabilidade: `InterfaceCartasRepository`, `InterfaceCartasService`, `InterfaceSorteadorPokemons`, `InterfaceDistribuicaoService` |
| **D** — Dependency Inversion | `CartasService` depende de `InterfaceCartasRepository` (não de `CartasRepository`); `DistribuicaoService` depende de `InterfaceSorteadorPokemons` (não de `PokeApiClient`) |

---

## 🚀 Como Executar Localmente

### Pré-requisitos

- Python 3.11+
- Conta no [Firebase](https://firebase.google.com/)
- Conta no [HiveMQ Cloud](https://www.hivemq.com/cloud/) 
- Arquivo `firebase-adminsdk.json` exportado do console do Firebase

### 1. Instale as dependências

```bash
cd Codigos
pip install -r requirements.txt
```

### 2. Configure o arquivo `.env`

Crie um arquivo `.env` dentro de `Codigos/`:

```env
HIVEMQ_HOST=seu-cluster.hivemq.cloud
HIVEMQ_PORT=8883
HIVEMQ_USER=seu-usuario
HIVEMQ_PASSWORD=sua-senha
```

Coloque também o `firebase-adminsdk.json` dentro de `Codigos/`.

> ⚠️ Ambos os arquivos estão no `.gitignore`.

### 3. Inicie o Worker (terminal 1)

```bash
python worker.py
```

### 4. Inicie o API Gateway (terminal 2)

```bash
python main.py
```

Acesse `http://localhost:8000` para abrir a interface, ou `http://localhost:8000/docs` para o Swagger.

---


### Casos de validação de troca

| Cenário | Resultado |
|---|---|
| Mesmo jogador nos dois lados | ❌ Rejeitado |
| Quantidades diferentes de cartas | ❌ Rejeitado |
| Jogador inexistente no banco | ❌ Rejeitado |
| Jogador oferece carta que não possui | ❌ Rejeitado |
| Troca resultaria em carta duplicada | ❌ Rejeitado |
| Todos os critérios atendidos | ✅ Aprovado e efetivado |
