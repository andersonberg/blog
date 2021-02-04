---
title: Programando em Python no Vim
date: 2011-09-08 14:45:20
tags: ["vim"]
category: Iniciante, Tutorial, Ferramentas
slug: programando-python-vim
summary: No Linux, um bom editor para código Python é o Vim. Costumo usar o Vim no Ubuntu e tem sido uma boa experiência. O Vim pode ser instalado também no Windows e é um bom substituto para o IDLE. Você pode fazer o download da versão para Windows no site do Vim. Versões recentes do Vim possuem suporte para Python nativo.
---

No Linux, um bom editor para código Python é o Vim. Costumo usar o Vim no Ubuntu e tem sido uma boa experiência. O Vim pode ser instalado também no Windows e é um bom substituto para o IDLE. Você pode fazer o download da versão para Windows no <a href="http://www.vim.org/download.php#pc">site do Vim</a>. Versões recentes do Vim possuem suporte para Python nativo. Para ter certeza disso abra o Vim e digite *:python print 'hello world'* (com dois pontos antes da palavra python). No Windows isso vai funcionar com o gVim.

O gVim já tem auto-identação e highlighting pra Python. Para ter o code completion no Vim é necessário ter um plugin instalado. Na versão 7.3 para Windows o omni completion já veio disponível, para testar bastar digitar ctrl+x e ctrl+o, que vai abrir uma janela dropdown com diversas opções. No Linux, para habilitar o omni completion, adicione a seguinte linha no arquivo /etc/vim/vimrc:

    autocmd FileType python set omnifunc=pythoncomplete#Complete

Outras funções interessantes que podem ser adicionadas ao Vim para codificação Python podem ser vistas em: [VIM as Python IDE](http://blog.dispatched.ch/2009/05/24/vim-as-python-ide/).

Update (17/02/12): Escrevemos  um post mais completo sobre como utilizar o [Vim como IDE pra Python](http://www.pythonize.org/tornando-o-vim-uma-ide-amigavel-pra-python/).
