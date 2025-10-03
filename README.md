🗂️ Estrutura Refinada do Projeto
bash
```
tcc2_migracao_inflacao/
│
├── notebooks/
│   ├── eda_populacional.ipynb        # Análise gráfica da interpolação e da correção
│   ├── modelo_basico.ipynb           # Modelagem simples (baseline)
│   └── modelo_lstm.ipynb             # Modelagem avançada (Deep Learning)
│
├── src/
│   ├── load_data.py                  # Carregamento dos dados brutos (DATASUS, Censo, TSE)
│   ├── preprocess_pop.py             # Correção da população, interpolação mensal, geração do dataset populacional
│   ├── feature_engineering.py        # Criação de features (lags, rolling, crescimento, densidade, etc.)
│   ├── train_model.py                # Script de treino dos modelos
│   └── utils.py                      # Funções auxiliares (plot, salvar CSV, métricas)
│
├── data/
│   ├── raw/                          # Dados brutos
│   │   ├── populacao_datasus.csv
│   │   ├── dados_censo_2010_a_2012.csv
│   │   ├── dados_censo_2022.csv
│   │   └── dados_tse.csv
│   ├── processed/                    # Dados tratados
│   │   └── pop_municipal_corrigido_mensal.csv
│   └── final_dataset.csv             # Dataset final consolidado (população + preços)
│
├── figures/
│   └── graficos_populacao/           # Gráficos dos resultados da interpolação e correção
│
├── main.tex                          # Documento LaTeX do TCC
├── README.md                         # Descrição do projeto
└── requirements.txt                  # Lista de dependências (pandas, numpy, seaborn, etc.)
```

