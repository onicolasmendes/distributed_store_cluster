from funcoesauxiliares import *


portasla1 = 56799
portasla2 = 56802
PORTAS = [65045,12345,65042]
i = 0
while i < 100:
    porta = random.choice(PORTAS)
    comando = random.choice(["W","R","gugu"])
    addr = random.randint(0, 255)  # Simular um endereço aleatório
    valor = random.randint(0, 100)
    
    # Criar um socket para o cliente
    cliente_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente_socket.connect(('localhost', porta))
        
    # Preparar a requisição (escrita ou leitura)
    requisicao = (comando,({valor}))
    print(f'enviando requisição: {requisicao},para porta: {porta}')


    requisicao = pickle.dumps(requisicao)
    
    enviar_estrutura(cliente_socket,requisicao)    
    resposta = receber_mensagem(cliente_socket)
    print(f"Resposta do servidor na porta {porta}: {resposta}")
        
    cliente_socket.close()
    
    i += 1