# ------------------
# Cliente Socket UDP
# ------------------


# importando as bibliotecas
import socket;
from time import sleep;

# Função usada para quando o servidor enviar varias mensagens que precisam ser impressas
def imprime_dados():
    while True:
            dados, endereco = cliente.recvfrom(9000);
            aux = str(dados.decode("utf-8"));
            if aux=="0":
                break;
            print(f'{aux}');

def confirmContinue(valor,enderecoServidor):
    print("Deseja consultar outra vez?");
    confimacao=int(input("Sim->1 | Não->2\n"));
    if confimacao==2:
        valor=0;
        cliente.sendto(str(valor).encode("utf-8"), enderecoServidor);
    elif confimacao==1:
        cliente.sendto(str(valor).encode("utf-8"), enderecoServidor);
    return valor;

print("Cliente\n");

# definindo ip e porta
HOST = '127.0.0.1';       # Endereco IP do Servidor
PORT = 9000;              # Porta que o Servidor ficará escutando

# criando o socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);

enderecoServidor = (HOST, PORT);

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
        # Envia o codigo para o servidor
        cliente.sendto(str(codigo).encode("utf-8"), enderecoServidor); 
        
        print("\nFiliais\n");
        imprime_dados();
        filial = int(input("Em que Filial foi a Venda-> "));
        cliente.sendto(str(filial).encode("utf-8"), enderecoServidor);

        print("\nFuncionarios da Filial\n");
        imprime_dados();
        vendedor = int(input("Qual o Vendedor-> "));
        cliente.sendto(str(vendedor).encode("utf-8"), enderecoServidor);

        valorDaVenda=float(input("Qual o Valor da Venda-> "));
        cliente.sendto(str(valorDaVenda).encode("utf-8"), enderecoServidor);

        mes=int(input("Mês da Venda (Em numeral)-> "));
        cliente.sendto(str(mes).encode("utf-8"), enderecoServidor);
        
        print("\n\nDeseja Efetuar um novo Registro?");
        auxiliar=int(input("Sim->1 | Não->0\n"));
        if auxiliar==0:
            cliente.sendto(str(auxiliar).encode("utf-8"), enderecoServidor);
            codigo=auxiliar;
    
    while codigo==2:
        # Codigo 2 do Gerente
        cliente.sendto(str(codigo).encode("utf-8"), enderecoServidor); # Envia o codigo para o servidor
        print("---GERENTE---");
        print("Gerente, bem vindo! \nO Que o deseja ?");
        print("\n1 - Total de vendas de um Vendedor");
        print("2 - Total de vendas de uma Loja");
        print("3 - Total de Vendas em Determinado Periodo");
        print("4 - Melhor Vendedor");
        print("5 - Melhor Loja");
        print("6 - Sair");
        operacao=int(input("\nEscolha uma opção-> "));
        cliente.sendto(str(operacao).encode("utf-8"), enderecoServidor);

        if operacao==6:
            codigo=0;
        
        while operacao==1: # Total de Vendas de um Vendedor
            print("\nDe Qual Filial é este Vendedor\n");
            imprime_dados();
            loja=int(input("Selecione-> "));
            cliente.sendto(str(loja).encode("utf-8"), enderecoServidor);

            print("\nQual Vendedor");
            imprime_dados();
            funcionario=int(input("Selecione-> "));
            cliente.sendto(str(funcionario).encode("utf-8"), enderecoServidor);

            dados, endereco = cliente.recvfrom(9000);
            print(dados.decode("utf-8"));
            print("");

            operacao=confirmContinue(operacao, enderecoServidor);
        
        while operacao==2: # Total de Vendas de uma Loja
            print("\nDe qual Loja deseja saber o total de Vendas?");
            imprime_dados();
            loja = int(input("Selecione-> "));
            cliente.sendto(str(loja).encode("utf-8"), enderecoServidor);

            dados, endereco = cliente.recvfrom(9000);
            print(dados.decode("utf-8"));
            print("");

            operacao=confirmContinue(operacao, enderecoServidor);
        
        while operacao==3: # Total de Vendas em Determinado Periodo
            mesInicial=int(input("\nA patir de qual Mês->  "));
            cliente.sendto(str(mesInicial).encode("utf-8"), enderecoServidor);
            sleep(0.5);
            mesFinal=int(input("\nAté qual Mês->  "));
            cliente.sendto(str(mesFinal).encode("utf-8"), enderecoServidor);
            
            dados, endereco = cliente.recvfrom(9000);
            print(dados.decode("utf-8"));
            print("");

            operacao=confirmContinue(operacao, enderecoServidor);
        
        while operacao==4:
            dados, endereco = cliente.recvfrom(9000);
            ajudande = dados.decode("utf-8");
            print(f"\n{ajudande}\n");
            operacao=0;

        while operacao==5:
            dados, endereco = cliente.recvfrom(9000);
            ajudande = dados.decode("utf-8");
            print(f"\n{ajudande}\n");
            operacao=0;
