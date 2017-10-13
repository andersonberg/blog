title: Introdução à Análise de Dados com o Pandas
date: 2017-10-12 23:42:00
tags: python, pandas
category: Intermediário
slug: analise-dados-pandas-2
summary: Neste post, vou mostrar algumas ferramentas mais avançadas do Pandas. Como exemplo prático, vou utilizar uma base de dados contendo informações das eleições primárias nos Estados Unidos.
image: images/data_analysis.jpg

No último post (que você pode ver [aqui](http://pythonize.org/analise-dados-pandas.html), vimos uma introdução à biblioteca Pandas e como dar os primeiros passos em análise de grande volume de dados. Agora vamos avançar um pouco e dar uma olhada no que o Pandas é capaz de fazer.

Eu estava outro dia garimpando uma base de dados legal no [kaggle](https://www.kaggle.com) pra poder usar com o Pandas. E encontrei uma que achei bem interessante. São os dados de votação das primárias das eleições norte-americanas. Você pode baixar neste [link](https://www.kaggle.com/benhamner/2016-us-election). O arquivo zip contém diversos dados, inclusive um arquivo do sqlite se você preferir trabalhar com um banco de dados. Mas vamos trabalhar aqui com o arquivo csv que contém o resultado das preliminares. Vamos organizar os dados e tentar extrair alguma informação que possa ser útil.

{% notebook pandas-data-analysis.ipynb %}
