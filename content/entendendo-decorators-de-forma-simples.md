title: Entendendo Decorators de forma simples
date: 2011-10-24 00:58:57
author: Rômulo Jales
tags: decorators
category: Programação
slug: entendendo-decorators-de-forma-simples
summary: O que é quando usar um decorator:

Sabe aquele trecho de código que vive se repetindo no seu código e você acha um saco ter repetir? Imagine que esse trecho repetido necessite uma refatoração e imagine que seu projeto é grande você já começa a vislumbrar um cenário caótico.

Sabe aquele trecho de código que vive se repetindo no seu código e você acha um saco ter repetir? Imagine que esse trecho repetido necessite uma refatoração e imagine que seu projeto é grande você já começa a vislumbrar um cenário caótico.

As boas práticas de programação tentam prevenir este tipo de problema. Mas tem horas que nem o seu mega modelo resolve. Um caso simples é quando o trecho de código que se repete necessita de parametrização ou muda de acordo com o contexto.

Decorators são uma tentativa de "economizar" código, manter a sanidade e as boas práticas de programação. Ok, eu sei que a razão principal de um decorator não é essa. Dá uma passada na
[PEP](http://www.python.org/dev/peps/pep-0318/ "PEP 318 - Decorators for Functions and Methods ") para descobrir mais. O lance é meio inception. Então eu curto a minha explicação... ;)

Então, se você viu um @ em cima de um método no código. Parabéns, você já sabe o que é um decorator e provavelmente já utiliza.

**Criando um decorator:**
=========================

- "mas eu quero criar um decorator"

Ok. Para fazer isso é simples:

Defina um método cujo o parametro será a assinatura de uma função decorada.

Então brinque com a função e retorne a função ou outra função. Lindo não? (se lembra que eu disse que era meio inception?)

Mas o decorator é isso mesmo. É um cara que vai pegar sua função bonitinha é modifica-la. Ou mesmo desfigura-la. Vou mostrar como cria um decorator brincando.

Suponha que você criou uma função de somar:

    def sum(a,b)
     return a+b

Função linda! Bom agora vou bagunçar a vida do cidadão que usa essa função e fazer que a soma seja a - b. Mas eu não quero perder o código original. Isto é um trabalho para o decorador:

    def bagunca(funcao):
     def subtrai(a,b):
     return a-b
    return subtrai

    @bagunca
    def sum(a,b):
     return a+b

Bom, agora deixo com vocês executarem o código no terminal e compreende que aconteceu com a função sum. Acredito que desta forma você compreenderá o uso do decorator.

Até a próxima
