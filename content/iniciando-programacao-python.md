title: Iniciando a programação em Python
date: 2011-09-04 15:06:10
tags: python
category: Iniciante, Tutorial
slug: iniciando-programacao-python
summary: Neste blog vou apresentar o que eu aprendi de Python durante mais de três anos e minhas experiências diárias com a linguagem. Vou começar do início, mostrando para aqueles que estão iniciando a como programar nesta poderosa linguagem.

Neste blog vou apresentar o que eu aprendi de Python durante mais de três anos e minhas experiências diárias com a linguagem. Vou começar do início, mostrando para aqueles que estão iniciando a como programar nesta poderosa linguagem.

Não vou dizer por que você deve programar em Python. Eu a escolhi porque acho uma linguagem simples e poderosa, com poucas linhas de código você consegue criar uma aplicação completa rapidamente. Gosto de Python também porque possui muitas ferramentas que facilitam o dia-a-dia do desenvolvimento de software tanto comercial quanto científico.
Então vamos ao que interessa, pra programar em Python você precisa fazer o download e instalar em sua máquina.
Instalação para os usuários Linux/Mac OS X
Se você usa uma distribuição Linux, seja Ubuntu, Fedora, OpenSUSE, CentOS, etc... ou se você usa o Mac OS X é bem provável que o Python já esteja instalado, basta abrir um terminal (konsole, para KDE ou gnome-terminal para Gnome) e digitar “python” (sem aspas) que o interpretador Python irá iniciar.

{% img align-center /images/blog/python-linux.png Interpretador Python no Shell do Linux %}
> Interpretador Python no Shell do Linux


Instalação para os usuários Windows
Para os usuários de Windows é necessário instalar o interpretador. Visite o site [http://www.python.org/download/](http://www.python.org/download/) e baixe a última versão. Python mantém duas versões: 2.7.x e 3.2.x. Se você não sabe qual escolher, vá de 2.7, pois muitas ferramentas e frameworks são compatíveis somente com a versão 2.7. Instale normalmente, como qualquer outro instalador Windows. Depois da instalação é preciso configurar a variável PATH do sistema. No Windows 7, abra o Painel de Controle, na pesquisa (no canto superior direito)  digite “variáveis de ambiente” (sem aspas) e clique em “Editar variáveis de ambiente para sua conta”. Na seção: “Variáveis de usuário” clique na variável PATH ou crie uma com este nome e no campo “Valor da variável” digite: “;C:\Python27” (sem aspas) no final do texto que já estiver lá (isso se você instalou o Python na pasta raiz C:)
Pronto, agora abra o prompt de comando e digite python, você terá o interpretador pronto pra trabalhar.

{% img align-center /images/blog/python-cmd1.png Chamando o interpretador Python na linha de comando %}
> Chamando o interpretador Python na linha de comando

Como alternativa, junto com o Python é instalado um ambiente Shell de desenvolvimento, o IDLE, que você pode usar como interpretador (da mesma forma que no cmd) ou como editor de arquivos Python.

{% img align-center /images/blog/idle-python.png IDLE Python %}
> IDLE Python

Primeiros passos no interpretador
Com o Python devidamente instalado no seu sistema, vamos fazer alguns testes para ter as primeiras impressões de como é a experiência de programação. Vamos então, usar o prompt do interpretador Python. Você pode usar o IDLE ou iniciar o interpretador na linha de comando. Para imprimir qualquer texto na linha de comando, basta digitar print seguido de um texto entre aspas. Por exemplo:

    >>> print "Hello World!"
    Hello World!

    >>> print “Meu primeiro teste em Python.”
    Meu primeiro teste em Python.

Bem simples, e você já fez o clássico “Hello World” em Python.
O interpretador Python pode ser usado como calculadora:

    >>> 2+8
    10
    >>>9*7
    63

Digite o seguinte no interpretador:

    >>> import math

Fazendo isso você estará carregando o módulo de funções matemáticas de Python. Com isso estarão disponíveis diversas funções matemáticas pra você testar:

    >>> math.sqrt(16)
    4.0
    >>> math.pow(5,3)
    125
    math.exp(4)
    54.598150033144236
