# chakeeper.py
import os
from kazoo.client import KazooClient
from kazoo.exceptions import NodeExistsError
import time
import sys
import threading

class ChatRoom:
    def __init__(self, username):
            self.username = username
            self.messages = set()  # Usando um conjunto para evitar mensagens duplicadas
            self.zk = KazooClient(hosts='localhost:2181')
            self.zk.start()

    def receive_messages(self):
        last_message_seen = ""

        @self.zk.ChildrenWatch("/chat/messages")
        def watch_messages(children):
            os.system('clear')
            nonlocal last_message_seen

            messages = []
            for child in children:
                if child > last_message_seen:
                    message_path = f"/chat/messages/{child}"
                    data, _ = self.zk.get(message_path)
                    messages.append(data.decode("utf-8"))

            # Ordenar as mensagens por timestamp antes de exibi-las
            messages.sort()

            for message in messages:
                sender = message.split(":")[1].strip()
                if sender != self.username:
                    print(message)

            # Atualizar o último id de mensagem visto
            last_message_seen = children[-1] if children else ""


    def send_message(self, message):
        timestamp = time.strftime("%H:%M:%S")
        self.zk.ensure_path("/chat/messages")
        self.zk.create("/chat/messages/message-", f"[{timestamp}] {self.username}: {message}".encode('utf-8'), sequence=True, ephemeral=True)

    def list_recent_messages(self):
        print("Mensagens recentes:")
        if self.messages:
            for message in self.messages:
                print(message)
        else:
            print("Nenhuma mensagem recente.")

    def list_connected_users(self):
        print("Usuários conectados:")
        users = self.zk.get_children("/chat/users")
        for user in users:
            print(user)

    def start_chat(self):
        threading.Thread(target=self.receive_messages, daemon=True).start()
        try:
            while True:
                user_input = input("")
                # os.system('clear')
                if user_input == "\\u":    # Listar Usuários conectados
                    self.list_connected_users()
                else:                      # Enviar a mensagem para o servidor
                    self.send_message(user_input)
        except KeyboardInterrupt:
            print("\nSaindo do chakeeper...")
            self.zk.ensure_path("/chat/users")
            self.zk.delete(f"/chat/users/{self.username}")
            self.zk.stop()
            sys.exit(1)

    def connect(self):
        self.zk.ensure_path("/chat/users")
        self.zk.create(f"/chat/users/{self.username}", ephemeral=True)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python chakeeper.py <username>")
        sys.exit(1)

    username = sys.argv[1]
    chat_room = ChatRoom(username)
    chat_room.connect()
    chat_room.start_chat()
