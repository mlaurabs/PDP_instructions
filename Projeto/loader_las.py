import lasio
import pandas as pd

def read(path):
    file = open(path, 'r')
    return file

def getWellpropdata(path):
    file = lasio.read(path)
    d = dict()
    for i, curve in enumerate(file.curves):
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

def getPropCount(path):
    las = lasio.read(path)
    prop_name = []
    curves = las.curves
    mnemonics = [curve.mnemonic for curve in curves]
    for mnemonic in mnemonics:
        prop_name.append(mnemonic)
    prop_count = len(prop_name)

    print(prop_count)
    print(prop_name)


#print(getWellpropdata('arquivoslas/P3.las'))
#getWellNames('arquivoslas/_firstexample.las')
getPropCount('arquivoslas/Export_Sigeo3.las')

