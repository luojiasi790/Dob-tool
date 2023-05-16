

class Ship:
    def __init__(self,id,name,shipclass,displacement,standard_rudder,hard_rudder,standard_speedloss,hard_speedloss,accel_0_75,accel_76_100,decel,armor1,armor2,crew,size,propulsion,DP,speed,weapon1,weapon2,weapon3,weapon4,weapon5,weapon6,weapon7,weapon8,weapon9,light_gun,dp0,dp25,dp50,dp75,dp90,dp100,sp0,sp25,sp50,sp75,sp90,sp100,rangefinder):
        # 永久数据
        self.id = id
        self.name = name
        self.shipclass = shipclass
        self.displacement = displacement
        self.standard_rudder = standard_rudder
        self.hard_rudder = hard_rudder
        self.standard_speedloss = standard_speedloss
        self.hard_speedloss = hard_speedloss
        self.accel_0_75 = accel_0_75
        self.accel_76_100 = accel_76_100
        self.decel = decel
        self.armor1 = armor1
        self.armor2 = armor2
        self.crew = crew
        self.size = size
        self.propulsion = propulsion
        self.DP = DP
        self.speed = speed
        self.weapon1 = weapon1
        self.weapon2 = weapon2
        self.weapon3 = weapon3
        self.weapon4 = weapon4
        self.weapon5 = weapon5
        self.weapon6 = weapon6
        self.weapon7 = weapon7
        self.weapon8 = weapon8
        self.weapon9 = weapon9
        self.light_gun = light_gun
        self.dp0 = dp0
        self.dp25 = dp25
        self.dp50 = dp50
        self.dp75 = dp75
        self.dp90 = dp90
        self.dp100 = dp100
        self.sp0 = sp0
        self.sp25 = sp25
        self.sp50 = sp50
        self.sp75 = sp75
        self.sp90 = sp90
        self.sp100 = sp100
        self.rangefinder = rangefinder

        # 临时数组
        self.weapons = [] #将weapon1-9和light_gun重新修正后，放入数组
        self.weapon_ids = []

        # 临时数据
        self.current_DP = DP # 当前DP
        self.current_speed = speed # 当前速度
        self.team = 0 # 所属team
        self.current_total_turn = 0 #当前回合转向加总
        self.smoke = 0 # 烟雾影响，每回合计划阶段检查,0不影响，1影响
        self.current_damage = 0 #当前阶段受到的伤害

        # 当前坐标，颜色，朝向
        self.x = 0
        self.y = 0
        self.color = "white"
        self.direction = 0
        # 回合开始时的坐标，朝向
        self.start_x = 0
        self.start_y = 0
        self.start_direction = 0
        
        # 被射击的武器列表
        self.be_fired_weapon_list = []

        # 被命中列表
        self.be_hit_list = []
    
    def take_damage(self, damage):
        self.current_DP -= damage
    
    def change_speed(self, new_speed):
        self.current_speed = new_speed

if __name__ == '__main__':
    print("test ship.py")