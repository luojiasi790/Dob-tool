

class Gun:
    
    def __init__(self,id,name,size,type,base_ship,ammo1,ammo2,ammo3,ammo4,guntype,angle_type,barrels_num,firepower,cd,rangefinder):
        # 永久数据
        self.id = id
        self.name = name
        self.size = size
        self.type = type
        self.base_ship = base_ship # 所属船
        self.ammo1 = ammo1
        self.ammo2 = ammo2
        self.ammo3 = ammo3
        self.ammo4 = ammo4
        self.guntype = guntype # TT鱼雷 LG轻炮组
        self.angle_type = angle_type #射界类型
        self.barrels_num = barrels_num # 炮管数
        self.firepower = firepower # 轻炮火力
        self.cd = cd #射击的冷却时间，基本上都是1

        self.rangefinder = rangefinder # 火炮上的测距仪

        self.angle = self.get_angel(angle_type,id)

        self.ammo_list = self.get_ammo_list(ammo1, ammo2, ammo3, ammo4)
        #if self.ammo_list !=[]:
        #    print(self.ammo_list)

        # 临时数据
        self.current_status = 1 # 是否可用 1可用 0不可用
        self.current_fired = 0 # 是否已射击 0可射击 n剩余cd数
        self.fire_turns_record = [] #记录在哪些回合射击过
        self.used_for_barrel = 0 #记录被炮管数修正使用过 0 未被用过 1被用过

    # 从射击角度类型获得射击角度数值
    def get_angel(self, angle_type, *gun_id):
        angle = []
        angle_list={
            "SS" : [0,180],
            "S" : [45,135],
            "PS" : [180,360],
            "P" : [225,315],
            "SW" : [0,135],
            "SQ" : [90,180],
            "SA" : [45,180],
            "F" : [[0,135],[225,360]],
            "SB" : [0,90],
            "PB" : [270,360],
            "A" : [45,315],
            "B" : [[0,20],[340,360]],
            "St" : [160,200],            
            "PW" : [225,360],
            "PQ" : [180,270],
            "PA" : [180,315],
            "All" : [0,360]
        }    
        # J1，松岛主炮特殊处理
        if angle_type == "Casemate" and self.base_ship == "J1":
            angle_type = "F"
        # J2，严岛主炮特殊处理
        if angle_type == "Casemate" and self.base_ship == "J2":
            angle_type = "A"
        # J3，桥立主炮特殊处理
        if angle_type == "Casemate" and self.base_ship == "J3":
            angle_type = "A"

        # C1，C2定镇主炮特殊射界
        if gun_id == "C1_0" or gun_id == "C2_0":
            return [[180, 340]]
        if gun_id == "C1_1" or gun_id == "C2_1":
            return [[0, 160]]

        # print(angle_type)

        if "&" in angle_type:
            for angle_set in angle_type.split("&"):
                if all(isinstance(x, list) for x in angle_list[angle_set]):
                    for set in angle_list[angle_set]:
                        angle.append(set)
                else:
                    angle.append(angle_list[angle_set])
        elif angle_type == "Casemate":
            print(f"{self.base_ship} have Casemate")        
        
        elif all(isinstance(x, list) for x in angle_list[angle_type]):
            for set in angle_list[angle_type]:
                angle.append(set)
        else:
            angle.append(angle_list[angle_type])

        # print(f"{self.base_ship}: {self.name}: {self.angle_type}: {angle}")
        return angle
    
    def get_ammo_list(self, ammo1, ammo2, ammo3, ammo4):
        ammo_list = [] 
        if "_" in ammo1:
            ammo1_list = ammo1.strip().split("_")
            ammo_list.append(ammo1_list)    
        if "_" in ammo2:
            ammo2_list = ammo2.strip().split("_")
            ammo_list.append(ammo2_list)
        if "_" in ammo3:
            ammo3_list = ammo3.strip().split("_")
            ammo_list.append(ammo3_list)
        if "_" in ammo4:
            ammo4_list = ammo4.strip().split("_")
            ammo_list.append(ammo4_list)
        
        return ammo_list




    