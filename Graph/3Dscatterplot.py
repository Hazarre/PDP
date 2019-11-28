from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
from matplotlib.colors import hsv_to_rgb
import csv

csv_in = open("CarWait.csv","rb")
in_rows = csv.reader(csv_in, delimiter=',')

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x1,y1,z1 =[],[],[]
for i in in_rows:
    x1.append(i[1])
    y1.append(i[2])
    z1.append(i[0])

xl = x1.pop(0)
yl = y1.pop(0)
zl = z1.pop(0)
x,y,z= [[],[],[],[],[]],[[],[],[],[],[]],[[],[],[],[],[]]
co = ['r','b','g','c','m']

for i in range(len(x1)):
    d = int(float(x1[i])*10-11)
    x[d].append(float(x1[i]))
    y[d].append(float(y1[i]))
    z[d].append(float(z1[i]))

for i in range(5):
    ax.scatter(x[i], y[i], z[i], c=co[i], marker='o')


ax.set_xlabel(xl)
ax.set_ylabel(yl)
ax.set_zlabel(zl)

plt.show()
