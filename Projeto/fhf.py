#Métodos para leitura do FHF
# linhas que começam "*" são comentários

def read(path):
    file = open(path, "r")
    return file

def onlyNumbers(row): # verifica se uma string contém apenas números - bool
    numeros = -1
    space = ["\t", "\n", " "]
    complex_n = [ "e", "T"]

    for i in range(len(row)):
        if(row[i] in space or row[i] in complex_n):
            continue
        if(not (ord(row[i]) >= 48 and  ord(row[i]) <= 57 )): # verfica se é um número
            numeros = 0
        if(numeros == 0):
            return False
        else:
            return True

def empty(row): #verifica se uma linha é vazia - bool
    # uma linha vazia na extensão .wlg é aquela que não contém letras ou números
    letras = -1
    numeros = -1
    for i in range(len(row)):
        if(ord(row[i]) >= 48 and  ord(row[i]) <= 57): # verfica se é um número
            numeros = 0
        if(ord(row[i]) >= 65 and  ord(row[i]) <= 90): # verfica se é uma letra maiúscula
            letras = 0
        elif(ord(row[i]) >= 97 and  ord(row[i]) <= 122): # verfica se é uma letra minúscula
            letras = 0
    if(letras == 0 or numeros == 0): # a linha não é vazia
        return False
    else:
        return True

def getColumns(linha): # identifica e retorna o nome das colunas
    properties = []
    aspas = 0 # conta as aspas
    col = ""
    space = [" ", "\t"]
    row = linha + " "
    for i in range(len(row)):
        if(row[i] in space and row[i-1] not in space): #verifica se já passamos por uma coluna (estamos entre colunas, ou seja, em um "espaço")
            if(aspas == 0 or aspas == 2): # se acabou de ler uma coluna com ou sem aspas
                properties.append(col.strip())
                col = ""
            else:
                col += " "
        elif(row[i] == "'"): # começa a ler uma coluna entre aspas
            if(aspas == 2): # se leu a última aspa
                aspas = 0
            aspas +=1
        else:
            col += linha[i]
    return properties

def header(path): # retorna um dicionário onde cada key é o nome de um dado do cabeçalho e o seu value é o valor correspondente - dicionário
    file = read(path)
    header_data = dict() # {data_historico: 1, ...}
    cont = 1 # contador das linhas
    tam = 0 # tam da lista de colunas 
    aux = False # variavel auxiliar
    propies = 0 # quantidade de colunas 

    for linha in file:
        linha = linha.rstrip()
        if(not empty(linha)):
            if(linha[0] != "*"): # se a linha não começar com "*" e não for vazia
                
                if(aux): # se as propriedades continuam em outra linha
                    colunas = add_list_to_list(getColumns(linha), colunas) # concatena as propriedades lidas na linha anterior com as propriedades da linha atual
                    header_data.update({"propriedades": colunas}) # atualiza as propriedades no dicionário
                    tam = len(colunas) 
                    if(tam == propies): # compara a quantidades de propriedades já lidas com o total de propriedades do arquivo
                        aux = False # terminou de ler as propriedades
                    cont +=1
                else: # caso colatado, através da ordem pré-determinada, sabemos qual o próximo dado lido
                    if(len(header_data) == 0):
                        header_data["data_histo"] = linha
                    elif(len(header_data) == 1):
                        header_data["titulo"] = linha.replace("'", "") # retira as aspas já inseridas na linha
                    elif(len(header_data) == 2):
                        header_data["tempo_zero"] = linha
                    elif(len(header_data) == 3):
                        header_data["unidade_tempo"] = linha.replace("'", "") # retira as aspas já inseridas na linha
                    elif(len(header_data) == 4):
                        propies = int(linha)
                        header_data["qtd_prop"] = propies
                    elif(len(header_data) == 5):
                        colunas = getColumns(linha)
                        header_data["propriedades"] = colunas
                        tam = len(colunas)
                        if(tam != propies): # caso todas as propriedades não estejam todas na mesma linha
                            aux = True
                    elif(len(header_data) == 6):
                        header_data["logunits"] = getColumns(linha)
                    elif(len(header_data) == 7):
                        header_data["qtd_wells"] = int(linha)
                        break   # terminou de ler o cabeçalho do arquivo
                    cont +=1
        else:
            cont += 1

    return header_data
        
def add_list_to_list(a, b): # adiciona na lista b a lista a
    for item in a:
        b.append(item)
    return b

def getWellPropNames(path):
    header_data = header(path)
    return header_data.get("propriedades")

def getDateHistory(path): 
    header_data = header(path)
    return header_data.get("data_histo")      

def getTitle(path): 
    header_data = header(path)
    return header_data.get("titulo")
      
def getTimeZero(path):
    header_data = header(path)
    return header_data.get("tempo_zero")

def getUnitTime(path): 
    header_data = header(path)
    return header_data.get("unidade_tempo")

def getWellPropCount(path): 
    header_data = header(path)
    return header_data.get("qtd_prop")

def getLogunits(path):
    header_data = header(path)
    return header_data.get("logunits")

def getWellCount(path):
    header_data = header(path)
    return header_data.get("qtd_wells")

def getWellNames(path):
    file = read(path)
    well_names = []
    poco_nome = []
    linha_anterior = ""
    cont = 1
    i = 0
    aux = 0 #contador de aspas
    #ola eu sou incrivel

    for linha in file:
        if linha[0] != '*' and not empty(linha):
            if cont >= 8 and onlyNumbers(linha_anterior):# até chegar no nome do poço obrigatoriamente ele andou 8 ou mais linhas e verifica se a linha anterior é um número ou não
                    if linha[0] == "'": # se a linha em questão começar com ' é pq ela é um nome de poço
                        while aux < 2: # verifica se já vimos todo o nome do poço dentro das aspas
                            poco_nome.append(linha[i])                                                 
                            if linha[i] == "'":   
                                aux += 1                          
                            i+=1
                        new = "".join(poco_nome) # transforma uma lista de strings separadas em uma onde elas ficam juntas
                        poco_nome = [] 
                        well_names.append(new)
                        aux = 0
                        i = 0
            linha_anterior = linha.rstrip('\n')
            cont += 1

    return well_names

def getPropData(path):
    colunas = getWellPropNames(path)
    n_cols = getWellPropCount(path)
    well_names = getWellNames(path)
    totalWells = getWellCount(path)
    logunits = getLogunits(path)
    file = read(path)
    i = 0 #contador de poços
    

print(getWellNames('pdp/UNISIM-I-H_Group-1-PRO.fhf'))
print(getWellCount("pdp/UNISIM-I-H_Group-1-PRO.fhf"))
print(getWellPropNames("pdp/UNISIM-I-H_Group-1-PRO.fhf"))
print(getWellPropCount("pdp/UNISIM-I-H_Group-1-PRO.fhf"))
print(getLogunits("pdp/UNISIM-I-H_Group-1-PRO.fhf"))
