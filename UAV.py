import random
import math
import numpy as np
random.seed(42)
np.random.seed(42)


class UAV:
    def __init__(self, n_UAV):
        """
        initialize UAV class
        :param n_UAV: integer number of UAVs
        """
        self.n_UAV = n_UAV
        self.uav_pos = {}
        self.gu_uav_dis = {}
        self.uavs_gus_score = {}   # Score of each UAV for every GU
        self.max_dis = 10**2+10**2+2**2
        self.B_UH = 20e6  # Bandwidth between UAV-HAV (MHz)
        self.P_TU = 10  # Transmission power of UAVs 10W
        self.K_B = 1.38e-23 # Boltzmann's constant J/K
        self.T_S = 1000             # system noise temperature (K)
        self.F_UH = 2.4e9   # frequency of U2H channel
        self.G_UH_dB = 15           # dB
        self.G_UH = 10 ** (self.G_UH_dB/10)     # Linear scale
        self.C = 3e8        # velocity of light
        self.L_l = 0.2
    def get_pos_uav(self):
        """
        Hardcoded position for 4 UAVs
        Returns: Set of UAVs with their position
        """
        self.uav_pos = {
            "u_1": [2.50, 2.50, 2],
            "u_2": [7.50, 2.50, 2],
            "u_3": [2.50, 7.50, 2],
            "u_4": [7.50, 7.50, 2]
        }
        return self.uav_pos

    def dis_uavs_gus(self, uav_pos_set, gu_pos_set):
        """
        Calcutate distance for all GU from each UAVs
        Ca
        Args:
            gu_pos_set: Takes input as a set for GU position {"m_1": (2,10),.....}
            uav_pos_set: Takes input as a set for UAVs position {"u_1": (2.50, 7.50, 2),...}
        Returns: List of distance from UAV-GU for all UAV and GU [d_1, .., d_4]
        """
        # List of the position of GU
        gu_pos_list = []
        for p in gu_pos_set:
            gu_pos_list.append(gu_pos_set[p])
        # print(f"GU position list on UAV\n{gu_pos_list}")

        # List of the position of UAV
        uav_pos_list = []
        for p in uav_pos_set:
            uav_pos_list.append(uav_pos_set[p])
        # print(f"UAV position list\n {uav_pos_list}")

        uavs_gus_dis_l = []
        for i in range(len(gu_pos_list)):
            """
            Iterate over each GU and calculate distance for all the UAV from each GU
            """
            uavs_gu_dis_l = []
            for j in range(len(uav_pos_list)):
                uavs_gu_dis = ((gu_pos_list[i][0]-uav_pos_list[j][0])**2 + (gu_pos_list[i][1]-uav_pos_list[j][1])**2 +
                           uav_pos_list[j][2]**2)
                uavs_gu_dis_l.append(uavs_gu_dis)
            uavs_gus_dis_l.append(uavs_gu_dis_l)
        return uavs_gus_dis_l
    def uav_remaining_energy(self):
        """
        After each time slot remaining enery will change based on decision, (computing energy and offloading energy need
        to be subtructed
        Returns: Remaining energy list of every UAVs
        """
        # For now consider just random value from range 0-1
        uavs_re_l = []
        for i in range(self.n_UAV):
            remainig_energy = round(random.uniform(0.5,1), 2)
            uavs_re_l.append(remainig_energy)
        return uavs_re_l

    def score_uavs_gu(self, dis_uavs_gus_l, uav_re_l):
        s_uavs_gus = {}    # Score for each uav for each gu {m_0:{u_0: 0.3, u_2: 0.45}, ...}
        for i in range(len(dis_uavs_gus_l)):
            s_uavs_gu = {}  # Score for each uav for a perticular gu
            for j in range(len(dis_uavs_gus_l[i])):
                score = 5*dis_uavs_gus_l[i][j] / self.max_dis + uav_re_l[j]
                s_uavs_gu["u_{0}".format(j)] = round(score,2)
                # print(s_uavs_gu)
            s_uavs_gus["m_{0}".format(i)] = s_uavs_gu
            # print(s_uavs_gus)
        self.uavs_gus_score = s_uavs_gus
        return self.uavs_gus_score

    def channel_rate_UH(self):
        uav_positions_s = self.get_pos_uav()
        # print(uav_positions_s)
        # List of the position of GU
        uav_position_l = []
        for p in uav_positions_s:
            uav_position_l.append(uav_positions_s[p])
        # print(f"GU position list on UAV\n{gu_pos_list}")

        # List of the position of UAV
        hap_position = [5, 5, 20]
        uavs_hap_dis_l = []
        for i in range(len(uav_position_l)):
            """
            Iterate over each uav to calculate distance from that uav to hap
            """
            uavs_hap_dis = ((uav_position_l[i][0]-hap_position[0])**2 + (uav_position_l[i][1]-hap_position[1])**2 +
                           (uav_position_l[i][2]-hap_position[2])**2)
            uavs_hap_dis = math.sqrt(uavs_hap_dis)
            uavs_hap_dis = round(uavs_hap_dis, 2)
            uavs_hap_dis_l.append(uavs_hap_dis)
            # print(uavs_hap_dis_l)
        # print(uavs_hap_dis_l)
        uh_cr = []
        for uav_hap_dis in uavs_hap_dis_l:
            # Free space loss
            fs_l = (self.C / (4 * np.pi * uav_hap_dis * self.F_UH)) ** 2

            # Channel rate between UAV and HAP
            c_uh = self.B_UH * np.log2(1+(self.P_TU * self.G_UH * fs_l * self.L_l) / (self.K_B * self.T_S * self.B_UH))
            uh_cr.append(round(c_uh, 2))
        """
        Since channel rate for all the UAVs are same so return a value
        uh_cr_s = {}
        for i in range(len(uh_cr)):
            uh_cr_s["u_{0}_h".format(i)] = uh_cr[i]
        """

        return uh_cr[0]
# a = UAV(4)
# y = a.channel_rate_UH()
# print(y)