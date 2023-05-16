import tkinter as tk
import math
import functools
import tkinter.simpledialog as sd
from tkscrolledframe import ScrolledFrame

class Map(tk.Canvas):
    def __init__(self, master, width, height, game):
        super().__init__(master, width=width, height=height, bg='white')
        self.scroll_x = tk.Scrollbar(master, orient='horizontal', command=self.xview)
        self.scroll_y = tk.Scrollbar(master, orient='vertical', command=self.yview)
        self.config(xscrollcommand=self.scroll_x.set, yscrollcommand=self.scroll_y.set)
        self.scroll_x.pack(side='bottom', fill='x')
        self.scroll_y.pack(side='right', fill='y')
        self.pack(side='left', fill='both', expand=True)

        self.game = game

        self.ship_dict = game.ship_dict

        # 绘制战场背景
        self.create_rectangle(0, 0, width, height, fill='gray')

        # 绑定右键点击事件
        self.bind('<Button-3>', self.show_menu)

        # 创建转向按钮
        self.turn_button = tk.Button(master, text='转向', command=self.turn_ship_with_input)
        self.turn_button.pack(side='top', padx=10, pady=10)

        # 添加舰船
        self.ships = []

        # 设置滚动范围
        self.config(scrollregion=self.bbox('all'))
        
        # 创建一个Label字典，主键为ship_id
        self.labels = {}  # Add this line to store the labels

        # 创建一个ship_dict的id的列表，存储ship的存档数据
        self.ship_id_list = []

        # 创建一个计划射击的数组
        self.fire_plan_list = []

        # print(self.game.ui.menu_frame.grid_size()[1])
    
    def add_ship(self, shipid):
        # 计算三角形的三个顶点坐标
        x = float(self.ship_dict[shipid].x)
        y = float(self.ship_dict[shipid].y)
        color = self.ship_dict[shipid].color
        direction = int(self.ship_dict[shipid].direction)
        r = 20
        l = 25
        angle = math.radians(15)
        points = [(x, y), (x - r * math.cos(angle + math.radians(direction)), y + r * math.sin(angle + math.radians(direction))), (x - r * math.cos(angle - math.radians(direction)), y - r * math.sin(angle - math.radians(direction)))]

        # To display a label at x, y with text 'name'
        label = tk.Label(self, text=shipid, bg='grey', highlightthickness=0, font=("", 8))
        label_window = self.create_window(x+15, y-15, window=label, anchor='nw')
        self.labels[shipid] = label

        # 绘制三角形
        ship = self.create_polygon(points, fill=color, tags=['ship', shipid])
        
        # self.create_oval(x-r, y-r, x+r, y+r, outline="black", dash=(3,5)) 想画个虚线圈
        self.ships.append(ship)
        self.ship_id_list.append(shipid)

        self.tag_lower(label_window)
        self.tag_raise(ship)

        self.game.ui.add_ship_button_on_menu(shipid)     
    
    def show_menu(self, event):
        # 获取鼠标点击位置
        x = self.canvasx(event.x)
        y = self.canvasy(event.y)
        # 获取最近的船只标签
        ship_id = self.find_closest(x, y)[0]        
        tags = self.gettags(ship_id)
        if 'ship' in tags:
            ship_tag = tags[1]
            # 创建菜单
            menu = tk.Menu(self, tearoff=0)
            menu.add_command(label=self.ship_dict[ship_tag].name, command=lambda: self.open_ship(ship_tag))
            # menu.add_command(label='移动', command=lambda: self.move_ship_with_input(ship_id, ship_tag))
            # menu.add_command(label='转向', command=lambda: self.turn_ship_with_input(ship_id, ship_tag))
            # menu.add_command(label='计划射击', command=lambda: self.attack_ship(ship_tag))
            menu.add_separator()
            menu.add_command(label='删除船只', command=lambda: self.remove_ship(ship_id, ship_tag))
            # 在鼠标位置弹出菜单
            # print(f"{self.winfo_rootx()},{self.winfo_rooty()}")
            menu.post(event.x+self.winfo_rootx(), event.y+self.winfo_rooty())

    def open_menu(self, tag):
        pass

    def open_ship(self,ship_tag):
        self.game.ui.open_tip(ship_tag)
        # print(f'Moving ship {ship_id}')

    def move_ship_with_input(self, ship_id, ship_tag):
        # 弹出输入框，获取转向角度
        move_str = sd.askstring('移动', '请输入移动码数', parent=self)  # 修改此处
        if move_str is None:
            return
        try:
            move = float(move_str) #1:10的兑换码数和地图坐标
        except ValueError:
            tk.messagebox.showerror('错误', '输入值不是有效的整数')
            return

        self.move_ship(ship_id, move)

    def move_ship(self, ship_id, move_ma):
        tags = self.gettags(ship_id)

        if 'ship' in tags:
            tag = tags[1]
        # 获取船只的当前位置和方向
        x = float(self.ship_dict[tag].x)
        y = float(self.ship_dict[tag].y)
        direction = int(self.ship_dict[tag].direction)

        move = float(move_ma) / 10 # move是真实值，是输入的码数/10

        # 计算新的位置
        new_x = x + move * math.cos(math.radians(direction))
        new_y = y - move * math.sin(math.radians(direction))

        # 更新船只的位置
        self.ship_dict[tag].x = new_x
        self.ship_dict[tag].y = new_y

        # 计算新的三角形顶点坐标
        r = 20
        angle_rad = math.radians(15)
        points = [(new_x, new_y), (new_x - r * math.cos(angle_rad + math.radians(direction)), new_y + r * math.sin(angle_rad + math.radians(direction))), (new_x - r * math.cos(angle_rad - math.radians(direction)), new_y - r * math.sin(angle_rad - math.radians(direction)))]

        # 扁平化坐标列表
        flat_points = [coord for point in points for coord in point]

        # 更新船只的形状
        self.coords(ship_id, *flat_points)

        # 更新船只的标签位置
        self.labels[tag].destroy()  
        del self.labels[tag]
        
        label = tk.Label(self, text=self.ship_dict[tag].id, bg='grey', highlightthickness=0, font=("", 8))
        self.create_window(new_x+25, new_y-25, window=label, anchor='nw')
        self.labels[tag] = label

        # 将船只提升到标签之上
        self.tag_raise(ship_id)

        # 画行进路线
        self.create_line(x, y, new_x, new_y, fill=self.ship_dict[tag].color, width=1, tags=['moveline'+ship_id])

        if new_x < 500 and new_y < 500:
            self.xview_moveto(0)
            self.yview_moveto(0)            
            return
        canvas_width = 100000
        canvas_height = 100000

        canvas_x = new_x-400
        canvas_y = new_y-200

        self.xview_moveto(canvas_x / canvas_width)
        self.yview_moveto(canvas_y / canvas_height)
        self.update()
    
    def attack_ship(self, ship_tag):
        self.game.uiplan.open_ui_plan(ship_tag)
        # 弹出输入框，获取转向角度
        # tagert_id = sd.askstring('攻击', '请输入攻击目标id', parent=self)  # 修改此处
        # if tagert_id is None:
        #    return
        # if tagert_id in self.ship_id_list:
        #    self.do_attack(ship_tag, tagert_id)
        # else:
        #    tk.messagebox.showerror('错误', '输入值不是有效的目标id')
        #    return      

    def do_attack(self, attacker_tag, target_tag):
        print(f'{attacker_tag} 攻击 {target_tag}')
        self.fire_plan_list.append([attacker_tag, target_tag]) 

    def remove_ship(self, ship_id, tag):
        self.delete(ship_id)
        self.labels[tag].destroy()  # Destroy the label using the tag
        del self.labels[tag]
            
    def turn_ship_with_input(self, ship_id, tag):
        # 弹出输入框，获取转向角度
        angle_str = sd.askstring('转向', '请输入转向角度：', parent=self)  # 修改此处
        if angle_str is None:
            return
        try:
            angle = int(angle_str)
        except ValueError:
            tk.messagebox.showerror('错误', '输入值不是有效的整数')
            return

        self.turn_ship(ship_id, angle)
    
    def turn_ship(self, ship_id, angle): 
        tags = self.gettags(ship_id)
        if 'ship' in tags:
            tag = tags[1]

        # 获取船只的当前位置和方向
        x = float(self.ship_dict[tag].x)
        y = float(self.ship_dict[tag].y)
        direction = int(self.ship_dict[tag].direction)

        # 计算新的方向
        new_direction = (direction + angle) % 360

        # 更新船只的方向
        self.ship_dict[tag].direction = new_direction

        # 计算新的三角形顶点坐标
        r = 20
        angle_rad = math.radians(15)
        points = [(x, y), (x - r * math.cos(angle_rad + math.radians(new_direction)), y + r * math.sin(angle_rad + math.radians(new_direction))), (x - r * math.cos(angle_rad - math.radians(new_direction)), y - r * math.sin(angle_rad - math.radians(new_direction)))]

        # 扁平化坐标列表
        flat_points = [coord for point in points for coord in point]

        # 更新船只的形状
        self.coords(ship_id, *flat_points)

    # 重置ship位置
    def reset_ship_position(self,ship_id):
        tags = self.gettags(ship_id)

        if 'ship' in tags:
            tag = tags[1]
            
        # 获取船只的当前位置和方向
        x = float(self.ship_dict[ship_id].x)
        y = float(self.ship_dict[ship_id].y)
        direction = int(self.ship_dict[ship_id].direction)

        # 计算新的三角形顶点坐标
        r = 20
        angle_rad = math.radians(15)
        points = [(x, y), (x - r * math.cos(angle_rad + math.radians(direction)), y + r * math.sin(angle_rad + math.radians(direction))), (x - r * math.cos(angle_rad - math.radians(direction)), y - r * math.sin(angle_rad - math.radians(direction)))]

        # 扁平化坐标列表
        flat_points = [coord for point in points for coord in point]

        # 更新船只的形状
        self.coords(ship_id, *flat_points)

        # 更新船只的标签位置
        self.labels[tag].destroy()  
        del self.labels[tag]

        label = tk.Label(self, text=self.ship_dict[tag].id, bg='grey', highlightthickness=0, font=("", 8))
        self.create_window(x+25, y-25, window=label, anchor='nw')
        self.labels[tag] = label

        # 将船只提升到标签之上
        self.tag_raise(ship_id)
        # 删除移动线
        line_ids = self.find_withtag(['moveline'+ship_id])
        print(line_ids)

        for line_id in line_ids:
            self.delete(line_id)

        self.game.ui.zoom(ship_id)

    def edit_plan(self):
        menu = tk.Menu(self, tearoff=0)
        menu.add_command(label="点击即删除")
        menu.add_separator()
        # 遍历 fire plan，将每组 fire plan 转换为字符串后添加到菜单上
        for fp in self.fire_plan_list:
            fp_str = f"{fp[0]} {self.ship_dict[fp[0]].name} 【射击】 {fp[1]} {self.ship_dict[fp[1]].name}"
            # menu.add_command(label=fp_str, command=lambda: self.del_fire_plan(fp))
            menu.add_command(label=fp_str, command=functools.partial(self.del_fire_plan, fp))
            
        # 弹出菜单
        menu.post(600, 100)

    def del_fire_plan(self, fp):   
        # print(fp)     
        self.fire_plan_list.remove(fp)

    def clear_objects(self):
        for item in self.find_all():
            if item != 1:
                self.delete(item)





