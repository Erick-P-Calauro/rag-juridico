import json

f = open("./data/documentos.json", "r")

d = json.loads(f.read())

contagem = [0 for _ in range(676)]

for i in d:
    sumula = str(i["metadata"]["source"])
    sumula = int(sumula[6:]) - 1

    contagem[sumula] += 1

for i in range(0, 676):
    print("{:d} = {:d} vezes".format(i+1, contagem[i]))