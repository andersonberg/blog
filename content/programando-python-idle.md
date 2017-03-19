title: Programando em Python no IDLE
date: 2011-09-08 00:46:47
tags: 
category: Iniciante, Tutorial, Ferramentas
slug: programando-python-idle
summary: Depois da instalação do Python e alguns testes vamos pôr a mão na massa e trabalhar de verdade com arquivos de código. Todo código que você faz no interpretador é perdido quando você fecha o interpretador. Mas eu fiz muito código legal e vou simplesmente perder tudo? Python também trabalha com arquivos de código que você pode salvar em sua máquina para rodar depois.

<p>Depois da instala&ccedil;&atilde;o do Python e alguns testes vamos p&ocirc;r a m&atilde;o na massa e trabalhar de verdade com arquivos de c&oacute;digo. Todo c&oacute;digo que voc&ecirc; faz no interpretador &eacute; perdido quando voc&ecirc; fecha o interpretador. Mas eu fiz muito c&oacute;digo legal e vou simplesmente perder tudo? Python tamb&eacute;m trabalha com arquivos de c&oacute;digo que voc&ecirc; pode salvar em sua m&aacute;quina para rodar depois.</p>
<p></p>
<p>Os arquivos Python t&ecirc;m extens&atilde;o .py. &Eacute; poss&iacute;vel rodar um arquivo Python a partir da linha de comando da seguinte forma:</p>
<pre>$ python nome_do_arquivo.py</pre>
<p>Com isso todo o c&oacute;digo que est&aacute; salvo no arquivo &eacute; transformado em bytecode, que &eacute; um arquivo bin&aacute;rio usado pelo interpretador. O bytecode &eacute; multiplataforma, ou seja, voc&ecirc; pode levar seu c&oacute;digo pra rodar em qualquer m&aacute;quina e qualquer sistema. O bytecode &eacute; armazenado em sua m&aacute;quina geralmente com a extens&atilde;o .pyc, quando voc&ecirc; executar seu c&oacute;digo novamente sem altera&ccedil;&otilde;es o programa n&atilde;o precisa ser compilado de novo, sendo executado mais r&aacute;pido. Sempre que o seu c&oacute;digo fonte &eacute; alterado, o interpretador gera um novo bytecode.</p>
<p>Voc&ecirc; pode escrever seu c&oacute;digo no tradicional bloco de notas, mas existem diversas alternativas para escrever c&oacute;digo Python e eu recomendo fortemente que n&atilde;o seja escrito no bloco de notas. Existem v&aacute;rios editores de texto e IDEs pr&oacute;prias pra se escrever c&oacute;digo em Python. No Windows temos o Notepad++ que tem highlighting (destaca palavras especiais e seu c&oacute;digo em cores) ou o pr&oacute;prio IDLE que tamb&eacute;m vem com highlighting, auto-identa&ccedil;&atilde;o e outros recursos que facilitam a cria&ccedil;&atilde;o do c&oacute;digo. No Linux tem o Vim, que possui todos esses recursos citados anteriormente ou o Kate. Voc&ecirc; pode ver outros editores na <a href="http://wiki.python.org/moin/PythonEditors">lista de editores Python</a>&nbsp;e tamb&eacute;m <a href="http://wiki.python.org/moin/IntegratedDevelopmentEnvironments">IDEs que suportam Python</a>.</p>
<p>Neste post vamos tratar do IDLE para Windows em outro post vou falar do Vim no Linux, se algu&eacute;m tiver experi&ecirc;ncia com outros editores ou IDEs, por favor compartilhe conosco nos coment&aacute;rios.</p>
<p><strong>IDLE</strong></p>
<p>O IDLE, al&eacute;m de ter uma linha de comando Python, tamb&eacute;m &eacute; usado como editor de arquivo fonte. Com a janela principal do IDLE aberta v&aacute; ao menu File-&gt;New Window e ser&aacute; aberta uma janela em branco onde &eacute; poss&iacute;vel escrever o c&oacute;digo.</p>
<p>Vamos fazer um pequeno teste. Na nova janela aberta digite o c&oacute;digo que est&aacute; na imagem (print "Hello World"):</p>
<div class="wp-caption aligncenter" id="attachment_73"><a href="http://www.pythonize.org/wordpress/wp-content/uploads/2011/09/helloworldidle2.png"><img src="http://www.pythonize.org/wordpress/wp-content/uploads/2011/09/helloworldidle2.png" title="helloworldidle" height="89" width="500" alt="" class="size-full wp-image-73" /></a>Hello World no IDLE
<p class="wp-caption-text"></p>
</div>
<p>Salve o arquivo com o nome: helloworld.py</p>
<p>Voc&ecirc; j&aacute; pode perceber a fun&ccedil;&atilde;o highlighting nesse c&oacute;digo.</p>
<p>Nesta mesma janela, v&aacute; ao menu Run-&gt;Run Module ou aperte a tecla F5. Vai ser impresso o texto Hello World na tela do interpretador.</p>
<p>Vamos avan&ccedil;ar um pouco mais. Escreva o seguinte trecho de c&oacute;digo no IDLE:</p>
<pre>#-- coding: latin1 --
x = 7*3&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; #Isto &eacute; um coment&aacute;rio<br />y = "Hello"&nbsp;&nbsp;&nbsp; &nbsp;#Este &eacute; mais um coment&aacute;rio<br />if y == "Hello":<br />x = x + 1<br />y = y + "World"&nbsp;&nbsp;&nbsp; #Concatena&ccedil;&atilde;o de strings<br />print x<br />print y</pre>
<p>Aqui, mais uma fun&ccedil;&atilde;o do IDLE: auto-identa&ccedil;&atilde;o, assim que voc&ecirc; digita linha 4 e d&aacute; Enter, o IDLE identifica um novo bloco de c&oacute;digo. O Python identifica blocos de c&oacute;digo atrav&eacute;s da identa&ccedil;&atilde;o, diferente de outras linguagens como C e Java que identificam blocos entre chaves ({}).</p>
<p>Outras fun&ccedil;&otilde;es interessante est&atilde;o no menu Format na janela de edi&ccedil;&atilde;o de c&oacute;digo.</p>
<div class="wp-caption aligncenter" id="attachment_77"><a href="http://www.pythonize.org/wordpress/wp-content/uploads/2011/09/idle_format.png"><img src="http://www.pythonize.org/wordpress/wp-content/uploads/2011/09/idle_format.png" title="idle_format" height="248" width="500" alt="" class="size-full wp-image-77" /></a>Menu Format no IDLE
<p class="wp-caption-text"></p>
</div>
<p>Neste menu voc&ecirc; pode identar ou tirar identa&ccedil;&atilde;o de um trecho selecionado, &eacute; poss&iacute;vel comentar ou descomentar o c&oacute;digo, transformar tab em espa&ccedil;os ou vice-versa.</p>
<p>D&uacute;vidas, opini&otilde;es, sugest&otilde;es e experi&ecirc;ncias, postem nos coment&aacute;rios!</p>