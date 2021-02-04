---
title: Como criar uma API REST com Django
date: 2014-10-05 19:37:02
tags: ["rest", "django", "api"]
category: Web
slug: criar-api-rest-django
summary: Como construir uma API Restful totalmente configurável , funcional e simples ? Como tornar essa API pública, ao mesmo tempo que protege seus dados? E como fazer tudo isso usando Django?
image: images/cloud-1.png
alias: /criar-api-rest-python/
       /como-criar-uma-api-rest-em-python/
---

Como construir uma  **API Restful**  totalmente  **configurável** ,  **funcional**  e  **simples** ?

Como tornar essa API **pública**, ao mesmo tempo que **protege** seus dados?

E como fazer tudo isso usando **Django**?

Você vai conhecer um pouco do **Tastypie**, um framework Python muito eficiente que provê uma [API](http://pt.wikipedia.org/wiki/API) (Application Programming Interface, em português: Interface de Programação de Aplicativos) [REST](http://pt.wikipedia.org/wiki/REST) totalmente configurável para trabalhar com Django.



Para acompanharo que vamos apresentar aqui, **não** é necessário ser expert emDjango. Vamos seguir um **passo-a-passo** bem simples. Se você já sabe como configurar e usar o Django, pode pular para a parte de configuração do Tastypie, ou utilizar este tutorial como lembrete.

Se você quer se aprofundar no estudo de Djangorecomendo os seguintes links: [Django Tutorial](https://docs.djangoproject.com/en/1.6/intro/tutorial01/), [Tango with Django](http://www.tangowithdjango.com/book/).

E para aprender mais sobre RESTful webservices, tem um tutorial bem interessante [aqui](http://www.restapitutorial.com/).

## Como Funciona o Tastypie
O Tastypie ajuda você a publicar os models criados no Django, ao mesmo tempo que permite total controle sobre que é exibido ou não. O Tastypie **serializa** a saída em diversos formatos, incluindo json. Através da criação de objetos 'Resource', o Tastypie implementa formas de obter dados (GET), criar (POST) e modificar (PUT/PATCH) dados e excluir dados (DELETE).

Com estas dicas, você irá construir uma pequena API pra um exemplo de **microblog**, como o Twitter.

## Configurando o ambiente de desenvolvimento
Antes de tudo e qualquer coisa, pra não bagunçar o seu ambiente, instale o [virtualenv](https://virtualenv.pypa.io/en/latest/). O virtualenv é uma ferramenta que cria um ambiente Python **separado** do seu sistema, evitando maiores dores de cabeça com configurações.

Para criar um ambiente virtual é bem simples, basta passar o comando virtualenv seguido do diretório onde vai ser armazenado o ambiente, por exemplo:

    $ virtualenv venv

Pronto, seu ambiente virtual foi instalado na pasta 'venv'. Agora, pra começar a usar é preciso ativar o ambiente:

    $ source venv/bin/activate

Você pode perceber que o contexto da sua linha de comando mudou, quer dizer que o ambiente está pronto pra ser usado.

##Instalação do Tastypie
Com o ambiente ativado, agora é a hora de instalar o django, em seguida instale algumas dependências do tastypie e ele próprio:

    $ pip install django
    $ pip install python-mimeparse lxml defusedxml
    $ pip install django-tastypie

Pra maiores detalhes de instalação e configuração, você pode olhar na [documentação](http://django-tastypie.readthedocs.org/en/latest/tutorial.html) do Tastypie.

##Criando um projeto Django
Com tudo instalado, criar um projeto django e uma aplicação dentro do projeto também é bem fácil:

    $ django-admin.py startproject webserver
    $ cd webserver/webserver
    $ python ../manage.py startapp rest_app

##Configurando o banco de dados
Vamos utilizar como banco de dados o Sqlite, verifique se no seu arquivo settings.py já está habilitado:

```python
DATABASES = {
'default': {
    'ENGINE': 'django.db.backends.sqlite3',
    'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
```

Crie o banco de dados inicial para o Django:

    $ python manage.py syncdb

### Testando tudo até aqui
Pra testar tudo até aqui, você pode iniciar o servidor:

    $ python manage.py runserver

E acessar através da url: http://localhost:8000


### pip freeze
O pip tem um comando que cria um registro dos pacotes que foram instalados no ambiente. Isso é útil se você quiser recriar o projeto e ter todos os pacotes nas versões necessárias.

    $ pip freeze > requirements.txt


## Criando a API
### Criando uma nova aplicação
Você cria um nova aplicação com o comando startapp:

    $python manage.py startapp rest_app

Lembre-se de atualizar o INSTALLED_APPS no seu arquivo settings.py com a aplicação criada.


### Configuração inicial do Tastypie
O primeiro passo é adicionar 'tastypie' em INSTALLED_APPS no arquivo settings.py do seu projeto Django. A documentação do Tastypie diz que essa é a única configuração obrigatória. Para nosso exemplo vai ser suficiente por enquanto.

Eu tive que fazer uma modificação no settings.py por causa de um problema com autenticação. Não sei se será seu caso, só tive que remover uma linha do MIDDLEWARE_CLASSES:

```python
MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    #'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)
```

### Criando seus models
O [model](https://docs.djangoproject.com/en/dev/topics/db/models/) é onde você armazena as informações básicas dos seus dados. Cada model é uma classe Python que herda de django.db.models.Model e que se torna uma tabela no seu banco de dados. Vamos criar alguns models para nossa aplicação.

Você só precisa criar um model para a nossa aplicação que é a classe que vai conter um post no microblog. A classe de usuário podemos obter do próprio Django.

Então, edite o seu arquivo models.py e adicione a seguinte classe:

```python
class Post(models.Model):
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(default=now)
    text = models.CharField(max_length=200)
    slug = models.SlugField()
```

Este model tem um usuário associado, a data de publicação do post, o próprio texto e um campo chamado ***slug***, que identifica um determinado post e vai ser útil pra poder fazer buscas.

Pra personalizar o slug, você precisa sobrescrever o método save() do model. Neste caso, vamos pegar somente os 50 primeiros caracteres do post como slug:

```python
def save(self, *args, **kwargs):
    if not self.slug:
        self.slug = slugify(self.text)[:50]
    return super(Entry, self).save(*args, **kwargs)
```


A classe completa fica assim:

```python
from tastypie.utils.timezone import now
from django.contrib.auth.models import User
from django.db import models
from django.utils.text import slugify


class Post(models.Model):
    user = models.ForeignKey(User)
    date_created = models.DateTimeField(default=now)
    text = models.CharField(max_length=200)
    slug = models.SlugField()

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.text)[:50]
        return super(Entry, self).save(*args, **kwargs)
```


### Criando Resources
Tudo certo, mas como eu faço para expor meus dados através da API?

Você precisa criar **resources**.

No Tastypie, resources são os intermediários entre o usuário da sua API e os models de Django.

Crie o arquivo api.py no diretório da aplicação que você gerou anteriormente:

```python
from tastypie.resources import ModelResource
from rest_app.models import Post

class PostResource(ModelResource):
    class Meta:
        resource_name = 'post'
        queryset = Post.objects.all()
```

Você também tem que criar um resource para a classe de usuário:

```python
class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
```

E associar um usuário a um post. Logo, é precisoadicionar a seguinte linha na classe PostResource:

```python
user = fields.ForeignKey(UserResource, 'user')
```

O arquivo api.py completo fica assim:

```python
from tastypie.resources import ModelResource
from webserver.rest_app.models import Post
from tastypie.authorization import Authorization
from django.contrib.auth.models import User
from tastypie import fields

class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        authorization = Authorization()


class PostResource(ModelResource):
    user = fields.ForeignKey(UserResource, 'user')

    class Meta:
        resource_name = 'post'
        queryset = Post.objects.all()
        authorization = Authorization()
```


A linha ***authorization = Authorization()*** serve para que você possa criar e modificar elementos na sua API utilizando o cURL, como vai ser mostrado mais a frente.

### Views e URLs
Agora você precisa exibir os resources de alguma forma para que seus usuário tenham acesso à API. Para isso, é necessário criar urls para acessar os seus dados. Edite o arquivo urls.py do seu projeto para que fique assim:

```python
from django.conf.urls import patterns, include, url
from webserver.rest_app.api import PostResource

post_resource = PostResource()

urlpatterns = patterns('',
    url(r'^api/', include(post_resource.urls)),
)
```


Você já pode iniciar o ***runserver*** e acessar sua API via URLs, por exemplo:

[http://127.0.0.1:8000/api/post/?format=json](http://127.0.0.1:8000/api/post/?format=json)

[http://127.0.0.1:8000/api/post/1/?format=json](http://127.0.0.1:8000/api/post/1/?format=json)

### Acessando a API
Você pode interagir com a API usando o [cURL](http://curl.haxx.se/). É possível usar uma ferramenta de gerenciamento de banco SQLite, mas você perde a função de criar o slug automaticamente.

#### Recuperando os Dados
Para visualizar os dados, ou seja, obter os dados com o curl, o procedimento é semelhante a acessar um URL via browser:

    $ curl http://localhost:8000/api/post/1/?format=json

#### Enviando Dados
Para enviar e criar novos dados, você precisa usar a função POST, como estamos utilizando json, você pode enviar nesse formato da seguinte forma:

    curl --dump-header - -H "Content-Type: application/json" -X POST --data '{"text": "Um post bem rápido", "user": "/api/user/1/"}' http://localhost:8000/api/post/

### O estado atual do Tastypie
Recentemente, o criador do Tastypie escreveu [este artigo](http://toastdriven.com/blog/2014/may/23/state-tastypie/) comentando sobre o atual status do Tastypie, não só em termos de desenvolvimento como em popularidade.

O Tastypie ainda não possui uma versão 1.0, pois existem alguns pontos que precisam ser melhorados. Um deles é o desempenho quando muitos objetos precisam ser serializados.

Outra questão importante é a incompatibilidade com o Django 1.7 e ele ainda comenta que possui um novo projeto para framework RESTFul, o [Restless](https://github.com/toastdriven/restless).

Minha intenção com este artigo é apenas mostrar como é simples criar uma API com Python e Django usando o Tastypie, mas existem outras opções que podem ser exploradas e você pode deixar seu comentário se já teve experiência com alguma delas.
