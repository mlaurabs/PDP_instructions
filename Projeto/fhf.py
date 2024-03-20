#Métodos para leitura do FHF

def read(path):
    file = open(path, "r")
    return file

def onlyNumbers(row): # verifica se uma string contém apenas números - bool
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

def teste(path): # continuar
    file = read(path)
    aux = dict() # {data historico: 5}
    cont = 1

    for linha in file:
        #print(logunits)
        if(linha[0] != "*" and not empty(linha)):
            if(len(aux) == 0):
                aux["data_histo"] = cont
            elif(len(aux) == 1):
                aux["titulo"] = cont
            elif(len(aux) == 2):
                aux["tempo0"] = cont
            elif(len(aux) == 3):
                aux["unidade_tempo"] = cont
            elif(len(aux) == 4):
                aux["qtd_prop"] = cont
            elif(len(aux) == 5):
                aux["coluna"] = cont
            cont +=1
        else:
            
            cont += 1

    print(aux)

def getColumns(linha): # identifica e retorna o nome das colunas
    properties = []
    aux = 0 # conta as aspas
    col = ""
    space = [" ", "\t"]
    for i in range(len(linha)):
        if(linha[i] in space and linha[i-1] not in space): #verifica se já passamos por uma coluna (estamos entre colunas, ou seja, em um "espaço")
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

def move(a, b):
    for item in a:
        b.append(item)
    return b

def getPropNames(path):
    file = read(path)
    aux = teste(path)
    row_col = aux['coluna']
    row_qtd_col = aux["qtd_prop"]
    i = 1
    plus = False
    properties = []
    qtd_props = 0

    for linha in file:
        linha = linha + " "
        if(plus):
            properties = move(getColumns(linha), properties)
            if(len(properties) == qtd_props):
                break
        elif(i == row_qtd_col):
            qtd_props = int(linha.rstrip().strip())
        elif(i == row_col):
            properties = getColumns(linha)            
            if(len(properties) == qtd_props):
                break
            else:
                plus = True
        i +=1
    
    return properties


def getDateHistory(path):
    file = read(path)
    linha = file.readline().rstrip()
    date = ""

    while(linha):
        if(linha[0] != "*"):
            date = linha
            break
        else:
            linha = file.readline().rstrip()
            #continue
    return date      

def getTitle(path):
    file = read(path)
    linha = file.readline().rstrip()
    title = ""

    while(linha):
        print(linha)
        if(linha[0] == "'"):
            title = linha
            break
        else:
            linha = file.readline().rstrip()
    return title      


#print(getTitle("arquivos/_first.fhf"))

#teste("arquivos/_first.fhf")

#getPropNames("arquivos/_includingsector.fhf")

#print(getDateHistory("arquivos/_first.fhf"))
#file = read("arquivos\_includingsector.fhf")

