import random
random.seed(42)
"""
In this code the declaration convention of variables are like gus_uav_dis: For all gus distance from each UAVs u_1:{'m_1': 
#, 'm_2': #, .....................}, .......
if uavs_gu_dis: m_1:{'u_1': #...}, .....
"""
import numpy as np
np.random.seed(42)
class GU:
    def __init__(self, n_gu):
        self.n_gu = n_gu
        # self.gu_list = []
        self.gu_task_set = {}                   # Task information set of gus: {'m_1': [s_m, c_m, l_m], 'm_2'....}
        self.gus_uavs_score_set = {}            # Set: For each uav, score of all gus
        self.gu_pos_set = {}                    # set: Gu position
        self.c_c_gu_set = {}                    # set: computation capacity of each gu
        self.max_dis = 10 ** 2 + 10 ** 2 + 2 ** 2

    def get_pos_gu(self):
        """
        Genrate GU position withing 1000m X 1000m
        :return: a list with position for all GU. Each element contains (x, y)
        """
        for i in range(self.n_gu):
            x = random.randint(0,10)
            y = random.randint(0, 10)
            self.gu_pos_set["m_{0}".format(i)] = [x, y]
        return self.gu_pos_set

    def gus_com_c(self):
        """
        Generate computation capacity of each GU in Mhz (0.2GHz-0.5Ghz)/(200Mhz-500Mhz)
        Returns: Set of computation capacity of GUs
        """
        for i in range(self.n_gu):
            self.c_c_gu_set["m_{0}".format(i)] = random.randint(500, 750)
        return self.c_c_gu_set
    def generate_task_gu(self):
        for i in range(self.n_gu):
            s_m = round(np.random.uniform(1, 8), 2)  # task size mbit
            c_m = np.random.randint(600, 750)         # Task complexity (required cycle/ bit)
            l_m = round(np.random.uniform(1, 7), 2)   # Latency requirement of tasks
            i_m = [s_m, c_m, l_m]                              # task information [task size, task complexity, latency requirement]
            self.gu_task_set["m_{0}".format(i)] = i_m

        return self.gu_task_set

    def dis_gus_uavs(self, uav_pos_set, gu_pos_set):
        """
        Calcutate distance for all GU from each UAVs
        Ca
        Args:
            gu_pos_set: Takes input as a set for GU position {"m_1": (2,10),.....}
            uav_pos_set: Takes input as a set for UAVs position {"u_1": (2.50, 7.50, 2),...}
        Returns: List of distance from UAV-GU for all UAV and GU [d_1, .., d_4]
        """
        # List of the position of GU
        uav_pos_list = []
        for p in uav_pos_set.keys():
            uav_pos_list.append(uav_pos_set[p])
        # print(f"UAVs position list\n{uav_pos_list}")

        # List of the position of UAV
        gu_pos_list = []
        for p in gu_pos_set:
            gu_pos_list.append(gu_pos_set[p])
        # print(f"GUs position list\n {gu_pos_list}")

        gus_uavs_dis_l = []
        for i in range(len(uav_pos_list)):
            """
            Iterate over each UAV and calculate distance for all the GU from each UAV
            """
            gus_uav_dis_l = []
            for j in range(len(gu_pos_list)):
                gus_uav_dis = ((uav_pos_list[i][0]-gu_pos_list[j][0])**2 + (uav_pos_list[i][1]-gu_pos_list[j][1])**2 + uav_pos_list[i][2]**2)
                gus_uav_dis_l.append(gus_uav_dis)
            gus_uavs_dis_l.append(gus_uav_dis_l)
        return gus_uavs_dis_l

    def calculate_score(self, gu_task_set, gus_uavs_dis_l):
        """
        Calculate score ((1-s_m * c_m) +l_m) for GUs becasue UAV will prefer GU with lowest sc
        :param gu_set: Set with all the task information of all ground users - from method generate_task_gu
        :return: Set of GUs with score
        """
        task_score_l = []
        for gu in gu_task_set:
            i_m = gu_task_set[gu]
            norm_s_c = (i_m[0] * i_m[1])/(10*750)     # normalize s_m(task_size) * c_m(task_complexity)
            norm_l = i_m[2]/7                       # normalize l_m(latency requirement of task)

            # print(norm_s_c)
            # print(norm_l)
            task_score = round((0.5 * (1-norm_s_c) + 0.5 * norm_l), 2)
            task_score_l.append(task_score)
        # print(f"Task score list\n{task_score_l}")

        s_gus_uavs_set = {}
        for i in range(len(gus_uavs_dis_l)):
            s_gus_uav_set = {}
            for j in range(len(gus_uavs_dis_l[i])):
                s_gus_uav_set["m_{0}".format(j)] = round((gus_uavs_dis_l[i][j]/self.max_dis + task_score_l[j]), 2)
            s_gus_uavs_set["u_{0}".format(i)] = s_gus_uav_set

        self.gus_uavs_score = s_gus_uavs_set

        return self.gus_uavs_score


