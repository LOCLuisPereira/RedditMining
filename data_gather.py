from json import load, dumps
from os import listdir

folder = 'Data/raw_data/'
gather = []
tot = len(listdir(folder))
for i, name in enumerate(listdir( folder )) :
    if i % 50000 == 0 :
        print(f'{i/tot*100}%')
    try :
        data = load(open(f'{folder}{name}','r'))
        gather.append(data)
        os.remove(f'{folder}{name}')
    except : pass

with open('Data/cluster.json','w') as handler :
    handler.write(dumps(gather,indent=2))