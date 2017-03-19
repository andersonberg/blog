title: Tutorial básico de NumPy
date: 2011-10-25 17:00:38
tags: numpy, matriz, matrizes
category: Tutorial, Computação Científica
slug: tutorial-basico-numpy
summary: NumPy é um pacote de Python que suporta operações com vetores e matrizes e é essencial para a computação científica com Python. O NumPy é baseado em C, portanto tem um desempenho superior se comparado às operações com vetores originais do Python. Neste post eu quero mostrar uma introdução básica ao NumPy para os iniciantes.

NumPy é um pacote de Python que suporta operações com vetores e matrizes e é essencial para a computação científica com Python. O NumPy é baseado em C, portanto tem um desempenho superior se comparado &agrave;s opera&ccedil;&otilde;es com vetores originais do Python. Neste post eu quero mostrar uma introdu&ccedil;&atilde;o b&aacute;sica ao NumPy para os iniciantes.

###INSTALA&Ccedil;&Atilde;O DO NUMPY
Primeiro vamos instalar o NumPy. No Windows, basta baixar a &uacute;ltima vers&atilde;o do numpy no site do [SourceForge][1] e instalar facilmente com o arquivo .exe. No Linux, instale o pacote "python-numpy" disponível nos repositórios da sua distribuição ou use o pip: 

    pip install numpy

Pronto, agora &eacute; s&oacute; abrir o console Python e importar o pacote:

    #!python
    >>> import numpy as np

<h3>CRIA&Ccedil;&Atilde;O DE UM ARRAY NUMPY</h3>
<p>Para criar um array, &eacute; bem simples:</p>

    #!python
    >>> a = np.array([0,1,2,3,4,5])
    >>> a
    array([0,1,2,3,4,5])

<p>A fun&ccedil;&atilde;o <em>array</em> do NumPy, recebe uma lista de Python e transforma em um array NumPy. Voc&ecirc; pode checar o tipo:</p>

    #!python
    >>> type(a)

<p>E o tipo dos elementos:</p>

    #!python
    >>> a.dtype

<p>Para criar matrizes multidimensionais &eacute; bem simples tamb&eacute;m:</p>

    #!python
    >>> a = np.array([[0,1,2,3], [4,5,6,7], [8,9,10,11]])

<p>A fun&ccedil;&atilde;o <em>arange</em> &eacute; bem parecida com a fun&ccedil;&atilde;o <em>range</em>, s&oacute; que retorna um array ao inv&eacute;s de uma lista:</p>

    #!python
    >>> x = np.arange(11.)
    array([ 0., 1., 2., 3., 4., 5., 6., 7., 8., 9., 10.])

<p>&Eacute; poss&iacute;vel definir mais par&acirc;metros pra fun&ccedil;&atilde;o <em>arange</em>:</p>

    #!python
    >>> x = np.arange(10, 30, 5) #(limite inferior, limite superior, passo)
    array([10, 15, 20, 25])

<h3>TAMANHO DO ARRAY</h3>
<p>A propriedade <em>shape</em> mostra o tamanho de cada dimens&atilde;o da matriz:</p>

    #!python
    >>> a.shape
    (3,4)

<p>&Eacute; poss&iacute;vel, tamb&eacute;m, modificar essa propriedade:</p>

    #!python
    >>> a.shape = (2,6)
    >>> a
    array([[ 0, 1, 2, 3, 4, 5],
    [ 6, 7, 8, 9, 10, 11]])

<h3>ACESSANDO ELEMENTOS</h3>
<p>Para acessar elementos:</p>

    #!python
    >>> a[1,3]
    9

<p>&Eacute; poss&iacute;vel acessar v&aacute;rios elementos ao mesmo tempo:</p>

    #!python
    >>>a[0,3:5]
    array([3, 4])
    >>>a[4:,4:]
    array([[44, 45],
    [54, 55]])
    >>>a[:,2]
    array([2,12,22,32,42,52])
    >>>a[2::2,::2]
    array([[20, 22, 24],
    [40, 42, 44]])


<div class="wp-caption alignright" id="attachment_175"></div>
<div class="wp-caption alignright"><img src="/static/media/uploads/blog/images/matriz.jpg" width="353" height="346" alt="Matriz numpy" title="Matriz numpy" /></div>
<div class="wp-caption alignright">Fonte: SciPy 2011 - Jonathan Rocher</div>
<div class="wp-caption alignright" id="attachment_175">
<p class="wp-caption-text"></p>
</div>


<h3>MATRIZ TRANSPOSTA</h3>
<p>Para obter a matriz transposta existem duas formas:</p>

    #!python
    >>> a.transpose()
    >>> a.T
    array([[ 0, 4, 8],
    [ 1, 5, 9],
    [ 2, 6, 10],
    [ 3, 7, 11]])

<h3>OUTRAS FUN&Ccedil;&Otilde;ES IMPORTANTES DO NUMPY</h3>

<p>A fun&ccedil;&atilde;o <em>sum</em> soma todos os elementos do array:</p>

    #!python
    >>> np.sum(a)
    66

<p>Podemos usar o par&acirc;metro axis e determinar em qual eixo queremos a soma:</p>

    #!python
    >>> np.sum(a, axis=0)
    array([12, 15, 18, 21])
    >>> np.sum(a, axis=1)
    array([ 6, 22, 38])

<p>Alternativamente, podemos usar o m&eacute;todo <em>sum</em>:</p>

    #!python
    >>> a.sum()
    66
    >>> a.sum(axis=0)
    array([12, 15, 18, 21])

<p>As fun&ccedil;&otilde;es amin e amax retornam o valor m&iacute;nimo e o valor m&aacute;ximo do array, respectivamente:</p>

    #!python
    >>> b = np.array([3.4, 5., 33., 8.])
    >>> np.amin(b)
    3.4
    >>> np.amax(b)
    33.0

<p><em>argmin</em> e <em>argmax</em> retornam o &iacute;ndice do menor valor e do maior valor do array, respectivamente:</p>

    #!python
    >>> b.argmax()
    2
    >>> b.argmin()
    0

<p>O atributo&nbsp;<em>flat</em>&nbsp;retorna um iterator que permite acessar elementos de um array multidimensional como se ele fosse uma lista:</p>

    #!python
    >>> a = np.array([[0,1,2,3], [4,5,6,7], [8,9,10,11]])
    >>> a.flat
    >>> a.flat[:]
    array([ 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11])

<p>Existem ainda outras diversas fun&ccedil;&otilde;es que podemos explorar em outro post.</p>


  [1]: http://sourceforge.net/projects/numpy/files/NumPy/