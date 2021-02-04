---
title: Introdução à programação em Cython
date: 2011-09-10 03:20:23
tags: ["cython"]
category: Tutorial
slug: introducao-programacao-cython
summary: Quando o seu programa exige muita velocidade, não tem jeito, o código tem que ser escrito em C. Mas todo programador sabe o quão penoso pode ser programar em C e os diversos problemas que podem surgir no seu código contribuindo com o atraso na entrega do programa final. E porque não juntar a facilidade de programar em Python com a rapidez de execução de C? Essa é a proposta do Cython, uma extensão Python que permite que sejam utilizados tipos de C dentro do código Python.
---

Quando o seu programa exige muita velocidade, não tem jeito, o código tem que ser escrito em C. Mas todo programador sabe o quão penoso pode ser programar em C e os diversos problemas que podem surgir no seu código contribuindo com o atraso na entrega do programa final. E porque não juntar a facilidade de programar em Python com a rapidez de execução de C? Essa é a proposta do Cython, uma extensão Python que permite que sejam utilizados tipos de C dentro do código Python.

### INSTALAÇÃO

O primeiro passo é a instalação. Você pode instalar o Cython através do setuptools, digitando, na linha de comando:

    $ easy_install cython

Esse comando funciona tanto na linha de comando no Linux, quanto no prompt do Windows.

Se você não tem instalado o setuptools no Linux basta procurar pelo pacote homônimo e instalá-lo. No Windows, basta baixar o executável, na [página do pacote](http://pypi.python.org/pypi/setuptools#windows) e instalar.

Uma alternativa é baixar o Cython no [site](http://www.cython.org), extrair os arquivos e fazer na linha de comando:

    $ python setup.py install

Dica do [Francisco](http://frsoares.wordpress.com/):

Em sistemas Debian e derivados, é possível instalar o cython pelo apt-get:

    $ sudo apt-get install cython

### TUTORIAL

Para utilizar Cython em seu código, é preciso primeiro criar um arquivo com extenção .pyx. Para um primeiro teste crie um arquivo chamado helloworld.pyx e escreva a seguinte linha:

    print "Hello World"

Em seguida, crie um arquivo chamado setup.py que tenha o seguinte conteúdo:

Então, basta compilar utilizando o seguinte comando:

    $ python setup.py build_ext --inplace

Depois é só entrar no interpretador e importar o módulo criado:

    >>> import helloworld
    Hello World

Vamos avançar e criar um código que realmente tenha tipos de dados de C. Vamos criar uma função que retorne todos os números primos de 1 até um limite passado como parâmetro e salvar num arquivo chamado primes.pyx.

Para declarar tipos C, você deve usar *cdef* e informar o tipo de dado, como nas linhas 2 e 3. Na linha 3, como qualquer array em C, deve ser informado o tamanho do array.

Nas linha 9 e 11 é que aparece o ganho no desempenho, a iteração dos blocos *while* é feita com tipos C, que torna a execução mais rápida.

Feito isso, basta criar o arquivo setup.py, como no exemplo anterior:

E compilar com o comando:

    $ python setup.py build_ext --inplace
