#Métodos para leitura do Single e Mutiple Welllog

def read(path):
    file = open(path, "r")
    return file

def countProperties(path): #DONE
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
    
def getProperties(path): # ajeitar no formato de cima --> mesma coisa mas com o col_name
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


print(countProperties("modelo.wlg"))
print(getProperties("RFT_mod_netto.wlg"))
    


