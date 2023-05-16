import tkinter as tk
import tkinter.ttk as ttk
import math
import time

from ship import Ship
from map import Map
from fire import Fire
from tkscrolledframe import ScrolledFrame

class UI:
    def __init__(self, root, game):
        # 传入的game实例处理
        self.game = game
        self.ship_dict = game.ship_dict
        # print(self.ship_dict["C1"].name)
        self.gun_dict = game.gun_dict

        self.dofire = game.fire

        # Map里面的ship list
        self.on_map_ship_list = []

        # 类变量，记录上一个tip窗口对象
        self.prev_tip = None
        # 类变量，记录上一个新建船只窗口对象
        self.prev_add_new_ship_window = None

        self.add_new_ship_window = None     

        # 初始化一个手动计划射击界面的武器列表按钮
        self.fire_gun_menu = None   
        # 初始化一个手动计划射击界面的目标列表按钮
        self.target_ship_menu = None

        # 记录武器命中记录
        self.hit_record = []
        # 记录被命中的ship列表
        self.be_hit_ship_list = []

        #设定一个添加船只按钮的默认column
        self.t1_button_column = 0
        self.t1_button_row = 2

        self.t2_button_column = 0
        self.t2_button_row = 4

        # 初始化命中率表格类别
        self.hit_tabel = ['0', '0*']

        #self.checkbox_false = tk.BooleanVar(value=False)
        #self.checkbox_true = tk.BooleanVar(value=True) 
        self.checkbox_var = tk.BooleanVar()
        # print(self.checkbox_false.get()) 

        # 生成页签
        self.notebook = ttk.Notebook(root) 

        self.map_sheet = ttk.Frame(self.notebook)
        self.plan_sheet = ttk.Frame(self.notebook)
        self.reactive_sheet = ttk.Frame(self.notebook)
        self.damage_sheet = ttk.Frame(self.notebook)

        self.notebook.add(self.map_sheet, text='Battle Map')
        self.notebook.add(self.plan_sheet, text='Plan Fire')
        self.notebook.add(self.reactive_sheet, text="Reactive Fire")
        self.notebook.add(self.damage_sheet, text="Damage Resolve")

        self.notebook.pack(expand=True, fill='both')

        # ======map页=======

        # map页签窗体上面加入菜单按钮区域
        self.menu_sf = ScrolledFrame(self.map_sheet, height=120)
        self.menu_sf.pack(side="top", fill="both", expand=True)

        # Bind the arrow keys to the scrolled frame
        self.menu_sf.bind_arrow_keys(self.map_sheet)
        self.menu_sf.bind_scroll_wheel(self.map_sheet)

        # Create a frame inside the scrolled frame for inner_frame
        self.menu_frame = self.menu_sf.display_widget(tk.Frame)

        add_ship_button = tk.Button(self.menu_frame, text="新建舰船", command=self.open_new_ship_window)
        add_ship_button.grid(row=0, column=0)

        load_turn_button = tk.Button(self.menu_frame, text="读取游戏", command=self.load_turn)
        load_turn_button.grid(row=0, column=1)

        save_turn_button = tk.Button(self.menu_frame, text="保存游戏", command=self.save_turn)
        save_turn_button.grid(row=0, column=2)

        edit_plan_button = tk.Button(self.menu_frame, text="删除计划", command=self.edit_plan)
        edit_plan_button.grid(row=0, column=3)

        smoke_button = tk.Button(self.menu_frame, text="判定烟雾", command=self.set_ships_smoke)
        smoke_button.grid(row=0, column=4)

        start_plan_fire_button = tk.Button(self.menu_frame, text="开始计划射击", command=self.start_plan_fire)
        start_plan_fire_button.grid(row=0, column=5)

        next_turn_button = tk.Button(self.menu_frame, text="下一回合", command=self.next_turn)
        next_turn_button.grid(row=0, column=6)

        game_turn = tk.Label(self.menu_frame, text="回合：")
        game_turn.grid(row=1, column=0)
        game_turn_entry = tk.Entry(self.menu_frame, width=6)
        game_turn_entry.grid(row=1,column=1)

        sea_state = tk.Label(self.menu_frame, text="海况：")
        sea_state.grid(row=1, column=2)
        sea_state_entry = tk.Entry(self.menu_frame, width=6)
        sea_state_entry.grid(row=1,column=3)

        sea_state = tk.Label(self.menu_frame, text="能见度：")
        sea_state.grid(row=1, column=4)
        sea_state_entry = tk.Entry(self.menu_frame, width=6)
        sea_state_entry.grid(row=1,column=5)

        self.checkbox_ht_var = tk.StringVar(value="0")

        hit_tabl_optionmenu = tk.OptionMenu(self.menu_frame, self.checkbox_ht_var, *self.hit_tabel, command=self.set_fire_level)
        hit_tabl_optionmenu.grid(row=1, column=6)

        # =====计划射击页=====
        # Create a scrolled frame for inner_frame
        self.inner_sf = ScrolledFrame(self.plan_sheet)
        self.inner_sf.pack(side="top", fill="both", expand=True)

        # Bind the arrow keys to the scrolled frame
        self.inner_sf.bind_arrow_keys(self.plan_sheet)
        self.inner_sf.bind_scroll_wheel(self.plan_sheet)

        # Create a frame inside the scrolled frame for inner_frame
        self.inner_frame = self.inner_sf.display_widget(tk.Frame)

        # Create a scrolled frame for record_frame
        self.record_sf = ScrolledFrame(self.plan_sheet)
        self.record_sf.pack(side="top", fill="both", expand=True)

        # Bind the arrow keys to the scrolled frame
        self.record_sf.bind_arrow_keys(self.plan_sheet)
        self.record_sf.bind_scroll_wheel(self.plan_sheet)

        # Create a frame inside the scrolled frame for record_frame
        self.record_frame = self.record_sf.display_widget(tk.Frame)

        # Create a button widget labeled "新增" and place it in the second row, left column of the window
        self.fire_button = tk.Button(self.inner_frame, text="执行计划", command=self.fire)
        self.fire_button.grid(row=0, column=1)

        self.resolve_button = tk.Button(self.inner_frame, text="结算命中", command=self.resolve_hit)
        self.resolve_button.grid(row=0, column=2)

        self.resolve_plan_damage_button = tk.Button(self.inner_frame, text="结算伤害", command=self.open_resolve_plan_damage)
        self.resolve_plan_damage_button.grid(row=0, column=3)

        label = tk.Label(self.inner_frame, text="||")
        label.grid(row=0, column=4)

        self.add_button = tk.Button(self.inner_frame, text="新增手动计划", command=self.add_row)
        self.add_button.grid(row=0, column=5)

        # Create a button widget labeled "保存" and place it in the second row, third column of the window
        self.save_button = tk.Button(self.inner_frame, text="保存计划", command=self.save)
        self.save_button.grid(row=0, column=6)

        # Create a button widget labeled "加载" and place it in the second row, fourth column of the window
        self.load_button = tk.Button(self.inner_frame, text="加载计划", command=self.load)
        self.load_button.grid(row=0, column=7)

        label = tk.Label(self.inner_frame, text="||")
        label.grid(row=0, column=8)

        self.clear_inner_frame_button = tk.Button(self.inner_frame, text="清空计划", command=self.clear_inner_frame)
        self.clear_inner_frame_button.grid(row=0, column=9)

        self.clear_record_frame_button = tk.Button(self.inner_frame, text="清空命中", command=self.clear_record_frame)
        self.clear_record_frame_button.grid(row=0, column=10)

        # Define the label texts
        label_texts = ["射击舰", "射击武器", "射击角", "速度", "转向", "距离", "受击舰", "受击角", "速度", "转向", "切换目标"]

        # Create and place the labels using a loop
        for i, text in enumerate(label_texts):
            label = tk.Label(self.inner_frame, text=text, width=6)
            label.grid(row=1, column=i+1)

        label_texts = ["是否射击","射击ID","射击舰名","受击ID","受击舰名","武器ID","武器名称","朝向","命中骰点","最终命中","基础命中", "环境修正","被射修正","集中修正","移速修正","转向修正","射速修正","测距仪修正","炮管修正","速度*着弹面修正","吨位修正","轻炮修正","加总修正","射程"]

        # Create and place the labels using a loop
        for i, text in enumerate(label_texts):
            label = tk.Label(self.record_frame, text=text)
            label.grid(row=1, column=i)

        # =====反应射击页=====

        # 在反应射击页签里面创建窗体
        self.replan_sf = ScrolledFrame(self.reactive_sheet)
        self.replan_sf.pack(side="top", fill="both", expand=True)

        # Bind the arrow keys to the scrolled frame
        self.replan_sf.bind_arrow_keys(self.reactive_sheet)
        self.replan_sf.bind_scroll_wheel(self.reactive_sheet)

        # Create a frame inside the scrolled frame for inner_frame
        self.replan_frame = self.replan_sf.display_widget(tk.Frame)

        open_reactive_button = tk.Button(self.replan_frame, text="打开反应", command=self.open_reactive_hit)
        open_reactive_button.grid(row=0, column=0)

        do_reactive_button = tk.Button(self.replan_frame, text="执行反应", command=self.do_reactive_hit)
        do_reactive_button.grid(row=0, column=1)

        resolve_reactive_button = tk.Button(self.replan_frame, text="结算命中", command=self.resolve_reactive_hit)
        resolve_reactive_button.grid(row=0, column=2)

        open_resolve_reactive_damage_button = tk.Button(self.replan_frame, text="结算伤害", command=self.open_resolve_reactive_damage)
        open_resolve_reactive_damage_button.grid(row=0, column=3)

        label = tk.Label(self.replan_frame, text="||")
        label.grid(row=0, column=4)

        clear_reactive_button = tk.Button(self.replan_frame, text="清除反应", command=self.clear_reactive_hit)
        clear_reactive_button.grid(row=0, column=5)

        label_texts = ["是否射击", "射击ID","射击舰名","武器ID","武器名称","武器射界","可选目标","---","---","命中骰点","最终命中","基础命中", "环境修正","被射修正","集中修正","移速修正","转向修正","射速修正","测距仪修正","炮管修正","速度*着弹面修正","吨位修正","轻炮修正", "加总修正"]

        # Create and place the labels using a loop
        for i, text in enumerate(label_texts):
            label = tk.Label(self.replan_frame, text=text)
            label.grid(row=1, column=i)

        # ==========伤害结算页面=============

        # Create a scrolled frame for damage_frame
        self.damage_sf = ScrolledFrame(self.damage_sheet)
        self.damage_sf.pack(side="top", fill="both", expand=True)

        # Bind the arrow keys to the scrolled frame
        self.damage_sf.bind_arrow_keys(self.damage_sheet)
        self.damage_sf.bind_scroll_wheel(self.damage_sheet)

        # Create a frame inside the scrolled frame for damage_frame
        self.damage_frame = self.damage_sf.display_widget(tk.Frame)

        open_resolve_list_button = tk.Button(self.damage_frame, text="打开结算", command=self.open_resolve_list)
        open_resolve_list_button.grid(row=0, column=0)

        resolve_damage_button = tk.Button(self.damage_frame, text="结算伤害", command=self.resolve_damage)
        resolve_damage_button.grid(row=0, column=1)

        resolve_critical_hit_button = tk.Button(self.damage_frame, text="结算暴击", command=self.resolve_critical_hit)
        resolve_critical_hit_button.grid(row=0, column=2)

        update_damage_button = tk.Button(self.damage_frame, text="更新伤害", command=self.update_damage)    
        update_damage_button.grid(row=0, column=3)

        label = tk.Label(self.damage_frame, text="||")
        label.grid(row=0, column=4)

        clear_resolve_list = tk.Button(self.damage_frame, text="清除结算", command=self.clear_resolve_list)
        clear_resolve_list.grid(row=0, column=5)
        
        label_texts = ["目标ID", "目标名称", "射击阶段", "射击舰ID", "射击舰名","射程", "武器ID", "武器名称", "命中骰点", "最终命中", "弹药类型", "是否过穿", "是否穿甲", "伤害", "总伤害", "暴击数量", "暴击骰点"]

        # Create and place the labels using a loop
        for i, text in enumerate(label_texts):
            label = tk.Label(self.damage_frame, text=text)
            label.grid(row=1, column=i+1)

    # 模拟加载中的装饰器
    def loading(func):
        def wrapper(*args, **kwargs):
            print("Loading...")
            time.sleep(1)  # 模拟加载中
            result = func(*args, **kwargs)
            return result
        return wrapper

    #在inner_frame增加纯entry的列
    def add_entry_row(self):
        current_rows = self.inner_frame.grid_size()[1]
        for i in range(10):
            new_entry = tk.Entry(self.inner_frame, width=6)
            new_entry.grid(row=current_rows, column=i+1)

    #在inner_frame增加一列，手动计划射击表
    def add_row(self):
        # Get the current number of rows
        current_rows = self.inner_frame.grid_size()[1]

        self.fire_ship = None
        
        fire_ship_list = self.on_map_ship_list
        if not fire_ship_list:
            print("图中没有舰船")
            return
        selected_value = tk.StringVar(value="选择射击舰船")
        fire_ship_menu = tk.OptionMenu(self.inner_frame, selected_value, *fire_ship_list, command=lambda ship_id: self.set_fire_ship(ship_id))
        fire_ship_menu.grid(row=current_rows, column=1)    

        self.fire_gun_list = ["默认全部武器"]
        self.gun_selected_value = tk.StringVar()
        self.gun_selected_value.set("默认全部武器")
        self.fire_gun_menu = tk.OptionMenu(self.inner_frame, self.gun_selected_value, *self.fire_gun_list)
        self.fire_gun_menu.grid(row=current_rows, column=2) 

        self.target_ship_list = ["请选择目标"]
        self.target_selected_value = tk.StringVar()
        self.target_selected_value.set("请选择目标")
        self.target_ship_menu = tk.OptionMenu(self.inner_frame, self.target_selected_value, *self.target_ship_list)
        self.target_ship_menu.grid(row=current_rows, column=7) 

        for i in [3,4,5,6,8,9,10]:
            new_entry = tk.Entry(self.inner_frame, width=6)
            new_entry.grid(row=current_rows, column=i)

    # 根据选择的射击船ip,刷新可用武器和目标
    def set_fire_ship(self, shipid):
        # 根据选择的射击船ip，刷新可用武器列表
        weapon_ids = self.ship_dict[shipid].weapon_ids
        self.fire_gun_list.clear()
        self.fire_gun_list.extend(weapon_ids)
        if self.fire_gun_menu:
            self.fire_gun_menu['menu'].delete(0, 'end')
        self.fire_gun_menu['menu'].add_command(label="默认全部武器", command=tk._setit(self.gun_selected_value, "默认全部武器"))
        for weapon_id in self.fire_gun_list:
            self.fire_gun_menu['menu'].add_command(label=f"{weapon_id}:{self.gun_dict[weapon_id].name}_{self.gun_dict[weapon_id].angle_type}", command=tk._setit(self.gun_selected_value, weapon_id))
        
        # 根据选择的射击船ip，刷新可用目标列表
        if shipid in self.game.t1:
            ship_list = self.game.t2
        if shipid in self.game.t2:
            ship_list = self.game.t1
        self.target_ship_list.clear()
        self.target_ship_list.extend(ship_list)
        if self.target_ship_menu:
            self.target_ship_menu['menu'].delete(0, 'end')
        for ship_id in self.target_ship_list:
            self.target_ship_menu['menu'].add_command(label=f"{ship_id}:{self.ship_dict[ship_id].name}", command=tk._setit(self.target_selected_value, ship_id))
            
    # 在inner_frame的row行11列处添加一个可选按钮，用于选择射击目标被阻挡时切换目标
    def add_select_target_widget(self, rowid, select_list):
        select_target_list = select_list

        selected_value = tk.StringVar(value=select_list[0])
        select_target_menu = tk.OptionMenu(self.inner_frame, selected_value, *select_target_list, command=lambda selected_value, row=rowid: self.reset_fire(row, selected_value))
        select_target_menu.grid(row=rowid, column=11)  
    
    # 重设inner_frame的row行的各种射击数据
    def reset_fire(self, row, selected_value):
        fire_ship = self.inner_frame.grid_slaves(row=row, column=1)[0].get()
        def_ship = selected_value # self.inner_frame.grid_slaves(row=row, column=11)[0].cget('text')
        if def_ship == "跳过" or def_ship == "跳过或可选":
            return
        def_speed = self.ship_dict[def_ship].current_speed 
        def_turn = self.ship_dict[def_ship].current_total_turn
        fire_item = self.get_other_ships_position(fire_ship, def_ship)        
        # self.inner_frame.grid_slaves(row=row, column=1)[0].insert(0, fire_ship_id)
        # self.inner_frame.grid_slaves(row=row, column=2)[0].insert(0, fire_gun_id)
        self.inner_frame.grid_slaves(row=row, column=3)[0].delete(0, 'end')
        self.inner_frame.grid_slaves(row=row, column=3)[0].insert(0, fire_item[1])
        # self.inner_frame.grid_slaves(row=row, column=4)[0].insert(0, fire_speed)
        # self.inner_frame.grid_slaves(row=row, column=5)[0].insert(0, fire_turn)
        self.inner_frame.grid_slaves(row=row, column=6)[0].delete(0, 'end')
        self.inner_frame.grid_slaves(row=row, column=6)[0].insert(0, int(fire_item[2]))
        self.inner_frame.grid_slaves(row=row, column=7)[0].delete(0, 'end')
        self.inner_frame.grid_slaves(row=row, column=7)[0].insert(0, def_ship)
        self.inner_frame.grid_slaves(row=row, column=8)[0].delete(0, 'end')
        self.inner_frame.grid_slaves(row=row, column=8)[0].insert(0, fire_item[3])
        self.inner_frame.grid_slaves(row=row, column=9)[0].delete(0, 'end')
        self.inner_frame.grid_slaves(row=row, column=9)[0].insert(0, def_speed)
        self.inner_frame.grid_slaves(row=row, column=10)[0].delete(0, 'end')
        self.inner_frame.grid_slaves(row=row, column=10)[0].insert(0, def_turn)

    # 根据fire_record，在record_frame中添加列，将各种命中修正填入该列各项中
    def add_fire_record(self, fire_record):
        # Get the current number of rows
        current_rows = self.record_frame.grid_size()[1]   
        # print(f"{fire_record[1]}: {fire_record}")     

        # 初始化各个修正值
        # 0射击舰ID，1受击舰ID，2武器名称,3射击角,4基础命中,5被射修正,6移速修正,7转向修正,8速度着弹面修正,9射速修正,10吨位修正,11武器id,12环境修正

        basic_hit = fire_record[4] # 基础命中
        environmental_correction = fire_record[12] # 环境修正        
        shot_correction = fire_record[5] # 被射修正
        concentration_correction = fire_record[13] # 集中修正
        speed_correction = fire_record[6] # 移速修正
        turning_correction = fire_record[7] # 转向修正
        firing_speed_correction = fire_record[9] # 射速修正
        rangefinder_correction = fire_record[17] # 测距仪修正
        gun_barrel_correction = fire_record[14] # 炮管修正
        light_gun_correction = fire_record[16] # 轻炮修正
        speed_hit_surface_correction = fire_record[8] # 速度着弹面修正 
        tonnage_correction = fire_record[10] # 吨位修正
        total_correction = 0 # 加总修正 
        final_hit = 0 # 最终命中
        hit_dice = self.game.fire.generate_random(1,100) # 命中骰点
        weapon_id = fire_record[11] #武器id
        fire_range = fire_record[18] #射程
        
        self.var = tk.BooleanVar()
        # 是否射击的勾选框，默认除鱼雷外都勾选
        
        if "aw" in fire_record[2]:
            new_checkbox = tk.Checkbutton(self.record_frame, variable=self.var)
            new_checkbox.deselect()
        else:
            new_checkbox = tk.Checkbutton(self.record_frame, variable=self.var)
            new_checkbox.select()
        '''
        new_checkbox = tk.Checkbutton(self.record_frame, variable=self.var)
        
        new_checkbox.select()
        '''
        new_checkbox.v = self.var
        new_checkbox.grid(row=current_rows, column=0)
        # print(new_checkbox.v.get())

        # 射击舰ID和名称
        new_entry = tk.Label(self.record_frame,width=6)
        new_entry.grid(row=current_rows, column=1)
        new_entry.config(text=fire_record[0])        
        new_entry = tk.Label(self.record_frame,width=6)
        new_entry.grid(row=current_rows, column=2)
        new_entry.config(text=self.ship_dict[fire_record[0]].name)
        # 受击舰ID和名称
        new_entry = tk.Label(self.record_frame,width=6)
        new_entry.grid(row=current_rows, column=3)
        new_entry.config(text=fire_record[1])        
        new_entry = tk.Label(self.record_frame,width=6)
        new_entry.grid(row=current_rows, column=4)
        new_entry.config(text=self.ship_dict[fire_record[1]].name)    
        # 武器ID
        new_entry = tk.Label(self.record_frame,width=6)
        new_entry.grid(row=current_rows, column=5)
        new_entry.config(text=weapon_id)
        # 武器名称
        new_entry = tk.Label(self.record_frame)
        new_entry.grid(row=current_rows, column=6)
        new_entry.config(text=fire_record[2][:12], anchor='w')
        # 射击朝向
        new_entry = tk.Label(self.record_frame,width=6)
        new_entry.grid(row=current_rows, column=7)
        new_entry.config(text=fire_record[3])
        # 基础命中
        new_entry = tk.Entry(self.record_frame,width=6)
        new_entry.grid(row=current_rows, column=10)
        new_entry.insert(0, basic_hit)
        # 环境修正
        new_entry = tk.Entry(self.record_frame,width=6)
        new_entry.grid(row=current_rows,column=11)
        new_entry.insert(0, environmental_correction)
        # 射击修正
        new_entry = tk.Entry(self.record_frame,width=6)
        new_entry.grid(row=current_rows,column=12)
        new_entry.insert(0, shot_correction)
        # "集中修正",
        new_entry = tk.Entry(self.record_frame,width=6)
        new_entry.grid(row=current_rows,column=13)
        new_entry.insert(0, concentration_correction)
        # "移速修正",
        new_entry = tk.Entry(self.record_frame,width=6)
        new_entry.grid(row=current_rows,column=14)
        new_entry.insert(0, speed_correction)
        # "转向修正",
        new_entry = tk.Entry(self.record_frame,width=6)
        new_entry.grid(row=current_rows,column=15)
        new_entry.insert(0, turning_correction)
        # "射速修正",
        new_entry = tk.Entry(self.record_frame,width=6)
        new_entry.grid(row=current_rows,column=16)
        new_entry.insert(0, firing_speed_correction)
        # "测距仪修正",
        new_entry = tk.Entry(self.record_frame,width=6)
        new_entry.grid(row=current_rows,column=17)
        new_entry.insert(0, rangefinder_correction)
        # "炮管修正",
        new_entry = tk.Entry(self.record_frame,width=6)
        new_entry.grid(row=current_rows,column=18)
        new_entry.insert(0, gun_barrel_correction)
        # "速度*着弹面修正",
        new_entry = tk.Entry(self.record_frame,width=8)
        new_entry.grid(row=current_rows,column=19)
        new_entry.insert(0, speed_hit_surface_correction)
        # "吨位修正",
        new_entry = tk.Entry(self.record_frame,width=6)
        new_entry.grid(row=current_rows,column=20)
        new_entry.insert(0, tonnage_correction)
        # "轻炮修正",
        new_entry = tk.Entry(self.record_frame,width=6)
        new_entry.grid(row=current_rows,column=21)
        new_entry.insert(0, light_gun_correction)
        # "加总修正",
        new_entry = tk.Entry(self.record_frame,width=6)
        new_entry.grid(row=current_rows,column=22)
        new_entry.insert(0, total_correction)
        # "最终命中",
        new_entry = tk.Entry(self.record_frame,width=6)
        new_entry.grid(row=current_rows,column=9)
        new_entry.insert(0, final_hit)
        # "命中骰点"
        new_entry = tk.Entry(self.record_frame,width=6)
        new_entry.grid(row=current_rows,column=8)
        new_entry.insert(0, hit_dice)
        # 射程
        new_entry = tk.Entry(self.record_frame,width=6)
        new_entry.grid(row=current_rows,column=23)
        new_entry.insert(0, fire_range)        

    # 射击，生成射击记录
    def fire(self):
        print("fire")
        noblock = 1 #标记，为1代表没有需要调整射击目标的，为0则代表需要调整射击目标 
        # 遍历inner_frame的每一行
        self.hit_record = []
        self.hit_dict = {}
        for row in range(2, self.inner_frame.grid_size()[1]):            
            col = 1
            widget = self.inner_frame.grid_slaves(row=row, column=col)[0]
            # 如果有可选目标，可选目标为友军，则跳过，可选目标为敌军，则将敌舰设定为可选目标
            if self.inner_frame.grid_slaves(row=row, column=11):
                selecte_target = self.inner_frame.grid_slaves(row=row, column=11)[0].cget('text')
                if selecte_target == "跳过" or selecte_target == "跳过或可选":
                    continue
                else:
                    def_ship = selecte_target

            # "射击舰", "射击武器", "射击角", "速度", "转向", "距离", "受击舰", "受击角", "速度", "转向", "切换目标"
            if isinstance(widget, tk.Entry):
                fire_ship = self.inner_frame.grid_slaves(row=row, column=col)[0].get()
                fire_weapon = self.inner_frame.grid_slaves(row=row, column=col+1)[0].get()
                def_ship = self.inner_frame.grid_slaves(row=row, column=col+6)[0].get()
            elif isinstance(widget, tk.OptionMenu):
                fire_ship = self.inner_frame.grid_slaves(row=row, column=col)[0].cget('text')
                fire_weapon = self.inner_frame.grid_slaves(row=row, column=col+1)[0].cget('text')
                def_ship = self.inner_frame.grid_slaves(row=row, column=col+6)[0].cget('text')

            fire_angle = self.inner_frame.grid_slaves(row=row, column=col+2)[0].get()
            fire_speed = self.inner_frame.grid_slaves(row=row, column=col+3)[0].get()
            fire_acc = self.inner_frame.grid_slaves(row=row, column=col+4)[0].get()

            fire_range = int(round(float(self.inner_frame.grid_slaves(row=row, column=col+5)[0].get())))    
                            
            def_angle = self.inner_frame.grid_slaves(row=row, column=col+7)[0].get()
            def_speed = self.inner_frame.grid_slaves(row=row, column=col+8)[0].get()
            def_acc = self.inner_frame.grid_slaves(row=row, column=col+9)[0].get()

            ship_weapons = []
            fire_acc_set = []

            # 获取ship的可用目标列表
            avaible_tagert_list = self.get_avaible_tagert(fire_ship)
            avaible_ships = [sub_array[0] for sub_array in avaible_tagert_list]

            if def_ship not in avaible_ships:
                # print(f"{fire_ship}射击的{def_ship}不是有效的目标")
                noblock = 0
                # 获取阻碍船
                block_ship = self.get_block_ship(fire_ship, def_ship)
                # 如果获取的阻碍船是友军，则跳过
                if self.ship_dict[block_ship].color == self.ship_dict[fire_ship].color:
                    print(f"{fire_ship}射击的{def_ship}时，阻挡船{block_ship}是友军，无法切换射击阻挡船")
                    self.add_select_target_widget(row, ["跳过"])
                    continue
                # 如果获取的阻碍船是敌军，则新增可选目标
                else:
                    print(f"{fire_ship}射击的{def_ship}时，阻挡船{block_ship}是敌军，可切换射击阻挡船")
                    self.add_select_target_widget(row, ["跳过或可选",block_ship])
                    continue

            def_hit_angle = def_angle

            ship_weapons = self.ship_dict[fire_ship].weapon_ids

            fire_angle_set = self.game.fire.get_fire_acc(fire_angle)                
            
            if not ship_weapons:
                print(fire_ship + self.ship_dict[fire_ship].name + ":武器数据为空")
                continue

            self.ship_dict[def_ship].be_fired_weapon_list = []

            fire_record = []

            # 如果是全舰射击
            if fire_weapon == "默认全部武器":
                for gunid in ship_weapons: 
                    # 跳过鱼雷
                    if self.gun_dict[gunid].guntype == "TT":
                        # print(f"{gunid},{self.gun_dict[gunid].name},{self.gun_dict[gunid].type}")
                        continue
                    # 跳过CD中的武器
                    if self.gun_dict[gunid].current_fired >= 1:
                        continue
                    # print(self.gun_dict[subset].name)
                    # 重设炮管数修正为未被使用过
                    self.gun_dict[gunid].used_for_barrel = 0
                    is_hit = self.game.fire.is_in_angle(fire_angle, self.gun_dict[gunid].angle)
                    # print(is_hit)
                    # print(subset) # ('C6', 'MG', 'F', '克虏伯21厘米RK L/30 C/84 C/德出口', '2')
                    # print(self.gun_dict[subset].angle_type)
                    if is_hit == 1: # self.gun_dict[subset].angle_type in fire_angle_set:
                        # 1射击舰编号（C1J1这种）、2口径、3射界、4目标舰编号、5距离、6射击角、7着弹角、8射击舰速度，9射击转向，10受击转向,，11受击速度”
                        hit = [gunid,fire_ship,self.gun_dict[gunid].size,self.gun_dict[gunid].angle_type,def_ship,fire_range,fire_angle,def_angle,fire_speed,fire_acc,def_acc,def_speed,0]
                        # print(hit)
                        self.hit_record.append(hit)  
                        self.hit_dict[gunid] = hit
                        self.ship_dict[def_ship].be_fired_weapon_list.append(gunid)
                    else:
                        continue
                        print(f"{fire_ship}的{gunid}无法射击到{def_ship}")
            # 如果是单独武器射击
            else:  
                # 重设炮管数修正为未被使用过
                self.gun_dict[gunid].used_for_barrel = 0
                # 跳过鱼雷
                if self.gun_dict[fire_weapon].guntype == "TT":
                    continue
                # 跳过CD中的武器
                if self.gun_dict[gunid].current_fired >= 1:
                    continue
                # print(self.gun_dict[subset].name)
                is_hit = self.game.fire.is_in_angle(fire_angle, self.gun_dict[fire_weapon].angle)
                # print(is_hit)
                # print(subset) # ('C6', 'MG', 'F', '克虏伯21厘米RK L/30 C/84 C/德出口', '2')
                # print(self.gun_dict[subset].angle_type)
                if is_hit == 1: # self.gun_dict[subset].angle_type in fire_angle_set:
                    # hit: 0武器id、1射击舰id、2口径、3射界、4目标舰编号、5距离、6射击角、7着弹角、8射击舰速度、9射击转向、10受击转向、11受击速度、12row(计划射击不用）”
                    hit = [fire_weapon,fire_ship,self.gun_dict[fire_weapon].size,self.gun_dict[fire_weapon].angle_type,def_ship,fire_range,fire_angle,def_angle,fire_speed,fire_acc,def_acc,def_speed,0]
                    self.hit_record.append(hit)  
                    self.hit_dict[fire_weapon] = hit
                    self.ship_dict[def_ship].be_fired_weapon_list.append(fire_weapon)     
                elif fire_weapon in self.hit_dict: 
                    del self.hit_dict[fire_weapon]
                    print(f"一个{fire_weapon}无法射击到{def_ship}")

        # 如果不需要调整射击目标，则射击
        if noblock == 1:
            '''
            for gunid, hit in self.hit_dict.items():
                # print(f"射界内{is_hit}")
                # 获取基础命中
                hitacc = self.dofire.get_hitacc(hit[0], hit[5], self.gun_dict)
                # 获取是否被射击修正
                getshot = self.dofire.get_shot(self, hit[1])
                # 获取速度修正
                speed_correction = self.dofire.get_speed_correction(hit[8])
                # 获取转向修正
                turning_correction = self.dofire.get_turning_correction(hit[9],hit[10])
                # 获取着弹面修正
                speed_hit_surface_correction = self.dofire.get_speed_hit_surface_correction(hit[11], hit[7])
                # 获取速度修正
                firing_speed_correction = self.dofire.get_firing_speed_correction(self.gun_dict[hit[0]].type)
                # 获取吨位修正
                tonnage_correction = self.dofire.get_tonnage_correction(self.ship_dict[hit[1]].size)
                # 获取环境修正
                environmental_correction = self.dofire.get_environmental_correction(hit[1])
                # 获取过度集中修正
                concentration_correction = self.dofire.get_concentration_correction(gunid, hit[4], hit[5])  
                # 获取炮管数修正          
                gun_barrel_correction = self.dofire.get_gun_barrel_correction(gunid, self.hit_dict)

                # 0射击舰ID,1受击舰ID,2武器名称,3射击角,4基础命中,5被射修正,6移速修正,7转向修正,8速度着弹面修正,9射速修正,10吨位修正,11武器id,12环境修正,13过度集中修正,14炮管数修正
                fire_record = [hit[1], hit[4], self.gun_dict[hit[0]].name, self.gun_dict[hit[0]].angle_type, hitacc, getshot, speed_correction, turning_correction, speed_hit_surface_correction, firing_speed_correction, tonnage_correction, hit[0], environmental_correction, concentration_correction, gun_barrel_correction]    
            '''    
            fire_record_list = self.game.fire.get_all_correction(self.hit_dict)

            for fire_record in fire_record_list:
                self.add_fire_record(fire_record)  

    def save(self):
        with open("firesave.txt", "w") as f:
            f.write("")
        # Loop through each row starting from the third row
        for row in range(2, self.inner_frame.grid_size()[1]):
            # Get the entry widget in the second column of the current row
            entry = self.inner_frame.grid_slaves(row=row, column=2)[0]
            row_text = ""
            # Check if the entry widget is not empty
            if isinstance(entry, tk.Entry) and entry.get() != "":
                # Get the text content of each widget in the current row and join them with commas
                for col in range(1,19):
                    widgets = self.inner_frame.grid_slaves(row=row, column=col)
                    if widgets and isinstance(widgets[0], tk.Entry):
                        widget = widgets[0]
                        # print(f"row={row}, col={col}, widget={widget.get()}")
                        row_text = row_text + ',' + widget.get()
                    else:
                        # print(f"widgets is Null")            
                        row_text = row_text + ',' + ""
                # Open the save.txt file in append mode and write the row text followed by a newline character
                with open("firesave.txt", "a") as f:
                    f.write(row_text + "\n")     
        with open("hitrecord.txt", "w") as f:
            for hit in self.hit_record:
                f.write(",".join(map(str, hit)) + "\n")  

    # 读取射击存档，firesave.txt
    def load(self):
            # Delete all rows starting from the third row
        for row in range(2, self.inner_frame.grid_size()[1]):
            for col in range(self.inner_frame.grid_size()[0]):
                # Get the widget in the current row and column and destroy it
                if self.inner_frame.grid_slaves(row=row, column=col):
                    self.inner_frame.grid_slaves(row=row, column=col)[0].destroy()

        # Read the contents of save.txt file in the current directory
        with open("firesave.txt", "r") as f:
            # Loop through the remaining lines and insert them into the grid
            for line in f:
                # Split the line into a list of values
                values = line.strip().split(",")
                # Insert a new row into the grid
                self.add_row()
                # Loop through the values and insert them into the widgets in the current row
                for col, value in enumerate(values):
                    if self.inner_frame.grid_slaves(row=self.inner_frame.grid_size()[1]-1, column=col):
                        self.inner_frame.grid_slaves(row=self.inner_frame.grid_size()[1]-1, column=col)[0].insert(0, value)
        

    def clear_inner_frame(self):
        # Delete all rows starting from the third row
        for row in range(2, self.inner_frame.grid_size()[1]):
            for col in range(self.inner_frame.grid_size()[0]):
                # Get the widget in the current row and column and destroy it
                if self.inner_frame.grid_slaves(row=row, column=col):
                    self.inner_frame.grid_slaves(row=row, column=col)[0].destroy()

    # 【结算命中】按钮，结算record_frame的结果，写入plan_hit_record.txt
    def resolve_hit(self):        
        for row in range(2, self.record_frame.grid_size()[1]):
            row_total = 0
            gun_id = self.record_frame.grid_slaves(row=row, column=5)[0].cget('text')
            if self.gun_dict[gun_id].used_for_barrel == 1:
                # 射击后重置cd
                self.gun_dict[gun_id].current_fired = self.gun_dict[gun_id].cd
                self.record_frame.grid_slaves(row=row, column=9)[0].config(state="readonly")
                continue
            for col in range(11, 22):
                if self.record_frame.grid_slaves(row=row, column=col):
                    # print(record_frame.grid_slaves(row=row, column=col)[0].get())
                    row_total += int(self.record_frame.grid_slaves(row=row, column=col)[0].get())
                    # print(f"{gun_id}加总:{str(row_total)}")
            if self.record_frame.grid_slaves(row=row, column=22):
                # record_frame.grid_slaves(row=row, column=21)[0].configure(state='normal')
                self.record_frame.grid_slaves(row=row, column=22)[0].delete(0, 'end')
                self.record_frame.grid_slaves(row=row, column=22)[0].insert(0, str(row_total * 2))
                # record_frame.grid_slaves(row=row, column=21)[0].configure(state='readonly')
            # 计算最终命中
            if self.record_frame.grid_slaves(row=row, column=9):
                final_hit = int(self.record_frame.grid_slaves(row=row, column=10)[0].get()) + row_total * 2
                self.record_frame.grid_slaves(row=row, column=9)[0].delete(0, 'end')
                self.record_frame.grid_slaves(row=row, column=9)[0].insert(0, str(final_hit))
            
            # 获取位于 record_frame 网格中第 row 行和第 0 列的复选框部件
            checkbox = self.record_frame.grid_slaves(row=row, column=0)[0]

            # 打印复选框的值
            # print("Checkbox value:", checkbox.v.get())
            if checkbox.v.get() == True:                
                gunid = self.record_frame.grid_slaves(row=row, column=5)[0].cget("text")
                # 射击后重置cd
                self.gun_dict[gunid].current_fired = self.gun_dict[gunid].cd                
                turn = int(self.game.turn)
                if turn not in self.gun_dict[gunid].fire_turns_record:
                    self.gun_dict[gunid].fire_turns_record.append(turn)   

        with open("plan_hit_record.txt", "w") as f:
            for hit in self.hit_record:
                f.write(",".join(map(str, hit)) + "\n")     
                    
    # 清除record_frame的内容
    def clear_record_frame(self):
        print("clear_record_frame")
        for row in range(2, self.record_frame.grid_size()[1]):
            for col in range(self.record_frame.grid_size()[0]):
                if self.record_frame.grid_slaves(row=row, column=col):
                    self.record_frame.grid_slaves(row=row, column=col)[0].destroy()
    
    # 读取游戏回合信息，重新从gamesave.txt读取战场上的ship，从fireplan.txt去读取射击计划，从gunfiresave.txt读火炮射击记录
    def load_turn(self):        
        # self.battle_map.clear_objects() 
        self.game.map.clear_objects()
        self.on_map_ship_list = [] 
        # 初始化双方队伍的舰船id列表
        self.game.t1 = [] #red
        self.game.t2 = [] #yellow
        self.game.t3 = [] #blue
        
        # 清除menu的船只按钮，重置船只按钮的初始位置
        for row in range(2, self.menu_frame.grid_size()[1]):
            for col in range(self.menu_frame.grid_size()[0]):
                if self.menu_frame.grid_slaves(row=row, column=col):
                    self.menu_frame.grid_slaves(row=row, column=col)[0].destroy()
        self.t1_button_column = 0
        self.t1_button_row = 2
        self.t2_button_column = 0
        self.t2_button_row = 4

        # 读取游戏存档
        with open("gamesave.txt", "r") as f:
            # 跳过两行注释
            f.readline()
            f.readline()
            # 第一行特殊处理
            first_line = f.readline().strip().split(",")
            turn = first_line[0]
            sea = first_line[1]
            visible = first_line[2]
            hit_table = first_line[3]

            self.game.turn = turn

            self.menu_frame.grid_slaves(row=1, column=1)[0].delete(0, 'end')
            self.menu_frame.grid_slaves(row=1, column=1)[0].insert(0, str(turn))

            self.menu_frame.grid_slaves(row=1, column=3)[0].delete(0, 'end')
            self.menu_frame.grid_slaves(row=1, column=3)[0].insert(0, str(sea))

            self.menu_frame.grid_slaves(row=1, column=5)[0].delete(0, 'end')
            self.menu_frame.grid_slaves(row=1, column=5)[0].insert(0, str(visible))

            # self.menu_frame.grid_slaves(row=1, column=6)[0].configure(text='')
            self.checkbox_ht_var.set(hit_table)
            
            self.set_fire_level(hit_table)

            # 第二行开始处理ship信息
            for line in f:
                # Split the line into a list of values
                values = line.strip().split(",")
                shipid = values[0]
                # 生成ship对象
                self.game.new_ship(shipid)
                # self.on_map_ship_list.append(shipid)
                self.ship_dict[shipid].x = values[1]
                self.ship_dict[shipid].y = values[2]
                self.ship_dict[shipid].color = values[3]
                self.ship_dict[values[0]].direction = values[4]
                self.ship_dict[values[0]].current_DP = values[5]
                self.ship_dict[values[0]].current_speed = values[6]
                self.ship_dict[values[0]].current_total_turn = values[7]
                self.ship_dict[values[0]].smoke = values[8]
                self.ship_dict[values[0]].start_x = values[9]
                self.ship_dict[values[0]].start_y = values[10]
                self.ship_dict[values[0]].start_direction = values[11]

                self.zoom(self.ship_dict[values[0]].id)
                # 地图上绘制舰船
                self.game.map.add_ship(shipid)
        
        # 读取射击计划存档
        with open("fireplan.txt", "r") as f:
            # self.battle_map.fire_plan_list = []
            self.game.plan_fire_list = []
            for line in f:
                if line.strip() == "":
                    continue
                # print(line)
                fire_plan = list(map(str, line.strip().split(",")))
                # print(fire_plan)
                # self.battle_map.fire_plan_list.append(fire_plan)
                self.game.plan_fire_list.append(line)
                if fire_plan[1] == "默认全部武器":
                    self.game.plan_fire_dict[fire_plan[0]] = str(fire_plan[6])  
                    # print(fire_plan[0])
                    # print(self.game.plan_fire_dict[fire_plan[0]])
                else:
                    self.game.plan_fire_dict[fire_plan[1]] = str(fire_plan[6]) 
                    # print(fire_plan[1]) 
                    # print(self.game.plan_fire_dict[fire_plan[1]])                

        # 读取Gun临时数据存档
        with open("gunfiresave.txt", "r") as f:
            f.readline()
            for line in f:
                gun = line.strip().split(",")
                # print(gun[0])
                self.gun_dict[gun[0]].current_status = int(gun[1]) # 可用状态
                self.gun_dict[gun[0]].current_fired = int(gun[2]) # cd
                # 射击回合记录
                self.gun_dict[gun[0]].fire_turns_record = []
                if "_" in gun[3]:
                    for tset in gun[3].strip().split(("_")):
                        self.gun_dict[gun[0]].fire_turns_record.append(tset)
                elif gun[3]:
                    self.gun_dict[gun[0]].fire_turns_record.append(gun[3])               

    # 保存游戏回合信息，保存到gamesave.txt，fireplan.txt，gunfiresave.txt
    def save_turn(self):
        with open("gamesave.txt", "w") as f:
            f.write(f"turn,sea,visible,,,,\n")
            f.write(f"id,x,y,color,direction,current_dp,currend_speed,current_total_turn,smoke,start_x,start_y,start_direction\n")
            turn = self.menu_frame.grid_slaves(row=1, column=1)[0].get()
            sea = self.menu_frame.grid_slaves(row=1, column=3)[0].get()
            visible =  self.menu_frame.grid_slaves(row=1, column=5)[0].get()
            hit_table = self.checkbox_ht_var.get()

            self.game.turn = turn

            f.write(f"{turn},{sea},{visible},{hit_table}\n")
            for ship_tag in self.on_map_ship_list:
                ship = self.ship_dict[ship_tag]
                f.write(f"{ship_tag},{ship.x},{ship.y},{ship.color},{ship.direction},{ship.current_DP},{ship.current_speed},{ship.current_total_turn},{ship.smoke},{ship.start_x},{ship.start_y},{ship.start_direction}\n")  
        
        # 保存射击计划
        with open("fireplan.txt", "w") as f:
            # for fire_plan in self.battle_map.fire_plan_list:
            for fire_plan in self.game.plan_fire_list:                
                f.write(fire_plan + "\n") # 这样写会包含[]和单引号，因为它是list
                # f.write(','.join(fire_plan) + '\n')

        # 保存武器临时状态
        with open("gunfiresave.txt", "w") as f:
            f.write(f"武器id,武器当前可用状态,武器当前CD状态,已射击回合\n")
            for gun_id, gun in self.gun_dict.items():
                turns_record = "_".join(map(str, gun.fire_turns_record))
                # print(turns_record)
                f.write(f"{gun_id},{gun.current_status},{gun.current_fired},{turns_record}\n")

    # 点击后窗体挪到ship的坐标处
    def zoom(self, ship_tag):
        x =  float(self.ship_dict[ship_tag].x)
        y = float(self.ship_dict[ship_tag].y)
        if x < 500 and y < 500:
            # self.battle_map.xview_moveto(0)
            # self.battle_map.yview_moveto(0)  
            self.game.map.xview_moveto(0) 
            self.game.map.yview_moveto(0)          
            return
        
        canvas_width = 100000
        canvas_height = 100000

        canvas_x = x-400
        canvas_y = y-200

        # self.battle_map.xview_moveto(canvas_x / canvas_width)
        # self.battle_map.yview_moveto(canvas_y / canvas_height)
        # self.battle_map.update()
        self.game.map.xview_moveto(canvas_x / canvas_width)
        self.game.map.yview_moveto(canvas_y / canvas_height)
        self.game.map.update()

    # 打开ship的tip窗体
    def open_tip(self, ship_tag):
        # 如果存在上一个tip窗口，先关闭它
        if self.prev_tip is not None:
            if self.prev_tip.winfo_exists():                
                self.prev_tip.destroy()

        tip = tk.Tk()
        tip.geometry('500x800+800+200')
        tip.title(ship_tag)  

        self.prev_tip = tip
        # Create labels for ship ID and name
        dp_rate = float(self.ship_dict[ship_tag].current_DP) / float(self.ship_dict[ship_tag].DP)
        id_label = tk.Label(tip, text=f"[ID]{self.ship_dict[ship_tag].id}[船名]{self.ship_dict[ship_tag].name}[当前DP]{self.ship_dict[ship_tag].current_DP}[DP比率]{dp_rate*100:.1f}%", anchor="w")
        move_label =  tk.Label(tip, text=f"[航速]{self.ship_dict[ship_tag].current_speed}节[航向]{self.ship_dict[ship_tag].direction}[总转向]{self.ship_dict[ship_tag].current_total_turn}[烟雾]{self.ship_dict[ship_tag].smoke}", anchor="w")

        # Position labels using grid
        id_label.grid(row=0, column=0)
        move_label.grid(row=1, column=0)
        
        weapons = self.ship_dict[ship_tag].weapon_ids

        for weid, weapon in enumerate(weapons):
            if self.gun_dict[weapon].current_status == 1:
                available = "[可用]"
            if self.gun_dict[weapon].current_status == 0:
                available = "[不可用]"
            """
            if self.gun_dict[weapon].current_fired == 1:
                isfired = "[未射击]"
            if self.gun_dict[weapon].current_fired == 0:
                isfired = "[已射击]" 
            """
            weapon_label = tk.Label(tip, text=f"{weapon}[武器]{self.gun_dict[weapon].name}[朝向{self.gun_dict[weapon].angle_type}]=>{available}[CD{self.gun_dict[weapon].current_fired}]", anchor="w")
            weapon_label.grid(row=weid+5, column=0)

        # 在tip的关闭按钮上增加设置前一个tip为None
        def close_tip():
            self.prev_tip = None
            tip.destroy()

        tip.protocol("WM_DELETE_WINDOW", close_tip)


    # 点击船名按钮，打开的内容
    def open_ship_menu(self, ship_tag):
        self.zoom(ship_tag)
        self.open_tip(ship_tag)
        self.game.uiplan.open_ui_plan(ship_tag)
        # self.battle_map.show_menu(ship_tag)

    # Map页签上的计划射击按钮，点击后将射击计划转到计划射击页签，并填入数值
    def start_plan_fire(self):
        self.notebook.select(self.plan_sheet)        
        # for fire_plan in self.battle_map.fire_plan_list:
        fire_plan_list = list(self.game.plan_fire_dict.items())
        self.game.plan_fire_list = []
        print(fire_plan_list)

        for fire_plan in fire_plan_list:
            
            if fire_plan[1] == '点击选择目标':
                print(f"{fire_plan[0]}未选择目标")
                continue

            tagert_ship_id = fire_plan[1]
            # 武器射击的话
            if "_" in fire_plan[0]:
                fire_gun_id = fire_plan[0]
                fire_ship_id = self.gun_dict[fire_gun_id].base_ship    
            # 全舰射击的话            
            else:
                fire_ship_id = fire_plan[0]
                fire_gun_id = "默认全部武器"

            att_angle, def_angle, distance = self.game.fire.get_angles_distance(fire_ship_id, tagert_ship_id)

            fire_speed = self.ship_dict[fire_ship_id].current_speed
            fire_turn = self.ship_dict[fire_ship_id].current_total_turn
            def_speed = self.ship_dict[tagert_ship_id].current_speed
            def_turn = self.ship_dict[tagert_ship_id].current_total_turn

            self.add_entry_row()

            # "射击舰", "射击武器", "射击角", "速度", "转向", "距离", "受击舰", "受击角", "速度", "转向"            

            self.inner_frame.grid_slaves(row=self.inner_frame.grid_size()[1]-1, column=1)[0].insert(0, fire_ship_id)
            self.inner_frame.grid_slaves(row=self.inner_frame.grid_size()[1]-1, column=2)[0].insert(0, fire_gun_id)
            self.inner_frame.grid_slaves(row=self.inner_frame.grid_size()[1]-1, column=3)[0].insert(0, att_angle)
            self.inner_frame.grid_slaves(row=self.inner_frame.grid_size()[1]-1, column=4)[0].insert(0, fire_speed)
            self.inner_frame.grid_slaves(row=self.inner_frame.grid_size()[1]-1, column=5)[0].insert(0, fire_turn)
            self.inner_frame.grid_slaves(row=self.inner_frame.grid_size()[1]-1, column=6)[0].insert(0, distance)
            self.inner_frame.grid_slaves(row=self.inner_frame.grid_size()[1]-1, column=7)[0].insert(0, tagert_ship_id)
            self.inner_frame.grid_slaves(row=self.inner_frame.grid_size()[1]-1, column=8)[0].insert(0, def_angle)
            self.inner_frame.grid_slaves(row=self.inner_frame.grid_size()[1]-1, column=9)[0].insert(0, def_speed)
            self.inner_frame.grid_slaves(row=self.inner_frame.grid_size()[1]-1, column=10)[0].insert(0, def_turn)

            fire_plan = ",".join([str(fire_ship_id), str(fire_gun_id), str(att_angle), str(fire_speed), str(fire_turn), str(distance), str(tagert_ship_id), str(def_angle), str(def_speed), str(def_turn)])
            self.game.plan_fire_list.append(fire_plan)
            #print(fire_plan)
            #print(self.game.plan_fire_list)

    def set_ships_smoke(self):
        #判定每艘船的烟雾状态
        for ship_id, ship in self.ship_dict.items(): 
            self.game.fire.set_ship_smoke(ship_id)

    def edit_plan(self):
        # self.battle_map.edit_plan()
        self.game.map.edit_plan()
        # print("edit plan")

    def clear_reactive_hit(self):
        print("clear_replan_frame")
        for row in range(2, self.replan_frame.grid_size()[1]):
            for col in range(self.replan_frame.grid_size()[0]):
                if self.replan_frame.grid_slaves(row=row, column=col):
                    self.replan_frame.grid_slaves(row=row, column=col)[0].destroy()

    # @loading #打开反应射击列表
    def open_reactive_hit(self):
        print("打开反应射击列表open_reactive_hit")
        for gun_id, gun in self.gun_dict.items(): 
            if gun.base_ship in self.on_map_ship_list:
                # print(f"{gun.id}, {gun.base_ship}, {gun.current_fired}")
                # 跳过鱼雷
                if gun.guntype == "TT":
                    continue
                # 生成可选目标
                avaible_tagert_list = self.get_avaible_tagert(gun.base_ship)
                inangle_tagert_list = self.get_inangle_tagert(gun_id, avaible_tagert_list)

                selected_value = tk.StringVar()
                # 跳过无可选目标的
                if inangle_tagert_list:
                    selected_value.set(inangle_tagert_list[0])                    
                    inangle_tagert_list.append("不反应射击")                    
                else:
                    selected_value.set("No targets available")
                    continue

                # 如果CD结束了
                if gun.current_fired <= 0:
                    # print(gun_id)
                    current_rows = self.replan_frame.grid_size()[1]

                    self.var = tk.BooleanVar()
                    # 是否射击的勾选框，默认除鱼雷外都勾选
                    
                    if "aw" in gun.name:
                        new_checkbox = tk.Checkbutton(self.replan_frame, variable=self.var)
                        new_checkbox.deselect()
                    else:
                        new_checkbox = tk.Checkbutton(self.replan_frame, variable=self.var)
                        new_checkbox.select()

                    new_checkbox.v = self.var
                    new_checkbox.grid(row=current_rows, column=0)

                    new_entry = tk.Label(self.replan_frame)
                    new_entry.grid(row=current_rows, column=1)
                    new_entry.config(text=gun.base_ship)

                    new_entry = tk.Label(self.replan_frame)
                    new_entry.grid(row=current_rows, column=2)
                    new_entry.config(text=self.ship_dict[gun.base_ship].name)
                    # 射击武器id
                    new_entry = tk.Label(self.replan_frame)
                    new_entry.grid(row=current_rows, column=3)
                    new_entry.config(text=gun_id)
                    # 射击武器名称
                    new_entry = tk.Label(self.replan_frame)
                    new_entry.grid(row=current_rows, column=4)
                    new_entry.config(text=gun.name[:12])
                    # 射击武器射界类型
                    new_entry = tk.Label(self.replan_frame)
                    new_entry.grid(row=current_rows, column=5)
                    new_entry.config(text=gun.angle_type)

                    selected_value.set(inangle_tagert_list[0])  # Set the default value

                    # 可选目标列表按钮
                    option_menu = tk.OptionMenu(self.replan_frame, selected_value, *inangle_tagert_list)
                    option_menu.grid(row=current_rows, column=6)

                    # Create and place new entry widgets in the new row
                    new_row = []
                    for i in range(15):
                        new_entry = tk.Entry(self.replan_frame, width=6)
                        new_entry.grid(row=current_rows, column=9+i)
                        new_row.append(new_entry)

    # 执行反应射击
    def do_reactive_hit(self):
        print("执行反应射击do_reactive_hit")
        hit_record = []
        hit_dict = {}
        reactive_hit_list = []
        for row in range(2, self.replan_frame.grid_size()[1]):
            # 获取位于 replan_frame 网格中第 row 行和第 0 列的复选框部件
            checkbox = self.replan_frame.grid_slaves(row=row, column=0)[0]
            # 勾选框如果为勾选状态
            if checkbox.v.get() == True:
                fire_ship_id = self.replan_frame.grid_slaves(row=row, column=1)[0].cget('text')
                fire_ship_name = self.replan_frame.grid_slaves(row=row, column=2)[0].cget('text')
                fire_weapon_id = self.replan_frame.grid_slaves(row=row, column=3)[0].cget('text')
                fire_weapon_name = self.replan_frame.grid_slaves(row=row, column=4)[0].cget('text')
                # fire_weapon_angle = self.replan_frame.grid_slaves(row=row, column=5)[0].cget('text')
                seleced_target = self.replan_frame.grid_slaves(row=row, column=6)[0].cget('text')              

                if seleced_target == "不反应射击":
                    continue
                
                seleced_set = seleced_target.strip().split((" "))
                def_ship = seleced_set[0]
                fire_weapon_angle = seleced_set[1]
                fire_range = seleced_set[2]
                def_angle = seleced_set[3]

                fire_speed = self.ship_dict[fire_ship_id].current_speed
                fire_acc = self.ship_dict[fire_ship_id].current_total_turn
                def_acc = self.ship_dict[def_ship].current_speed
                def_speed = self.ship_dict[def_ship].current_total_turn
                # 重设武器的炮管修正使用状态
                self.gun_dict[fire_weapon_id].used_for_barrel = 0

                # 1射击舰编号（C1J1这种）、2口径、3射界、4目标舰编号、5距离、6射击角、7着弹角、8射击舰速度，9射击转向，10受击转向, 11受击速度, 12row”
                # hit: 0武器id、1射击舰id、2口径、3射界、4目标舰编号、5距离、6射击角、7着弹角、8射击舰速度、9射击转向、10受击转向、11受击速度、12row(计划射击不用）”
                hit = [fire_weapon_id,fire_ship_id,self.gun_dict[fire_weapon_id].size,self.gun_dict[fire_weapon_id].angle_type,def_ship,fire_range,fire_weapon_angle,def_angle,fire_speed,fire_acc,def_acc,def_speed,row]
                hit_record.append(hit)  
                hit_dict[fire_weapon_id] = hit
                self.ship_dict[def_ship].be_fired_weapon_list.append(fire_weapon_id)           

                # print(f"{fire_ship_id},{fire_ship_name},{fire_weapon_id},{fire_weapon_name},{fire_weapon_angle},{seleced_target}")
                reactive_hit_list.append([fire_weapon_id,fire_weapon_name,fire_ship_id,self.gun_dict[fire_weapon_id].size,fire_weapon_angle,seleced_set[0],seleced_set[2],seleced_set[1],seleced_set[3]])
                # 保存武器临时状态                

        # 0射击舰ID,1受击舰ID,2武器名称,3射击角,4基础命中,5被射修正,6移速修正,7转向修正,8速度着弹面修正,9射速修正,10吨位修正,11武器id,12环境修正,13过度集中修正,14炮管数修正，15row，16轻炮修正
        fire_record_list = self.game.fire.get_all_correction(hit_dict)

        for fire_record in fire_record_list:
            #print(fire_record)
            #print(fire_record[15])
            rowid = fire_record[15]
            hit_dice = self.game.fire.generate_random(1,100)
            # "是否射击", "射击ID","射击舰名","武器ID","武器名称","武器射界","可选目标","---","---","9命中骰点","最终命中","基础命中", "环境修正","被射修正","集中修正","移速修正","转向修正","射速修正","测距仪修正","炮管修正","速度*着弹面修正","吨位修正","加总修正"
            self.replan_frame.grid_slaves(row=rowid, column=9)[0].delete(0, 'end')
            self.replan_frame.grid_slaves(row=rowid, column=9)[0].insert(0, hit_dice) # 命中骰点
            self.replan_frame.grid_slaves(row=rowid, column=10)[0].delete(0, 'end')
            self.replan_frame.grid_slaves(row=rowid, column=10)[0].insert(0, 0) # 最终命中
            self.replan_frame.grid_slaves(row=rowid, column=11)[0].delete(0, 'end')
            self.replan_frame.grid_slaves(row=rowid, column=11)[0].insert(0, fire_record[4]) # 基础命中
            self.replan_frame.grid_slaves(row=rowid, column=12)[0].delete(0, 'end')
            self.replan_frame.grid_slaves(row=rowid, column=12)[0].insert(0, fire_record[12]) # 环境修正
            self.replan_frame.grid_slaves(row=rowid, column=13)[0].delete(0, 'end')
            self.replan_frame.grid_slaves(row=rowid, column=13)[0].insert(0, fire_record[5]) # 被射修正
            self.replan_frame.grid_slaves(row=rowid, column=14)[0].delete(0, 'end')
            self.replan_frame.grid_slaves(row=rowid, column=14)[0].insert(0, fire_record[13]) # 集中修正
            self.replan_frame.grid_slaves(row=rowid, column=15)[0].delete(0, 'end')
            self.replan_frame.grid_slaves(row=rowid, column=15)[0].insert(0, fire_record[6]) # 移速修正
            self.replan_frame.grid_slaves(row=rowid, column=16)[0].delete(0, 'end')
            self.replan_frame.grid_slaves(row=rowid, column=16)[0].insert(0, fire_record[7]) # 转向修正
            self.replan_frame.grid_slaves(row=rowid, column=17)[0].delete(0, 'end')
            self.replan_frame.grid_slaves(row=rowid, column=17)[0].insert(0, fire_record[9]) # 射速修正
            self.replan_frame.grid_slaves(row=rowid, column=18)[0].delete(0, 'end')
            self.replan_frame.grid_slaves(row=rowid, column=18)[0].insert(0, fire_record[17]) # 测距仪修正
            self.replan_frame.grid_slaves(row=rowid, column=19)[0].delete(0, 'end')
            self.replan_frame.grid_slaves(row=rowid, column=19)[0].insert(0, fire_record[14]) # 炮管修正
            self.replan_frame.grid_slaves(row=rowid, column=20)[0].delete(0, 'end')
            self.replan_frame.grid_slaves(row=rowid, column=20)[0].insert(0, fire_record[8]) # 速度*着弹面修正
            self.replan_frame.grid_slaves(row=rowid, column=21)[0].delete(0, 'end')
            self.replan_frame.grid_slaves(row=rowid, column=21)[0].insert(0, fire_record[10]) # 吨位修正            
            self.replan_frame.grid_slaves(row=rowid, column=22)[0].delete(0, 'end')
            self.replan_frame.grid_slaves(row=rowid, column=22)[0].insert(0, fire_record[16]) # 轻炮修正
            self.replan_frame.grid_slaves(row=rowid, column=23)[0].delete(0, 'end')
            self.replan_frame.grid_slaves(row=rowid, column=23)[0].insert(0, 0) # 加总修正

        with open("reactive_hit_record.txt", "w") as f:
            for hit in reactive_hit_list:
                # print(hit)
                # print(f"{hit[0]}, {hit[1]}, {hit[2]}, {hit[3]}, {hit[4]}, {hit[5]}, {hit[6]}, {hit[7]}, {hit[8]}")
                f.write(f"{hit[0]},{hit[1]},{hit[2]},{hit[3]},{hit[4]},{hit[5]},{hit[6]},{hit[7]},{hit[8]}\n")

    # 结算反应命中resolve_reactive_hit            
    def resolve_reactive_hit(self):
        print("结算反应命中resolve_reactive_hit")
        for row in range(2, self.replan_frame.grid_size()[1]):
            gun_id = self.replan_frame.grid_slaves(row=row, column=3)[0].cget('text')
            if self.gun_dict[gun_id].used_for_barrel == 1:
                self.gun_dict[gun_id].current_fired = self.gun_dict[gun_id].cd
                self.replan_frame.grid_slaves(row=row, column=10)[0].config(state="readonly")
                continue
            row_total = 0
            target = self.replan_frame.grid_slaves(row=row, column=6)[0].cget('text')
            if target == "不反应射击":
                self.replan_frame.grid_slaves(row=row, column=10)[0].config(state="readonly")
                continue
            fire_range = self.replan_frame.grid_slaves(row=row, column=11)[0].get()
            if fire_range == "超射程":
                self.replan_frame.grid_slaves(row=row, column=10)[0].config(state="readonly")
                continue
            for col in range(12, 23):
                if self.replan_frame.grid_slaves(row=row, column=col):
                    row_total += int(self.replan_frame.grid_slaves(row=row, column=col)[0].get())
            if self.replan_frame.grid_slaves(row=row, column=23):
                self.replan_frame.grid_slaves(row=row, column=23)[0].delete(0, 'end')
                self.replan_frame.grid_slaves(row=row, column=23)[0].insert(0, str(row_total))
            # 计算最终命中
            if self.replan_frame.grid_slaves(row=row, column=10):
                final_hit = int(self.replan_frame.grid_slaves(row=row, column=11)[0].get()) + row_total * 2
                self.replan_frame.grid_slaves(row=row, column=10)[0].delete(0, 'end')
                self.replan_frame.grid_slaves(row=row, column=10)[0].insert(0, str(final_hit))
            
            # 武器进入CD
            self.gun_dict[gun_id].current_fired = self.gun_dict[gun_id].cd

    # 根据射击船和目标船id，计算enemy_ship, att_angle, distance, def_angle
    def get_other_ships_position(self, shipid, enemy_ship):
        if not enemy_ship == shipid:
            '''
            # 获取船的坐标和方向
            def_x, def_y, def_d = float(self.ship_dict[enemy_ship].x), float(self.ship_dict[enemy_ship].y), int(self.ship_dict[enemy_ship].direction)
            att_x, att_y, att_d = float(self.ship_dict[shipid].x), float(self.ship_dict[shipid].y), int(self.ship_dict[shipid].direction)
            # 计算两船之间的距离
            distance = int(math.sqrt((att_x - def_x) ** 2 + (att_y - def_y) ** 2) * 10 )# 坐标转码数 * 10
            # 计算两船之间的角度
            # att_angle = math.degrees(math.atan2(def_y - att_y, def_x - att_x)) - att_d
            att_angle = int(math.degrees(math.atan2(att_y - def_y, def_x - att_x)) - att_d)
            if att_angle < 0:
                att_angle += 360
            att_angle = 360 - att_angle
            def_angle = int(math.degrees(math.atan2(def_y - att_y, att_x - def_x)) - def_d)
            if def_angle < 0:
                def_angle += 360
            def_angle = 360 - def_angle
            '''
            att_angle, def_angle, distance = self.game.fire.get_angles_distance(shipid, enemy_ship)

            # 以enemy_ship、att_angle、distance为元素创建一个新的列表
            new_item = [enemy_ship, att_angle, distance, def_angle]

            return new_item

    # 根据shipid，获取其他船相对它的位置，以列表形式[enemy_ship, att_angle, distance, def_angle]
    def get_other_ships_position_list(self,shipid):
        reactive_list = []
        for enemy_ship in self.on_map_ship_list:          
            # 跳过自己
            if enemy_ship == shipid:
                continue
            # 以enemy_ship、att_angle、distance为元素创建一个新的列表
            new_item = self.get_other_ships_position(shipid, enemy_ship)
            # 将新的列表加入到reactivelist数组中
            reactive_list.append(new_item)

        return reactive_list

    # 根据射击舰ID，获取可射击的目标列表，排除友军和±5度内遮挡的
    def get_avaible_tagert(self, shipid):

        reactive_list = self.get_other_ships_position_list(shipid)

        # 按射击角正序排序
        sorted_reactive_list = sorted(reactive_list, key=lambda x: x[1], reverse=True)       

        i = 0
        while i < len(sorted_reactive_list) - 1:
            j = i + 1
            item1 = sorted_reactive_list[i]
            item2 = sorted_reactive_list[j]
            angle_diff = abs(item1[1] - item2[1])

            if angle_diff <= 5 or angle_diff >= 355:
                if item1[2] > item2[2]:
                    del sorted_reactive_list[i]
                else:
                    del sorted_reactive_list[j]
            else:
                i += 1
        # 筛除掉友军，子数组的第一个字符和shipid的第一个字符相等
        filtered_reactive_list = [item for item in sorted_reactive_list if item[0][0] != shipid[0]]
        # 按射程倒序，小的在最前面
        avaible_tagert_list = sorted(filtered_reactive_list, key=lambda x: x[2], reverse=False) 

        # print(shipid)
        # print(reactive_list)
        return avaible_tagert_list

    # 传入射击船和被射击船，计算其中阻碍船
    def get_block_ship(self, fire_ship, def_ship):
        # 射击舰和目标舰的相对位置数据
        position = self.get_other_ships_position(fire_ship, def_ship)
        block_distance = position[2] 
        block_ship = def_ship
        block_angle = position[1]

        ship_list = self.get_other_ships_position_list(fire_ship)

        # 按距离排序
        sorted_ship_list = sorted(ship_list, key=lambda x: x[2], reverse=True)

        while True:
            noblock = True
            for enemy_ship in sorted_ship_list:
                # 如果是射击舰或目标舰或超出距离，则跳过
                if enemy_ship[0] == fire_ship or enemy_ship[0] == block_ship or enemy_ship[2] >= block_distance:
                    continue
                angle_diff = abs(block_angle - enemy_ship[1])
                if angle_diff <= 5 or angle_diff >= 355:
                    if block_distance > enemy_ship[1]:
                        block_distance = enemy_ship[2] 
                        block_ship = enemy_ship[0]
                        block_angle = enemy_ship[1]
                        noblock = False
            if noblock:
                break        
        return block_ship

    # 传入gunid和可用列表，来计算在该gunid的射界内的list[enemy_ship, att_angle, distance, def_angle]
    def get_inangle_tagert(self, gun_id, avaible_tagert_list):
        inangle_list = []
        for list in avaible_tagert_list:
            gun_angel = self.gun_dict[gun_id].angle
            if self.game.fire.is_in_angle(list[1], gun_angel) == 1:
                inangle_list.append(list)
        return inangle_list
    
    # 在地图上生成一个新船
    def open_new_ship_window(self):        
        # 如果存在上一个tip窗口，先关闭它
        if self.prev_add_new_ship_window is not None:
            if self.prev_add_new_ship_window.winfo_exists():                
                self.prev_add_new_ship_window.destroy()

        self.add_new_ship_window = tk.Tk()
        self.add_new_ship_window.geometry('400x400+400+400')
        self.add_new_ship_window.title("新增船只")  

        self.prev_add_new_ship_window = self.add_new_ship_window
        # Create labels for ship ID and name
        id_label = tk.Label(self.add_new_ship_window, text=f"船ID：")
        id_Entry =  tk.Entry(self.add_new_ship_window, width=8)
        id_label.grid(row=1, column=0)
        id_Entry.grid(row=1, column=1) 

        dir_label = tk.Label(self.add_new_ship_window, text=f"航向：")
        dir_Entry = tk.Entry(self.add_new_ship_window, width=8)
        # color_label = tk.Label(self.add_new_ship_window, text=f"颜色：")
        # color_Entry = tk.Entry(self.add_new_ship_window, width=8)   

        dir_label.grid(row=1, column=2)
        dir_Entry.grid(row=1, column=3)
        # color_label.grid(row=1, column=4)
        # color_Entry.grid(row=1, column=5)
        
        x_label = tk.Label(self.add_new_ship_window, text=f"坐标x：")
        x_Entry = tk.Entry(self.add_new_ship_window, width=8)
        y_label = tk.Label(self.add_new_ship_window, text=f"坐标y：")
        y_Entry = tk.Entry(self.add_new_ship_window, width=8)

        x_label.grid(row=3, column=0)
        x_Entry.grid(row=3, column=1)
        y_label.grid(row=3, column=2)
        y_Entry.grid(row=3, column=3)


        followshipid_label = tk.Label(self.add_new_ship_window, text=f"相对船：")
        followshipid_Entry = tk.Entry(self.add_new_ship_window, width=8)
        followshipdir_label = tk.Label(self.add_new_ship_window, text=f"该船的方向：")
        followshipdir_Entry = tk.Entry(self.add_new_ship_window, width=8)
        followshipdis_label = tk.Label(self.add_new_ship_window, text=f"离该船距离：")
        followshipdis_Entry = tk.Entry(self.add_new_ship_window, width=8)

        followshipid_label.grid(row=5, column=0)
        followshipid_Entry.grid(row=5, column=1)
        followshipdir_label.grid(row=5, column=2)
        followshipdir_Entry.grid(row=5, column=3)
        followshipdis_label.grid(row=5, column=4)
        followshipdis_Entry.grid(row=5, column=5)

        add_button = tk.Button(self.add_new_ship_window, text="创建", command=self.add_new_ship)
        add_button.grid(row=6, column=0)

        # 在tip的关闭按钮上增加设置前一个tip为None
        def close_add_new_ship_window():
            self.prev_add_new_ship_window = None
            self.add_new_ship_window.destroy()

        self.add_new_ship_window.protocol("WM_DELETE_WINDOW", close_add_new_ship_window)

    # 从新建船只的窗口获取数据来新建船只
    def add_new_ship(self):

        shipid = self.add_new_ship_window.grid_slaves(row=1, column=1)[0].get()
        shipdir = self.add_new_ship_window.grid_slaves(row=1, column=3)[0].get()
        # shipcolor = self.add_new_ship_window.grid_slaves(row=1, column=5)[0].get()
        shipx = self.add_new_ship_window.grid_slaves(row=3, column=1)[0].get()
        shipy = self.add_new_ship_window.grid_slaves(row=3, column=3)[0].get()
        followshipid = self.add_new_ship_window.grid_slaves(row=5, column=1)[0].get()
        followshipdir = self.add_new_ship_window.grid_slaves(row=5, column=3)[0].get()
        followshiprange = self.add_new_ship_window.grid_slaves(row=5, column=5)[0].get()        

        if shipid and shipdir:            
            if shipx and shipy:
                self.game.new_ship(shipid)
                self.ship_dict[shipid].direction = shipdir
                # self.ship_dict[shipid].color = shipcolor
                self.ship_dict[shipid].x = shipx
                self.ship_dict[shipid].y = shipy
                self.game.map.add_ship(shipid)

            elif followshipid and followshipdir and followshiprange:
                followshipx = float(self.ship_dict[followshipid].x)
                followshipy = float(self.ship_dict[followshipid].y)
                r = float(followshiprange) / 10
                d = math.radians(int(followshipdir))
                # theta = math.radians(90 - d)

                shipx = followshipx + r * math.cos(d)
                shipy = followshipy - r * math.sin(d)

                self.game.new_ship(shipid)
                self.ship_dict[shipid].direction = shipdir
                # self.ship_dict[shipid].color = shipcolor
                self.ship_dict[shipid].x = shipx
                self.ship_dict[shipid].y = shipy
                self.game.map.add_ship(shipid)

    def add_ship_button_on_menu(self, shipid):
        if self.ship_dict[shipid].team == 1:
            button = tk.Button(self.menu_frame, text=shipid + "," + self.ship_dict[shipid].name, command=lambda tag=shipid: self.game.ui.open_ship_menu(tag))
            button.grid(row=self.t1_button_row, column=self.t1_button_column)
            
            # 当前行数
            self.t1_button_column += 1
            if self.t1_button_column == 20:
                self.t1_button_row += 1
                self.t1_button_column = 0
        if self.ship_dict[shipid].team == 2:
            button = tk.Button(self.menu_frame, text=shipid + "," + self.ship_dict[shipid].name, command=lambda tag=shipid: self.game.ui.open_ship_menu(tag))
            button.grid(row=self.t2_button_row, column=self.t2_button_column)
            
            # 当前行数
            self.t2_button_column += 1
            if self.t2_button_column == 20:
                self.t2_button_row += 1
                self.t2_button_column = 0
    # 下一回合
    def next_turn(self):

        # self.follow_ship("C8","J3")

        turn = int(self.game.turn)
        turn = turn + 1        
        self.game.turn = turn
        # 更新回合数
        self.menu_frame.grid_slaves(row=1, column=1)[0].delete(0, 'end')
        self.menu_frame.grid_slaves(row=1, column=1)[0].insert(0, str(turn))
        # 更新每条船的回合临时数据
        for ship_id, ship in self.ship_dict.items():
            ship.start_x = ship.x
            ship.start_y = ship.y
            ship.start_direction = ship.direction
            ship.current_total_turn = 0
            ship.current_damage = 0
            ship.be_fired_weapon_list = []
            ship.be_hit_list = []
                        
        # 更新每门炮的回合临时数据
        for gun_id, gun in self.gun_dict.items():
            # 每门炮CD减一
            if gun.current_fired <= 0:
                continue
            gun.current_fired -= 1

    # 求出ship1到ship2的移动方案
    def move_ship1_to_ship2(self, ship1, ship2):
        att_angle, def_angle, distance = self.game.fire.get_angles_distance(ship1, ship2)
        # print(f"att_angle:{att_angle}, def_angle:{def_angle}, distance:{distance}")       
        
        # ship1和ship2在同一条直线上，且ship1在ship2后面
        if att_angle == 0 or att_angle == 360:
            move, turn = distance, 0
        # ship1和ship2在同一条直线上，且ship1在ship2前面
        elif att_angle == 180:
            move, turn = distance, 180      
        # ship1在ship2后面，可以通过180度以内的转向移动去ship2
        elif 0 < att_angle <= 90 or 270 <= att_angle < 360:
            print(f"{ship1}在{ship2}后面,可以通过180度以内的转向移动去{ship2}")
            move, turn = self.follow_ship(ship1, ship2)
        # ship1在ship2前面，无法通过180度以内的转向移动去ship2
        elif 90 < att_angle < 270:
            print(f"{ship1}在{ship2}前面,无法通过180度以内的转向移动去{ship2}")
            move, turn = self.follow_ship(ship1, ship2)
        
        print(f"move:{move},turn:{turn}")
        return move, turn


    # 获取ship1跟随ship2所需的移动距离和转向角度
    def follow_ship(self,ship1,ship2):
        # 假设ship1的朝向为d1，ship1的位置为(x1, y1)，ship2的朝向为d2，ship2的位置为(x2, y2)
        d1 = int(self.ship_dict[ship1].direction)  # 角度值
        d2 = int(self.ship_dict[ship2].direction)  # 角度值
        x1, y1 = float(self.ship_dict[ship1].x),  float(self.ship_dict[ship1].y)
        x2, y2 = float(self.ship_dict[ship2].x),  float(self.ship_dict[ship2].y) 

        # 计算x1,x2的差的绝对值
        lenA = abs(x2 - x1)
        lenB = abs(y1 - y2)
        direction_diff = d2 - d1

        # 将朝向转化为弧度制
        r1 = math.radians(d1)
        r2 = math.radians(d2)

        if r1 == r2:
            print("两船朝向相同，无需转向")
            return 0, 0

        # 通过正弦定理计算ship1前延线到达ship2的后延线的交差点，的距离, 以坐标系值
        matchlen = abs(lenA - abs((lenB/math.tan(r2)))) * math.sin(180 - r2) / math.sin(r2 - r1)
        
        print(f"前进:{matchlen}, 转向:{direction_diff}")

        return matchlen, direction_diff
    
    # 打开计划射击的伤害结算
    def open_resolve_plan_damage(self):        
        self.clear_resolve_list()
        self.notebook.select(self.damage_sheet)  
        
        # 重置所有ship的be_hit_list
        for ship_id in self.on_map_ship_list:
            self.ship_dict[ship_id].be_hit_list = []
        # 重置被命中的ship列表
        self.be_hit_ship_list = []
        # 从record_frame中统计数据
        for row in range(2, self.record_frame.grid_size()[1]):
            final_DR = int(self.record_frame.grid_slaves(row=row, column=9)[0].get())
            rolled_DR = int(self.record_frame.grid_slaves(row=row, column=8)[0].get())
            # print(f"final_DR:{final_DR}, rolled_DR:{rolled_DR}")
            if rolled_DR <= final_DR and final_DR > 0:                
                ship = self.record_frame.grid_slaves(row=row, column=3)[0].cget('text')
                ship_name = self.ship_dict[ship].name
                fire_id = self.record_frame.grid_slaves(row=row, column=1)[0].cget('text')
                fire_name = self.ship_dict[fire_id].name
                gun_id = self.record_frame.grid_slaves(row=row, column=5)[0].cget('text')
                gun_name = self.gun_dict[gun_id].name
                fire_range = self.record_frame.grid_slaves(row=row, column=23)[0].get()

                # ["目标ID", "目标名称", "射击阶段", "射击舰ID", "射击舰名", "射程", "武器ID", "武器名称", "命中骰点", "最终命中"]
                hit = [ship, ship_name, '计划射击', fire_id, fire_name, fire_range, gun_id, gun_name[:12], rolled_DR, final_DR]
                self.ship_dict[ship].be_hit_list.append(hit)
                self.be_hit_ship_list.append(ship)
        
        self.add_damage_row()

    # 打开反应射击的伤害结算
    def open_resolve_reactive_damage(self):  

        self.clear_resolve_list()
        self.notebook.select(self.damage_sheet) 

        # 重置所有ship的be_hit_list
        for ship_id in self.on_map_ship_list:
            self.ship_dict[ship_id].be_hit_list = [] 

        # 重置被命中的ship列表
        self.be_hit_ship_list = []

        # 从replan_frame中统计数据
        for row in range(2, self.replan_frame.grid_size()[1]):   
            final_DR = self.replan_frame.grid_slaves(row=row, column=10)[0].get()
            rolled_DR = self.replan_frame.grid_slaves(row=row, column=9)[0].get()     
            # print(f"final_DR:{final_DR}, rolled_DR:{rolled_DR}")
            if final_DR and int(rolled_DR) <= int(final_DR) and int(final_DR) > 0:
                ship = self.replan_frame.grid_slaves(row=row, column=6)[0].cget('text').strip().split((" "))[0]
                ship_name = self.ship_dict[ship].name
                fire_id = self.replan_frame.grid_slaves(row=row, column=1)[0].cget('text')
                fire_name = self.ship_dict[fire_id].name
                gun_id = self.replan_frame.grid_slaves(row=row, column=3)[0].cget('text')
                gun_name = self.gun_dict[gun_id].name
                seleced_target = self.replan_frame.grid_slaves(row=row, column=6)[0].cget('text')      
                if seleced_target == "不反应射击":
                    continue
                seleced_set = seleced_target.strip().split((" "))
                fire_range = seleced_set[2]

                # ["目标ID", "目标名称", "射击阶段", "射击舰ID", "射击舰名", "射程", "武器ID", "武器名称", "命中骰点", "最终命中"]
                hit = [ship, ship_name, '反应射击', fire_id, fire_name, fire_range, gun_id, gun_name[:12], rolled_DR, final_DR]
                self.ship_dict[ship].be_hit_list.append(hit)
                self.be_hit_ship_list.append(ship)

        self.add_damage_row() 
    
    # 打开结算列表
    def open_resolve_list(self):        
        print("open_resolve_list")
        self.clear_resolve_list()
        # 重置所有ship的be_hit_list
        for ship_id in self.on_map_ship_list:
            self.ship_dict[ship_id].be_hit_list = []
        
        # 重置被命中的ship列表
        self.be_hit_ship_list = []
        
        # 从record_frame中统计数据
        for row in range(2, self.record_frame.grid_size()[1]):
            final_DR = int(self.record_frame.grid_slaves(row=row, column=9)[0].get())
            rolled_DR = int(self.record_frame.grid_slaves(row=row, column=8)[0].get())
            # print(f"final_DR:{final_DR}, rolled_DR:{rolled_DR}")
            if rolled_DR <= final_DR and final_DR > 0:                
                ship = self.record_frame.grid_slaves(row=row, column=3)[0].cget('text')
                ship_name = self.ship_dict[ship].name
                fire_id = self.record_frame.grid_slaves(row=row, column=1)[0].cget('text')
                fire_name = self.ship_dict[fire_id].name
                gun_id = self.record_frame.grid_slaves(row=row, column=5)[0].cget('text')
                gun_name = self.gun_dict[gun_id].name
                fire_range = self.record_frame.grid_slaves(row=row, column=23)[0].get()

                # ["目标ID", "目标名称", "射击阶段", "射击舰ID", "射击舰名", "射程", "武器ID", "武器名称", "命中骰点", "最终命中"]
                hit = [ship, ship_name, '计划射击', fire_id, fire_name, fire_range, gun_id, gun_name[:12], rolled_DR, final_DR]
                self.ship_dict[ship].be_hit_list.append(hit)
                self.be_hit_ship_list.append(ship)

        # 从replan_frame中统计数据
        for row in range(2, self.replan_frame.grid_size()[1]):   
            final_DR = self.replan_frame.grid_slaves(row=row, column=10)[0].get()
            rolled_DR = self.replan_frame.grid_slaves(row=row, column=9)[0].get()     
            # print(f"final_DR:{final_DR}, rolled_DR:{rolled_DR}")
            if final_DR and int(rolled_DR) <= int(final_DR) and int(final_DR) > 0:
                ship = self.replan_frame.grid_slaves(row=row, column=6)[0].cget('text').strip().split((" "))[0]
                ship_name = self.ship_dict[ship].name
                fire_id = self.replan_frame.grid_slaves(row=row, column=1)[0].cget('text')
                fire_name = self.ship_dict[fire_id].name
                gun_id = self.replan_frame.grid_slaves(row=row, column=3)[0].cget('text')
                gun_name = self.gun_dict[gun_id].name
                seleced_target = self.replan_frame.grid_slaves(row=row, column=6)[0].cget('text')      
                if seleced_target == "不反应射击":
                    continue
                seleced_set = seleced_target.strip().split((" "))
                fire_range = seleced_set[2]

                # ["目标ID", "目标名称", "射击阶段", "射击舰ID", "射击舰名", "射程", "武器ID", "武器名称", "命中骰点", "最终命中"]
                hit = [ship, ship_name, '反应射击', fire_id, fire_name, fire_range, gun_id, gun_name[:12], rolled_DR, final_DR]
                self.ship_dict[ship].be_hit_list.append(hit)
                self.be_hit_ship_list.append(ship)

        self.add_damage_row()

    # 新增结算列
    def add_damage_row(self):
        print("add_damage_row")
        for ship_id in self.on_map_ship_list:
            if self.ship_dict[ship_id].be_hit_list !=[]:
                be_hit_list = self.ship_dict[ship_id].be_hit_list
                for one_hit_list in be_hit_list:                  
                    # print(one_hit_list)
                    current_rows = self.damage_frame.grid_size()[1]
                    gun_id = one_hit_list[6]
                    for i in range(0,10):
                        new_label = tk.Label(self.damage_frame)
                        new_label.grid(row=current_rows, column=i+1)
                        new_label.config(text=one_hit_list[i])  

                    ammo_list = self.gun_dict[gun_id].ammo_list

                    ammo_selected_value = tk.StringVar()

                    if ammo_list != []:
                        ammo_selected_value.set(ammo_list[0])
                    else:
                        ammo_list.append("无弹药")
                        ammo_selected_value.set("无弹药")

                    # 弹药选择
                    ammo_btn_menu = tk.OptionMenu(self.damage_frame, ammo_selected_value, *ammo_list)
                    ammo_btn_menu.grid(row=current_rows, column=11)
                    # 是否过穿
                    over_piercing = tk.Entry(self.damage_frame, width=8)
                    over_piercing.grid(row=current_rows, column=12)
                    # 是否穿甲
                    is_piercing = tk.Entry(self.damage_frame, width=8)
                    is_piercing.grid(row=current_rows, column=13)
                    # 伤害
                    get_damage = tk.Entry(self.damage_frame, width=8)
                    get_damage.grid(row=current_rows, column=14)
                    # 总伤害
                    total_damage = tk.Entry(self.damage_frame, width=8)
                    total_damage.grid(row=current_rows, column=15)
                    # 致命损伤数
                    ch_num = tk.Entry(self.damage_frame, width=8)
                    ch_num.grid(row=current_rows, column=16)
                    # 致命损伤骰点
                    ch_rolls = tk.Entry(self.damage_frame, width=8)
                    ch_rolls.grid(row=current_rows, column=17)

    # 结算伤害
    def resolve_damage(self):
        self.damage_list = []
        for row in range(2, self.damage_frame.grid_size()[1]):
            ammo_list = self.damage_frame.grid_slaves(row=row, column=11)[0].cget('text')
            fire_range = self.damage_frame.grid_slaves(row=row, column=6)[0].cget('text')
            target = self.damage_frame.grid_slaves(row=row, column=1)[0].cget('text')  
            gun_id = self.damage_frame.grid_slaves(row=row, column=7)[0].cget('text')
            fire_phase = self.damage_frame.grid_slaves(row=row, column=3)[0].cget('text')
            # print(ammo_list, fire_range, target)
            op, ip, gd = self.game.fire.get_damage(target, fire_range, ammo_list, gun_id, fire_phase)
            self.damage_frame.grid_slaves(row=row, column=12)[0].delete(0, 'end')
            self.damage_frame.grid_slaves(row=row, column=12)[0].insert(0, op)
            self.damage_frame.grid_slaves(row=row, column=13)[0].delete(0, 'end')
            self.damage_frame.grid_slaves(row=row, column=13)[0].insert(0, ip)
            self.damage_frame.grid_slaves(row=row, column=14)[0].delete(0, 'end')
            self.damage_frame.grid_slaves(row=row, column=14)[0].insert(0, gd)  
            self.damage_list.append([target, gd])
    
    # 结算暴击
    def resolve_critical_hit(self):
        resolve_damage_list = []
        for damage in self.damage_list:
            self.ship_dict[damage[0]].current_damage += damage[1]
        for row in range(2, self.damage_frame.grid_size()[1]):
            target = self.damage_frame.grid_slaves(row=row, column=1)[0].cget('text')
            if not target in resolve_damage_list:
                ch_num = self.game.fire.get_ch_num(target)
                ch_rolls = self.game.fire.get_ch_rolls(ch_num)
                self.damage_frame.grid_slaves(row=row, column=15)[0].delete(0, 'end')
                self.damage_frame.grid_slaves(row=row, column=15)[0].insert(0, self.ship_dict[target].current_damage)
                self.damage_frame.grid_slaves(row=row, column=16)[0].delete(0, 'end')
                self.damage_frame.grid_slaves(row=row, column=16)[0].insert(0, ch_num)
                self.damage_frame.grid_slaves(row=row, column=17)[0].delete(0, 'end')
                self.damage_frame.grid_slaves(row=row, column=17)[0].insert(0, ch_rolls)
                resolve_damage_list.append(target)
    # 更新损伤
    def update_damage(self):
        for ship_id in self.on_map_ship_list:
            current_DP = float(self.ship_dict[ship_id].current_DP)
            current_DP = current_DP - float(self.ship_dict[ship_id].current_damage)
            self.ship_dict[ship_id].current_DP = current_DP
            self.ship_dict[ship_id].current_damage = 0

    # 清除结算列表
    def clear_resolve_list(self):
        for row in range(2, self.damage_frame.grid_size()[1]):
            for col in range(self.damage_frame.grid_size()[0]):
                if self.damage_frame.grid_slaves(row=row, column=col):
                    self.damage_frame.grid_slaves(row=row, column=col)[0].destroy()

    # 设定炮术等级
    def set_fire_level(self, *var):
        if self.checkbox_ht_var.get() == "0":
            self.game.fire.fire_level = []
            self.game.fire.fire_level = self.game.fire.fire_level_0
        elif self.checkbox_ht_var.get() == "0*":
            self.game.fire.fire_level = []
            self.game.fire.fire_level = self.game.fire.fire_level_0star
        else:
            print("error, fire level is not 0 or 0*")


    


        
