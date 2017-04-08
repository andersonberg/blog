title: Python e lambda
date: 2012-01-16 02:12:27
tags: lambda, iniciante
category: Iniciante
slug: python-lambda
summary: Sabe lambda? Lambda é algo muito legal. Com lambda você pode criar em tempo de execução funções e fazer algumas graças.

Sabe lambda? Lambda é algo muito legal. Com lambda você pode criar em tempo de execução funções e fazer algumas graças.

Vejamos algo bonito com lambda. Suponha a função fatorial.

A função fatorial é definida tal que dado um número x o fatorial deste número é:

    x\*(x-n) com n variando de (x-1) até 1.

Logo podemos traduzir num código python:

    def fatorial(x):
        if x<=1:
            return 1
        else:
            return x*fatorial(x-1)

Esse código usa recursão, espero que você saiba o que é recursão... ;)

Bom, com lambda esse mesmo código pode ter apenas uma linha, duvida?

    fatorial = lambda x: 1 if x <=1 else x*fatorial(x-1)

Definimos em fatorial uma função que executa o calculo de um fatorial de um dado número x.

Agora abra o seu interpratador python copie e cole o código para testar. Né lindo?

Python tanto na versão 2 quanto na versão 3 define lambda com um atalho para criação de funções. A sintaxe é definida assim:

    lambda_form  ::= "lambda" [parameter_list]: expression

    old_lambda_form ::=  "lambda" [parameter_list]: old_expression

Vou ler para você: uma expressão lambda é formada pela palavra reservada lambda seguida por uma lista (não o objeto lista) de parametros seperada por ":" e a expressão.

No nosso código a cima, fatorial é o nome da expressão lambda. O python sabe que a função é um lambda porque você disse isso usando a string lambda logo no inicio da expressão.

O x é o parametro. Se você quisesse passar mais parametros, bastava separa-lo por virgulas. Assim:

    funcao = lambda x,y,z: x+y+z

pergunta, qual o retorno de funcao(1,2,3) ?

Agora a parte mais difícil, a expressão.

A expressão é como você vai manipular os parametros para ter um retorno. Com lambda não é necessário por a palavra reservada return.

Essa expressão só pode ser de três formas:

-   Uma comando de uma linha (x+1)

-   outra expressão lambda.

-   Ou uma expressão condicional. (incluem testes de lógica \[or, and, not\])

No fatorial eu usei uma expressão condicional. Na funcao eu usei uma expressão de uma linha. E poderia usar outra expressão lambda.

Mas para memorizar, você deve escrever a sua expressão sempre com uma linha.

Você pode fazer uso de recursão e uso avançados de exepressão.

original : [http://romulojales.com/python-e-lambda/](http://romulojales.com/python-e-lambda/)
