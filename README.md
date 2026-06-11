# 🎴 Distribuição de Cartas Pokémon

Aplicação responsável por gerenciar a distribuição de Pokémons para jogadores recém cadastrados, utilizando dados da **PokéAPI**.
###### Feito por Fernando Puebla Stein, Mauro Iwama, Rafael Braga Santos e Ramirez Wallace Villela Santos da Silva

<img width="2816" height="1536" alt="Gemini_Generated_Image_q9p8ivq9p8ivq9p8" src="https://github.com/user-attachments/assets/1c07e9c4-eda8-4c2b-bc31-94c216957366" />

---

## 📌 Descrição

Esta aplicação realiza automaticamente a atribuição de **cinco Pokémons aleatórios** para cada jogador no momento do cadastro.

Os dados são obtidos dinamicamente da PokéAPI e armazenados para permitir consulta posterior por outras aplicações.

---

## ⚙️ Funcionalidades

- 🎲 Geração aleatória de Pokémons via PokéAPI  
- 🧩 Distribuição automática de 5 Pokémons por jogador  
- 🚫 Garantia de **não repetição de Pokémons por jogador** - 🔁 Permite repetição de Pokémons entre jogadores diferentes  
- 📡 Disponibilização de dados para consulta externa (API)

---

## 🏗️ Arquitetura e Comunicação (Microsserviços)

O projeto foi estruturado em dois módulos independentes, simulando o trabalho de equipes distintas e isoladas que se integram via contratos e eventos:

- **`DistribuicaoService`**: Domínio responsável por consultar a rede externa (PokéAPI) e aplicar as regras de negócio para gerar o "Deck Inicial".
- **`DeckService`**: Domínio responsável pelo inventário, regras de transação das cartas e persistência isolada no banco de dados.

**Comunicação entre as aplicações:**
A comunicação utiliza o padrão de **Arquitetura Orientada a Eventos**. 
- **Ações de Escrita (Eventos):** O Gateway da aplicação (`main.py`) publica as intenções dos usuários (ex: criar jogador, trocar cartas) em um broker de mensageria **MQTT (HiveMQ)**. O serviço `worker.py` atua como um *Listener* em segundo plano, escuta os tópicos, aprova as regras de negócio e injeta os dados do serviço de distribuição diretamente no repositório do serviço de deck.
- **Ações de Leitura (Síncronas):** Consultas de inventário ocorrem via requisições HTTP REST (FastAPI) para prover resposta imediata à interface.

---

## 🚀 Como Executar o Projeto

### Pré-requisitos
1. Python 3.8 ou superior instalado.
2. Instale as dependências do ecossistema:
   ```bash
   pip install -r requirements.txt
   ```
3. Crie um arquivo **`.env`** na raiz do projeto contendo as credenciais de acesso ao cluster MQTT:
   ```env
   HIVEMQ_HOST=sua_url_cluster.s1.eu.hivemq.cloud
   HIVEMQ_PORT=8883
   HIVEMQ_USER=seu_usuario
   HIVEMQ_PASSWORD=sua_senha
   ```
4. Adicione o arquivo de chave privada do banco de dados (`firebase-adminsdk.json`) na raiz do projeto.

### Inicialização
Como a arquitetura divide a recepção e o processamento, é necessário rodar dois terminais em paralelo:

**Terminal 1: O Processador de Eventos (Worker)**
Fica em silêncio aguardando mensagens no broker para alterar o banco de dados.
```bash
python worker.py
```

**Terminal 2: A API Gateway e Interface**
Serve as rotas REST HTTP e a interface de usuário (Pokédex).
```bash
python main.py
```

Com ambos rodando, acesse a interface visual através do seu navegador em: **`http://localhost:8000`**

---

## 🔗 Integração

A aplicação utiliza a API pública:

- 🌐 https://pokeapi.co/