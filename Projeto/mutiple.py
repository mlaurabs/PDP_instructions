#Métodos para leitura do Mutiple Welllog
import numpy as np

def read(path):
    file = open(path, "r")
    return file

def countProperties(path): # retorna a quantidade de propriedade em um arquivo
    # como as colunas sempre aparecem na primeira linha, pegamos direto ela
    file = read(path)
    linha = file.readline().rstrip() + " " #tira o \n e adiciona um espaço ao final
    coluna = 0
    aux = 0 # conta as aspas
    space = [" ", "\t"]
    for i in range(len(linha)):
        if(linha[i] in space and linha[i-1] != " "): #verifica se já passamos por uma coluna (estamos entre colunas, ou seja, em um "espaço")
            if(aux == 0 or aux == 2): # se acabou de ler uma coluna com ou sem aspas
                coluna +=1
        elif(linha[i] == "'"): # começa a ler uma coluna entre aspas
            if(aux == 2): # se leu a última aspa
                aux = 0
            aux +=1
    return coluna
    
def getProperties(path): # retorna uma lista com o nome das propriedades
    file = read(path)
    linha = file.readline().rstrip() + " " #tira o \n e adiciona um espaço ao final
    properties = []
    aux = 0
    col = ""
    space = [" ", "\t"]
    for i in range(len(linha)):
        if(linha[i] in space and linha[i-1] != " "): #verifica se já passamos por uma coluna (estamos entre colunas, ou seja, em um "espaço")
            if(aux == 0 or aux == 2): # se acabou de ler uma coluna com ou sem aspas
                properties.append(col.strip())
                col = ""
            else:
                col += " "
        elif(linha[i] == "'"): # começa a ler uma coluna entre aspas
            if(aux == 2): # se leu a última aspa
                aux = 0
            aux +=1
        else:
            col += linha[i]
    return properties


def onlyNumbers(row):
    numeros = -1
    space = ["\t", "\n"]

    for i in range(len(row)):
        if(row[i] in space):
            continue
        if(not (ord(row[i]) >= 48 and  ord(row[i]) <= 57)): # verfica se é um número
            numeros = 0
        if(numeros == 0):
            return False
        else:
            return True

def empty(row):
    letras = -1
    numeros = -1
    for i in range(len(row)):
        if(ord(row[i]) >= 48 and  ord(row[i]) <= 57): # verfica se é um número
            numeros = 0
            print("achei um numero")
        if(ord(row[i]) >= 65 and  ord(row[i]) <= 90): # verfica se é uma letra
            letras = 0
            print("achei uma letra")
        elif(ord(row[i]) >= 97 and  ord(row[i]) <= 122):
            letras = 0
            print("achei uma letra")
    if(letras == 0 or numeros == 0):
        return False
    else:
        return True

        
def getNameDateWell(row):
    # - the well name must be enclosed in single or double quotes

    aux = 0 # contador de aspas
    aspas = ["'", '"']
    name = ""
    date = "" # formato a data?
    dados = []
    print(f"Essa é a row {row}")
    for i in range(len(row)):
        if(row[i] in aspas):
            if(aux != 2):
                aux +=1
        elif(aux == 2):
            if(ord(row[i]) >= 48 and ord(row[i]) <= 57): # verfica se é um número
                date += row[i]
        else:
            if(aux == 1):
                name += row[i]
        
    dados.append(name)
    dados.append(date)
    return dados

def getWellNames(path):
    """
    info:
    - the well name must be enclosed in single or double quotes
    - logunits are optional
    - logunits when are included on the file, they are located at the second line
    """

    file = read(path)
    #linha = file.readline().rstrip()
    logunits = -1 # variavel auxiliar para identificar se já a leitura dos dados dos poços já se inciou
    unidades = "logunits"
    cont  = 1 # contador de linhas
    well_names = []
    for linha in file:
        linha = linha.rstrip() # tira o \n da linha
        if(cont == 2 and not empty(linha)): # verifica se o iterador aponta pra linha 2 e não é uma linha vazia
            row = linha.lower()
            if(unidades in row): # verifica se a linha 2 é logunits (opcional nos documentos)
                logunits = 0 # atribui valor zero caso seja logunits
            else: # se não logunits lê o nome do poço
                poco_nome = getNameDateWell(linha)  
                well_names.append(poco_nome[0])              
        elif(cont > 2): # se passou da linha 2
            if(logunits == 0): # se o logunits estava na linha 2, ler na linha 3 o nome do poço
                poco_nome = getNameDateWell(linha)  
                well_names.append(poco_nome[0])  
                logunits = -1 # já passou pelo logunits            
            elif(not empty(linha)): # se a linha não foi vazia
                #lista = linha.split(" ")
                if(not onlyNumbers(linha)): # se a linha não tiver apenas números
                    poco_nome = getNameDateWell(linha)  
                    print(poco_nome)
                    well_names.append(poco_nome[0])   
        cont += 1
    return well_names
    

"""def organize(path, columns): # organiza os dados de cada poço em un dicionario

    file = read(path)
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
        print()"""




#arq = "arquivos\RFT_mod_netto.wlg"

#colu = countProperties(arq)
#getProperties(arq)
#organiza(arq, colu)
#print(getNameDateWell("'RCB-0001' 19820407"))
#print(readingData("1926.0 159.9"))
print(getWellNames("arquivos/multiplewelllogwith2d.wlg"))
#print(empty("\t\n alvcmvbh9087645"))
#print(onlyNumbers("\t\n86947746752"))





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