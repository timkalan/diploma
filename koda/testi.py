import igraj 
import agent
import matplotlib.pyplot as plt
import pandas as pd

igre = []

a = igraj.main(epizode=10, nasprotnik=agent.TD('p2'), nalozi=False)
igre.append(a)

for i in range(1000):
    #main(p1=TD('p1', epsilon=0.05), 
    #     p2=TD('p2', epsilon=0.05), 
    #     m=3,
    #     n=3,
    #     k=3,
    #     gravitacija=False,
    #     trening=True,
    #     epizode=1000,
    #     nalozi=False,
    #     nalozi_iz='454g', 
    #     shrani=True, 
    #     shrani_v='333',
    #     nasprotnik=Clovek('p2'), 
    #     strategija='333',
    #     zacne=True):

    a = igraj.main(epizode=10, nasprotnik=agent.TD('p2'), nalozi=True, nalozi_iz='674g')
    igre.append(a)

print(igre)
df = pd.DataFrame(igre)
print(df)
df.plot.line()
plt.show()