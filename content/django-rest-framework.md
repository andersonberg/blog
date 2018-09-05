title: Criando APIs com Django Rest Framework
date: 2018-09-05 15:35:00
tags: rest, django, api, drf
category: Web
slug: django-rest-framework
summary: Como construir uma API Restful com Django usando o Django Rest Framework
image: images/cloud-1.png

Um dos frameworks mais populares para criar APIs RESTful em Python é o Django Rest Framework. Baseado no Django, possui a mesma flexibilidade e rapidez no desenvolvimento. Vamos falar sobre como construir sua [API](http://pt.wikipedia.org/wiki/API) [REST](http://pt.wikipedia.org/wiki/REST) do zero e consumir os dados providos por ela.



Para acompanhar o que vamos apresentar aqui, **não** é necessário ser expert em Django. Vamos seguir um **passo-a-passo** bem simples. Se você já sabe como configurar e usar o Django, pode pular para a parte de configuração do DRF, ou utilizar este tutorial como lembrete.

Se você quer se aprofundar no estudo de Djangorecomendo os seguintes links: [Django Tutorial](https://docs.djangoproject.com/en/1.6/intro/tutorial01/), [Tango with Django](http://www.tangowithdjango.com/book/).

E para aprender mais sobre RESTful webservices, tem um tutorial bem interessante [aqui](http://www.restapitutorial.com/).


# Django Rest Framework

A página do DRF lista algumas vantagens de usar o framework:

 - API navegável: Vem com uma interface web integrada
 - Mecanismos de autenticação inclusos
 - Serialização tanto com ORM quanto sem
 - Totalmente customizável
 - Extensa documentação [http://www.django-rest-framework.org/](http://www.django-rest-framework.org/)
 - Usado por grandes companhias como Mozilla, Heroku e Eventbrite