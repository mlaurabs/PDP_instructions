import lasio
import pandas as pd

def getWellpropdata(path): # entender porque o valor é atribuído arredondado
    file = lasio.read(path)
    d = dict()
    for curve in file.curves:
        key = curve.mnemonic
        d[key] = file[curve.mnemonic]
    dt = pd.DataFrame(d)
    dt = dt.fillna(value=' ')
    dt = dt.to_string(index='')
    return dt

def getWellCount():
    return 1

def getWellNames(path):
    las = lasio.read(path)
    well_info = las.well
    well_name = well_info['WELL'].value
    return well_name

def getPropNames(path):
    las = lasio.read(path)
    properties = dict()
    curves = las.curves
    for curve in curves:
        properties[curve.mnemonic] = curve.descr
    return properties

def getWellPropCount(path):
    propies = getPropNames(path)
    return len(propies)

#print(getWellpropdata('arquivoslas/P3.las'))
#getWellNames('arquivoslas/_firstexample.las')
#getPropCount('arquivos/Export_Sigeo3.las')

print(getWellpropdata("arquivos/P23.las"))

