import tkinter as tk
import random
import math

from gun import Gun

class Fire:

    def __init__(self, game):
        self.gun_dict = {}
        self.game = game
        self.ship_dict = game.ship_dict
        self.gun_dict = game.gun_dict
        self.ui = self.game.ui

        # 炮术等级
        self.fire_level = []

        # 炮术等级0：
        self.fire_level_0 = [[[0,500],[501,1000]],[[1001,1500],[1501,2000],[2001,2500]],[[2501,3000],[3001,3500],[3501,4000]],[[4501,5000],[5001,5500],[5501,6000],[6001,6500],[6501,7000]]]

        # 炮术等级0*
        self.fire_level_0star = [[[0,1000],[1001,2000]],[[2001,3000],[3001,4000],[4001,5000]],[[5001,6000],[7001,8000],[8001,9000]],[[9001,9500],[9501,10000],[10001,10500],[10501,11000],[11001,13000]]]

        self.range_level = []
    
    # 从数值上检查是否在射界内
    def is_in_angle(self, fire_angel, gun_angle):
        for angle in gun_angle:
            if float(angle[0]) <= float(fire_angel) <= float(angle[1]):
                return 1
        return 0

    def get_range_type(self, range, fire_level):
        # print(range, self.fire_level)
        for fire_range in fire_level:
            for rs in fire_range:
                if int(rs[0]) <= int(range) <= int(rs[1]):                    
                    # print(range, rs)
                    range_level1 = fire_level.index(fire_range) #近中远极限
                    range_level2 = fire_range.index(rs) #近1，近2，中1，中2
                    return (range_level1, range_level2)        
        return (9, 9) # 超射程

    # 根据射界左侧角度或射界右侧角度，来判定射击角度满足哪些射界类型
    def get_fire_acc(self, fire_angel):
        fireacc = []
        if fire_angel != "":
            fa = float(fire_angel)
            if 0 <= fa <= 180:
                fireacc.append("SS") # 右侧火炮射击角度在0-180度之间，射击精度为SS
            if 45 <= fa <= 135:
                fireacc.append("S") # 右侧火炮射击角度在45-135度之间，射击精度为S
            if 0 <= fa <= 135:
                fireacc.append("SW") # 右侧火炮射击角度在0-135度之间，射击精度为SW
            if 90 <= fa <= 180:
                fireacc.append("SQ") # 右侧火炮射击角度在90-180度之间，射击精度为SQ
            if 45 <= fa <= 180:
                fireacc.append("SA") # 右侧火炮射击角度在45-180度之间，射击精度为SA           
            if 0 <= fa <= 135:
                fireacc.append("F") # 右侧火炮射击角度在0-135度之间，射击精度为F
            if 0 <= fa <= 90:
                fireacc.append("SB") # 右侧火炮射击角度在0-90度之间，射击精度为SB
            if 45 <= fa <= 180:
                fireacc.append("A") # 右侧火炮射击角度在45-180度之间，射击精度为A
            if 0 <= fa <= 20:
                fireacc.append("B") # 右侧火炮射击角度在0-20度之间，射击精度为B
            if 160 <= fa <= 180:
                fireacc.append("St") # 右侧火炮射击角度在160-180度之间，射击精度为St
            if 180 <= fa <= 360:
                fireacc.append("PS") # 左侧火炮射击角度在0-180度之间，射击精度为PS
            if 225 <= fa <= 315:
                fireacc.append("P") # 左侧火炮射击角度在45-135度之间，射击精度为P
            if 225 <= fa <= 360:
                fireacc.append("PW") # 左侧火炮射击角度在0-135度之间，射击精度为PW
            if 180 <= fa <= 270:
                fireacc.append("PQ") # 左侧火炮射击角度在90-180度之间，射击精度为PQ
            if 180 <= fa <= 315:
                fireacc.append("PA") # 左侧火炮射击角度在45-180度之间，射击精度为PA           
            if 225 <= fa <= 360:
                fireacc.append("F") # 左侧火炮射击角度在0-135度之间，射击精度为F
            if 270 <= fa <= 360:
                fireacc.append("PB") # 左侧火炮射击角度在0-90度之间，射击精度为PB
            if 180 <= fa <= 315:
                fireacc.append("A") # 左侧火炮射击角度在45-180度之间，射击精度为A
            if 340 <= fa <= 360:
                fireacc.append("B") # 左侧火炮射击角度在0-20度之间，射击精度为B
            if 180 <= fa <= 200:
                fireacc.append("St") # 左侧火炮射击角度在160-180度之间，射击精度为St

        # print(fireacc)
        return fireacc

    # 获取命中率
    def get_hitacc(self, gunid, range, gun_dict):
        # print(gunid, range)
        # for gun in guns:
            # if gun[1] == gunname:

        # 获取命中表类型，炮术等级
        hit_table = self.game.ui.checkbox_ht_var.get()

        if gunid not in gun_dict:
            print(f"{gunid} + :没有gun数据")
            return # 如果gun_dict[gunid]不存在，则直接返回空
        
        if not gun_dict[gunid].size:
            print(f"{gunid} + :没有size数据")
            return
        
        gun_size = int(gun_dict[gunid].size)    

        if gun_size >= 201:
            fire_level_type = self.get_range_type(range, self.fire_level)
        else:
            fire_level_type = self.get_range_type(range, self.fire_level_0)
        
        hit_acc_dict = {
            (0, 0): (30,30,30,25),
            (0, 1): (25,25,20,18),
            (1, 0): (20,20,18,12),
            (1, 1): (18,18,16,8),
            (1, 2): (16,16,14,4),
            (2, 0): (14,12,10,2),
            (2, 1): (12,10,8,1),
            (2, 2): (10,8,6,0),
            (2, 3): (8,6,4,0),
            (3, 0): (6,4,2,0),
            (3, 1): (4,2,1,0),
            (3, 2): (2,1,0,0),
            (3, 3): (1,0,0,0),
            (3, 4): (0,0,0,0),
        } 
        # print(fire_level_type)
        # print(hit_acc_dict[fire_level_type])
        if fire_level_type == (9,9):
           return "超射程"
        if gun_size >= 201:
            return hit_acc_dict[fire_level_type][0]
        if gun_size >= 101:
            return hit_acc_dict[fire_level_type][1]
        if gun_size >= 55:
            return hit_acc_dict[fire_level_type][2]        
        if gun_size < 55:
            return hit_acc_dict[fire_level_type][3]        

    # 根据id获取该船是否被射击，是则返回0，否则返回2
    def get_shot(self, ui, shipid):
        # 从row2开始循环遍历每个row
        # 获取所有表格的row长度，这是由于grid_size()方法只能返回显示出来的表格，无法处理未显示的表格
        if len(self.ship_dict[shipid].be_fired_weapon_list) > 0:
            return 0
        else:
            return 2
        '''
        rows = set()
        for child in ui.inner_frame.grid_slaves():
            row = child.grid_info()['row']
            rows.add(row)
        num_rows = len(rows)

        for row in range(2, num_rows):
            slaves = ui.inner_frame.grid_slaves(row=row, column=8)
            if slaves and isinstance(slaves[0], tk.Entry) and slaves[0].get() == shipid:
                return 0
        return 2
        '''

    # 过度集中修正
    def get_concentration_correction(self, gunid, targetid, range_value):
        gun_size = int(self.gun_dict[gunid].size)
        if gun_size >= 201:
            fire_level_type = self.get_range_type(range_value, self.fire_level)
        else:
            fire_level_type = self.get_range_type(range_value, self.fire_level_0)
        # 射程中和近的，不受影响
        if fire_level_type[0] == 0 or fire_level_type[0] == 1:
            return 0
        gt = self.gun_dict[gunid].guntype
        if gt == "LG" or gt == "TT":
            return 0
        # print(gunid, targetid, range_value)
        # print(f"{self.ship_dict[targetid].be_fired_weapon_list}")
        
        # 目标舰被射击的武器id列表
        gun_list = self.ship_dict[targetid].be_fired_weapon_list

        # 射击武器的口径类型
        gunid_s = self.get_sizetype(gunid)
        # print(gunid_s)

        gun_list_copy = gun_list.copy()
        # 删除轻武器，因为它们不影响过度集中
        for lg in range(len(gun_list_copy)-1, -1, -1):
            gtype = self.gun_dict[gun_list[lg]].guntype
            if gtype == "LG" or gtype == "TT":
                del gun_list[lg]

        # print(gun_list)

        gun_list_copy = gun_list.copy()

        # 对gun_list里面的元素进行遍历，如果有同口径的，且属于同一船的，则删除
        delete_indices = []
        for i in range(len(gun_list) - 1, -1, -1):
            for j in range(i):
                if self.gun_dict[gun_list[i]].base_ship == self.gun_dict[gun_list[j]].base_ship and self.get_sizetype(gun_list[i]) == self.get_sizetype(gun_list[j]):
                    # print(f"删除{j}, {gun_list[j]}, {gun_list[i]}和{gun_list[j]}同属于{self.gun_dict[gun_list[i]].base_ship}，且口径类型都为{self.get_sizetype(gun_list[i])}")
                    delete_indices.append(j) 

        # 删除delete_indices中重复的元素
        delete_indices = list(set(delete_indices))

        # print(f"从{gun_list}中删除{delete_indices}")
        # 统一删除需要删除的元素
        for index in sorted(delete_indices, reverse=True):
            del gun_list[index]

        gunsize_list = [self.get_sizetype(gun) for gun in gun_list]
        # 计算gunid_s的出现次数，即有多少艘在集火，这里包含自己
        count = gunsize_list.count(gunid_s)
        if count < 1:
            print("过度集中get_concentration_correction计算有误")
            print(f"{gunid}对{targetid}的射击的过度集中修正有误{gun_list}")
            return 0
        if count == 1:
            return 0 
        #print(f"{gunid}对{targetid}的射击有{1-count}的过度集中修正")        
        #for g in gun_list:
        #    print(f"{g}_{self.gun_dict[g].name}_{self.gun_dict[g].base_ship}_{self.gun_dict[g].size}_{self.get_sizetype(g)}")
        return 1-count
    
    # 根据gunid获取gunsize，然后返回口径类型（命中同一列的）：
    def get_sizetype(self, gunid):
        s = int(self.gun_dict[gunid].size)
        if s >= 201:
            return 201
        if 200 >= s >= 101:
            return 101
        if 100 >= s >= 55:
            return 55
        if 54>= s:
            return 54

    # 舰船速度修正
    def get_speed_correction(self, shipspeed):
        if shipspeed:
            if int(shipspeed) <= 6:
                return 1
            if 6 < int(shipspeed) < 12:
                return 0
            if 12 <= int(shipspeed) < 18:
                return -1
            if 18 <= int(shipspeed) < 24:
                return -2    
            if 24 <= int(shipspeed):
                return -3
        return 0 

    # 转向修正
    def get_turning_correction(self, fire_acc, def_acc):
        if fire_acc and def_acc:
            if int(fire_acc) > 10 or int(def_acc) > 10 or (int(fire_acc) + int(def_acc)) > 10:
                return -2
            return 0
        return 0

    # 射速修正
    def get_firing_speed_correction(self, type):
        if "SL" in type:
            return -2    
        if type == "SF":
            return -2
        if type == "QF":
            return 2
        if type == "RF":
            return 4
        return 0

    # 吨位修正
    def get_tonnage_correction(self, shipsize):
        if shipsize == "B":
            return 1
        if shipsize == "E":
            return -1
        if shipsize == "F" or shipsize == "G":
            return -2
        return 0

    # 获取速度*着弹面修正
    def get_speed_hit_surface_correction(self, speed, angle):
        if speed and angle:
            speed = int(speed)
            acc = int(angle)
            if speed == 0:
                if acc < 20 or acc > 340 or 160 < acc < 200: 
                    return 2
                if 20 <= acc < 60 or 120 < acc <= 160 or 200 <= acc < 240 or 300 < acc <= 340:
                    return 3
                if 60 <= acc <= 120 or 240 <= acc <= 300:
                    return 3
            if 1 <= speed <= 6:
                if acc < 20 or acc > 340 or 160 < acc < 200: 
                    return 2
                if 20 <= acc < 60 or 120 < acc <= 160 or 200 <= acc < 240 or 300 < acc <= 340:
                    return 2
                if 60 <= acc <= 120 or 240 <= acc <= 300:
                    return 2
            if 7 <= speed <= 12:
                if acc < 20 or acc > 340 or 160 < acc < 200:  
                    return 1
                if 20 <= acc < 60 or 120 < acc <= 160 or 200 <= acc < 240 or 300 < acc <= 340:
                    return 1
                if 60 <= acc <= 120 or 240 <= acc <= 300:
                    return 0
            if 13 <= speed <= 18:
                if acc < 20 or acc > 340 or 160 < acc < 200:
                    return 0
                if 20 <= acc < 60 or 120 < acc <= 160 or 200 <= acc < 240 or 300 < acc <= 340:
                    return -1
                if 60 <= acc <= 120 or 240 <= acc <= 300:
                    return -2
            if 19 <= speed:
                if acc < 20 or acc > 340 or 160 < acc < 200: 
                    return -1
                if 20 <= acc < 60 or 120 < acc <= 160 or 200 <= acc < 240 or 300 < acc <= 340:
                    return -2
                if 60 <= acc <= 120 or 240 <= acc <= 300:
                    return -3

        return 0
    
    # 环境修正
    def get_environmental_correction(self, ship_id):
        smoke = int(self.ship_dict[ship_id].smoke)
        if smoke == 1:            
            # print(f"{ship_id}有-2烟雾修正")
            return -2
        else:
            return 0
    
    # 检定烟雾
    def set_ship_smoke(self, ship_id):
        if self.get_fire_101_5t(ship_id):
            i = self.generate_random(1,10)
            if i >= 7:
                self.ship_dict[ship_id].smoke = 1
                print(f"{ship_id}受烟雾影响")
        else:
            self.ship_dict[ship_id].smoke = 0

    # 获取舰船是否有101火炮连续5回合在射击
    def get_fire_101_5t(self, ship_id):
        # 如果回合数小于等于5，则不计算
        t = int(self.game.turn)
        if t <= 5:
            return False
        turnlist = [str(t-4), str(t-3), str(t-2), str(t-1), str(t-5)]
        for gunid in self.ship_dict[ship_id].weapon_ids:
            size = int(self.gun_dict[gunid].size)
            fire_list = self.gun_dict[gunid].fire_turns_record
            if size >= 101:
                if all(a in self.gun_dict[gunid].fire_turns_record for a in turnlist):
                    return True
        return False
    
    # 获取炮管数修正
    def get_gun_barrel_correction(self, fire_gun_id, hit_dict):
        barrel_num = 0
        # print(f"[test]{hit_dict[fire_gun_id]}") #[test]['C10_8', 'C10', '54', 'PS', 'J3', 2013, '335', '168', '14', '10', '0', '14']
        if self.gun_dict[fire_gun_id].used_for_barrel == 1:
            return 0
        elif int(self.gun_dict[fire_gun_id].size) >= 201:
            barrel_num = int(self.gun_dict[fire_gun_id].barrels_num)
        elif "SL" in self.gun_dict[fire_gun_id].type:
            barrel_num = int(self.gun_dict[fire_gun_id].barrels_num)
        else:
            fire_size = self.gun_dict[fire_gun_id].size
            fire_ship = self.gun_dict[fire_gun_id].base_ship
            target_ship = hit_dict[fire_gun_id][4]
            for gun_id, hit in hit_dict.items():
                used = self.gun_dict[gun_id].used_for_barrel
                if used == 1:
                    continue
                if gun_id == fire_gun_id:
                    barrel_num = barrel_num + int(self.gun_dict[gun_id].barrels_num)
                    # print(f"{fire_gun_id}, {gun_id}, {barrel_num}")
                    continue
                #同口径同船同目标
                if self.gun_dict[gun_id].size == fire_size and self.gun_dict[gun_id].base_ship == fire_ship and hit_dict[gun_id][4] == target_ship:
                    barrel_num = barrel_num + int(self.gun_dict[gun_id].barrels_num)
                    # print(f"{fire_gun_id}, {gun_id}, {barrel_num}")
                    # 设置为用过，在炮管数修正中
                    self.gun_dict[gun_id].used_for_barrel = 1    
        
        if barrel_num <= 2:
            return 0
        if barrel_num <= 4:
            return 1
        if barrel_num <= 6:
            return 2 
        if barrel_num <= 8:
            return 3      
        if barrel_num >= 9:
            return 4 
           
    # 获取轻炮命中修正
    def get_light_gun_correction(self, fire_gun_id):
        if self.gun_dict[fire_gun_id].guntype == "LG":
            fire_power = self.gun_dict[fire_gun_id].firepower
            if fire_power <= 1.0:
                return -1
            if fire_power <= 2.0:
                return 0
            if fire_power <= 4.0:
                return 1
            if fire_power <= 6.0:
                return 2
            if fire_power <= 8.0:
                return 3
            if fire_power <= 10.0:
                return 4
            if fire_power <= 12.0:
                return 5
            if fire_power > 12.0:
                return 6 
        else:
            return 0
        
    # 获取测距仪修正    
    def get_rangefinder_correction(self, gun_id, fire_range, fire_angle):
        if not self.gun_dict[gun_id].rangefinder:
            # print(f"没有测距仪")
            return 0
        elif int(fire_range) > 4000:
            # print(f"射程大于4000")
            return 0
        else:
            fire_range = int(fire_range)
            rangefinder = self.gun_dict[gun_id].rangefinder
            # print(rangefinder)
            rangefinder_data = rangefinder.strip().split(" ")
            rangefinder_angle = rangefinder_data[0]
            rangefinder_nums = rangefinder_data[1]
            rangefinder_type = rangefinder_data[2]
            if "/" in rangefinder_angle:
                rangefinder_set = rangefinder_angle.strip().split("/")
                for set in rangefinder_set:
                    set_angle = Gun.get_angel(set)
                    if self.is_in_angle(fire_angle, set_angle) == 1:
                        return 3
            else:
                rf_angle = Gun.get_angel(Gun,rangefinder_angle)
                if self.is_in_angle(fire_angle, rf_angle) == 1:
                    return 3
            return 0             

    # 计算所有修正
    def get_all_correction(self, hit_dict):

        fire_record_list = []

        for gunid, hit in hit_dict.items():
            # print(f"射界内{is_hit}")
            # hit: 0武器id、1射击舰id、2口径、3射界、4目标舰编号、5距离、6射击角、7着弹角、8射击舰速度、9射击转向、10受击转向、11受击速度、12row(计划射击不用）”
            # 获取基础命中
            hitacc = self.get_hitacc(hit[0], hit[5], self.gun_dict)
            # 获取是否被射击修正
            getshot = self.get_shot(self.ui, hit[1])
            # 获取速度修正
            speed_correction = self.get_speed_correction(hit[8])
            # 获取转向修正
            turning_correction = self.get_turning_correction(hit[9],hit[10])
            # 获取着弹面修正
            speed_hit_surface_correction = self.get_speed_hit_surface_correction(hit[11], hit[7])
            # 获取速度修正
            firing_speed_correction = self.get_firing_speed_correction(self.gun_dict[hit[0]].type)
            # 获取吨位修正
            tonnage_correction = self.get_tonnage_correction(self.ship_dict[hit[4]].size)
            # print(f"{hit[1]}->{hit[4]}, size:{self.ship_dict[hit[4]].size}, tonnage_correction:{tonnage_correction}")
            # 获取环境修正
            environmental_correction = self.get_environmental_correction(hit[1])
            # 获取过度集中修正
            concentration_correction = self.get_concentration_correction(gunid, hit[4], hit[5])  
            # 获取炮管数修正          
            gun_barrel_correction = self.get_gun_barrel_correction(gunid, hit_dict)
            # 获取轻炮修正
            light_gun_correction = self.get_light_gun_correction(gunid)
            # 获取测距仪修正
            rangefinder_correction = self.get_rangefinder_correction(hit[0], hit[5], hit[6])

            # 0射击舰ID,1受击舰ID,2武器名称,3射击角,4基础命中,5被射修正,6移速修正,7转向修正,8速度着弹面修正,9射速修正,10吨位修正,11武器id,12环境修正,13过度集中修正,14炮管数修正,15row,16轻炮修正，17测距仪修正,18射程
            fire_record = [hit[1], hit[4], self.gun_dict[hit[0]].name, self.gun_dict[hit[0]].angle_type, hitacc, getshot, speed_correction, turning_correction, speed_hit_surface_correction, firing_speed_correction, tonnage_correction, hit[0], environmental_correction, concentration_correction, gun_barrel_correction, hit[12], light_gun_correction, rangefinder_correction, hit[5]]    
            
            fire_record_list.append(fire_record)
        
        return fire_record_list        

    # 生成随机数
    def generate_random(self, min, max):
        if not isinstance(min, int) or not isinstance(max, int) or min < 0 or max < 0 or max <= min:
            raise ValueError("min and max must be positive integers and max must be greater than min")
        # random.seed(seed)
        random_int = random.randint(min, max)
        return random_int

    # 传入射击船id，目标船id，获取两者的射击角，受击角，射程
    def get_angles_distance(self, fire_ship_id, tagert_ship_id):
        # 获取船的坐标和方向
        att_x, att_y, att_d = float(self.ship_dict[fire_ship_id].x), float(self.ship_dict[fire_ship_id].y), int(self.ship_dict[fire_ship_id].direction)
        def_x, def_y, def_d = float(self.ship_dict[tagert_ship_id].x), float(self.ship_dict[tagert_ship_id].y), int(self.ship_dict[tagert_ship_id].direction)
        
        # 计算两船之间的距离
        distance = int(round(float( math.sqrt((att_x - def_x) ** 2 + (att_y - def_y) ** 2) * 10 )))# 坐标转码数 * 10

        # 计算两船之间的角度
        # att_angle = math.degrees(math.atan2(def_y - att_y, def_x - att_x)) - att_d
        att_angle = int(math.degrees(math.atan2(att_y - def_y, def_x - att_x)) - att_d)
        # print(math.degrees(math.atan2(att_y - def_y, def_x - att_x)))
        if att_angle < 0:
            att_angle += 360
        att_angle = 360 - att_angle # 从船头顺时针
        
        def_angle = int(math.degrees(math.atan2(def_y - att_y, att_x - def_x)) - def_d)

        if def_angle < 0:
            def_angle += 360
        def_angle = 360 - def_angle # 从船头顺时针

        return att_angle, def_angle, distance
    
    # 获取伤害值
    def get_damage(self, target, fire_range, ammo_list, gun_id, fire_phase):
        op, ip, gd = "No","No",0.0
        fire_range = int(fire_range)
        gun_size = int(self.gun_dict[gun_id].size)
        # 处理轻火炮的火力值带来的不同射程下的伤害
        if self.gun_dict[gun_id].guntype == "LG":
            lg_damage_dict = {
                (0, 1.0): [3,2,1],
                (1.1, 2.0): [5,4,2],
                (2.1, 4.0): [8,6,3],
                (4.1, 6.0): [11,9,4],
                (6.1, 8.0): [15,12,5],
                (8.1, 10.0): [20,16,6],
                (10.1, 12.0): [25,20,7],
                (12.1, 99): [30,25,8],
            }
            fp = float(self.gun_dict[gun_id].firepower)
            for r in lg_damage_dict:
                if  r[0] <= fp <= r[1]:
                    ld = lg_damage_dict[r]
            if fire_range <= 1000:
                d = ld[0]
            elif 1000 < fire_range <= 2500:
                d = ld[1]
            elif 2500 < fire_range <= 4500:
                d = ld[2]
            elif 4500 < fire_range <= 7000:
                d = 0     
            gd = d    

        # 非轻炮的伤害
        else:
            ammo = ammo_list.strip().split(" ")
            
            if gun_size >= 201:
                fire_level_type = self.get_range_type(fire_range, self.fire_level)
            else:
                fire_level_type = self.get_range_type(fire_range, self.fire_level_0)

            if fire_level_type[0] == 0:
                p = ammo[1]
                d = ammo[2]
            elif fire_level_type[0] == 1:
                p = ammo[3]
                d = ammo[4]
            elif fire_level_type[0] == 2:
                p = ammo[5]
                d = ammo[6]
            elif fire_level_type[0] == 3:
                p = ammo[7]
                d = ammo[8]

            ship_armor = int(self.ship_dict[target].armor1)
            p, d = int(p), float(d)
            if ship_armor == 0:
                ship_armor = 1
            if p > ship_armor * 10  and ship_armor <= 4:
                op = "Yes"
            if p > ship_armor:
                ip = "Yes"
            if p <= ship_armor:
                d = d * 0.1
            gd = d
        # print(fire_phase)
        if fire_phase == "反应射击":
            gd = float(gd) * 0.5
        return op, ip, gd
    
    # 获取暴击数量
    def get_ch_num(self, ship_id):
        current_damage = float(self.ship_dict[ship_id].current_damage)
        current_DP = float(self.ship_dict[ship_id].current_DP)
        if current_damage >= current_DP:
            print(f"{ship_id}已沉没")
            return 0
        damage_rate = current_damage / (current_DP - current_damage)
        # print(damage_rate,current_damage,current_DP,current_DP - current_damage)
        damage_rate_dict = {
            (0, 0.1): (0,0,0,0,0,1),
            (0.1, 0.2): (0,0,0,0,1,2),
            (0.2, 0.3): (0,0,0,1,2,3),
            (0.3, 0.4): (0,0,1,2,3,4),
            (0.4, 0.5): (0,1,2,3,4,5),
            (0.5, 0.6): (1,2,3,4,5,6),
            (0.6, 0.7): (2,3,4,5,6,7),
            (0.7, 0.8): (3,4,5,6,7,8),
            (0.8, 0.9): (4,5,6,7,8,9),
            (0.9, 1.0): (5,6,7,8,9,10),
            (1.0, 1.2): (6,7,8,9,10,11),
            (1.2, 1.4): (7,8,9,10,11,12),
            (1.4, 1.6): (8,9,10,11,12,13),
            (1.6, 1.8): (9,10,11,12,13,14),
            (1.8, 2.0): (10,11,12,13,14,15),
        }
        for r in damage_rate_dict:
            if r[0] <= damage_rate < r[1]:
                d = self.generate_random(1,6)
                print (f"{ship_id}的伤害比率为{damage_rate*100:.1f}%，暴击数判定骰点为{d}，暴击数为{damage_rate_dict[r][d-1]}")
                return damage_rate_dict[r][d-1]
        if damage_rate >= 2.0:
            diff = math.ceil((damage_rate - 2.0) / 0.2)
            d = self.generate_random(1,6)
            return damage_rate_dict[(1.8, 2.0)][d-1] + diff
    # 获取ch骰点的list
    def get_ch_rolls(self, ch_num):
        ch_rolls = []
        for i in range(ch_num):
            ch_rolls.append(self.generate_random(1,100))
        return ch_rolls

