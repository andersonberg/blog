title: Python - Dividindo uma Lista em N Partes
date: 2012-01-18 01:52:26
tags: listas
category: Iniciante, Programação
slug: python-dividindo-lista-n-partes
summary: frequentemente eu uso esse código, então ao invés de ir no código antigo vou neste post.Basicamente o que eu quero é o seguinte: Tenho uma lista e quero dividir em n partes quase-iguais. Explico

<p>frequentemente eu uso esse c&oacute;digo, ent&atilde;o ao inv&eacute;s de ir no c&oacute;digo antigo vou neste post.<br />Basicamente o que eu quero &eacute; o seguinte: Tenho uma lista e quero dividir em n partes quase-iguais. Explico</p>
<p></p>
<p>Suponha a lista [1,2,3,4,5,6,7,8,9,10] quero dividir a lista em 5 partes.</p>
<p>A divis&atilde;o da lista resultaria em [1,2], [3,4], [5,6], [7,8], [9,10]</p>
<p>Ok, isso &eacute; chato de fazer...</p>
<p>Mas vamos ao c&oacute;digo.</p>

##A lista
    lista = [1,2,3,4,5,6,7,8,9,10]
 
quebrando tudo:

    #!python
    def quebrador(lista,partes):
        return list(lista[ parte*len(lista)/partes:(parte+1)*len(lista)/partes ] for parte in range(partes))
    print quebrador(lista,5)
    print quebrador(lista,2)
    print quebrador(lista,10)
    print quebrador(lista,0)

<p>&Eacute; poss&iacute;vel que ocorrram varia&ccedil;&otilde;es para o tipo de lista.</p>
<p>original: <a href="http://romulojales.com/python-dividindo-uma-lista-em-n-partes" title="http://romulojales.com/python-dividindo-uma-lista-em-n-partes">http://romulojales.com/python-dividindo-uma-lista-em-n-partes</a></p>