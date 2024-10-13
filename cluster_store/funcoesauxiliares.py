import time
import pickle
import socket
import threading
import random
import pickle

def enviar_mensagem(socket,mensagem):
    socket.send(mensagem.encode('utf-8'))
    confirmacao_de_chegada = socket.recv(2048).decode('utf-8')
    if(confirmacao_de_chegada == "confirmado"):
        return
    else:
        print("algo de errado esta acontecendo")
        print(f"esperava \"confirmado\" entretanto foi recebido {confirmacao_de_chegada}")
        return

def receber_mensagem(socket):
    dado = socket.recv(2048).decode('utf-8')
    socket.send("confirmado".encode('utf-8'))
    return dado

def enviar_estrutura(socket,dado):
    socket.send(dado)
    confirmacao_de_chegada = socket.recv(2048).decode('utf-8')
    if(confirmacao_de_chegada == "confirmado"):
        return
    else:
        print("algo de errado esta acontecendo")
        print(f"esperava \"confirmado\" entretanto foi recebido {confirmacao_de_chegada}")
        return

def receber_estrutura(socket):
    dado = socket.recv(8192*2)
    
    socket.send("confirmado".encode('utf-8'))
    return dado

def connect_primary_node(sock,port, ip,retry_interval=5):
    while True:
        try:
            # Tenta conectar ao endereço IP e porta fornecidos
            sock.connect((ip, port))
            print(f"Conectado ao primarca {ip} na porta {port}")
            return 0
        except Exception as e:
            print(f"Erro ao conectar ao endereço {ip} na porta {port}: {e}")
            print(f"Tentando novamente em {retry_interval} segundos...")
            time.sleep(retry_interval)  # Aguarda antes de tentar novamente

def primary_connection(sock,registro,flag):
    try:    
        while True:  
            print("mensagem thread: esperando dados")
            dados = sock.recv(2048)
            print("mensagem thread: ordem de atualização recebida")
            dados = pickle.loads(dados)
            print(dados)
            #atualizar registro
            atualiza_registro(registro,dados)
            print("mensagem thread: notificando primarca")
            sock.send("Atualizado".encode('utf-8'))
            print("mensagem thread: primarca notificado")
            flag.set()

    except Exception as e:
        print(f"Erro: {e}")

def backup_connection(connection,registro,connections_list,evento,flag_communicação):
    try:
        print(f'')    
        while True:
            print("mensagem thread: esperando dados")
            dados = connection.recv(2048)
           
            if(dados != "Atualizado".encode('utf-8')):
                print("mensagem thread: novo elemento a ser atualizado")
                dados = pickle.loads(dados)
                print(f'mensagem thread: {dados}')
                # atualizar registro
                atualiza_registro(registro,dados)
                print("mensagem thread: elemento atualizado")
                print(f'mensagem thread: registro atual: {dados}')
                dados = pickle.dumps(dados)
                for conn in connections_list:
                        #envia os dados para todos os nós
                        print("mensagem thread: enviando requisiçoes de atualizaçao")
                        conn.send(dados)
                        
                connection.recv(2048).decode('utf-8')
                print(f"mensagem thread: atualziação recebida")

                flag_communicação.wait()
                print("mensagem thread: todos os nós atualizados")
                flag_communicação.clear()
            else:
                print("mensagem thread: mensagem de confirmação recebida")
                flag_communicação.set()
                evento.set()
    except Exception as e:
        print(f"Erro: {e}")


def buscar(dado, lista):
    if dado not in lista:
        return False
    else:
        return True

def atualiza_registro(registro,mensagem):
    if mensagem in registro:
        return True
    else:
        registro.append(mensagem)
        return True