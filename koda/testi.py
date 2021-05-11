import igraj 
import agent
import matplotlib.pyplot as plt
import pandas as pd

igre = []
igralec1 = agent.AgentNN
igralec2 = agent.AgentNN
igra = 'test'

a = igraj.main(p1=igralec1('p1', epsilon=0.05), 
               p2=igralec2('p2', epsilon=0.05), 
               m=3,
               n=3,
               k=3,
               gravitacija=False,
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

for i in range(20):
    #epsilon = 1 / (i + 1)
    #alfa = 1 / (i + 1)

    a = igraj.main(p1=igralec1('p1'), 
                   p2=igralec2('p2'), 
                   m=3,
                   n=3,
                   k=3,
                   gravitacija=False,
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



print(igre)
df = pd.DataFrame(igre)
print(df)
df.plot.line()
plt.xlabel("Število iger x 1000")
plt.show()