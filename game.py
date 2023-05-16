import tkinter as tk
import tkinter.ttk as ttk

import cProfile

from map import Map
from ui import UI
from ship import Ship
from gun import Gun
from fire import Fire
from uiplan import UIPlan
from tkscrolledframe import ScrolledFrame
import getpass

class Game:  
    def __init__(self):
        self.is_running = False

        self.ship_dict = self.load_ship_dict()
        self.init_all_ship_weapons()
        self.gun_dict = self.load_gun_dict()
        # 初始化双方队伍的舰船id列表
        self.t1 = [] #red
        self.t2 = [] #yellow
        self.t3 = [] #blue

        # 初始化计划射击字典，gunid：targetshipid
        self.plan_fire_dict = {}
        self.plan_fire_list = []

        # 初始化反应射击列表
        self.reactive_fire_list = []

        self.map =  None
        self.fire = None
        self.ui = None
        self.uiplan = None # UIPlan(self)
        # 记录回合数
        self.turn = 1

    def start(self):
        self.is_running = True
        print('Game started.')

    def pause(self):
        self.is_running = False
        print('Game paused.')

    def resume(self):
        self.is_running = True
        print('Game resumed.')

    def game_over(self):
        self.is_running = False
        print('Game over.')

    # 从shipdata里面读取每行，生成一个ship的实例
    def read_ship_data(self):
        ships = []
        with open('shipdata.csv', 'r') as f:
            next(f) # 跳过第一行
            next(f) # 跳过第二行
            for line in f:
                try:
                    ship_data = line.strip().split(',')
                    # 创建船只对象
                    ship = Ship(*ship_data)
                    # 将船只对象添加到船只列表中
                    ships.append(ship)
                except:
                    print("Error: Could not create ship object from line: " + line)
        return ships

    # 将ship实例传入ship_dict字典
    def load_ship_dict(self):        
        self.ship_dict = {ship.id: ship for ship in self.read_ship_data()}        
        return self.ship_dict    

    # 添加一个ship对象
    def read_one_ship_data(self, shipid):
        with open('shipdata.csv', 'r') as f:
            next(f) # 跳过第一行
            next(f) # 跳过第二行
            for line in f:
                try:
                    ship_data = line.strip().split(',')
                    # 创建船只对象
                    if ship_data[0] == shipid:
                        ship = Ship(*ship_data)
                        return ship
                except:
                    print("Error: Could not create ship object from line: " + line)
        print (f"在shipdata.csv中找不到shipid:{shipid}")

    # 根据id将ship对象添加到ship_dict
    def add_ship_dict(self, shipid):
        if shipid not in self.ship_dict:
            self.ship_dict[shipid] = self.read_one_ship_data(shipid)

    # 读gundata.csv，重新创建gun实例
    def read_gun_data(self):
        guns = []
        # 读取gundata数据，获得武器的基础数据
        annex = {}
        with open('gundata.csv', 'r') as f:
            next(f) # 跳过第一行
            next(f) # 跳过第二行
            for line in f:
                try:
                    annex_data = line.strip().split(',')
                    # 将annex的name作为主键，annex_data作为值
                    annex[annex_data[1]] = annex_data
                except:
                    print("Error: Could not create gun object from line: " + line)
        for ship_id, ship in self.ship_dict.items():
            for index, weapon in enumerate(ship.weapons):             
                weapon_type = weapon[1]
                weapon_name = weapon[3]
                rangefinder = ""
                if "//" in weapon_name:
                    weapon_names = weapon_name
                    names = weapon_names.strip().split("//")
                    weapon_name = names[0]
                    rangefinder = names[1] 
                if weapon[1] == "MG":   
                    # print(weapon) # ('C1', 'MG', 'PS', 'Krupp 30.5cm RK L/22 C/76 C/Ge Exp', '2', 1)
                    # print(annex[weapon[3]]) # ['34', 'Krupp 30.5cm RK L/22 C/76 C/Ge Exp', '305', 'SL1', 'APp_18_16_16_16_14_15_11_15', 'Com_9_15_8_15_7_14_6_14', 'AP_30_17_26_17_22_16_19_15', 'Com_10_16_9_16_7_15_6_15', '']
                    # 0id,1name,2size,3type,4base_ship,5ammo1,6ammo2,7ammo3,8ammo4,9guntype,10angle_type,11barrels_num,12firepower,13cd
                    if len(annex[weapon_name][3]) >= 3:
                        cd = int(annex[weapon_name][3][2])
                    else:
                        cd = 0                        
                    ammo1,ammo2,ammo3,ammo4 = annex[weapon_name][4],annex[weapon_name][5],annex[weapon_name][6],annex[weapon_name][7]
                    gun = Gun(ship.id + "_" + str(index), weapon_name, annex[weapon_name][2], annex[weapon_name][3], ship.id, ammo1, ammo2, ammo3, ammo4, annex[weapon_name][8], weapon[2], weapon[4],0,1+cd,rangefinder)
                    ship.weapon_ids.append(gun.id)
                    guns.append(gun) 
                if weapon[1] == "LG":
                    # print(weapon) # ('C1', 'LG', 'SS', '2 3pdr 8 1pdr revolver ', 1.8, 'L')
                    gun = Gun(ship.id + "_" + str(index), weapon_name, "54", "RF", ship.id, "LG_HE", "LG_CP", "LG_Com", "LG_AP", "LG", weapon[2], "1", weapon[4], 1, rangefinder)               
                    ship.weapon_ids.append(gun.id)
                    guns.append(gun)
        return guns
    
    # 读取gun字典
    def load_gun_dict(self):
        gun_dict = {gun.id: gun for gun in self.read_gun_data()}
        return gun_dict
    
    # 初始化ship weapons
    def init_ship_weapons(self, ship_id):
        """
        根据shipid初始化shipweapons, ship_dict[shipid].weapons
        weapons依次为:MG/LG,射界,名称,炮管数
        """
        ship_weapons = [] #这个没用到
        # Get the ship object with the given ID
        ship = self.ship_dict.get(ship_id)    
        if ship:
            # Loop through the ship's weapon attributes and add them to the ship_weapons list
            for weapon_index, weapon in enumerate([ship.weapon1, ship.weapon2, ship.weapon3, ship.weapon4, ship.weapon5, ship.weapon6, ship.weapon7, ship.weapon8, ship.weapon9]):
                if weapon:
                    # Split the weapon attribute into its name and accuracy components
                    weapon_acc, weapon_name = weapon.split(' ', 1)
                    # Append the weapon name and accuracy to the ship_weapons list
                    weapon_acc_set, weapon_acc_tut_num = weapon_acc.split('(', 1)                
                    if '/' in weapon_acc_set:
                        weapon_acc_subset = []
                        weapon_acc_subset = weapon_acc_set.split('/')
                        #print (weapon_acc_subset)
                        for subset in weapon_acc_subset:
                            if subset[0].isdigit() and int(subset[0]) >= 2 and int(subset[0]) <= 9:
                                for i in range(int(subset[0])):
                                    ship.weapons.append((ship.id, "MG", subset[1:], weapon_name, weapon_acc_tut_num.split(')')[0], weapon_index+1))
                            else:
                                ship.weapons.append((ship.id, "MG", subset, weapon_name, weapon_acc_tut_num.split(')')[0], weapon_index+1))
                    else:
                        ship.weapons.append((ship.id, "MG", weapon_acc_set, weapon_name, weapon_acc_tut_num.split(')')[0], weapon_index+1))
            for lightgun in [ship.light_gun]:
                if lightgun:
                    lightgun_name, lightgun_power = lightgun.split('(', 1)
                    ship.weapons.append((ship.id, "LG", "SS", lightgun_name, float(lightgun_power[:-1])/2, "L"))
                    ship.weapons.append((ship.id, "LG", "PS", lightgun_name, float(lightgun_power[:-1])/2, "L"))

    #初始化所有ship的ship weapons
    def init_all_ship_weapons(self):
        for ship_id in self.ship_dict:
            self.init_ship_weapons(ship_id)  
            
    # 新建ship，初始化对象，添加到ship字典，添加到onmaplist
    def new_ship(self, shipid):
        # 初始化
        self.add_ship_dict(shipid)
        self.ui.on_map_ship_list.append(shipid)
        self.add_team(shipid)

    # 将shipid加入阵营，以便分配颜色和友军
    def add_team(self, shipid):
        # 如果t1为空，则该ship加入t1
        if not self.t1:
            self.t1.append(shipid)
            self.ship_dict[shipid].color = "red"
            self.ship_dict[shipid].team = 1
        # 如果t1非空，且ship与t1[0]首字母，相等，则加入t1，为友军
        elif shipid[0] == self.t1[0][0]:
            self.t1.append(shipid)
            self.ship_dict[shipid].color = "red"
            self.ship_dict[shipid].team = 1
        elif not self.t2:
            self.t2.append(shipid)
            self.ship_dict[shipid].color = "yellow"
            self.ship_dict[shipid].team = 2
        elif shipid[0] == self.t2[0][0]:
            self.t2.append(shipid)
            self.ship_dict[shipid].color = "yellow"
            self.ship_dict[shipid].team = 2           

    def main(self):
        '''
        password = getpass.getpass("输入口令: ")
        if password == "撞击吉野":
            print("口令正确")
        else:
            print("口令错误")
            return
        '''

        # 创建 Game 对象并启动游戏
        root = tk.Tk()
        root.geometry('1200x800')
        root.title('Dob Tool v0.1 By Jehuty')   

        # self.init_all_ship_weapons()       

        self.ui = UI(root, self)
        self.uiplan = UIPlan(root, self)
        self.map = Map(self.ui.map_sheet, width=100000, height=100000, game=game)
        self.map.pack()
        self.fire = Fire(self)

        root.mainloop()

if __name__ == '__main__':
        game = Game()
        # cProfile.run('game.main()')
        game.main()


    