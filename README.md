# ChaKeeper

<div align="right">
  
[![HitCount](https://hits.dwyl.com/JVSMOTA/ChaKeeper.svg?style=flat-square)](http://hits.dwyl.com/JVSMOTA/ChaKeeper)

</div>

## 📝 Descrição
ChaKeeper é um simples sistema de chat distribuído usando o ZooKeeper como mecanismo de mensagens e controle de usuários.

## 🎯 Objetivo
O objetivo do ChaKeeper é fornecer uma plataforma de chat que possa ser facilmente distribuída em uma rede de computadores, permitindo que os usuários se comuniquem em tempo real. Ele utiliza o ZooKeeper para gerenciar a comunicação entre os usuários e armazenar as mensagens do chat.

## ⚙️ Funcionalidades
- Envio de mensagens em tempo real entre usuários conectados.
- Listagem de usuários conectados.

## 📋 Pré-requisitos
- Python 3.x
- ZooKeeper instalado e em execução em `localhost:2181`.

## 🚀 Como iniciar o ChaKeeper na sua máquina
1. Clone este repositório para o seu ambiente local:
    ```
    git clone https://github.com/JVSMOTA/ChaKeeper.git
    ```

2. Instale as dependências do Python:
    ```
    pip install kazoo
    ```

3. Inicie o ZooKeeper na sua máquina, se ainda não estiver em execução.

4. Execute o script `chakeeper.py` passando o nome de usuário como argumento:
    ```
    python chakeeper.py <username>
    ```

5. Agora você pode começar a usar o ChaKeeper para se comunicar com outros usuários conectados.

## 💡 Como usar
- Após iniciar o ChaKeeper, você pode digitar suas mensagens no terminal e pressionar Enter para enviá-las.
- Para listar os usuários conectados, digite `\u` e pressione Enter.
- Para sair do ChaKeeper, pressione `Ctrl + C`.
