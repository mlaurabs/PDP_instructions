#Métodos para leitura do Mutiple Welllog
import time as tm
import pandas as pd

def read(path):
    file = open(path, "r")
    return file

def getWellPropCount(path): # retorna a quantidade de propriedade em um arquivo
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
    
def getPropNames(path): # retorna uma lista com o nome das propriedades
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
        
def getNameDateWell(row): # retorna o nome e a data de um poço
    # - the well name must be enclosed in single or double quotes

    aux = 0 # contador de aspas
    aspas = ["'", '"']
    name = ""
    date = "" # formato a data?
    dados = []
    
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

def getWellNames(path): # retorna uma lista com os nomes dos poços de um arquivo
    """
    info:
    - the well name must be enclosed in single or double quotes
    - logunits are optional
    - logunits when are included on the file, they are located at the second line
    """
    file = read(path)
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
                if(not onlyNumbers(linha)): # se a linha não tiver apenas números
                    poco_nome = getNameDateWell(linha)
                    well_names.append(poco_nome[0])   
        cont += 1
    return well_names

def getWellCount_v1(path):
    wells = getWellNames(path)
    countWells = len(wells)
    return countWells

def getWellCount(path): # retorna a quantidade de poços de um arquivo
    file = read(path)
    logunits = -1 # variavel auxiliar para identificar se já a leitura dos dados dos poços já se inciou
    unidades = "logunits"
    cont  = 1 # contador de linhas
    countWells = 0

    for linha in file:
        if(cont == 2):
            row = linha.lower()
            if(unidades in row): # verifica se a linha 2 é logunits (opcional nos documentos)
                logunits = 0 # atribui valor zero caso seja logunits
        else:
            if(cont > 2):
                if(logunits == 0):
                    logunits = -1
                    countWells +=1
                else:
                    if(not empty(linha) and not onlyNumbers(linha)):
                        countWells += 1
        cont +=1
    return countWells

def replace(row, a, b):
    space = [a, b]
    dados = list(row)
    for i in range(len(dados)):
        if(dados[i] in space):
            dados[i] = " "
    return "".join(dados)
    
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
    colunas = getPropNames(path)
    n_cols = getWellPropCount(path)
    well_names = getWellNames(path)
    totalWells = getWellCount(path)
    file = read(path)
    aux = 0
    i = 0 # contador de pocos
    data_per_well = dict()
    well = ""
    dados = []
    wellPropData = []

    for linha in file:
        linha = linha.rstrip()
        if(well_names[i] in linha):
            if(aux > 0):
                data_per_well[well] = dados
                dados = []
                well = well_names[i]
                if(i < totalWells-1):
                    aux += 1
                    i += 1        
            else:
                well = well_names[i]
                aux += 1
                i += 1
        elif(aux <= totalWells):
            if(not empty(linha) and onlyNumbers(linha)): # verificando se estamos na linha que contém dados
                linha = replace(linha,  "\n", "\t")
                dados.append(linha.split())
        if(i == totalWells - 1):
            data_per_well[well] = dados
  
    for key in data_per_well: # reorganiza os dados de cada well de acordo com suas propriedades
        dados = data_per_well.get(key)
        data_per_well[key] = organizeData(dados, colunas, n_cols)

    for i in range(totalWells):
        key = well_names[i]
        table = pd.DataFrame(data_per_well.get(key))
        wellPropData.append(table)

    return wellPropData

# wellproptype - TO DO    

"""
- algoritmo de tempo de execucao 
start_time = tm.time()
lista = getWellPropData("arquivos/RFT_LINGUADO.wlg")
well = getWellNames("arquivos/RFT_LINGUADO.wlg")
for i in range(len(lista)):
        print("\n")
        print(well[i])
        print(lista[i])
end_time = tm.time()
execution_time = end_time-start_time

print(f"\n\nExecution Time: {execution_time}")
"""
