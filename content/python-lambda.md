title: Python e lambda
date: 2012-01-16 02:12:27
tags: lambda
category: Iniciante, Core
slug: python-lambda
summary: Sabe lambda? Lambda é algo muito legal. Com lambda você pode criar em tempo de execução funções e fazer algumas graças.

<p>Sabe lambda? Lambda &eacute; algo muito legal. Com lambda voc&ecirc; pode criar em tempo de execu&ccedil;&atilde;o fun&ccedil;&otilde;es e fazer algumas gra&ccedil;as.</p>
<p>Vejamos algo bonito com lambda. Suponha a fun&ccedil;&atilde;o fatorial.</p>
<p>A fun&ccedil;&atilde;o fatorial &eacute; definida tal que dado um n&uacute;mero x o fatorial deste n&uacute;mero &eacute;:<!--more--></p>
<p>x*(x-n) com n variando de (x-1) at&eacute; 1.</p>
<p>Logo podemos traduzir num c&oacute;digo python:</p>
<pre><br />def fatorial(x):<br /> if x&lt;=1:<br /> return 1<br /> else:<br /> return x*fatorial(x-1)</pre>
<p>Esse c&oacute;digo usa recurs&atilde;o, espero que voc&ecirc; saiba o que &eacute; recurs&atilde;o... ;)</p>
<p>Bom, com lambda esse mesmo c&oacute;digo pode ter apenas uma linha, duvida?</p>
<pre><br />fatorial = lambda x: 1 if x &lt;=1 else x*fatorial(x-1)</pre>
<p>Definimos em fatorial uma fun&ccedil;&atilde;o que executa o calculo de um fatorial de um dado n&uacute;mero x.</p>
<p>Agora abra o seu interpratador python copie e cole o c&oacute;digo para testar. N&eacute; lindo?</p>
<p>Python tanto na vers&atilde;o 2 quanto na vers&atilde;o 3 define lambda com um atalho para cria&ccedil;&atilde;o de fun&ccedil;&otilde;es. A sintaxe &eacute; definida assim:</p>
<pre><strong id="grammar-token-lambda_form">lambda_form </strong> ::= "lambda" [<a href="http://docs.python.org/reference/compound_stmts.html#grammar-token-parameter_list"><tt>parameter_list</tt></a>]: <a href="http://docs.python.org/reference/expressions.html#grammar-token-expression"><tt>expression</tt></a></pre>
<p></p>
<pre id="index-1018"><strong id="grammar-token-old_lambda_form">old_lambda_form</strong> ::=  "lambda" [<a href="http://docs.python.org/reference/compound_stmts.html#grammar-token-parameter_list"><tt>parameter_list</tt></a>]: <a href="http://docs.python.org/reference/expressions.html#grammar-token-old_expression"><tt>old_expression</tt></a></pre>
<p><br />Vou ler para voc&ecirc;: uma express&atilde;o lambda &eacute; formada pela palavra reservada lambda seguida por uma lista (n&atilde;o o objeto lista) de parametros seperada por ":" e a express&atilde;o.</p>
<p>No nosso c&oacute;digo a cima, fatorial &eacute; o nome da express&atilde;o lambda. O python sabe que a fun&ccedil;&atilde;o &eacute; um lambda porque voc&ecirc; disse isso usando a string lambda logo no inicio da express&atilde;o.</p>
<p>O x &eacute; o parametro. Se voc&ecirc; quisesse passar mais parametros, bastava separa-lo por virgulas. Assim:</p>
<pre><br />funcao = lambda x,y,z: x+y+z</pre>
<p>pergunta, qual o retorno de funcao(1,2,3) ?</p>
<p>Agora a parte mais dif&iacute;cil, a express&atilde;o.</p>
<p>A express&atilde;o &eacute; como voc&ecirc; vai manipular os parametros para ter um retorno. Com lambda n&atilde;o &eacute; necess&aacute;rio por a palavra reservada return.</p>
<p>Essa express&atilde;o s&oacute; pode ser de tr&ecirc;s formas:</p>
<p></p>
<ul>
<ul>
<li>Uma comando de uma linha (x+1)</li>
</ul>
</ul>
<p></p>
<ul>
<ul>
<li>outra express&atilde;o lambda.</li>
</ul>
</ul>
<p></p>
<ul>
<ul>
<li>Ou uma express&atilde;o condicional. (incluem testes de l&oacute;gica [or, and, not] )</li>
</ul>
</ul>
<p></p>
<p><br />No fatorial eu usei uma express&atilde;o condicional. Na funcao eu usei uma express&atilde;o de uma linha. E poderia usar outra express&atilde;o lambda.</p>
<p>Mas para memorizar, voc&ecirc; deve escrever a sua express&atilde;o sempre com uma linha.</p>
<p>Voc&ecirc; pode fazer uso de recurs&atilde;o e uso avan&ccedil;ados de exepress&atilde;o.</p>
<p>original :<a href="http://romulojales.com/python-e-lambda/"> http://romulojales.com/python-e-lambda/</a></p>