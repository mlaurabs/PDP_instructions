import pandas as pd
from single import countProperties, getProperties, read


 # ALTERAR O ARQUIVO!

def organiza(arq, colunas):

    file = read(arq)
    l=[]                            #lista onde vão ficar todos valores de cada coluna 
    dWlg = dict()                   
    nomeEdata = []                  #lista que pega os nomes e as datas
    num = 0                         #contagem de valores que tem em um unico poço
    qtd = []                        #lista com as contagens acima

    for linha in file:
        linha = linha.strip().split()
        if linha != []:             #verifica se tem espaços vazios dentro do arquivo
            if linha[0][0] == '"' or linha[0][0] == "'":   #verifica se a linha é o nome e a data
                nomeEdata.append(linha)
                qtd.append(num)
                num = 0
            else:
                if len(linha) == colunas:                     #verifica se a quantidade de indices é igual as colunas
                    l.append(linha)
                num += 1
    qtd.pop(0)                                        #remove o numero 0
    qtd.append(num)


    j = 0
    for n, item in enumerate(qtd):                       #começa a organizar as listas
        divisor = []                                     
        for index in range(item):
            divisor.append(l[j])                      
            j += 1
        nome = nomeEdata[n][0] + "__" + nomeEdata[n][1]  #separa o nome e a data com um delimitador e adiciona
        dWlg[nome] = divisor                             #na chave do dicionario



    for k, v in dWlg.items():                            #for só pra printar o dicionario
        print(k, v)
        print()




arq = "Projeto/RFT_mod_netto.wlg"

colu = countProperties(arq)
getProperties(arq)
organiza(arq, colu)






# ----------------------------------------------------------IGNORAR----------------------------------------------------------

    # x = 0
    # b = 0
    # for j in range(cont):
    #     a = []
    #     for index, itens in enumerate(l):
    #         if index == x:
    #             nome = nomeEdata[0][0]
    #             a.append(nome)
    #             x = x + qtd[b]
    #             b += 1
    #         a.append(itens[j])

        
    #     dWlg[j] = a
    


    # myvar = pd.DataFrame(dWlg)
    # print(myvar)

    # for k, v in dWlg.items():
    #     print(k)
    #     myvar = pd.DataFrame(dWlg[k])
    #     print(myvar)