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

def getColumns(linha): # identifica e retorna o nome das colunas
    properties = []
    header_data = 0 # conta as aspas
    col = ""
    space = [" ", "\t"]
    row = linha + " "
    for i in range(len(row)):
        if(row[i] in space and row[i-1] not in space): #verifica se já passamos por uma coluna (estamos entre colunas, ou seja, em um "espaço")
            if(header_data == 0 or header_data == 2): # se acabou de ler uma coluna com ou sem aspas
                properties.append(col.strip())
                col = ""
            else:
                col += " "
        elif(row[i] == "'"): # começa a ler uma coluna entre aspas
            if(header_data == 2): # se leu a última aspa
                header_data = 0
            header_data +=1
        else:
            col += linha[i]
    return properties

def header(path): # continuar
    file = read(path)
    header_data = dict() # {data historico: 5, ...}
    cont = 1 # iterador das linhas
    tam = 0 # tam da lista de colunas 
    aux = False # variavel auxiliar
    propies = 0 # quantidade de colunas 

    for linha in file:
        linha = linha.rstrip()
        if(not empty(linha)):
            if(linha[0] != "*"): # se a linha não começar com "*" e não for vazia
                # caso colatado, através da ordem pré-determinada, sabemos qual o próximo dado lido
                if(aux): # se as propriedades continuam em outra linha
                    tam += len(getColumns(linha)) 
                    if(tam == propies): # terminou de ler as propriedades
                        aux = False
                    cont +=1
                else:
                    if(len(header_data) == 0):
                        header_data["data_histo"] = cont
                    elif(len(header_data) == 1):
                        header_data["titulo"] = cont
                    elif(len(header_data) == 2):
                        header_data["tempo0"] = cont
                    elif(len(header_data) == 3):
                        header_data["unidade_tempo"] = cont
                    elif(len(header_data) == 4):
                        header_data["qtd_prop"] = cont
                        propies = int(linha)
                    elif(len(header_data) == 5):
                        header_data["coluna"] = cont
                        tam += len(getColumns(linha))
                        if(tam != propies): # caso as propriedades não estejam todas na mesma linha
                            aux = True
                    elif(len(header_data) == 6):
                        header_data["logunits"] = cont
                    elif(len(header_data) == 7):
                        header_data["qtd_wells"] = cont
                        break   
                    cont +=1
        else:
            cont += 1

    return header_data

def move(a, b):
    for item in a:
        b.append(item)
    return b

def getPropNames(path):
    file = read(path)
    header_data = header(path)
    row_col = header_data['coluna']
    row_qtd_col = header_data["qtd_prop"]
    i = 1
    plus = False
    properties = []
    qtd_props = 0

    for linha in file:
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


def getDateHistory(path): # alterar
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

def getTitle(path): # alterar
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

print(header("arquivos/_first.fhf"))

#print(getPropNames("arquivos/_includingsector.fhf"))

#print(getDateHistory("arquivos/_first.fhf"))
#file = read("arquivos\_includingsector.fhf")

