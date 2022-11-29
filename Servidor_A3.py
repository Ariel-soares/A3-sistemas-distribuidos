# -------------------
# Servidor Socket TCP
# -------------------

# importando as bibliotecas
import socket;
from time import sleep;


# Definindo Funções usadas

# Função usada para enviar dados de listas que precisam ser impressos
def mostra_lista(lista): 
    for indice, nome in enumerate(lista):
        aju = str(indice+1) +" - "+ str(nome);
        conexaoCliente.sendall(aju.encode("utf-8"));
        sleep(0.5);
    conexaoCliente.sendall("0".encode("utf-8"));


# Função para Determinar a Filial e Vendedor Desejados
def selecFilialEVendedor(listaDeFiliais,f1,f2,f3):
    # Determinando a filial Desejada
    mostra_lista(listaDeFiliais);
    dados = conexaoCliente.recv(2);
    auxi = (int(dados.decode("utf-8")))-1;
    # Determinando Funcionario Desejado
    filial=str();
    pessoa=str();
    if auxi == 0:
        filial='SALVADOR';
        mostra_lista(f1);
        dados = conexaoCliente.recv(1024);
        pessoa = salvador[(int(dados.decode("utf-8")))-1];

    elif auxi == 1:
        filial='ITAPARICA';
        mostra_lista(f2);
        dados = conexaoCliente.recv(1024);
        pessoa = itaparica[(int(dados.decode("utf-8")))-1];

    elif auxi==2:
        filial='ILHEUS';
        mostra_lista(f3);
        dados = conexaoCliente.recv(1024);
        pessoa = ilheus[(int(dados.decode("utf-8")))-1];
    return filial,pessoa;
        

# Declarando Filiais E FUNCIONARIOS que trabalham nelas
filiais=["SALVADOR","ITAPARICA","ILHEUS"];

salvador=["JOAO","ARIEL","LUCAS"];
itaparica=["MARIO","GABRIEL","JORGE"];
ilheus=["MIGUEL","JOSE","LEANDRO"];


vendas=list(); # Lista usada pra registrar as vendas
registro=dict(); # Dicionario usado para resgistrar as vendas

print("Eu sou o SERVIDOR!");
while (True):
    # definindo ip e porta
    HOST = '127.0.0.1';       # Endereco IP do Servidor
    PORT = 6000;              # Porta que o Servidor ficará escutando

    # criando o socket e associando ao endereço e porta
    servidor = socket.socket(socket.AF_INET,socket.SOCK_STREAM);
    servidor.bind((HOST,PORT));


    # servidor escutando (aguardando cliente)
    servidor.listen();
    print("Aguardando Conexão...");

    # cliente conectou - recuperando informações do cliente
    conexaoCliente, enderecoCliente = servidor.accept();
    print(f"Cliente {enderecoCliente} conectou.");

    # conversando com o cliente
    while (True):
        # recebendo dados
        dados = conexaoCliente.recv(1024);
        codigo = int(dados.decode("utf-8"));
        
        # testando dados enviados
        if (not dados):
            # encerrando conexão e saindo do loop
            print ("Encerrando a conexão...");
            sleep(3);
            conexaoCliente.close();
            break;
        
        # Codigo 1 --> Funcionario
        while codigo==1:
            print("\nRegistrando Venda\n");

            # Determinando a Filial e Vendedor Desejados
            filial,pessoa = selecFilialEVendedor(filiais,salvador,itaparica,ilheus);

            dados = conexaoCliente.recv(1024);
            valorDaVenda = float(dados.decode("utf-8"));

            dados = conexaoCliente.recv(1024);
            mesDaVenda = int(dados.decode("utf-8"));

            print(f"Filial selecionada => {filial}");
            print(f"Vendedor Selecionado => {pessoa}");
            print(f"Valor da Venda {valorDaVenda}");
            print(f"Mês da Venda-> {mesDaVenda}");
            print("\n");
            registro.clear;
            registro['LOJA'] = filial;
            registro['VENDEDOR'] = pessoa;
            registro['PRECO'] = valorDaVenda;
            registro['MES'] = mesDaVenda;
            vendas.append(registro.copy());
            codigo=0;

        # Codigo 2 --> Gerente
        while codigo==2:
            dados = conexaoCliente.recv(1024);
            operacao = int(dados.decode("utf-8"));
            if operacao == 6:
                codigo=0;

            while operacao==1:
                print("1 - Total de vendas de um Vendedor");
                store,funcionario = selecFilialEVendedor(filiais,salvador,itaparica,ilheus);
                totalFuncionario=float(0);
                for regis in vendas:
                    if regis['LOJA']==store:
                        if regis['VENDEDOR'] == funcionario:
                            totalFuncionario = totalFuncionario + regis['PRECO'];
                auxil="Total do Funcionario "+funcionario+" da loja "+store+" -> R$"+str(totalFuncionario);
                conexaoCliente.sendall(auxil.encode("utf-8"));
                print(auxil);

                dados = conexaoCliente.recv(1024);
                operacao = int(dados.decode("utf-8"));

            while operacao==2:
                print("2 - Total de Vendas De uma Loja");
                mostra_lista(filiais);
                dados = conexaoCliente.recv(1024);
                loja = int(dados.decode("utf-8"));
                totalLoja=float(0);
                if loja==1:
                    aju='SALVADOR';
                    for regis in vendas:
                        if regis['LOJA']==aju:
                            totalLoja = totalLoja + regis['PRECO'];
                if loja==2:
                    aju='ITAPARICA';
                    for regis in vendas:
                        if regis['LOJA']==aju:
                            totalLoja = totalLoja + regis['PRECO'];
                if loja==3:
                    aju='ILHEUS';
                    for regis in vendas:
                        if regis['LOJA']==aju:
                            totalLoja = totalLoja + regis['PRECO'];
                
                auxil="Total da Loja "+aju+" -> R$"+str(totalLoja);
                conexaoCliente.sendall(auxil.encode("utf-8"));
                print(auxil);

                dados = conexaoCliente.recv(1024);
                operacao = int(dados.decode("utf-8"));
            
            while operacao==3:
                print("\n3 - Total de Vendas em Determinado Periodo\n");
                totalPorPeriodo=float(0);

                dados = conexaoCliente.recv(1024);
                mesInicial = int(dados.decode("utf-8"));
                dados = conexaoCliente.recv(1024);
                mesFinal = int(dados.decode("utf-8"));

                for regis in vendas:
                    if regis['MES'] >= mesInicial:
                        if regis['MES'] <=mesFinal:
                            totalPorPeriodo = totalPorPeriodo + regis['PRECO'];
                
                auxil="Total de Vendas do Mês "+str(mesInicial)+" até o Mês "+str(mesFinal)+" -> R$"+str(totalPorPeriodo);
                conexaoCliente.sendall(auxil.encode("utf-8"));
                print(auxil);

                dados = conexaoCliente.recv(1024);
                operacao = int(dados.decode("utf-8"));

            if operacao == 4:
                print("\n4 - Melhor vendedor\n");
                nomes = list();
                nomes=salvador+itaparica+ilheus;
                melhorVendedor=str();
                maiorVendedor=float(-1);
                for indice, nome in enumerate(nomes):
                    comparaPreco=float(0);
                    for regis in vendas:
                        if regis['VENDEDOR']==nome:
                            comparaPreco = comparaPreco + regis['PRECO'];
                    if comparaPreco>maiorVendedor:
                        melhorVendedor = nome;
                        maiorVendedor = comparaPreco;
                    elif comparaPreco==maiorVendedor:
                        melhorVendedor = melhorVendedor +" E "+ nome;

                auxil="Melhor VENDEDOR é "+melhorVendedor+", com um total de vendas de "+str(maiorVendedor);
                conexaoCliente.sendall(auxil.encode("utf-8"));
                print(f"{auxil}\n");
                
            while operacao==5:
                print("\n4 - Melhor Loja\n");
                melhorLoja=str();
                maiorLoja=float(-1);
                for indice, nome in enumerate(filiais):
                    comparaPreco=float(0);
                    for regis in vendas:
                        if regis['LOJA']==nome:
                            comparaPreco = comparaPreco + regis['PRECO'];
                    if comparaPreco>maiorLoja:
                        melhorLoja = nome;
                        maiorLoja = comparaPreco;
                    elif comparaPreco==maiorLoja:
                        melhorLoja = melhorLoja +" E "+ nome;
                        
                auxil="Melhor Loja é "+melhorLoja+", com um total de vendas de "+str(maiorLoja);
                conexaoCliente.sendall(auxil.encode("utf-8"));
                print(f"{auxil}\n");
                operacao=0;