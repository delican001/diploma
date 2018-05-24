from xml.dom import minidom
import numpy as np
import ll_to_xy
import matplotlib.pyplot as plt
import smoothing


def get_axes(items):
    minlat = float(items[0].attributes['minlat'].value)
    minlon = float(items[0].attributes['minlon'].value)
    maxlat = float(items[0].attributes['maxlat'].value)
    maxlon = float(items[0].attributes['maxlon'].value)
    axes = {'minlat' : minlat,
            'minlon' : minlon,
            'maxlat' : maxlat,
            'maxlon' : maxlon}
    print(axes)
    return axes

def draw(points):
    colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
    for i in range(len(points[0])):
        if (len(points[0][i])==1):
            plt.plot(points[0][i][0],points[1][i][0],marker='o')
        else:
            color = np.random.randint(0,len(colors)-1)
            for j in range(1,len(points[0][i])):
                plt.plot([points[0][i][j-1],points[0][i][j]],[points[1][i][j-1],points[1][i][j]],marker='o',color=colors[color])

    plt.show()

xml_path = 'map_new.xml'
xmldoc = minidom.parse(xml_path)
itemlist = xmldoc.getElementsByTagName('bounds')
axes = get_axes(itemlist)
nodes = xmldoc.getElementsByTagName('node')
xml_ways = xmldoc.getElementsByTagName('way')
ways = [[],[],[]]
for i in range(len(xml_ways)):
    coords_x=[]
    coords_y=[]
    coords_color=[]
    ref_nodes = xml_ways[i].getElementsByTagName('nd')
    for j in range(len(ref_nodes)):
        ref = ref_nodes[j].attributes['ref'].value
        node = None
        for k in range(len(nodes)):
            if (nodes[k].attributes['id'].value==ref):
                node = nodes[k]
                break
        if (node!=None):
            coords_x.append(float(node.attributes['lat'].value))
            coords_y.append(float(node.attributes['lon'].value))
            coords_color.append(-1)
    if len(coords_x)!=0:
        ways[0].append(coords_x)
        ways[1].append(coords_y)
        ways[2].append(coords_color)
print(ways)
for i in range(len(ways[0])):
    for j in range(len(ways[0][i])):
        ways[0][i][j],ways[1][i][j] = ll_to_xy.lat_long_to_xy(ways[0][i][j],ways[1][i][j],axes['minlat'],axes['minlon'])
print("###")
ways = smoothing.go(ways)
print(ways)