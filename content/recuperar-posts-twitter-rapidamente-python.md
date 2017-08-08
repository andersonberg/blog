title: Como Recuperar Posts do Twitter Rapidamente com Python
date: 2012-02-07 18:00:00
tags: python, twitter
category: Tutorial, Programação, Web
slug: recuperar-posts-twitter-rapidamente-python
summary: Neste post vamos criar um crawler para recuperar tweets públicos. Tweets públicos são aqueles que não necessitam de autenticação, ou seja, não é necessário ter uma conta no Twitter para ler esses tweets.
image: images/twitter-buttons-medio.jpg

Neste post vamos criar um **crawler** para recuperar **tweets** públicos. Tweets públicos são aqueles que não necessitam de autenticação, ou seja, não é necessário ter uma conta no Twitter para ler esses tweets.

Com Python, é bem simples recuperar qualquer status do Twitter, para isso, vamos utilizar o pacote [python-twitter](http://code.google.com/p/python-twitter/), que pode ser instalado via setuptools:

    $ easy_install python-twitter

Ou, pode ser baixado neste [link](http://code.google.com/p/python-twitter/downloads/list). Para instalar, extraia o conteúdo, vá até a pasta onde foi extraído e faça:

    $ python setup.py build
    $ python setup.py install

O python-twitter provê acesso a API do Twitter via código Python.

Para ler a Api e buscar ajuda, faça:

    $ pydoc twitter.Status
    $ pydoc twitter.User
    $ pydoc twitter.DirectMessage

Para começar a utilizar o python-twitter, basta importar o pacote e criar uma instância da classe twitter.Api():

    #!python
    import twitter
    api = twitter.Api()

Então, é possível obter os últimos tweets públicos facilmente com a função *GetPublicTimeline*, que retorna uma lista contendo em torno de 20 objetos do tipo *twitter.Status*, o texto do tweet em si está no atributo *text*:

    #!python
    tweets = api.GetPublicTimeline()
    for tweet in tweets:
        print tweet.text

Agora, para recuperar os 20 últimos tweets de um usuário específico, existe a função *GetUserTimeline*. Trocando '*user*' por um usuário real do twitter no código abaixo, você obtém uma lista semelhante a que foi retornada pela função *GetPublicTimeline:*

    #!python
    user_tweets = api.GetUserTimeline('user')
    for tweet in user_tweets:
        print tweet.text

A função *GetUserTimeline* permite configurar a quantidade de tweets a serem recuperados através do parâmetro *count:*

    #!python
    user_tweets = []
    tweets = api.GetUserTimeline(user, count=30)
    for tweet in tweets:
        user_tweets.append(tweet.text.encode('utf-8') + '\n')
    print user_tweets

Neste código utilizei a função *encode* para imprimir caracteres especiais em português.

Você pode encontrar mais detalhes das funções mostradas aqui na documentação da API, basta fazer no terminal:

    $ pydoc twitter.Api

O que você achou de usar a API do Twitter com Python?
Já tentou outras formas de acessar a API?
Deixe seu comentário logo abaixo!
