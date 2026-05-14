# Crescimento Populacional e Preços de Aluguel no Brasil

Análise e modelagem da relação entre o crescimento populacional e a variação dos preços de aluguel nas principais capitais brasileiras.

## 📋 Sobre o Projeto

Este é um Trabalho de Conclusão de Curso (TCC) que investiga a correlação entre dados demográficos (populacionais) e preços de aluguel no Brasil, utilizando análise exploratória de dados (EDA), modelagem estatística e machine learning para gerar insights sobre tendências econômicas regionais.

## 📊 Datasets Utilizados

- **CENSO 2022**: Dados populacionais dos municípios brasileiros (IBGE)
- **FipeZAP**: Preços de aluguel mensais por m² nas principais capitais (painel de dados)
- **IPCA**: Índice de Preços ao Consumidor Amplo (inflação)
- **Cesta Básica**: Série temporal de preços da cesta básica brasileira

## 🏗️ Estrutura do Projeto

```
.
├── notebooks/
│   ├── eda_aluguel.ipynb                    # EDA de preços de aluguel
│   ├── eda_populacional.ipynb               # EDA de dados populacionais
│   ├── eda_macroeconomics.ipynb             # EDA de indicadores macroeconômicos
│   └── migracao_regional_e_alugueis.ipynb   # Análise de migração regional
├── src/
│   └── pre_process/
│       ├── load_data.py                     # Funções para carregar dados brutos
│       ├── preprocess_pop.py                # Pré-processamento de dados populacionais
│       ├── preprocess_aluguel_fipezap.py    # Pré-processamento de dados FipeZAP
│       ├── final_data_set.py                # Consolidação do dataset final
│       └── stepwise.py                      # Seleção de features com stepwise
├── figures/                                  # Gráficos e visualizações geradas
│   ├── grafico_previsao_aluguel.pdf
│   ├── grafico_serie_temporal_macro.pdf
│   ├── grafico_feature_importance.pdf
│   └── grafico_forest_plot.pdf
├── requirements.txt                         # Dependências do projeto
└── README.md                                # Este arquivo
```

## 🛠️ Dependências

O projeto utiliza as seguintes bibliotecas Python:

```
pandas             # Manipulação de dados
numpy              # Operações numéricas
matplotlib         # Visualizações básicas
seaborn            # Visualizações avançadas
openpyxl           # Leitura de arquivos Excel
statsmodels        # Modelos estatísticos
linearmodels       # Modelos de regressão linear
scikit-learn       # Machine Learning
mlxtend            # Algoritmos de ML adicionais
scipy              # Computações científicas
xgboost            # Gradient Boosting
optuna             # Otimização de hiperparâmetros
```

## 📦 Instalação

1. Clone o repositório:
```bash
git clone <repository-url>
cd tcc-crescimento-populacional-e-precos-de-aluguel-no-brasil
```

2. Crie um ambiente virtual:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate      # Windows
```

3. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🔄 Pipeline de Dados

### 1. Carregamento (`src/pre_process/load_data.py`)
- Função `diagnostico_csv()`: Diagnóstico de arquivos CSV
- Função `load_censo_2022()`: Carregamento e limpeza de dados do Censo 2022
- Função `load_ibge()`: Carregamento de dados do IBGE

### 2. Pré-processamento de População (`src/pre_process/preprocess_pop.py`)
- Tratamento de dados populacionais
- Validação de códigos IBGE
- Tratamento de valores ausentes

### 3. Pré-processamento de Aluguel (`src/pre_process/preprocess_aluguel_fipezap.py`)
- Leitura de múltiplas abas do arquivo Excel FipeZAP
- Transformação de dados mensais para anuais
- Cálculo de logaritmo natural e variações anuais
- Filtragem de cidades e períodos com dados válidos

### 4. Consolidação (`src/pre_process/final_data_set.py`)
- Merge de todos os datasets
- Criação do painel final com todas as variáveis

### 5. Seleção de Features (`src/pre_process/stepwise.py`)
- Seleção automática de variáveis significativas usando método stepwise

## 📈 Análises Realizadas

### Notebooks de Análise Exploratória

1. **eda_aluguel.ipynb**: 
   - Distribuição de preços de aluguel
   - Variação temporal por cidade
   - Correlações com outras variáveis

2. **eda_populacional.ipynb**:
   - Crescimento populacional por região
   - Distribuição demográfica
   - Identificação de padrões regionais

3. **eda_macroeconomics.ipynb**:
   - Análise de indicadores macroeconômicos
   - IPCA, cesta básica, variáveis de mercado
   - Série temporal de indicadores

4. **migracao_regional_e_alugueis.ipynb**:
   - Relação entre migração regional e preços
   - Análise por regiões geográficas
   - Identificação de tendências

## 📊 Visualizações Geradas

- **grafico_previsao_aluguel.pdf**: Modelo de previsão de preços de aluguel
- **grafico_serie_temporal_macro.pdf**: Série temporal de indicadores macroeconômicos
- **grafico_feature_importance.pdf**: Importância das features no modelo
- **grafico_forest_plot.pdf**: Gráfico Forest Plot de resultados

## 🎯 Objetivos Alcançados

✅ Consolidação de múltiplas fontes de dados  
✅ Análise exploratória completa dos dados  
✅ Pré-processamento automatizado  
✅ Modelagem estatística e de machine learning  
✅ Otimização de hiperparâmetros com Optuna  
✅ Geração de gráficos e visualizações  
✅ Seleção de features significativas  

## 🚀 Como Usar

### Carregar e Explorar os Dados
```python
from src.pre_process.load_data import load_censo_2022, diagnostico_csv

# Diagnóstico de um arquivo
diagnostico_csv('caminho/para/arquivo.csv')

# Carregar dados do Censo 2022
df_censo = load_censo_2022('caminho/para/censo2022.csv')
```

### Pré-processar Dados
```python
from src.pre_process.preprocess_aluguel_fipezap import preprocessar_fipezap_anual

# Pré-processar dados de aluguel
preprocessar_fipezap_anual('caminho/aluguel.xlsx', 'saida.csv', cidade_ibge_dict)
```

### Executar Notebooks
```bash
jupyter notebook notebooks/eda_aluguel.ipynb
```

## 📝 Metodologia

1. **Coleta de Dados**: Consolidação de dados de múltiplas fontes (IBGE, FipeZAP, etc.)
2. **Limpeza e Validação**: Tratamento de valores ausentes e outliers
3. **Análise Exploratória**: EDA para compreensão dos dados
4. **Modelagem**: Uso de regressão linear, XGBoost e outros algoritmos
5. **Validação**: Métricas de performance e validação cruzada
6. **Otimização**: Hyperparameter tuning com Optuna
7. **Visualização**: Geração de gráficos explicativos

## 📚 Referências Técnicas

- Estatística Descritiva e Inferencial
- Análise de Séries Temporais
- Machine Learning Supervisionado
- Econometria de Dados em Painel

## 📄 Licença

Projeto acadêmico - TCC

## ✏️ Autor

Gustavo Guilherme Sutil Alberton

---

**Última atualização**: Maio de 2026
