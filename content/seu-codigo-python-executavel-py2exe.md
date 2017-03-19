title: Transformando seu Código Python em Executável com o py2exe
date: 2011-09-14 19:58:12
tags: executavel, py2exe
category: Tutorial, Programação
slug: seu-codigo-python-executavel-py2exe
summary: Em diversas situações é necessário criar um arquivo executável a partir do seu código. 

Em diversas situa&ccedil;&otilde;es &eacute; necess&aacute;rio criar um arquivo execut&aacute;vel a partir do seu c&oacute;digo. 

&Agrave;s vezes &eacute; preciso entregar um programa a um cliente que n&atilde;o tem Python instalado ou n&atilde;o tem as diversas bibliotecas que voc&ecirc; usou pra criar sua aplica&ccedil;&atilde;o. Ou at&eacute; mesmo no caso de voc&ecirc; querer usar o seu programa em qualquer outra m&aacute;quina Windows sem precisar da instala&ccedil;&atilde;o do Python.<span>

Neste post vamos fazer um tutorial sobre como fazer isso utilizando o </span><a href="http://www.py2exe.org">py2exe</a><span>.</span></p>

<h3>INSTALA&Ccedil;&Atilde;O DO PY2EXE</h3>
O primeiro passo &eacute; instalar o py2exe. Pra isso basta ir ao <a href="http://sourceforge.net/projects/py2exe/files/">site</a>&nbsp;e baixar a &uacute;ltima vers&atilde;o. Baixe a vers&atilde;o para o seu Windows (32 ou 64 bits) e de acordo com a vers&atilde;o do python (2.5, 2.6, 2.7...). &nbsp;

A instala&ccedil;&atilde;o &eacute; simples e padr&atilde;o. Ap&oacute;s a instala&ccedil;&atilde;o adicione a pasta de scripts ao PATH do sistema, geralmente C:\Python27\Scripts.

<h3>TUTORIAL</h3>
Primeiro vamos escrever um c&oacute;digo qualquer em Python. Voc&ecirc; pode escrever um c&oacute;digo importando qualquer pacote, desde que este esteja instalado no seu sistema. 

Para este exemplo voc&ecirc; pode escrever seu pr&oacute;prio c&oacute;digo, eu vou dar um simples exemplo utilizando a biblioteca matem&aacute;tica do Python, crie um arquivo em qualquer pasta chamado calc.py e escreva o seguinte c&oacute;digo:</p>

    #!python
    import math
    def main():
        modelo = raw_input(&quot;Digite 1 para seno e 2 para cosseno: &quot;)
        n = raw_input(&quot;Entre com um número: &quot;)
        choice = int(modelo)
        num = float(n)
     
        if choice == 1:
            print math.sin(num)
     
        elif choice == 2:
            print math.cos(num)
     
    if __name__ == "__main__":
        main()

<p>Teste o seu c&oacute;digo:</p>

    C:\Pythonize> python calc.py

O segundo passo &eacute; criar um script de setup. Crie um arquivo chamado setup_calc.py na mesma pasta que voc&ecirc; salvou o c&oacute;digo anterior e escreva este c&oacute;digo:

    #!python
    from distutils.core import setup
    import py2exe
    setup(console=['calc.py'])

Pronto, para criar seu arquivo execut&aacute;vel, rode seu script:

    C:\Pythonize>python setup_calc.py py2exe

Ser&atilde;o criadas duas pastas: build e dist. 

A pasta build &eacute; usada somente para compilar o c&oacute;digo e criar o execut&aacute;vel e pode ser exclu&iacute;da ap&oacute;s o t&eacute;rmino do processo. A pasta dist cont&eacute;m os arquivos necess&aacute;rios para rodar sua aplica&ccedil;&atilde;o. 

Agora voc&ecirc; pode testar seu execut&aacute;vel:

    C:\Pythonize>cd dist
    C:\Pythonize\dist>calc.exe
    Digite 1 para seno e 2 para cosseno: 1
 
    Entre com um número: 4
 
    -0.756802495308

Funcionando muito bem!

Se voc&ecirc; quer distribuir seu programa e levar para outro computador Windows, &eacute; preciso levar toda a pasta dist para que sua aplica&ccedil;&atilde;o funcione corretamente. Para outras informa&ccedil;&otilde;es, veja o <a href="http://www.py2exe.org/index.cgi/Tutorial">tutorial do py2exe</a>.</p>
<p>Para utilizar o py2exe com outros pacotes e m&oacute;dulos, veja o link:&nbsp;<a href="http://www.py2exe.org/index.cgi/WorkingWithVariousPackagesAndModules">Working with Various Packages and Modules</a>.</p>