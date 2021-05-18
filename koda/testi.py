import koda.igraj 
import koda.agent
import matplotlib.pyplot as plt
import pandas as pd

igre = []
igralec1 = koda.agent.AgentNN
igralec2 = koda.agent.AgentNN
igra = 'test'

a = koda.igraj.main(p1=igralec1('p1', epsilon=0.05, alfa=0.2), 
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
               nasprotnik=koda.igraj.Nakljucni('p2'), 
               strategija=igra,
               zacne=True)
igre.append(a)

for i in range(100):
    #epsilon = 1 / (i + 1)
    #alfa = 1 / (i + 1)

    a = koda.igraj.main(p1=igralec1('p1', epsilon=0.05, alfa=0.2), 
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
                   nasprotnik=koda.igraj.Nakljucni('p2'), 
                   strategija=igra,
                   zacne=True)

    igre.append(a)



print(igre)
df = pd.DataFrame(igre)
print(df)
df.plot.line()
plt.xlabel("Število iger x 2000")
plt.show()