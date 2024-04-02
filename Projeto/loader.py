def read(path):
    file = open(path, "r")
    return file

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
    columns = []
    aspas = 0 # conta as aspas
    col = ""
    space = [" ", "\t"]
    row = linha + " "
    for i in range(len(row)):
        if(row[i] in space and row[i-1] not in space): #verifica se já passamos por uma coluna (estamos entre colunas, ou seja, em um "espaço")
            if(aspas == 0 or aspas == 2): # se acabou de ler uma coluna com ou sem aspas
                columns.append(col.strip())
                col = ""
            else:
                col += " "
        elif(row[i] == "'"): # começa a ler uma coluna entre aspas
            if(aspas == 2): # se leu a última aspa
                aspas = 0
            aspas +=1
        else:
            col += linha[i]
    return columns
"""
métodos que seriam sobrescitos dependendo do tipo de loader:
onlyNumbers(row)
wellPropData()
orginizeData()

interface:
wellproptype(()
wellpropcount()
wellcount()
wellnames()
wellpropnames()
wellpropdata()

"""