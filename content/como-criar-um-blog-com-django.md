title: Como Criar um Blog de Forma Simples e Rápida com Django
date: 2014-12-28 01:11:22
tags: django, blog, mezzanine
category: Web
slug: como-criar-um-blog-com-django
summary: Você quer criar um blog pra espalhar suas ideias na rede? Quer fazer isso em poucos passos usando Django? Nas últimas semanas fizemos algumas mudanças no Pythonize e agora o blog está totalmente em Django! Neste post vou contar um pouco como foi a experiência de criar um blog em Django usando o **Mezzanine**, um CMS muito poderoso que já vem com um admin pronto para blogs.
image: /images/blog_on.jpg



Você quer criar um blog pra espalhar suas ideias na rede?

Quer fazer isso em **poucos passos** usando **Django**?

Nas últimas semanas fizemos algumas mudanças no Pythonize e agora o blog está totalmente em **Django**! Já era uma coisa que eu planejava fazer, afinal um blog que fala sobre Python é bom que seja feito com Python.

Neste post vou contar um pouco como foi a experiência de criar um blog em Django usando o **Mezzanine**, um CMS muito poderoso que já vem com um admin pronto para blogs.

**Continue lendo este artigo** para aprender, com detalhes, como instalar o Mezzanine, criar um projeto, configurar e aplicar um tema. No final, ainda vou dar uma dica bônus.

Também fizemos a migração do servidor para o [DigitalOcean](https://www.digitalocean.com/?refcode=c831ddc18699). Se você ainda não tem um servidor, recomendo o DigitalOcean e clicando [neste link](https://www.digitalocean.com/?refcode=c831ddc18699) para fazer o cadastro, você ajuda a pagar uma parte da conta do Pythonize :)


##Instalando o Mezzanine


O Mezzanine vem com diversas features bem úteis como integração com **Analytics**, **Disqus** e **Gravatar**. A lista completa você pode ver em: http://mezzanine.jupo.org/docs/overview.html#features

A instalação do Mezzanine é bem simples, vamos começar criando um ambiente virtual.

###Criando um ambiente virtual
Antes de tudo é sempre recomendável instalar o virtualenv, pra não poluir o seu ambiente. O virtualenv é uma ferramenta que cria um ambiente Python separado do seu sistema, evitando maiores dores de cabeça com configurações.

Para criar um ambiente virtual é bem simples, basta passar o comando virtualenv seguido do diretório onde vai ser armazenado o ambiente, por exemplo:

    $ virtualenv venv

No Windows você precisa fazer:

    > \path\to\env\Scripts\activate

###Instalando o Mezzanine e as dependências

Com o ambiente virtual ativado, você pode usar o pip para instalar o Mezzanine e todas as dependências necessárias:

    $ pip install mezzanine

Pronto, o pip se encarrega de instalar todas as dependências e o próprio Mezzanine. No final, você já estará pronto para criar seu primeiro projeto com o Mezzanine.

##Usando o Mezzanine

O Mezzanine funciona de uma forma muito parecida do Django. Para criar um novo projeto Mezzanine, faça de forma semelhante a criar um projeto Django:

    $ mezzanine-project meu_blog

Simples né?
Agora o Mezzanine já criou toda a estrutura do projeto, igualzinho como o Django faz:

###Criando um banco de dados

O Mezzanine vem com algumas ferramentas além das que já conhecemos do Django. Para criar e iniciar um banco de dados basta você rodar o seguinte comando:

    python manage.py createdb

Quando você rodar este comando vão aparecer algumas perguntas que você pode responder facilmente.

###Editando as configurações

Agora, antes de começar a testar é hora de você mexer nas configurações da sua aplicação. Abra o arquivo settings.py na raiz do seu projeto e procure a seguinte linha:

    #!python
    ALLOWED_HOSTS = []

E troque pelo seguinte:

    #!python
    ALLOWED_HOSTS = [
   		'.example.com', # Allow domain and subdomains
   		'.example.com.', # Also allow FQDN and subdomains
   	]

Esta é uma lista de strings que representam os hosts e domínios que seu site Django pode servir. Lembre-se de trocas 'example.com' pelo nome do seu domínio.

Busque também pela linha:

    #!python
    TIME_ZONE =

E substitua pelo seu fuso horário, por exemplo:

    #!python
    TIME_ZONE = 'America/Recife'

### Testando seu site

Para ver como está o seu blog até agora, execute o seguinte na linha de comando (com o ambiente virtual ativado):

    python manage.py runserver

Você pode ver seu site acessando o endereço http://127.0.0.1:8000/ no seu browser. Para terminar o servidor, pressione CTRL+C.

###Escreva novos artigos

Você tem acesso à tela de administração indo até: http://127.0.0.1:8000/admin/ e digitando usuário e senha que você criou quando executou o comando para criação do banco de dados.

Lá você terá acesso ao dashboard do Mezzanine, onde é possível escrever artigos, gerenciar arquivos de mídia, criar novas páginas pro site e outras coisas.

### Aplicando um tema

Um site não é nada sem um bom layout. Até agora, só cuidamos do back-end do blog, precisamos então dar uma cara pra ele.

O Mezzanine já tem temas prontos para serem usados e que se integram à ferramenta, todos baseados no bootstrap. Você pode optar por [temas gratuitos](http://thecodinghouse.in/themes/) ou [temas premium pagos](http://mezzathe.me/).

Escolha um dos temas gratuitos e faça o download. O tema é um app Django, então basta copiar dentro do projeto Mezzanine e adicionar ao INSTALLED_APPS no arquivo settings.py. É recomendável que seja o primeiro app na lista.

Pronto, seu blog está totalmente configurado e com um belo template, agora é só criar conteúdo para seus leitores.

## Bônus: Como migrar seu site Wordpress para Mezzanine

Com o Mezzanine é possível importar artigos de outras plataformas de blog como Wordpress e Blogger.

Para fazer a importação dos seus artigos do Wordpress, primeiro é preciso instalar o [feedparser](https://code.google.com/p/feedparser/), que pode ser instalar via pip.

    pip install feedparser

Faça login no seu blog Wordpress e vá em Ferramentas -> Exportar. Nesta tela você pode configurar alguns filtros e realizar a exportação do arquivo. Lembre-se de guardar o caminho onde o arquivo foi baixado.

O comando pra importar os artigos do Wordpress só funciona com o Python 2. Quando criar o ambiente virtual é importante informar ao virtualenv qual é a versão do Python que você deseja utilizar, por exemplo, no Linux:

    virtualenv -p /usr/bin/python2.7 venv

Por último, simplesmente execute o comando import_wordpress, passando o seu usuário no mezzanine e o caminho onde está o arquivo no argumento 'url':

    python manage.py import_wordpress --mezzanine-user=.. --url=[caminho_do_arquivo]


### Concluindo

Foi muito gratificante finalmente conseguir migrar o Pythonize pra Django. E o Mezzanine facilitou bastante esse trabalho. Agora é muito mais fácil pra mim gerenciar o site e fazer modificações, pois está tudo em Python e não em PHP como no Wordpress.

Consegui integrar com todas as ferramentas que utilizava antes no Wordpress, principalmente Analytics e Disqus, tudo foi muito simples.


Agora tenho uma pergunta para você

O que você achou de trabalhar com Django e Mezzanine para criar um blog?

Deixe seu comentário logo abaixo!


Imagem por: [futureshape][1]


  [1]: http://www.flickr.com/photos/futureshape/4977096245/
