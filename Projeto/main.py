
import loader_single as sing
import loader_fhf as fhf
import loader_multiple as mul
import loader_las as las


print("WELLOG SINGLE")
file_path = "arquivos/2_singlewelllogwithnullvalue.log"
print(sing.getWellNames(file_path))
print(sing.getWellPropNames(file_path))
print(sing.getWellPropData(file_path))

print("\n")

print("WELLOG MUTIPLE")
file_path = "arquivos/multiplewelllogwith2d.wlg"
print(mul.getWellNames(file_path))
print(mul.getWellPropNames(file_path))

dataframes = mul.getWellPropData(file_path)
for table in dataframes:
    print(table)

print("\n")
print("FHF")
file_path = "arquivos\_first.fhf"
print(fhf.getWellNames(file_path))
print(fhf.getWellPropNames(file_path))

dataframes = fhf.getWellPropData(file_path)
for table in dataframes:
    print(table)

