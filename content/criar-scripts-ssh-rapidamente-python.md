title: Como Criar Scripts SSH Rapidamente com Python
date: 2013-05-20 13:45:46
tags: ssh, script
category: Tutorial
slug: criar-scripts-ssh-rapidamente-python
summary: Às vezes é necessário trabalhar com vários dispositivos ligados em rede, quer sejam computadores, roteadores ou outros tipos de equipamentos. Em muitas ocasiões precisamos enviar comandos e instruções para estes equipamentos. Tudo bem entrar em um terminal e enviar um comando ou dois pra um equipamento ou outro. Mas e se forem milhares de dispositivos interconectados?

Às vezes é necessário trabalhar com **vários** dispositivos ligados em **rede**, quer sejam computadores, roteadores ou outros tipos de equipamentos.

Em muitas ocasiões precisamos enviar **comandos** e **instruções** para estes equipamentos. Isso geralmente é feito através do envio de comandos ou dados&nbsp;via **SSH**.

Tudo bem entrar em um terminal e enviar um comando ou dois pra um equipamento ou outro.

Mas e se forem **milhares** de dispositivos interconectados?

Ou se são **dezenas** ou **centenas** de instruções em série?

E se estas duas situações ocorrem **juntas**?

Nesses casos é preciso criar scripts que façam tudo automatizado.

Neste artigo vou compartilhar minha experiência com o Paramiko, um módulo Python que fornece uma interface ao protocolo SSH2.

SSH é um protocolo de rede criptografado que realiza conexão segura entre computadores e permite executar comandos remotamente. Em diversas situações é necessário automatizar o processo de conexão e execução de comandos em um computador remoto.

##Como instalar o Paramiko##
Para instalar o Paramiko é necessário instalar antes o PyCrypto, que pode ser encontrado via easy_install ou no repositório da sua distribuição Linux. Encontrei algumas dificuldades para instalar o pycrypto no Windows, por sorte existem alguns binários compilados do pycrypto: <a href="http://www.voidspace.org.uk/python/modules.shtml#pycrypto" target="_blank" title="PyCrypto Windows">http://www.voidspace.org.uk/python/modules.shtml#pycrypto</a>

Depois é só instalar o paramiko via easy_install ou procurando no repositório da distro Linux.

O paramiko tem uma classe base que fornece toda a interface para comunicação: ***paramiko.SSHClient***. Para criar um objeto e criar uma conexão com um servidor é bem simples:

    #!python
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.connect('127.0.0.1', username='anderson', password='123')

Neste exemplo, a função 'connect' está conectando ao servidor SSH local, passando nome de usuário e senha através dos par&acirc;metros 'username' e 'password', respectivamente.

Quando você conecta em um servidor ssh pela primeira vez, uma chave é automaticamente armazenada em disco num arquivo chamado "***.ssh/known_hosts***" na sua pasta home. Para isto é preciso o usuário, manualmente, aceitar o armazenamento da chave do servidor, confirmando a confiabilidade deste. Para fazermos isso automaticamente através do Paramiko, utilizamos o objeto "set_missing_host_key_policy", passando "***paramiko.AutoAddPolicy()***" como parâmetro para aceitar automaticamente as chaves. Então, nosso código anterior pode ser modificado:

    #!python
    import paramiko
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect('127.0.0.1', username='anderson', password='123')

Tenha o cuidado de somente utilizar este artifício com servidores que você confia.

##Enviando comandos via ssh##
Já aprendemos como conectar em um computador remotamente via ssh. Agora vamos ver como enviar comandos e receber os resultados destes comandos. Isto é feito com o método "exec_command" do SSHClient(). Este método retorna uma tupla de objetos (stdin, stdout, stderr) que você pode ler (no caso do stdout e stderr) ou escrever (stdin). A sintaxe para executar um comando é a seguinte:

    #!python
    stdin, stdout, stderr = ssh.exec_command('ls\n')

Que vai enviar o comando 'ls' para listar os arquivos do diretório atual. Para exibir o retorno deste comando podemos ler o conte&uacute;do do objeto stdout e, em seguida, fechar a conexão ssh:

    #!python
    print stdout.readlines()
    ssh.close()

Em alguns casos precisamos enviar outras informações para execução do comando, como por exemplo uma senha de administrador. Podemos fazer isto escrevendo no objeto stdin.

    #!python
    stdin, stdout, stderr = ssh.exec_command('sudo fdisk -l\n')
    stdin.write('1234\n')
    stdin.flush()
    print stdout.readlines()

O retorno dos comando pode ser tratado com as poderosas ferramentas de manipulação de string de Python, ou ainda filtradas com expressões regulares, dando ainda mais opções ao programador na hora de criar um script completo. Em outro post darei mais detalhes sobre a utilização do Paramiko.
