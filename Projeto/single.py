"""
Outra versão de definir as colunas em teste :
file = open(path, "r")
    linha = file.readline().rstrip() #tira o \n
    coluna = 0 # contabiliza colunas
    pos_ini = 0
    aux = 0 # variavel auxiliar que contabiliza aspas
    j = 0 # iterador para fatiar a string
    for i in range(len(linha)):
        var = linha[i]
        if(linha[i] == " " and linha[i-1] != " "): #verifica se já passamos por uma coluna
            col_name = linha[pos_ini:pos_ini+j]
            if("'" not in col_name):
                coluna +=1
                pos_ini = i+1
                j = 0
        if(linha[i] == "'"): # começa a ler uma coluna entre aspas
                j = 0
                aux +=1
        if(aux == 2): # já terminou de ler uma coluna entre aspas
            aux = 0
            coluna +=1
            j = 0
        j +=1        
    return coluna


"""

def countCols(path): #DONE
    file = open(path, "r")
    linha = file.readline().rstrip() #tira o \n
    coluna = 0
    aux = 0
    opcoes = [" ", "'"] 
    for i in range(len(linha)):
        if(linha[i] == " " and linha[i-1] not in opcoes): #verifica se já passamos por uma coluna
            coluna +=1
        elif(linha[i] == "'"): # começa a ler uma coluna entre aspas
            if(aux != 2): # lendo uma aspa
                aux +=1
        if(aux == 2): # já terminou de ler uma coluna entre aspas
            aux = 0
            coluna +=1
        
    return coluna
    

def getDataItems(path): # ajeitar no formato de cima --> mesma coisa mas com o col_name
    file = open(path, "r")
    linha = file.readline().rstrip() #tira o \n
    data_items = []
    aux = 0
    col = ""

    for i in range(len(linha)):
        if(linha[i] == " " and linha[i+1] != " " and linha[i-1] != "'"): #verifica se já passamos por uma coluna
           if(aux == 0): #se estamos fora de "aspas", ou seja, terminamos de ler uma coluna que não está entre aspas
                data_items.append(col.strip())
                col = ""
           else:
               col += linha[i]
        elif(linha[i] == "'"): # começa a ler uma coluna entre aspas
            if(aux != 2): # lendo a última aspa
                aux +=1
        else:            
            col += linha[i]
        if(aux == 2): # já terminou de ler uma coluna entre aspas
            aux = 0
            data_items.append(col.strip())
            col = ""
    print(data_items)




# DEPTH np 'Production e ola'
#string = "DEPTH NP"
print(countCols("Projeto/modelo.wlg"))
#getDataItems("modelo.wlg")
    


