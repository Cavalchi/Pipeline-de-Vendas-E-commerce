<h1 align="center">
  📦 E-Commerce Data Pipeline (Olist dataset)
</h1>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white"/>
  <img src="https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white"/>
  <img src="https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white"/>
  <img src="https://img.shields.io/badge/SQLAlchemy-D71F00?style=for-the-badge&logo=sqlalchemy&logoColor=white"/>
</p>

## 📌 Visão Geral do Projeto
Este projeto de **Engenharia de Dados** tem como objetivo resolver um problema clássico de negócio: a complexidade de cruzar informações espalhadas de centenas de milhares de logs de compras.

Estruturei um Pipeline de ETL (*Extract, Transform, Load*) completo onde dados não-estruturados, brutos e massivos são ingeridos através do **Python**, sanitizados contra falhas transacionais na biblioteca Pandas e descarregados de forma relacional (com chaves conectadas) em um *Data Warehouse* em **PostgreSQL**. Tudo orquestrado e versionado.

## 🏗️ Arquitetura do Fluxo de Dados
```mermaid
graph LR;
    A[(Kaggle CSVs)] -->|Python (Pandas)| B(Limpeza de Duplicatas & Parsing);
    B -->|SQLAlchemy| C(Injeção Relacional);
    C -->|psycopg2| D[(PostgreSQL)];
    D -->|Analytics| E(Consultas SQL Otimizadas);
```

## 🚀 Ferramentas & Competências Empenhadas
* **Python Avançado:** Conexão nativa e tratamento estrito via algoritmos tabulares nativos de alto desempenho.
* **Database Design:** Aderência e uso de constraints em tabelas fato dimensionais. As tabelas seguem o padrão logístico real (Orders ➔ Payments ➔ Items ➔ Customers).
* **Business Intelligence (via SQL):** Uso profícuo de sintaxes de Agregação e `JOIN` em `02_analysis.sql` para tomadas direitas de decisão como análise por ticket médio GMV.

## 📊 Principais Descobertas e Ganhos de Negócio
Logo na primeira semana iterando o banco de dados finalizado, foram descobertos os seguintes insights gerenciais rodando o script analítico de SQL customizado:

1. **Previsões Logísticas Quebradas no Extremo Norte:** Apesar de SP e RJ entregarem com sobra em 12 dias em média. Clientes de estados como AP e RR amargam um atraso colossal de até **48 dias além do prazo estimado**, derrubando imediatamente o CSAT (Nível de Satisfação do Consumidor).
2. **Volumetria de Rentabilidade Isolada:** O SQL comprovou numericamente que as verticais "Cama, Mesa e Banho", "Beleza e Saúde" e "Relógios" suportam a força bruta do GMV da Olist, compensando o buraco logístico.

---

### 💻 Como Reproduzir Localmente

**1. Requisitos:** 
Instale o Python 3.x, pip, e o PostgreSQL devidamente configurado em `localhost:5433` (com a senha do script).

**2. Clone e Inicie:**
```bash
git clone https://github.com/Cavalchi/Pipelina-de-Vendas-E-commerce.git
cd Pipelina-de-Vendas-E-commerce
pip install -r requirements.txt
```

**3. Dados:** Baixe os Olist CSVs do Kaggle, coloque na pasta `data/raw/` e rode o código mestre:
```bash
python src/ingestion/etl_olist.py
```

<hr>
<blockquote>
"Em busca da verdade escondida através do volume de dados". <br>
— Fique a vontade para dar um Fork ou entrar em contato se quiser bater um papo forte de tecnologia! 🤝
</blockquote>
