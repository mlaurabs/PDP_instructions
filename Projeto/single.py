#Métodos para leitura do Single Welllog
import pandas as pd

# logunits deve ser incluído no DateFrame?
# o wellcount e wellnames é necessário? pq o single contém apenas 1 poço por arquivo


def read(path):
    file = open(path, "r")
    return file

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

def empty(row): #verifica de uma linha é vazia
    letras = -1
    numeros = -1
    for i in range(len(row)):
        if(ord(row[i]) >= 48 and  ord(row[i]) <= 57): # verfica se é um número
            numeros = 0
        if(ord(row[i]) >= 65 and  ord(row[i]) <= 90): # verfica se é uma letra
            letras = 0
        elif(ord(row[i]) >= 97 and  ord(row[i]) <= 122):
            letras = 0
    if(letras == 0 or numeros == 0):
        return False
    else:
        return True

def getColumns(linha): # identifica e retorna o nome das colunas
    properties = []
    aux = 0 # conta as aspas
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

def getPropNames(path):
    # TThe first line is the well name and an optional date and/or null value. 
    # The next line may optionally contain log units which must be input using the keyword LOGUNITS
    # The next line contains the log names (column headings). 
    
    file = read(path)
    cont = 1 # contador de linhas
    logunits = -1 # variavel auxiliar para identificar se já a leitura dos dados dos poços já se inciou
    unidades = "logunits"
    propNames = []

    for linha in file:
        linha = linha.rstrip() + " " #tira o \n e adiciona um espaço ao final
        if(cont == 2 and not empty(linha)):
            row = linha.lower()
            if(unidades not in row): # verifica se a linha 2 é logunits (opcional nos documentos)
                propNames = getColumns(linha)
                break
        elif(cont > 2):
            if(not empty(linha)):
                propNames = getColumns(linha)
                break
        cont +=1
    
    return propNames

def getWellPropCount(path):
    propNames = getPropNames(path)
    return len(propNames)

def getWellName(path):
    file = read(path)
    linha = file.readline().rstrip() # tira o "\n"
    dados = linha.split() 
    return dados[0]

def organizeData(lista, colunas, n_cols): # organiza os dados de acordo com as propriedades do documento
    # lista são os dados de um determindado well
    # colunas são as proriedades listadas no arquivo
    # n_cols é o número de propriedades listadas no arquivo
    data = dict()
    j = 0
    while(j < n_cols): # para cada coluna
        key = colunas[j] # atribui key do dicionario o nome da coluna
        valor = [] # cria uma lista para reorganizar os dados de acordo com sua coluna
        for item in lista: # percorre a lista (cada item é uma linha)
            valor.append(item[j]) #pega o valor da linha respectivo a coluna
            data[key] = valor # atribui os dados organizados a sua respectiva coluna
        j +=1
    return data

def getWellPropData(path):
    file = read(path)
    colunas = getPropNames(path)
    n_cols = getWellPropCount(path)
    well_name = getWellName(path)
    dados = []

    for linha in file:
        linha = linha.rstrip() # tira o "\n"
        if(not empty(linha) and onlyNumbers(linha)):
            dados.append(linha.split())

    prop_data = dict()
    prop_data[well_name] = pd.DataFrame(organizeData(dados, colunas, n_cols))

    return prop_data[well_name]

# wellproptype - TO DO    

# print(getWellName("arquivos/2_singlewelllogwithnullvalue.log"))
# getWellPropData("arquivos/2_singlewelllogwithnullvalue.log")