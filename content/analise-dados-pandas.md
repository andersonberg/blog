title: Análise de Dados com o Pandas
date: 2017-05-03 22:05:00
tags: python, pandas
category: Intermediário
slug: analise-dados-pandas
summary:
image:
Status: draft

Pandas (Python Data Analysis) é uma biblioteca de alto desempenho para análise de dados. O pandas tem diversas ferramentas para tratamento e preparação de dados. Combinando com o IPython também tem funcionalidades para análise e modelagem de dados. Neste artigo vamos mostrar através de exemplos bem práticos como utilizar o pandas e Ipython para analisar grande volumes de dados.

Pra iniciar, vou mostrar como fazer o tratamento de dados a partir de um arquivo excel. O exemplo que vou utilizar é do resultado do senso no estado de Pernambuco. Você pode baixar os arquivos excel no site do [IBGE](http://www.ibge.gov.br/home/estatistica/populacao/censo2010/resultados_gerais_amostra/resultados_gerais_amostra_tab_xls.shtm).

{% notebook pandas.ipynb %}

<!-- |   | Código do município | Nome do município     | Total da população 2000 | Total de homens | Total de mulheres | Total da população urbana | Total da população rural | Total da população 2010 |
|---|---------------------|-----------------------|-------------------------|-----------------|-------------------|---------------------------|--------------------------|-------------------------|
| 0 | 2600054             | Abreu e Lima          | 89039.0                 | 45165.0         | 49263.0           | 86589.0                   | 7839.0                   | 94428.0                 |
| 1 | 2600104             | Afogados da Ingazeira | 32922.0                 | 16790.0         | 18301.0           | 27406.0                   | 7685.0                   | 35091.0                 |
| 2 | 2600203             | Afrânio               | 15014.0                 | 8751.0          | 8837.0            | 5859.0                    | 11729.0                  | 17588.0                 |
| 3 | 2600302             | Agrestina             | 20036.0                 | 10938.0         | 11742.0           | 16955.0                   | 5725.0                   | 22680.0                 |
| 4 | 2600401             | Água Preta            | 28531.0                 | 16581.0         | 16465.0           | 18708.0                   | 14338.0                  | 33046.0                 | -->

No exemplo, "df_pop" é uma estrutura de dados chamada DataFrame. O DataFrame tem duas dimensões e transforma os dados em uma tabela. Cada linha ou coluna de um DataFrame possui outra estrutura do pandas chamado de Series, que nada mais é do que um array unidimensional.

Suponha agora que você quer remover algumas colunas desnecessárias para melhorar a visualização e facilitar a manipulação dos dados. Trabalho simples de ser feito no pandas:

    df_pop = df_pop.drop('Código do município', axis=1)

Para remover várias colunas ao mesmo tempo, é um pouco diferente:

    df_pop = df_pop.drop(df_pop.columns[[3, 4, 5, 6]], axis=1)

A função "drop" retorna um novo DataFrame sem as colunar especificadas, por isso temos que atribuir novamente ao DataFrame original. Para evitar isso, você pode utilizar o atributo "inplace". Vamos renomear algumas colunas e utilizar o inplace para modificar diretamente o DataFrame original:

    df_pop.rename(columns={"Total da população 2000": "Total 2000", "Total da população 2010": "Total 2010"}, inplace=True)
    df_pop.head()

|   | Nome do município     | Total 2000 | Total 2010 |
|---|-----------------------|------------|------------|
| 0 | Abreu e Lima          | 89039.0    | 94428.0    |
| 1 | Afogados da Ingazeira | 32922.0    | 35091.0    |
| 2 | Afrânio               | 15014.0    | 17588.0    |
| 3 | Agrestina             | 20036.0    | 22680.0    |
| 4 | Água Preta            | 28531.0    | 33046.0    | 
