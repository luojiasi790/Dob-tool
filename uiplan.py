import tkinter as tk
import tkinter.ttk as ttk
import math
import time

from ship import Ship
from map import Map
from fire import Fire
from tkscrolledframe import ScrolledFrame

# 计划射击的UI，显示和输入射击计划以及舰船速度
class UIPlan:
    def __init__(self, root, game):
        # 设定前一个打开的计划射击ui，用于打开新ui时判断关闭前一个计划射击ui
        self.prev_ui_plan = None

        self.game = game
        self.root = root # 传入主窗体root，以便刷新
        self.ship_dict = game.ship_dict
        self.gun_dict = game.gun_dict
        self.plan_fire_dict = game.plan_fire_dict
        self.plan_window = None

        self.ship_id = None

        self.target = "点击选择跟随目标"

    # 打开船的射击计划
    def open_ui_plan(self, shipid):      
        self.ship_id = shipid  
        # 如果存在上一个tip窗口，先关闭它
        if self.prev_ui_plan is not None:
            if self.prev_ui_plan.winfo_exists():    
                self.prev_ui_plan.destroy()

        self.plan_window = tk.Toplevel(self. root)
        self.plan_window.geometry('550x800+1300+200')
        self.plan_window.title(f"{shipid}计划")  
        
        self.prev_ui_plan = self.plan_window
        
        speed_label = tk.Label(self.plan_window, text=f"当前速度/DP/总转向:")
        speed_Entry =  tk.Entry(self.plan_window, width=8)
        speed_label.grid(row=1, column=0)
        speed_Entry.grid(row=1, column=1) 
        speed_Entry.insert(0, self.ship_dict[shipid].current_speed)       

        dp_Entry =  tk.Entry(self.plan_window, width=8)
        dp_Entry.grid(row=1, column=2)
        dp_Entry.insert(0, self.ship_dict[shipid].current_DP)

        turn_Entry =  tk.Entry(self.plan_window, width=8)
        turn_Entry.grid(row=1, column=3)
        turn_Entry.insert(0, self.ship_dict[shipid].current_total_turn)

        confirm_button = tk.Button(self.plan_window, text="保存计划", command=self.add_fire_plan)
        confirm_button.grid(row=2, column=0) 

        reset_button = tk.Button(self.plan_window, text="重置船只位置", command=self.reset_ship_position)
        reset_button.grid(row=2, column=1)

        follow_list = ["无目标"]
        follow_list = follow_list + self.game.ui.on_map_ship_list

        selected_follow_value = tk.StringVar()
        selected_follow_value.set("点击选择跟随目标") 

        follow_label = tk.Label(self.plan_window, text="跟随:")
        follow_label.grid(row=3, column=0)        
        follow_list = tk.OptionMenu(self.plan_window, selected_follow_value, *follow_list, command=lambda selected_value: self.get_follow(selected_value))
        follow_list.grid(row=3, column=1)
        follow_result = tk.Label(self.plan_window, text="请选择跟随目标")
        follow_result.grid(row=3, column=2)

        match_length = tk.Entry(self.plan_window, width=8)
        match_length.grid(row=4, column=0)
        match_button = tk.Button(self.plan_window, text="前进", command=self.uiplan_match)
        match_button.grid(row=4, column=1)
        turn_Entry = tk.Entry(self.plan_window, width=8)
        turn_Entry.grid(row=4, column=2)
        turn_button = tk.Button(self.plan_window, text="转向", command=self.uiplan_turn)
        turn_button.grid(row=4, column=3)

        # 生成可选目标
        if shipid in self.game.t1:
            tagert_list = self.game.t2
        if shipid in self.game.t2:
            tagert_list = self.game.t1  
        tagert_list.append("无目标")      
        
        rowid = 6

        selected_value = tk.StringVar()

        if shipid in self.plan_fire_dict:
            selected_value.set(self.plan_fire_dict[shipid]) 
        else:
            selected_value.set("点击选择射击目标")

        shipid_label = tk.Label(self.plan_window, text=f"{shipid}")
        shipname_label = tk.Label(self.plan_window, text=f"{self.ship_dict[shipid].name} 目标：")
        ship_menu = tk.OptionMenu(self.plan_window, selected_value, *tagert_list)
        shipid_label.grid(row=5, column=0)
        shipname_label.grid(row=5,column=1)
        ship_menu.grid(row=5, column=2)
        
        for gunid in self.ship_dict[shipid].weapon_ids:    
            selected_value = tk.StringVar()
            selected_value.set("点击选择目标")
            if gunid in self.plan_fire_dict:
                selected_value.set(self.plan_fire_dict[gunid])    
            
            ammo_list = self.gun_dict[gunid].ammo_list
            ammo_selected_value = tk.StringVar()
            if ammo_list != []:
                ammo_selected_value.set(ammo_list[0])
            else:
                ammo_list.append("无弹药")
                ammo_selected_value.set("无弹药")

            gunid_label = tk.Label(self.plan_window, text=f"{gunid}")
            gun_label = tk.Label(self.plan_window, text=f"{self.gun_dict[gunid].name[:12]}...>{self.gun_dict[gunid].angle_type}:")
            gun_menu = tk.OptionMenu(self.plan_window, selected_value, *tagert_list)
            ammo_menu = tk.OptionMenu(self.plan_window, ammo_selected_value, *ammo_list)
            gunid_label.grid(row=rowid, column=0)
            gun_label.grid(row=rowid, column=1)
            gun_menu.grid(row=rowid, column=2)
            ammo_menu.grid(row=rowid, column=3)
            rowid = rowid + 1
        
        # 在tip的关闭按钮上增加设置前一个tip为None
        def close_ui_plan_window():
            self.prev_ui_plan = None
            self.plan_window.destroy()

        self.plan_window.protocol("WM_DELETE_WINDOW", close_ui_plan_window)
    
    def add_fire_plan(self):
        # 保存当前速度,DP,总转向
        self.ship_dict[self.ship_id].current_speed = int(self.plan_window.grid_slaves(row=1, column=1)[0].get())
        self.ship_dict[self.ship_id].current_DP = float(self.plan_window.grid_slaves(row=1, column=2)[0].get())
        self.ship_dict[self.ship_id].current_total_turn = int(self.plan_window.grid_slaves(row=1, column=3)[0].get())

        # 保存射击计划
        for row in range(5, self.plan_window.grid_size()[1]):
            key = self.plan_window.grid_slaves(row=row, column=0)[0].cget('text')
            value = self.plan_window.grid_slaves(row=row, column=2)[0].cget('text')
            if value == "点击选择目标":
                continue
            self.plan_fire_dict[key] = value        
            # print(f"key:{key}, value:{value}")

    # 前进
    def uiplan_match(self):
        match_ma = self.plan_window.grid_slaves(row=4, column=0)[0].get()
        matchma = float(match_ma)
        self.game.map.move_ship(self.ship_id, matchma)
        # 更新当前跟随信息
        if self.target == "无目标" or self.target == "点击选择跟随目标":
            return
        self.get_follow(self.target)

    # 转向
    def uiplan_turn(self):        
        turn_angle = int(self.plan_window.grid_slaves(row=4, column=2)[0].get())
        self.game.map.turn_ship(self.ship_id, turn_angle)
        # 求turn_angle的绝对值
        self.ship_dict[self.ship_id].current_total_turn = int(self.ship_dict[self.ship_id].current_total_turn) + abs(turn_angle)
        self.plan_window.grid_slaves(row=1, column=3)[0].delete(0, 'end')
        self.plan_window.grid_slaves(row=1, column=3)[0].insert(0, self.ship_dict[self.ship_id].current_total_turn) 

        # 更新当前跟随信息
        if self.target == "无目标" or self.target == "点击选择跟随目标":
            return
        
        self.get_follow(self.target)        
    
    # 获取跟随目标的数据：距离和方向差
    def get_follow(self, target_id):

        if target_id == "无目标" or target_id == "点击选择跟随目标":
            return
        
        self.target = target_id

        fire_angle, def_angle, fire_range = self.game.fire.get_angles_distance(self.ship_id, target_id)
        print(f"fire_angle:{fire_angle}, def_angle:{def_angle}, fire_range:{fire_range}")
        if fire_angle > 180:
            fire_angle = fire_angle - 360

        match_len, turn_angle = self.game.ui.move_ship1_to_ship2(self.ship_id, target_id)
        print(f"match_len:{match_len}, turn_angle:{turn_angle}")
        
        # 如果要向后移动，则设置为0
        if match_len < 0:
            match_len = 0
            turn_angle = 0 - fire_angle

        self.plan_window.grid_slaves(row=4, column=0)[0].delete(0, tk.END)
        self.plan_window.grid_slaves(row=4, column=0)[0].insert(0, int(match_len))
        self.plan_window.grid_slaves(row=4, column=2)[0].delete(0, tk.END)
        self.plan_window.grid_slaves(row=4, column=2)[0].insert(0, turn_angle)
    
    # 重置ship位置
    def reset_ship_position(self):
        self.ship_dict[self.ship_id].x = self.ship_dict[self.ship_id].start_x
        self.ship_dict[self.ship_id].y = self.ship_dict[self.ship_id].start_y
        self.ship_dict[self.ship_id].direction = self.ship_dict[self.ship_id].start_direction

        self.ship_dict[self.ship_id].current_total_turn = 0
        self.plan_window.grid_slaves(row=1, column=3)[0].delete(0, 'end')
        self.plan_window.grid_slaves(row=1, column=3)[0].insert(0, 0) 

        self.game.map.reset_ship_position(self.ship_id)

        self.get_follow(self.target)



 