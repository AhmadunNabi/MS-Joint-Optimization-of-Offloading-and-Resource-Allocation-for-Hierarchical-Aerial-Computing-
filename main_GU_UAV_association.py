from UAV import UAV
from GU import GU
import math

class Association:
    def __init__(self):
        n_gu = 100
        n_uav = 4
        gus = GU(n_gu)
        uavs = UAV(n_uav)

        # GUs and UAV position set
        gus_pos_set = gus.get_pos_gu()
        uavs_pos_set = uavs.get_pos_uav()
        # print(f"GUs position set\n{gus_pos_set}\n")
        # print(f"UAVs position set\n{uavs_pos_set}\n")

        # Calculate score of all UAVs for each GU
        uavs_gus_dis_l = uavs.dis_uavs_gus(uav_pos_set=uavs_pos_set, gu_pos_set=gus_pos_set)
        # print(f"Distance for each GU from that GU to all 4 UAVs\n{uavs_gus_dis_l}\n")
        uavs_re_l = uavs.uav_remaining_energy()
        # print(f"uavs remaining energy list\n{uavs_re_l}\n")
        score_uavs_gus = uavs.score_uavs_gu(dis_uavs_gus_l=uavs_gus_dis_l, uav_re_l=uavs_re_l)
        # print(f"Scroe of all the UAVs for each GUs in a set.\n{score_uavs_gus}\n")

        # Calculate score of all GUs for each UAV
        gus_uavs_dis_l = gus.dis_gus_uavs(gu_pos_set=gus_pos_set, uav_pos_set=uavs_pos_set)
        # print(f"Distance for each UAV from that UAV to all GUs\n{gus_uavs_dis_l}\n")
        gus_c_c = gus.gus_com_c()
        # print(f"Computation capacity of all GU in Mhz\n{gus_c_c}\n")
        gus_task_set = gus.generate_task_gu()
        # print(f"All GU set:\n{gus_task_set}\n")
        score_gus_uavs = gus.calculate_score(gu_task_set=gus_task_set, gus_uavs_dis_l=gus_uavs_dis_l)
        # print(f"score of all GUs for each UAV\n{score_gus_uavs}\n")

        # GU-UAV association algorithm based on gale shapley
        def sort_score_s(score_set):
            sorted_set = {}
            for key in score_set:
                sub_set = score_set[key]
                s_sub_set = dict(sorted(sub_set.items(), key=lambda item: item[1], reverse= True))
                sorted_set[key] = s_sub_set
                # print(s_sub_set)
            return sorted_set

        # Sort the two set based on score
        sorted_gus_uav_s = sort_score_s(score_gus_uavs)         # UAV dict
        sorted_uavs_gus_s = sort_score_s(score_uavs_gus)        # GU dict
        # print(f"Sorted GUs set for each uav \n{sorted_gus_uav_s}\n")
        # print(f"Sorted UAVs set for each GU \n{sorted_uavs_gus_s}\n")


        gus_l = [i for i in gus_pos_set.keys()]
        gu_local_l = []
        gu_need_matching_l = []

        for gu in gus_l:
            gu_task_info = gus_task_set[gu]
            # print(f"{gu} gu task info {gu_task_info}")
            # print(f"{gu} gu computation capacity {gus_c_c[gu]}")

            required_ckl_gu = gu_task_info[0] * gu_task_info[1]
            task_lr_gu = gu_task_info[2]
            gu_c_c = gus_c_c[gu]
            if required_ckl_gu < task_lr_gu * gu_c_c:
                gu_local_l.append(gu)
            else:
                gu_need_matching_l.append(gu)
                # print(gu)

        print(f"GUs that will compute locally\n{gu_local_l}\n")
        print(f"GUs that need matching\n{gu_need_matching_l}\n")


        unmatched_gu_l = gu_need_matching_l
        # print(f"GUs list\n{unmatched_gu_l}\n")
        unmatched_uav_list = [i for i in uavs_pos_set.keys()]
        # print(f"UAVs list\n{unmatched_uav_list}\n")
        gu_matched_s = {}
        uav_matched_s = {}
        num_gu_uav_sprt = math.ceil(len(unmatched_gu_l)/n_uav)
        # print(f"Max number of GUs each UAV can support: {num_gu_uav_sprt}\n")

        while len(unmatched_gu_l)>0:
            gu = unmatched_gu_l.pop(0)
            gu_preference_s = sorted_uavs_gus_s[gu]
            # print(f"{gu}'s preference set of UAVs: {gu_preference_s}")
            for uav in gu_preference_s.keys():

                if uav not in gu_matched_s.values():
                    # print(uav)
                    gu_matched_s[gu] = uav
                    uav_matched_s[uav] = [gu]
                    break
                elif len(uav_matched_s[uav]) < num_gu_uav_sprt:
                    gu_matched_s[gu] = uav
                    uav_matched_s[uav].append(gu)
                    break
                else:
                    score_matched_gu_s = {}
                    for matched_gu in uav_matched_s[uav]:
                        score_matched_gu_s[matched_gu] = score_gus_uavs[uav][matched_gu]
                    min_score_matched_gu = min(score_matched_gu_s, key=score_matched_gu_s.get)
                    # print("The UAV", uav)
                    # print("Min scored matched GU", min_score_matched_gu, "score", score_gus_uavs[uav][min_score_matched_gu])
                    # print("New GU", gu, "New GU score", score_gus_uavs[uav][gu])

                    if score_gus_uavs[uav][min_score_matched_gu] < score_gus_uavs[uav][gu]:
                        del gu_matched_s[min_score_matched_gu]
                        uav_matched_s[uav].remove(min_score_matched_gu)
                        gu_matched_s[gu] = uav
                        uav_matched_s[uav].append(gu)
                        unmatched_gu_l.append(min_score_matched_gu)
                        break
                    else:
                        continue

        print(f"GU matched set\n{gu_matched_s}\n")
        print(f"UAV matched set\n{uav_matched_s}\n")

        self.uav_matched_task_info = {}
        for uav in uav_matched_s:
            # print(uav)
            self.uav_matched_task_info[uav] = []
            for gu_s in uav_matched_s[uav]:
                # print(gus_task_set[gu_s])
                self.uav_matched_task_info[uav].append(gus_task_set[gu_s])

        print(self.uav_matched_task_info)

    def uav_task_info(self):
        return self.uav_matched_task_info


a = Association()
uav_task = a.uav_task_info()
print(uav_task)