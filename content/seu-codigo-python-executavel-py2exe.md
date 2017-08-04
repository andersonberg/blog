title: Transformando seu Código Python em Executável com o py2exe
date: 2011-09-14 19:58:12
tags: executavel, py2exe
category: Tutorial, Programação
slug: seu-codigo-python-executavel-py2exe
summary: Em diversas situações é necessário criar um arquivo executável a partir do seu código.
alias: /pt-br/transformando-seu-codigo-python-em-executavel-com-o-py2exe/
       /transformando-seu-codigo-python-em-executavel-com-o-py2exe/

Em diversas situações é necessário criar um arquivo executável a partir do seu código.

Às vezes é preciso entregar um programa a um cliente que não tem Python instalado ou não tem as diversas bibliotecas que você usou pra criar sua aplicação. Ou até mesmo no caso de você querer usar o seu programa em qualquer outra máquina Windows sem precisar da instalação do Python.<span>

Neste post vamos fazer um tutorial sobre como fazer isso utilizando o [py2exe](http://www.py2exe.org).

### INSTALAÇÃO DO PY2EXE
O primeiro passo é instalar o py2exe. Pra isso basta ir ao [site](http://sourceforge.net/projects/py2exe/files/) e baixar a última versão. Baixe a versão para o seu Windows (32 ou 64 bits) e de acordo com a versão do python (2.5, 2.6, 2.7...).  

A instalação é simples e padrão. Após a instalação adicione a pasta de scripts ao PATH do sistema, geralmente C:\Python27\Scripts.

### TUTORIAL
Primeiro vamos escrever um código qualquer em Python. Você pode escrever um código importando qualquer pacote, desde que este esteja instalado no seu sistema.

Para este exemplo você pode escrever seu próprio código, eu vou dar um simples exemplo utilizando a biblioteca matemática do Python, crie um arquivo em qualquer pasta chamado calc.py e escreva o seguinte código:

    #!python
    import math
    def main():
        modelo = raw_input('Digite 1 para seno e 2 para cosseno: ')
        n = raw_input('Entre com um número: ')
        choice = int(modelo)
        num = float(n)

        if choice == 1:
            print math.sin(num)

        elif choice == 2:
            print math.cos(num)

    if __name__ == "__main__":
        main()

Teste o seu código:

    C:\Pythonize> python calc.py

O segundo passo é criar um script de setup. Crie um arquivo chamado setup_calc.py na mesma pasta que você salvou o código anterior e escreva este código:

    #!python
    from distutils.core import setup
    import py2exe
    setup(console=['calc.py'])

Pronto, para criar seu arquivo executável, rode seu script:

    C:\Pythonize>python setup_calc.py py2exe

Serão criadas duas pastas: build e dist.

A pasta build é usada somente para compilar o código e criar o executável e pode ser excluída após o término do processo. A pasta dist contém os arquivos necessários para rodar sua aplicação.

Agora você pode testar seu executável:

    C:\Pythonize>cd dist
    C:\Pythonize\dist>calc.exe
    Digite 1 para seno e 2 para cosseno: 1

    Entre com um número: 4

    -0.756802495308

Funcionando muito bem!

Se você quer distribuir seu programa e levar para outro computador Windows, é preciso levar toda a pasta dist para que sua aplicação funcione corretamente. Para outras informações, veja o <a href="http://www.py2exe.org/index.cgi/Tutorial">tutorial do py2exe</a>.
Para utilizar o py2exe com outros pacotes e módulos, veja o link: <a href="http://www.py2exe.org/index.cgi/WorkingWithVariousPackagesAndModules">Working with Various Packages and Modules</a>.
