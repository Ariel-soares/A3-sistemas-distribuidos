# ------------------
# Cliente Socket TCP
# ------------------


# importando as bibliotecas
import socket;
from time import sleep;

# Função usada para quando o servidor enviar varias mensagens que precisam ser impressas
def imprime_dados():
    while True:
            dados = cliente.recv(1024);
            aux = str(dados.decode("utf-8"));
            if aux=="0":
                break;
            print(f'{aux}');

def confirmContinue(valor):
    print("Deseja consultar outra vez?");
    confimacao=int(input("Sim->1 | Não->2\n"));
    if confimacao==2:
        valor=0;
        cliente.sendall(str(valor).encode("utf-8"));
    elif confimacao==1:
        cliente.sendall(str(valor).encode("utf-8"));
    return valor;

print("Cliente\n");
# definindo ip e porta
HOST = '127.0.0.1';       # Endereco IP do Servidor
PORT = 6000;              # Porta que o Servidor ficará escutando

# criando o socket
cliente = socket.socket(socket.AF_INET,socket.SOCK_STREAM);

# cliente se conectando ao servidor
cliente.connect((HOST,PORT));

x=0;
while x==0:
    print("MENU:");
    print("1 - Vendedor");
    print("2 - Gerente");
    print("3 - Sair");
    codigo = int(input("Escolha uma opção: "));
    
    if codigo==3:
        x=codigo;
        print("Encerrando Client");
        sleep(1);
        cliente.close();
    
    while codigo==1:
        # Codigo 1 do Funcionario
        cliente.sendall(str(codigo).encode("utf-8")); # Envia o codigo para o servidor
        
        print("\nFiliais\n");
        imprime_dados();
        filial = int(input("Em que Filial foi a Venda-> "));
        cliente.sendall(str(filial).encode("utf-8"));

        print("\nFuncionarios da Filial\n");
        imprime_dados();
        vendedor = int(input("Qual o Vendedor-> "));
        cliente.sendall(str(vendedor).encode("utf-8"));

        valorDaVenda=float(input("Qual o Valor da Venda-> "));
        cliente.sendall(str(valorDaVenda).encode("utf-8"));

        mes=int(input("Mês da Venda (Em numeral)-> "));
        cliente.sendall(str(mes).encode("utf-8"));
        
        print("\n\nDeseja Efetuar um novo Registro?");
        auxiliar=int(input("Sim->1 | Não->0\n"));
        if auxiliar==0:
            cliente.sendall(str(auxiliar).encode("utf-8"));
            codigo=auxiliar;
    
    while codigo==2:
        # Codigo 2 do Gerente
        cliente.sendall(str(codigo).encode("utf-8")); # Envia o codigo para o servidor
        print("---GERENTE---");
        print("Gerente, bem vindo! \nO Que o deseja ?");
        print("\n1 - Total de vendas de um Vendedor");
        print("2 - Total de vendas de uma Loja");
        print("3 - Total de Vendas em Determinado Periodo");
        print("4 - Melhor Vendedor");
        print("5 - Melhor Loja");
        print("6 - Sair");
        operacao=int(input("\nEscolha uma opção-> "));
        cliente.sendall(str(operacao).encode("utf-8"));

        if operacao==6:
            codigo=0;
        
        while operacao==1: # Total de Vendas de um Vendedor
            print("\nDe Qual Filial é este Vendedor\n");
            imprime_dados();
            loja=int(input("Selecione-> "));
            cliente.sendall(str(loja).encode("utf-8"));

            print("\nQual Vendedor");
            imprime_dados();
            funcionario=int(input("Selecione-> "));
            cliente.sendall(str(funcionario).encode("utf-8"));

            dados = cliente.recv(1024);
            print(dados.decode("utf-8"));
            print("");

            operacao=confirmContinue(operacao);
        
        while operacao==2: # Total de Vendas de uma Loja
            print("\nDe qual Loja deseja saber o total de Vendas?");
            imprime_dados();
            loja = int(input("Selecione-> "));
            cliente.sendall(str(loja).encode("utf-8"));

            dados = cliente.recv(1024);
            print(dados.decode("utf-8"));
            print("");

            operacao=confirmContinue(operacao);
        
        while operacao==3: # Total de Vendas em Determinado Periodo
            mesInicial=int(input("\nA patir de qual Mês->  "));
            cliente.sendall(str(mesInicial).encode("utf-8"));
            sleep(0.5);
            mesFinal=int(input("\nAté qual Mês->  "));
            cliente.sendall(str(mesFinal).encode("utf-8"));
            
            dados = cliente.recv(1024);
            print(dados.decode("utf-8"));
            print("");

            operacao=confirmContinue(operacao);
        
        while operacao==4:
            dados = cliente.recv(1048576);
            ajudande = dados.decode("utf-8");
            print(f"\n{ajudande}\n");
            operacao=0;

        while operacao==5:
            dados = cliente.recv(1024);
            ajudande = dados.decode("utf-8");
            print(f"\n{ajudande}\n");
            operacao=0;