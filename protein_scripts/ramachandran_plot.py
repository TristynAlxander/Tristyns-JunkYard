import matplotlib.pyplot as plt
from colour import Color
import math

# Import Angles
phi_list = [line.replace("\n", "") for line in open("phi.dat", 'r')]
psi_list = [line.replace("\n", "") for line in open("psi.dat", 'r')]
res_list = [line.replace("\n", "") for line in open("res.dat", 'r')]

# Cast to Floats
for i, phi in enumerate(phi_list):
    try:
        phi_list[i] = float(phi)
    except ValueError:
        continue
for i, psi in enumerate(psi_list):
    try:
        psi_list[i] = float(psi)
    except ValueError:
        continue

if(len(phi_list) != len(psi_list)):
    print("Lists of Different lengths, you messed something up.")

# Remove Non-floats
phi_floats = [phi for phi,psi in zip(phi_list,psi_list) if (type(phi) == float and type(psi) == float)]
psi_floats = [psi for phi,psi in zip(phi_list,psi_list) if (type(phi) == float and type(psi) == float)]


red = Color("red")
colors = [c.hex_l for c in list(red.range_to(Color("blue"),len(phi_list)))]


for i,(phi,psi,res) in enumerate(zip(phi_floats,psi_floats,res_list)):
    
    if(res == "GLY"):
        plt.plot(phi,psi, c=colors[i], marker='x', markersize=4)
    else:
        plt.plot(phi,psi, c=colors[i], marker='o', markersize=3)
    

plt.figtext(.5,.94,'Ramachandran Plot', fontsize=18, ha='center')                                       # Title
plt.figtext(.5,.9,'Resides colored by order from red to blue.',fontsize=10,ha='center')                 # Subtitle

plt.legend(frameon=False)
plt.axis([-math.pi,math.pi,-math.pi,math.pi])
#plt.title("Ramachandran Plot")
plt.xlabel("Phi Angle")
plt.ylabel("Psi Angle")
plt.show()

"""
x = np.random.rand(N)
y = np.random.rand(N)
colors = np.random.rand(N)
area = (30 * np.random.rand(N))**2  # 0 to 15 point radii

plt.scatter(x, y, s=area, c=colors, alpha=0.5)
plt.show()
"""