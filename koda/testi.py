import igraj 
import agent
import matplotlib.pyplot as plt
import pandas as pd

igre = []
igralec1 = agent.Agent
igralec2 = agent.Agent
# format: algo-igralec-igra-stevilo

m = 3
n = 3
k = 3
grav = False
epsilon = 0.3
alfa = 0.2
zacne = True
igra = 'td0-333-10000'

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

for i in range(20):
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

g = 'g' if grav else ''
turn = '-1' if zacne else '-2'
df.to_csv(f'rezultati/{str(m) + str(n) + str(k)}{g}{turn}.csv')
plt.xlabel('Število iger x 1000')
plt.ylabel('Število')
if zacne:
    plt.title(f'{m}' + ',' + f'{n}' + ',' + f'{k}' + '-igra: agent proti naključnemu igralcu')
else: 
    plt.title(f'{m}' + ',' + f'{n}' + ',' + f'{k}' + '-igra: naključni igralec proti agentu')
plt.show()