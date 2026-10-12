
# Pipeline ETL — Viagens a Serviço (Portal de Transparência)

Projeto desenvolvido como atividade avaliativa do curso de Análise de Dados com Python, do SENAI/LAB365, referente ao Módulo 1 — Semana 13.
Um pipeline de dados em **Python + PostgreSQL** que baixa os dados abertos de *Viagens a Serviço* do Governo Federal, guarda o dado bruto sem alterar nada, limpa e organiza esse dado e responde perguntas de negócio com tabelas e gráficos.

## O problema que este projeto resolve:

O Portal da Transparência disponibiliza dados sobre despesas com viagens a serviço. No entanto, essas informações precisam passar por um processo de tratamento antes de serem utilizadas em análises. A base original é composta por quatro arquivos CSV, que somam quase 1,9 milhão de linhas, com desafios como codificação de caracteres, valores decimais separados por vírgula, datas em formatos específicos, campos sem preenchimento e inconsistências nos nomes das colunas.

Diante disso, o projeto implementa um fluxo completo de processamento de dados, desde a extração e preservação dos arquivos originais até a limpeza, padronização, tipagem e consolidação das informações. Ao final, os dados ficam estruturados para responder a perguntas analíticas de maneira confiável, permitindo que o processo seja executado novamente sem gerar duplicidades ou comprometer a integridade da base.

## Técnicas e tecnologias utilizadas:

- **Python 3:** utilização das bibliotecas `pandas`, `psycopg2`, `requests` e `matplotlib` para manipulação, integração, extração e visualização dos dados.
- **PostgreSQL:** criação e estruturação de tabelas com restrições de integridade (`PRIMARY KEY`, `FOREIGN KEY`, `NOT NULL`, `CHECK` e `UNIQUE`), além de consultas com `JOIN`, `GROUP BY` e `HAVING`, criação de tabelas derivadas com `CREATE TABLE AS` e elaboração de views com `CREATE VIEW`.
- **Arquitetura Medallion:** organização do processamento em três camadas — Raw, Silver e Gold —, separando os dados originais, os dados tratados e as informações consolidadas para análise.
- **Processamento de grandes volumes:** leitura dos arquivos CSV em partes, por meio de `chunksize`, e inserção eficiente de registros no banco com `execute_values`.
- **Confiabilidade e reexecução:** utilização de `TRUNCATE` para permitir a recarga controlada dos dados e tratamento de exceções com `try/except` e `rollback()` para lidar com falhas durante as operações.
- **Segurança das credenciais:** armazenamento das informações de conexão no arquivo `.env`, mantendo-as separadas do código-fonte e fora do controle de versão do Git.


## Estrutura do repositório:

| Arquivo | Descrição |
|---|---|
| `0_criar_banco.sql` | Etapa inicial: configura o banco de dados `transparencia` e cria as oito tabelas das camadas Raw e Silver. |
| `1_extrair.py` | Realiza o download do arquivo ZIP armazenado no Google Drive, processa os quatro CSVs em blocos e insere os dados na camada Raw. |
| `2_transformar.py` | Trata e padroniza os dados, converte os tipos de campos, gera colunas derivadas e popula as tabelas da camada Silver. |
| `3_analise.ipynb` | Desenvolve a camada Gold, executa as consultas para responder às sete perguntas propostas e produz visualizações gráficas. |
| `config.py` / `banco.py` | Centralizam as configurações do projeto, incluindo a leitura das variáveis do arquivo `.env`, e estabelecem a conexão com o PostgreSQL. |
| `.env.example` | Disponibiliza um modelo para configurar as credenciais e os parâmetros de conexão com o banco de dados. |
| `requirements.txt` | Lista as bibliotecas Python necessárias para executar o projeto. |
| `.gitignore` | Define os arquivos e diretórios que não devem ser enviados ao Git, como `.env`, `data/`, arquivos ZIP e arquivos CSV. |


## Como executar:

1. **Ambiente:** `pip install -r requirements.txt`
2. **Credenciais:** copie `.env.example` para `.env` e preencha `POSTGRES_PASSWORD` com a sua senha do PostgreSQL.
3. **Dados:** o arquivo é o `viagens_2025_6meses.zip`, na pasta `data` do Drive do projeto. O `DRIVE_FILE_ID` do `config.py` já está preenchido com o ID dele; o `1_extrair.py` baixa e descompacta os 4 CSVs em `data/` (cerca de 25 segundos). Se preferir, baixe o `.zip` pelo navegador e coloque os 4 CSVs em `data/`: o script não baixa de novo se eles já estiverem lá.
4. **Banco e tabelas:** o `0_criar_banco.sql` tem **duas partes**. Conectado no banco `postgres`, execute o `CREATE DATABASE`. Depois troque a conexão para o banco `transparencia` (por exemplo, na extensão PostgreSQL do VS Code) e execute o restante do arquivo.
5. **Pipeline:**

   ```bash
   python 1_extrair.py
   python 2_transformar.py

6. **Análise:** abra `3_analise.ipynb` no VS Code e execute todas as células.

Cada script pode ser executado **várias vezes**: as tabelas são esvaziadas antes de cada carga.


## Conclusões e os insights a partir dos gráficos e análise de base:

- O Ministério da Justiça e Segurança Pública é o orgão com maior despesa total com R$ 485,7 milhões;

- Brasília/ DF é o destino com maior custo médio por viagem custando (R$ 27.401,80 por viagem, em 283 viagens);

- A viagem mais longa foi a vinculada ao Ministério da Previdência Social, teve duração de 384 dias, entre 13/01/2025 e 31/01/2026. Apesar da duração, o custo total registrado foi de R$ 0,00.

- A categoria de pagamento que apresenta o maior valor médio gasto é com diárias;

- O meio de transporte que aparece com maior frequência nos trechos é o veículo oficial;

- São Paulo registra o maior número de trechos, com 81.727 ocorrências, seguido pelo Distrito Federal, com 77.962.;

- Foram encontradas três viagens cujo custo final ficou abaixo de zero, pois os valores devolvidos superaram a soma das despesas registradas;

- 18.545 viagens realizadas apresentam custo total de R$ 0,00, incluindo a viagem de maior duração. Isso indica que não há despesas registradas para essas viagens nas categorias analisadas, o que pode ocorrer, por exemplo, quando os custos são cobertos por outra fonte. Portanto, o valor zero reflete o registro disponível na base e não um erro da conversão;

- O volume expressivo atribuído à categoria Sigiloso limita a identificação de quem efetivamente financiou parte das despesas,

- A identificação de viagens com duração superior a 180 dias pode indicar missões prolongadas ou situações que merecem uma verificação mais detalhada.


## Limitações e oportunidades de melhoria:

- **Tratamento dos destinos:** separar as cidades da lista em `destinos` (uma linha por destino) permitiria comparações mais consistentes entre os locais;

- **Informações sigilosas ou inválidas:** registros classificados como `Sigiloso` no campo de pagador não permitem identificar o órgão responsável. Da mesma forma, a categoria `Inválido` no meio de transporte é preservada conforme disponibilizada pela fonte original;

- **Validação dos dados:** implementar testes automatizados para as funções de conversão e ampliar as verificações de consistência entre as camadas Raw e Silver contribuiria para aumentar a confiabilidade do processamento,

- **Automatização do pipeline:** programar a execução periódica das etapas e atualizar a base com os dados dos meses seguintes permitiria manter as análises atualizadas.
