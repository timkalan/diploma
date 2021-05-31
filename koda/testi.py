import igraj 
import agent
import matplotlib.pyplot as plt
import pandas as pd

igre = []
igralec1 = agent.AgentNN
igralec2 = agent.AgentNN
igra = 'test'
m = 4
n = 5
k = 4
grav = True

a = igraj.main(p1=igralec1('p1', epsilon=0.05, alfa=0.01), 
               p2=igralec2('p2', epsilon=0.05, alfa=0.01), 
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
               zacne=True)
igre.append(a)

for i in range(100):
    #epsilon = 1 / (2 * i + 1)
    #alfa = 1 / (i + 1)

    a = igraj.main(p1=igralec1('p1', epsilon=0.05, alfa=0.01), 
                   p2=igralec2('p2', epsilon=0.05, alfa=0.01), 
                   m=m,
                   n=n,
                   k=k,
                   gravitacija=grav,
                   trening=True,
                   epizode=1000,
                   nalozi=True,
                   nalozi_iz=igra, 
                   shrani=True, 
                   shrani_v=igra,
                   nasprotnik=igraj.Nakljucni('p2'), 
                   strategija=igra,
                   zacne=True)

    igre.append(a)
    print(f'\nSmo pri i = {i}\n')



print(igre)
df = pd.DataFrame(igre)
print(df)
df.plot.line()

g = 'g' if grav else ''
df.to_csv(f'rezultati/{str(m) + str(n) + str(k)}{g}.csv')
plt.xlabel('Število iger x 1000')
plt.title(f'{m}' + ',' + f'{n}' + ',' + f'{k}' + '-igra: agent proti naključnemu igralcu')
plt.show()