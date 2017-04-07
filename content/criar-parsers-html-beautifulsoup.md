title: Como criar parsers HTML poderosos com BeautifulSoup
date: 2011-12-31 15:45:19
tags: parser, html
category: Web
slug: criar-parsers-html-beautifulsoup
summary: Neste post você vai aprender como criar um parser pra recuperar informações de páginas HTML utilizando o BeautifulSoup. O BeautifulSoup pode ser usado para arquivos HTML ou XML, com ele fica muito simples navegar e buscar textos em páginas HTML. Uma grande vantagem da BeautifulSoup é que ela consegue criar uma estrutura mesmo com páginas html mal formatadas, facilitando o trabalho do programador.
image: images/beautifulsoup.jpg

Neste post você vai aprender como criar um parser pra recuperar
informações de páginas HTML utilizando o BeautifulSoup. O BeautifulSoup
pode ser usado para arquivos HTML ou XML, com ele fica muito simples
navegar e buscar textos em páginas HTML. Uma grande vantagem da
BeautifulSoup é que ela consegue criar uma estrutura mesmo com páginas
html mal formatadas, facilitando o trabalho do programador.

Instalando o BeautifulSoup
--------------------------

Você pode fazer a instalação via *pip* ou *easy\_install*. Também estão
disponíveis pacotes em diferentes distribuições Linux.

Inicie o interpretador Python para testar os códigos que vamos
apresentar a seguir.

Para processar páginas HTML, importe o BeautifulSoup da seguinte forma:

    from BeautifulSoup import BeautifulSoup

Se você for processar arquivos XML:

    from BeautifulSoup import BeautifulStoneSoup

Você pode também consultar a documentação do BeautifulSoup
[aqui](http://www.crummy.com/software/BeautifulSoup/bs4/doc/ "BeautifulSoup").

Criando o parser
----------------

Por enquanto vamos processar apenas páginas html. Vamos usar a biblioteca urllib2 para recuperar uma página html.

    import urllib2
    pagina = urllib2.urlopen("http://www.globo.com").read()

Isso vai criar uma string com todo o código html da página. Então, para criar o parser basta:

    soup = BeautifulSoup(pagina)

É possível transformar esse objeto BeautifulSoup em string com o método
prettify, que manipula o código bruto adicionando quebra de linha e
espaçamento recriando a estrutura do código html.

    soup.prettify()

Para listar todos os links da página recuperada, usamos o método
findAll:

    links = soup.findAll('a')

Neste código, '*links*' é uma lista contendo objetos do tipo Tag da
biblioteca BeautifulSoup (class BeautifulSoup.Tag). Vamos agora, listar
somente os links (tirando qualquer texto ou marcação) que estão nesses
objetos Tag:

    for link in links:
        print link['href']

Para recuperar somente uma área da página, é possível usar o método find
com o parâmetro id, por exemplo:

    colunas = soup.find(id="glb-area-colunas")
    linkscol = colunas.findAll('a')
    for link in linkscol:
        print link['href']

A biblioteca BeautifulSoup facilita muito na hora de criar parsers e
crawlers para páginas html ou xml. Usada junto com o urllib2 são
poderosos aliados na recuperação de informação na web.
