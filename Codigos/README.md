# Sistema de Gestão de Cartas Pokémon

Este diretório contém a implementação do sistema dividida em dois projetos independentes, seguindo uma arquitetura de microsserviços/módulos desacoplados conforme o diagrama de classes.

## Estrutura de Pastas

O código foi dividido em:

1.  **/CartasProject**: Responsável pela gestão centralizada das cartas, repositório de dados e lógica de trocas entre jogadores.
2.  **/DistribuicaoProject**: Responsável pela lógica de geração e distribuição de novas cartas, integrando-se com a [PokeAPI](https://pokeapi.co/) para obter dados reais dos 151 Pokémon originais.

---

## Detalhes dos Projetos

### 🃏 CartasProject
Gerencia o inventário de cartas e as requisições de troca.
- **Interfaces**: Definições de contrato para serviços e repositórios.
- **Serviços**: Regras para consulta e validação de trocas.
- **DTOs**: Objetos de transferência para requisições de troca.

### 🎁 DistribuicaoProject
Gerencia a entrada de novas cartas no sistema.
- **PokeApiClient**: Cliente que consome a PokeAPI (v2) limitada aos IDs 1-151 (Geração 1).
- **Serviços**: Gera cartas aleatoriamente (ID, Nome e Tipos) e solicita ao `CartasProject` a adição das mesmas ao jogador.
- **JSON Output**: O controlador está configurado para retornar os dados dos Pokémon em formato JSON estruturado.

---

## Como Executar (Exemplo Distribuicao)

Para testar a lógica de distribuição e integração com a API:

```bash
python3 DistribuicaoProject/main.py
```

Isso executará um fluxo completo:
1. Geração de ID de jogador randômico.
2. Consulta de 5 Pokémon aleatórios na PokeAPI.
3. Exibição do JSON resultante.
4. Simulação da persistência no repositório de cartas.
