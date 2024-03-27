"""
o que dividi os headers da body dos dados é "#"
a cada coluna: linha pontilhada "---------"
a cada seção: ~
"""

global deli_sec
deli_sec = "~" 

file = open("_firstexample.las", "r")
secoes = ["well", "curve", "Ascii"]
tam_col = []

linha = file.readline()
cont_sec = 0
aux = 0

table = dict()

while(linha):
    if(aux == cont_sec): # estamos nos dados de uma mesma seção
        if(linha[0] == "#"): #leitura dos dados
            if("-" in linha):
                tracos = 0
                for i in range(len(linha)):
                    if(linha[i] == "-"):
                        tracos +=1
                    else:
                        tam_col.append(tracos)
                        tracos = 0
 
    if(linha[0] == deli_sec):
        print(f"Incializando a leitura da seção {linha[1:]}")
        cont_sec +=1
        aux = cont_sec
    linha = file.readline()

print(tam_col)