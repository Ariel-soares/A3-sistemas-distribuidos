# -------------------
# Servidor Socket UDP
# -------------------

# importando as bibliotecas
import socket;
from time import sleep;


# Definindo Funções usadas

# Função usada para enviar dados de listas que precisam ser impressos
def mostra_lista(lista, enderecoCliente): 
    for indice, nome in enumerate(lista):
        aju = str(indice+1) +" - "+ str(nome);
        servidor.sendto(aju.encode("utf-8"),enderecoCliente);
        sleep(0.5);
    servidor.sendto("0".encode("utf-8"), enderecoCliente);


# Função para Determinar a Filial e Vendedor Desejados
def selecFilialEVendedor(listaDeFiliais,f1,f2,f3,enderecoCliente):
    # Determinando a filial Desejada
    mostra_lista(listaDeFiliais, enderecoCliente);
    dados, enderecoCliente = servidor.recvfrom(9000);
    auxi = (int(dados.decode("utf-8")))-1;
    # Determinando Funcionario Desejado
    filial=str();
    pessoa=str();
    if auxi == 0:
        filial='SALVADOR';
        mostra_lista(f1, enderecoCliente);
        dados, enderecoCliente = servidor.recvfrom(9000);
        pessoa = salvador[(int(dados.decode("utf-8")))-1];

    elif auxi == 1:
        filial='ITAPARICA';
        mostra_lista(f2, enderecoCliente);
        dados, enderecoCliente = servidor.recvfrom(9000);
        pessoa = itaparica[(int(dados.decode("utf-8")))-1];

    elif auxi==2:
        filial='ILHEUS';
        mostra_lista(f3, enderecoCliente);
        dados, enderecoCliente = servidor.recvfrom(9000);
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

# definindo ip e porta
HOST = '127.0.0.1';       # Endereco IP do Servidor
PORT = 9000;              # Porta que o Servidor ficará escutando

# criando o socket e associando ao endereço e porta
servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
servidor.bind((HOST,PORT));

# conversando com o cliente
while (True):
    # recebendo dados
    dados, enderecoCliente = servidor.recvfrom(9000);
    codigo = int(dados.decode("utf-8"));
    
    # Codigo 1 --> Funcionario
    while codigo==1:
        print("\nRegistrando Venda\n");

        # Determinando a Filial e Vendedor Desejados
        filial,pessoa = selecFilialEVendedor(filiais,salvador,itaparica,ilheus,enderecoCliente);

        dados, enderecoCliente = servidor.recvfrom(9000);
        valorDaVenda = float(dados.decode("utf-8"));

        dados, enderecoCliente = servidor.recvfrom(9000);
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
        dados, enderecoCliente = servidor.recvfrom(9000);
        operacao = int(dados.decode("utf-8"));

        if operacao == 6:
            codigo=0;

        while operacao==1:
            print("1 - Total de vendas de um Vendedor");
            store,funcionario = selecFilialEVendedor(filiais,salvador,itaparica,ilheus,enderecoCliente);
            totalFuncionario=float(0);
            for regis in vendas:
                if regis['LOJA']==store:
                    if regis['VENDEDOR'] == funcionario:
                        totalFuncionario = totalFuncionario + regis['PRECO'];
            auxil="Total do Funcionario "+funcionario+" da loja "+store+" -> R$"+str(totalFuncionario);
            servidor.sendto(auxil.encode("utf-8"), enderecoCliente);
            print(auxil);

            dados, enderecoCliente = servidor.recvfrom(9000);
            operacao = int(dados.decode("utf-8"));

        while operacao==2:
            print("2 - Total de Vendas De uma Loja");
            mostra_lista(filiais, enderecoCliente);
            dados, enderecoCliente = servidor.recvfrom(9000);
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
            servidor.sendto(auxil.encode("utf-8"), enderecoCliente);
            print(auxil);

            dados, enderecoCliente = servidor.recvfrom(9000);
            operacao = int(dados.decode("utf-8"));
        
        while operacao==3:
            print("\n3 - Total de Vendas em Determinado Periodo\n");
            totalPorPeriodo=float(0);

            dados, enderecoCliente = servidor.recvfrom(9000);
            mesInicial = int(dados.decode("utf-8"));
            dados, enderecoCliente = servidor.recvfrom(9000);
            mesFinal = int(dados.decode("utf-8"));

            for regis in vendas:
                if regis['MES'] >= mesInicial:
                    if regis['MES'] <=mesFinal:
                        totalPorPeriodo = totalPorPeriodo + regis['PRECO'];
            
            auxil="Total de Vendas do Mês "+str(mesInicial)+" até o Mês "+str(mesFinal)+" -> R$"+str(totalPorPeriodo);
            servidor.sendto(auxil.encode("utf-8"), enderecoCliente);
            print(auxil);

            dados, enderecoCliente = servidor.recvfrom(9000);
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
            servidor.sendto(auxil.encode("utf-8"), enderecoCliente);
            print(f"{auxil}\n");
            
        if operacao==5:
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
            servidor.sendto(auxil.encode("utf-8"), enderecoCliente);
            print(f"{auxil}\n");
