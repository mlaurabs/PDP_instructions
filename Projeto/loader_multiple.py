#Métodos para leitura do Multiple Welllog
import time as tm
import pandas as pd
import loader as l

def onlyNumbers(row): # verifica se uma string contém apenas números - bool
    numeros = -1
    space = ["\t", "\n"]

    for i in range(len(row)):
        if(row[i] in space): # lendo um espaço
            continue
        if(not (ord(row[i]) >= 48 and  ord(row[i]) <= 57)): # verfica se não é um número
            numeros = 0 
        if(numeros == 0): # contém um carcter que não é um número
            return False
        else: # contém apenas números na string
            return True

#ideia: teria a opção de simplesmente retornar o length da lista com o nome das propriedades
def getWellPropCount(path): # retorna a quantidade de propriedade em um arquivo - int
    # como as colunas sempre aparecem na primeira linha, ela é acessada diretamente
    file = l.read(path)
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

def getWellPropNames(path): # retorna uma lista com o nome das propriedades - array
    file = l.read(path)
    linha = file.readline().rstrip() #tira o \n
    properties = l.getColumns(linha)
    return properties
        
def getNameDateWell(row): # retorna uma lista com o nome e a data de um poço - array
    aux = 0 # contador de aspas
    aspas = ["'", '"']
    name = ""
    date = "" # formatar a data?
    dados = []
    
    #estrutura da linha: "well name" data

    for i in range(len(row)):
        if(row[i] in aspas):
            if(aux != 2):
                aux +=1
        elif(aux == 2): # já leu a data
            if(ord(row[i]) >= 48 and ord(row[i]) <= 57): # verfica se é um número
                date += row[i]
        else:
            if(aux == 1): # ainda está lendo a data
                name += row[i]
        
    dados.append(name)
    dados.append(date)
    return dados

def getWellNames(path): # retorna uma lista com os nomes dos poços de um arquivo - array
    file = l.read(path)
    logunits = -1 
    unidades = "logunits"
    cont  = 1 # contador de linhas
    well_names = []
    for linha in file:
        linha = linha.rstrip() # tira o \n da linha
        if(cont == 2 and not l.empty(linha)): # verifica se o iterador aponta pra linha 2 e não é uma linha vazia
            row = linha.lower()
            if(unidades in row): # verifica se a linha 2 é logunits (opcional nos documentos)
                logunits = 0 # atribui valor zero caso seja logunits
            else: # se não é logunits, lê o nome do poço
                poco_nome = getNameDateWell(linha)  
                well_names.append(poco_nome[0])              
        elif(cont > 2): # se passou da linha 2
            if(logunits == 0): # se o logunits estava na linha 2, ler na linha 3 o nome do poço
                poco_nome = getNameDateWell(linha)  
                well_names.append(poco_nome[0])  
                logunits = -1 # já passou pelo logunits            
            elif(not l.empty(linha)): # se a linha não é vazia
                if(not onlyNumbers(linha)): # se a linha não tiver apenas números
                    poco_nome = getNameDateWell(linha)
                    well_names.append(poco_nome[0])   
        cont += 1
    return well_names

def getWellCount_v1(path):
    wells = getWellNames(path)
    countWells = len(wells)
    return countWells

# alternativa: contabilizar o length da lista de well names
def getWellCount(path): # retorna a quantidade de poços de um arquivo - int
    file = l.read(path)
    logunits = -1 
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
                    if(not l.empty(linha) and not onlyNumbers(linha)):
                        countWells += 1
        cont +=1
    return countWells
  
def organizeData(lista, colunas, n_cols): # organiza os dados de acordo com as propriedades do documento - dictionary
    # lista são os dados de um determindado well
    # colunas são as proriedades listadas no arquivo
    # n_cols é o número de propriedades listadas no arquivo
    data = dict()
    j = 0
    while(j < n_cols): 
        key = colunas[j] # atribui a key do dicionario o nome da coluna/propriedade
        valor = [] 
        for item in lista: # percorre a lista onde cada item é uma linha
            valor.append(item[j]) #pega o valor da linha na posiçao respectiva a coluna
            data[key] = valor # atribui os dados organizados a sua respectiva coluna (key)
        j +=1
    return data

def getWellPropData(path): # retorna uma lista com os dataframes dos poços - array
    colunas = getWellPropNames(path)
    n_cols = getWellPropCount(path)
    well_names = getWellNames(path)
    totalWells = getWellCount(path)
    file = l.read(path)
    i = 0 # contador de poços
    data_per_well = dict() # estrutura do dicionario: {nome do poço: [dados]}
    well = ""
    dados = [] # estrutura da lista: [[linha 0], [linha1], ..., [linha n]]
    wellPropData = [] # estrutura da lista: [dataframe1, dataframe2, ..., dataframen]

    for linha in file:
        linha = linha.rstrip()
        if(well_names[i] in linha): # caso esteja lendo a linha do poço
            if(i > 0): # se o primeiro poço já inciou a leitura
                data_per_well[well] = dados
                dados = []
                well = well_names[i]
                if(i < totalWells-1) and totalWells > 1: # se ainda falta poço para ler
                    i += 1        
            else: # iniciando leitura do primeiro poco
                well = well_names[i]
                if (totalWells > 1):
                    i += 1
        elif(i <= totalWells): # se ainda falta poço para ler
            if(not l.empty(linha) and onlyNumbers(linha)): # verificando se estamos na linha que contém dados
                dados.append(linha.split())
        if(i == totalWells - 1): # se estamos na última linha de dados do último poço
            data_per_well[well] = dados
  
    for key in data_per_well: # reorganiza os dados de cada well de acordo com suas propriedades
        dados = data_per_well.get(key)
        print(dados)
        data_per_well[key] = organizeData(dados, colunas, n_cols)


    for i in range(totalWells): # criando os dataframes
        key = well_names[i]
        table = pd.DataFrame(data_per_well.get(key))
        wellPropData.append(table)

    return wellPropData


lista = getWellPropData("Projeto/arquivos/RFT_LINGUADO.wlg")

file_csv = open("Projeto/dados_em_csv/teste.csv", "a")
for item in lista:
    new_item = item.dropna()
    new_item.to_csv(file_csv, index=False)
    file_csv.write("\n\n")

'''def transformarEmCsv(path):
    lista = getWellPropData(path)
    file_name = l.getFileName(path)
    for item in lista:
        df = pd.DataFrame(item)
        print(df)
        df.to_csv(file_name + '.csv') 

transformarEmCsv('Projeto/arquivos/multiplewelllogwith2d.wlg')
'''
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

"""
- funções não utilizadas:

def replace(row, a, b):
    space = [a, b]
    dados = list(row)
    for i in range(len(dados)):
        if(dados[i] in space):
            dados[i] = " "
    return "".join(dados)
  

"""