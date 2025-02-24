from GU import GU
from UAV import UAV
import matplotlib.pyplot as plt

uavs = UAV(4)
gus = GU(100)


fig = plt.figure()
ax = fig.add_subplot(projection='3d')

gus_pos = gus.get_pos_gu()
print(f"gus_pos\n{gus_pos}")
gus_pos_l = []
for p in gus_pos:
    gus_pos_l.append(gus_pos[p])
print(f"gus_pos_list\n{gus_pos_l}")

uavs_pos = uavs.get_pos_uav()
uavs_pos_l = []
for p in uavs_pos:
    uavs_pos_l.append(uavs_pos[p])
print(f"uavs_pos\n{uavs_pos}")
print(f"uavs_pos_list\n{uavs_pos_l}")

x_gu = [x[0] for x in gus_pos_l]
y_gu = [x[1] for x in gus_pos_l]
z_gu = [0 for _ in gus_pos_l]

x_uav = [x[0] for x in uavs_pos_l]
y_uav = [x[1] for x in uavs_pos_l]
z_uav = [x[2] for x in uavs_pos_l]

x_hap = 5.00
y_hap = 5.00
z_hap = 20

ax.scatter(x_gu, y_gu, z_gu, marker="+", color="black", linewidths=1)
ax.scatter(x_uav, y_uav, z_uav, marker="v", color="b", linewidths=2)
ax.scatter(x_hap, y_hap, z_hap, marker="p", color="r", linewidths=3)

ax.set_xlabel('(km)')
ax.set_ylabel('(km)')
ax.set_zlabel('(km)')
# plt.title('Coverage area of UAVs and HAP')
ax.legend(['GU', 'UAV', 'HAP'])
ax.set_zlim(zmin=0)
plt.savefig('plot.png', dpi=800)
plt.show()