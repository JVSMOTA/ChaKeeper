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
        self.zk = KazooClient(hosts='localhost:2181')
        self.zk.start()

    def receive_messages(self):
        @self.zk.ChildrenWatch("/chat/messages")
        def watch_messages(children):
            os.system('clear')
            messages = []
            for child in children:
                message_path = f"/chat/messages/{child}"
                data, _ = self.zk.get(message_path)
                messages.append(data.decode("utf-8"))

            # Ordenar as mensagens por timestamp antes de exibi-las
            messages.sort()

            for message in messages:
                sender = message.split(":")[1].strip()
                if sender != self.username:
                    print(message)

    def send_message(self, message):
        timestamp = time.strftime("%H:%M:%S")
        message_data = f"[{timestamp}] {self.username}: {message}".encode('utf-8')

        # Garantir que o nó /chat/messages exista
        self.zk.ensure_path("/chat/messages")
        
        # Armazenar a mensagem no ZooKeeper com um ttl
        self.zk.create("/chat/messages/message-", message_data, ephemeral=True, sequence=True)

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
