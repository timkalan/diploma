import igraj 
import agent
import matplotlib.pyplot as plt
import pandas as pd

igre = []
igralec = agent.Agent
igra = '444'

a = igraj.main(p1=igralec('p1', epsilon=0.05), 
               p2=igralec('p2', epsilon=0.05), 
               m=4,
               n=4,
               k=4,
               gravitacija=False,
               trening=True,
               epizode=10,
               nalozi=False,
               nalozi_iz=igra, 
               shrani=True, 
               shrani_v=igra,
               nasprotnik=igralec('p2'), 
               strategija=igra,
               zacne=True)
igre.append(a)

for i in range(1000):
    epsilon = 1 / (i + 1)
    alfa = 1 / (i + 1)

    a = igraj.main(p1=igralec('p1', epsilon=epsilon, alfa=alfa), 
               p2=igralec('p2', epsilon=epsilon, alfa=alfa), 
               m=4,
               n=4,
               k=4,
               gravitacija=False,
               trening=True,
               epizode=10,
               nalozi=True,
               nalozi_iz=igra, 
               shrani=True, 
               shrani_v=igra,
               nasprotnik=igralec('p2'), 
               strategija=igra,
               zacne=True)

    igre.append(a)



print(igre)
df = pd.DataFrame(igre)
print(df)
df.plot.line()
plt.xlabel("Število iger x 10")
plt.show()