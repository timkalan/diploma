import igraj 
import agent
import matplotlib.pyplot as plt
import pandas as pd

igre = []
igralec1 = agent.AgentNN
igralec2 = agent.AgentNN
# format: algo-igralec-igra-stevilo

m = 6
n = 7
k = 4
grav = True

# epsilon za navadnega
#epsilon = 0.3
# epsilon za nn
epsilon = 0.05

# alfa za navadnega
#alfa = 0.2
# alfa za nn
alfa = 0.01

zacne = True
algo = 'tdnn'
# 'λ'
kdo_igra = 'TD(0)-NM'
igra = algo + '-674g-100000'
g = 'g' if grav else ''
turn = '1' if zacne else '2'

a = igraj.main(p1=igralec1('p1', epsilon=epsilon, alfa=alfa), 
               p2=igralec2('p2', epsilon=epsilon, alfa=alfa), 
               m=m,
               n=n,
               k=k,
               gravitacija=grav,
               trening=True,
               epizode=0,
               nalozi=False,
               nalozi_iz=igra, 
               shrani=True, 
               shrani_v=igra,
               nasprotnik=igraj.Nakljucni('p2'), 
               strategija=igra,
               zacne=zacne)
igre.append(a)

for i in range(200):
    #epsilon = 1 / (2 * i + 1)
    #alfa = 1 / (i + 1)

    a = igraj.main(p1=igralec1('p1', epsilon=epsilon, alfa=alfa), 
                   p2=igralec2('p2', epsilon=epsilon, alfa=alfa), 
                   m=m,
                   n=n,
                   k=k,
                   gravitacija=grav,
                   trening=True,
                   epizode=500,
                   nalozi=True,
                   nalozi_iz=igra, 
                   shrani=True, 
                   shrani_v=igra,
                   nasprotnik=igraj.Nakljucni('p2'), 
                   strategija=igra,
                   zacne=zacne)

    igre.append(a)
    print(f'\nSmo pri i = {i}\n')



print(igre)
df = pd.DataFrame(igre)
print(df)
df.plot.line()


df.to_csv(f'rezultati/{algo}-{str(m) + str(n) + str(k)}{g}-{(i + 1) * 500}-{turn}.csv')
plt.xlabel('Število iger x 500')
plt.ylabel('Število')
if zacne:
    plt.title(f'{m}' + ',' + f'{n}' + ',' + f'{k}' + f'-igra: {kdo_igra} proti naključnemu igralcu')
else: 
    plt.title(f'{m}' + ',' + f'{n}' + ',' + f'{k}' + f'-igra: naključni igralec proti {kdo_igra}')
plt.show()