import networkx as nx
import matplotlib.pyplot as plt
# %matplotlib inline
G_fb = nx.read_edgelist("data/facebook_combined.txt", create_using = nx.Graph(), nodetype = int)
#Quick snapshot of the Network
print nx.info(G_fb)

#Create network layout for visualizations
spring_pos = nx.spring_layout(G_fb)

plt.axis("off")
nx.draw_networkx(G_fb, pos = spring_pos, with_labels = False, node_size = 35)
plt.show()
