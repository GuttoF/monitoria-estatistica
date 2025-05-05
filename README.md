# Dashboard de Análise do Questionário - Estatística Aplicada a Data Science

## Visão Geral

Este projeto apresenta um dashboard interativo construído com **Streamlit** para visualizar e analisar os resultados de um questionário aplicado aos alunos da disciplina de **Estatística Aplicada a Data Science** da **Faculdade Nova Roma Caruaru**.

O objetivo principal é fornecer insights sobre:

- A **disponibilidade dos alunos para monitorias**.
- A **percepção sobre a avaliação N1**.
- Os **principais desafios enfrentados**.

Essas informações visam **facilitar a tomada de decisões pedagógicas** e o **planejamento de atividades de apoio**.

---

## Funcionalidades Principais

- ### **Análise de Disponibilidade**

  Visualização gráfica (gráfico de barras agrupado) da quantidade de alunos disponíveis em cada período (**Manhã, Tarde, Noite**) para cada dia da semana (**Segunda a Sábado**).

- ### **Análise da N1**

  - **Gráfico de pizza** mostrando a proporção de alunos satisfeitos e insatisfeitos com a nota da N1.
  - **Gráfico de barras** exibindo os maiores desafios apontados pelos alunos na prova N1.

- ### **Informações sobre Monitorias**

  Seção informativa sobre o formato, modalidade e recursos das futuras sessões de monitoria.

- ### **Conclusões Preliminares**

  Um resumo textual destacando os principais achados da análise, incluindo:
  - Os horários de pico de disponibilidade.
  - Os desafios mais comuns na N1.

- ### **Visualização de Dados**

  Tabela interativa exibindo os dados brutos carregados do questionário.

- ### **Footer Personalizado**

  Inclui um logo (opcional) e informações sobre o dashboard.

---

## Tecnologias Utilizadas

- **Python**: Linguagem de programação principal.
- **Streamlit**: Framework para criação rápida de aplicações web de dados.
- **Pandas**: Biblioteca para manipulação e análise de dados.
- **Plotly Express**: Biblioteca para criação de gráficos interativos.
- **Docker**: Para containerização da aplicação.

---

## Estrutura do Projeto

```bash
monitoria-estatistica/
├── app
│ └── main.py # Código principal da aplicação Streamlit
├── assets
│ └── nr-logo.png # Logo utilizado no footer
├── data
│ └── data.csv # Arquivo CSV com os dados do questionário
├── Dockerfile # Instruções para construir a imagem Docker
├── pyproject.toml # Gerenciamento de dependências e configuração do projeto Python
├── README.md # Este arquivo
└── uv.lock # Arquivo de bloqueio gerado pelo gerenciador UV
```

---

## Fonte de Dados

Os dados utilizados pelo dashboard são carregados a partir do arquivo `data/data.csv`. Espera-se que este arquivo contenha as seguintes colunas (ou colunas que serão renomeadas para estes nomes dentro do script):

- `ID_Aluno` (ou similar, renomeado para `ID_Aluno`)
- `Segunda` (Disponibilidade na Segunda)
- `Terça` (Disponibilidade na Terça)
- `Quarta` (Disponibilidade na Quarta)
- `Quinta` (Disponibilidade na Quinta)
- `Sexta` (Disponibilidade na Sexta)
- `Sábado` (Disponibilidade no Sábado)
- `N1_Satisfatoria` (Resposta "Sim" ou "Não" sobre a satisfação com a nota N1)
- `Desafios` (Texto descrevendo o maior desafio na N1)

> **Nota:** Os valores nas colunas de disponibilidade devem indicar os períodos (ex: `"Manhã"`, `"Tarde"`, `"Noite"`, `"Manhã, Tarde"`). Valores ausentes são tratados como **"Indisponível"**.
