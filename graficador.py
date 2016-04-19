__author__ = 'Belen Bouzon'
import networkx as nx
import matplotlib.pyplot as plt
import colorsys

#Recibo <numero de nodo, su numero de color>
#iteracionesColores = open("iteraciones.txt",'r')
#nodes = eval(iteracionesColores.readline())

nodes = eval("[(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1), (8, 1), (9, 1), (10, 1), (11, 1), (12, 1), (13, 1)]")
#cantColores = 2

#Recibo las aristas
aristas = [(1,1), (1,11), (10,10), (3,3), (3,4), (3,14), (7,11), (13,13), (5,11), (6,11), (11,15), (11,5), (11,6), (11,7), (11,8), (11,9), (11,2), (11,16), (11,12), (11,14), (8,11), (9,11), (2,11), (12,11), (12,12), (4,1), (4,3), (4,8), (4,12), (4,17)]

cantidadDeNodos = len(nodes)

#Hago un array con tantos colores como cantidad de nodos tengo
#HSV_tuples = [(x/(cantidadDeNodos*0.1555555555555), 0.3, 0.9) for x in range(cantColores+2)]
#RGB_tuples = map(lambda x: colorsys.hsv_to_rgb(*x), HSV_tuples)

#index = 0
#while nodes != []:
    #Armo un array con los colores ordenados en el orden natural de los nodos
nodeColors = []

#for i in range (0, cantidadDeNodos):
#    color =  [nodo[1] for nodo in nodes if nodo[0] == i][0]
#    nodeColors.insert(i,RGB_tuples[color])
G=nx.Graph()
G.add_nodes_from([x[0] for x in nodes])
G.add_edges_from(aristas)
pos=nx.spring_layout(G)
plt.figure(figsize=(8,8))
#nx.draw_graphviz(G,prog='neato',node_color = nodeColors, node_size=700, with_labels = True)
nx.draw(G,pos,node_size=300, with_labels= True, alpha=0.7, node_shape="h", linewidths=0.5, width= 0.5,style= 'solid', font_size =10)
plt.axis('equal')
plt.savefig(str(cantidadDeNodos) + "Nodos4.png", transparent = False)
plt.close()
#    index += 1
#    var = iteracionesColores.readline()
#    if var != "":
#        nodes= eval(var)
#    else:
#        nodes = []

#iteracionesColores.close()
#h = hexagono
