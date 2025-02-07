#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time     : 2025/1/19 上午12:15
# @Author   : Admin
# @File     : Gui.py
# @Software : PRC_FOREIGN_PERMANENT_RESIDENT_ID_CARD
# @实现功能  :
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import IdCardGenerator as IDGener
import Nationality
import pyperclip


class Yjj2023(tk.Frame):
    """永居证的页面"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # 证件信息
        self.id_info = None
        # 创建证件号码标签和输入框
        self.label_ID_No = tk.Label(self, text="证件号码:", anchor="e")
        self.label_ID_No.grid(row=1, column=0, sticky='e')
        self.ID_No = tk.StringVar()
        self.entry_ID_No = tk.Entry(self, textvariable=self.ID_No)
        self.entry_ID_No.grid(row=1, column=1)
        # 添加复制按钮
        self.btn_copy_ID_No = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.ID_No.get()))
        self.btn_copy_ID_No.grid(row=1, column=2)

        # 创建中文名标签和输入框
        self.label_name_CH = tk.Label(self, text="中文名:")
        self.label_name_CH.grid(row=2, column=0, sticky='e')
        self.name_CH = tk.StringVar()
        self.entry_name_CH = tk.Entry(self, textvariable=self.name_CH)
        self.entry_name_CH.grid(row=2, column=1)
        self.btn_copy_name_CH = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.name_CH.get()))
        self.btn_copy_name_CH.grid(row=2, column=2)

        # 创建英文名标签和输入框
        self.label_name_EN = tk.Label(self, text="英文名:")
        self.label_name_EN.grid(row=3, column=0, sticky='e')
        self.name_EN = tk.StringVar()
        self.entry_name_EN = tk.Entry(self, textvariable=self.name_EN)
        self.entry_name_EN.grid(row=3, column=1)
        self.btn_copy_name_EN = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.name_EN.get()))
        self.btn_copy_name_EN.grid(row=3, column=2)

        # 创建生日标签和输入框
        self.label_birthday = tk.Label(self, text="生日:", anchor="e")
        self.label_birthday.grid(row=4, column=0, sticky='e')
        self.birthday = tk.StringVar()
        self.entry_birthday = tk.Entry(self, textvariable=self.birthday)
        self.entry_birthday.grid(row=4, column=1)
        self.btn_copy_birthday = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.birthday.get()))
        self.btn_copy_birthday.grid(row=4, column=2)

        # 创建性别标签和输入框
        self.label_gender = tk.Label(self, text="性别:")
        self.label_gender.grid(row=5, column=0, sticky='e')
        self.gender = tk.StringVar()
        self.gender.set('')
        self.entry_gender_M = tk.Radiobutton(self, text='男', value='男', variable=self.gender)
        self.entry_gender_F = tk.Radiobutton(self, text='女', value='女', variable=self.gender)
        self.entry_gender_M.grid(row=5, column=1)
        self.entry_gender_F.grid(row=5, column=2)

        # 创建办理地区码标签和输入框
        self.label_province_code = tk.Label(self, text="办理地区码:")
        self.label_province_code.grid(row=6, column=0, sticky='e')
        self.province_code = tk.StringVar()
        self.entry_province_code = tk.Entry(self, textvariable=self.province_code)
        self.entry_province_code.grid(row=6, column=1)
        self.btn_copy_province_code = tk.Button(self, text="复制",
                                                command=lambda: pyperclip.copy(self.province_code.get()))
        self.btn_copy_province_code.grid(row=6, column=2)

        # 创建办理省份标签和输入框
        self.label_province_name = tk.Label(self, text="办理省份:")
        self.label_province_name.grid(row=7, column=0, sticky='e')
        self.province_name = tk.StringVar()
        self.entry_province_name = tk.Entry(self, textvariable=self.province_name)
        self.entry_province_name.grid(row=7, column=1)
        self.btn_copy_province_name = tk.Button(self, text="复制",
                                                command=lambda: pyperclip.copy(self.province_name.get()))
        self.btn_copy_province_name.grid(row=7, column=2)

        # 创建国籍代码标签和输入框
        self.label_nationality_number = tk.Label(self, text="国籍代码:")
        self.label_nationality_number.grid(row=8, column=0, sticky='e')
        self.nationality_number = tk.StringVar()
        self.entry_nationality_number = tk.Entry(self, textvariable=self.nationality_number)
        self.entry_nationality_number.grid(row=8, column=1)
        self.btn_copy_nationality_number = tk.Button(self, text="复制",
                                                     command=lambda: pyperclip.copy(self.nationality_number.get()))
        self.btn_copy_nationality_number.grid(row=8, column=2)

        # 创建国籍标签和输入框
        self.label_nationality_code = tk.Label(self, text="国籍简写:")
        self.label_nationality_code.grid(row=9, column=0, sticky='e')
        self.nationality_code = tk.StringVar()
        self.entry_nationality_code = tk.Entry(self, textvariable=self.nationality_code)
        self.entry_nationality_code.grid(row=9, column=1)
        self.btn_copy_nationality_code = tk.Button(self, text="复制",
                                                   command=lambda: pyperclip.copy(self.nationality_code.get()))
        self.btn_copy_nationality_code.grid(row=9, column=2)

        # 创建国家简称标签和输入框
        self.label_nationality_name_cn = tk.Label(self, text="国家简称:")
        self.label_nationality_name_cn.grid(row=10, column=0, sticky='e')
        self.nationality_name_cn = tk.StringVar()
        self.entry_nationality_name_cn = tk.Entry(self, textvariable=self.nationality_name_cn)
        self.entry_nationality_name_cn.grid(row=10, column=1)
        self.btn_copy_nationality_name_cn = tk.Button(self, text="复制",
                                                      command=lambda: pyperclip.copy(self.nationality_name_cn.get()))
        self.btn_copy_nationality_name_cn.grid(row=10, column=2)

        # 生成按钮
        self.btn_generate = tk.Button(self, text="自定义生成", command=self.generate_by_input)
        self.btn_generate.grid(row=11, column=0)
        # 刷新按钮
        self.btn_refresh = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh.grid(row=11, column=1)
        # 合成图像按钮
        self.btn_generate_image = tk.Button(self, text="合成图像", command=self.generate_image)
        self.btn_generate_image.grid(row=11, column=2)

        self.button_check = tk.Button(self, text="合法性校验", command=self.prompt)
        self.button_check.grid(row=12, column=0)

        self.button_check_gat = tk.Button(self, text="校验位补全",command=self.prompt)
        self.button_check_gat.grid(row=12, column=1)

        self.button_quit = tk.Button(self, text="退出", command=self.master.destroy)
        self.button_quit.grid(row=12, column=2)

        '''
        只有本类型的页面需要调用生成号码的逻辑,否则子类在使用super调用的时候会报错,因为子类会调用子类自己的generate_default()方法
        generate_default()中在show_info()时,此时子类并未完成初始化,会报错提示子类无某个属性
        '''
        if type(self) is Yjj2023:
            self.generate_default()

    def generate_by_input(self, event=None):
        # 依据自定义输入,需要同步修改其他文件的内容
        self.id_info = IDGener.TypeYJZ()
        self.show_info(self.id_info)

    def generate_default(self, event=None):  # event就是点击事件
        self.id_info = IDGener.TypeYJZ()
        # messagebox.showinfo("提示", "校验方法")
        self.show_info(self.id_info)

    def show_info(self, card_info: IDGener.TypeYJZ):
        """
        显示卡片信息。

        为所有标签绑定的变量实现赋值，以在界面上展示证件持有者的相关信息。

        参数:
        card_info (IDGener.TypeYJZ): 外国人永久居留证对象。
        """
        self.ID_No.set(card_info.No)
        self.name_EN.set(card_info.name_EN)
        self.name_CH.set(card_info.name_ch)
        self.birthday.set(card_info.birthday)
        self.gender.set(card_info.gender)
        self.province_code.set(card_info.province_code)
        self.province_name.set(Nationality.CODE_PROVINCE_DATA.get(int(card_info.province_code), '未知'))
        self.nationality_number.set(card_info.nationality_number)
        self.nationality_code.set(card_info.nationality_code)
        self.nationality_name_cn.set(card_info.nationality_name_ch)

    def generate_image(self, event=None):
        file_path = self.id_info.generate_image()
        pyperclip.copy(file_path)
        messagebox.showinfo("提示", f"生成证件图片并复制路径到剪切板:{file_path}")

    def prompt(self, event=None):
        print(type(self), event)
        messagebox.showinfo("提示", f"该功能暂未实现")


class Yjj2017(Yjj2023):
    """永居证的页面"""

    def __init__(self, master=None):
        super().__init__(master)

        # 取消显示办理地区码
        self.label_province_code.grid_forget()
        self.entry_province_code.grid_forget()
        self.btn_copy_province_code.grid_forget()
        self.label_province_name.grid_forget()
        self.entry_province_name.grid_forget()
        self.btn_copy_province_name.grid_forget()

        # 创建办理地区码标签和输入框
        self.label_city_code = tk.Label(self, text="办理省市码:")
        self.label_city_code.grid(row=6, column=0, sticky='e')
        self.city_code = tk.StringVar()
        self.entry_city_code = tk.Entry(self, textvariable=self.city_code)
        self.entry_city_code.grid(row=6, column=1)
        self.btn_copy_city_code = tk.Button(self, text="复制",
                                            command=lambda: pyperclip.copy(self.city_code.get()))
        self.btn_copy_city_code.grid(row=6, column=2)

        # 创建办理省份标签和输入框
        self.label_city_name = tk.Label(self, text="办理省市:")
        self.label_city_name.grid(row=7, column=0, sticky='e')
        self.city_name = tk.StringVar()
        self.entry_city_name = tk.Entry(self, textvariable=self.city_name)
        self.entry_city_name.grid(row=7, column=1)
        self.btn_copy_city_name = tk.Button(self, text="复制",
                                            command=lambda: pyperclip.copy(self.city_name.get()))
        self.btn_copy_city_name.grid(row=7, column=2)

        self.generate_default()

    def generate_default(self, event=None):  # event就是点击事件
        id_info = IDGener.TypeYJZ2017()
        # messagebox.showinfo("提示", "校验方法")
        self.show_info(id_info)

    def generate_by_input(self, event=None):
        # 依据自定义输入,需要同步修改其他文件的内容
        id_info = IDGener.TypeYJZ2017()
        self.show_info(id_info)

    def show_info(self, card_info: IDGener.TypeYJZ2017):
        """
        显示卡片信息。

        为所有标签绑定的变量实现赋值，以在界面上展示证件持有者的相关信息。

        参数:
        card_info (IDGener.TypeYJZ): 外国人永久居留证对象。
        """

        self.ID_No.set(card_info.No)
        self.name_EN.set(card_info.name_EN)
        self.name_CH.set(card_info.name_ch)
        self.birthday.set(card_info.birthday)
        self.gender.set(card_info.gender)
        self.city_code.set(card_info.city_code)
        province_code = card_info.city_code[0:2] + '0000'
        province_name = Nationality.administrative_division.get(province_code)
        self.city_name.set(province_name + card_info.city_name)
        self.nationality_number.set(card_info.nationality_number)
        self.nationality_code.set(card_info.nationality_code)
        self.nationality_name_cn.set(card_info.nationality_name_ch)


class GATJzz(tk.Frame):
    """港澳台居住证的页面"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # 创建港澳台页面的组件
        self.id_type = tk.StringVar()
        self.label_id_type = tk.Label(self, text="证件类别:")
        self.label_id_type.grid(row=1, column=0, sticky='e')
        gat_id_type = tuple(member.value for member in IDGener.GATPermanentResident)
        self.combobox_id_type = ttk.Combobox(self, textvariable=self.id_type, values=gat_id_type)
        self.combobox_id_type.bind("<<ComboboxSelected>>", self.generate_default)
        self.combobox_id_type.grid(row=1, column=1, sticky='w')

        self.label_name_CH = tk.Label(self, text="中文名:")
        self.label_name_CH.grid(row=2, column=0, sticky='e')
        self.name_CH = tk.StringVar()
        self.entry_name_CH = tk.Entry(self, textvariable=self.name_CH)
        self.entry_name_CH.grid(row=2, column=1)
        self.btn_copy_name_CH = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.name_CH.get()))
        self.btn_copy_name_CH.grid(row=2, column=2)

        self.label_ID_No = tk.Label(self, text="证件号码:", anchor="e")
        self.label_ID_No.grid(row=3, column=0, sticky='e')
        self.ID_No = tk.StringVar()
        self.entry_ID_No = tk.Entry(self, textvariable=self.ID_No)
        self.entry_ID_No.grid(row=3, column=1)
        self.btn_copy_ID_No = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.ID_No.get()))
        self.btn_copy_ID_No.grid(row=3, column=2)

        # 创建生日标签和输入框
        self.label_birthday = tk.Label(self, text="生日:", anchor="e")
        self.label_birthday.grid(row=4, column=0, sticky='e')
        self.birthday = tk.StringVar()
        self.entry_birthday = tk.Entry(self, textvariable=self.birthday)
        self.entry_birthday.grid(row=4, column=1)
        self.btn_copy_birthday = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.birthday.get()))
        self.btn_copy_birthday.grid(row=4, column=2)

        # 创建性别标签和输入框
        self.label_gender = tk.Label(self, text="性别:")
        self.label_gender.grid(row=5, column=0, sticky='e')
        self.gender = tk.StringVar()
        self.gender.set('')
        self.entry_gender_M = tk.Radiobutton(self, text='男', value='男', variable=self.gender)
        self.entry_gender_F = tk.Radiobutton(self, text='女', value='女', variable=self.gender)
        self.entry_gender_M.grid(row=5, column=1)
        self.entry_gender_F.grid(row=5, column=2)

        # 创建办理地区码标签和输入框
        self.label_province_code = tk.Label(self, text="地区码:")
        self.label_province_code.grid(row=6, column=0, sticky='e')
        self.province_code = tk.StringVar()
        self.entry_province_code = tk.Entry(self, textvariable=self.province_code)
        self.entry_province_code.grid(row=6, column=1)
        self.btn_copy_province_code = tk.Button(self, text="复制",
                                                command=lambda: pyperclip.copy(self.province_code.get()))
        self.btn_copy_province_code.grid(row=6, column=2)

        # 创建办理省份标签和输入框
        self.label_province_name = tk.Label(self, text="地区:")
        self.label_province_name.grid(row=7, column=0, sticky='e')
        self.province_name = tk.StringVar()
        self.entry_province_name = tk.Entry(self, textvariable=self.province_name)
        self.entry_province_name.grid(row=7, column=1)
        self.btn_copy_province_name = tk.Button(self, text="复制",
                                                command=lambda: pyperclip.copy(self.province_name.get()))
        self.btn_copy_province_name.grid(row=7, column=2)

        # 生成按钮
        self.btn_generate_gat = tk.Button(self, text="自定义生成", command=lambda: print("生成港澳台"))
        self.btn_generate_gat.grid(row=11, column=0)
        # 刷新按钮
        self.btn_refresh_gat = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh_gat.grid(row=11, column=1)

        self.button_check_gat = tk.Button(self, text="合法性校验")
        self.button_check_gat.grid(row=11, column=2)

        self.button_check_gat = tk.Button(self, text="校验位补全")
        self.button_check_gat.grid(row=11, column=3)

        self.button_quit_gat = tk.Button(self, text="退出", command=self.master.destroy)
        self.button_quit_gat.grid(row=11, column=4)

        # 默认显示香港居住证
        self.id_type.set(IDGener.GATPermanentResident.HKG_PERMANENT_RESIDENT.value)
        self.generate_default()

    def generate_by_input(self, event=None):
        # 依据自定义输入,需要同步修改其他文件的内容
        id_info = IDGener.TypeGATJZZ(self.id_type.get())
        self.show_info(id_info)

    def generate_default(self, event=None):  # event就是点击事件
        id_info = IDGener.TypeGATJZZ(self.id_type.get())
        # messagebox.showinfo("提示", "校验方法")
        self.show_info(id_info)

    def show_info(self, card_info: IDGener.TypeGATJZZ):
        self.ID_No.set(card_info.No)
        self.name_CH.set(card_info.name_ch)
        self.birthday.set(card_info.birthday)
        self.gender.set(card_info.gender)
        self.province_code.set(card_info.region_code)
        self.province_name.set(card_info.province_name)


class GAtxz(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # 创建港澳台页面的组件
        self.id_type = tk.StringVar()
        self.label_id_type = tk.Label(self, text="证件类别:")
        self.label_id_type.grid(row=1, column=0, sticky='e')
        ga_id_type = tuple(member.value for member in IDGener.HkgMacPermit)
        self.combobox_id_type = ttk.Combobox(self, textvariable=self.id_type, values=ga_id_type)
        self.combobox_id_type.bind("<<ComboboxSelected>>", self.generate_default)
        self.combobox_id_type.grid(row=1, column=1, sticky='w')

        self.label_ID_No = tk.Label(self, text="证件号码:", anchor="e")
        self.label_ID_No.grid(row=2, column=0, sticky='e')
        self.ID_No = tk.StringVar()
        self.entry_ID_No = tk.Entry(self, textvariable=self.ID_No)
        self.entry_ID_No.grid(row=2, column=1, sticky='w')
        self.btn_copy_ID_No = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.ID_No.get()))
        self.btn_copy_ID_No.grid(row=2, column=2)

        self.label_name_CH = tk.Label(self, text="中文名:")
        self.label_name_CH.grid(row=3, column=0, sticky='e')
        self.name_CH = tk.StringVar()
        self.entry_name_CH = tk.Entry(self, textvariable=self.name_CH)
        self.entry_name_CH.grid(row=3, column=1)
        self.btn_copy_name_CH = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.name_CH.get()))
        self.btn_copy_name_CH.grid(row=3, column=2)

        self.btn_refresh_gat = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh_gat.grid(row=4, column=0)

        self.btn_refresh_gat = tk.Button(self, text="退出", command=self.master.destroy)
        self.btn_refresh_gat.grid(row=4, column=1)

        # 默认显示香港通行证
        self.id_type.set(IDGener.HkgMacPermit.HKG_PERMIT.value)
        self.generate_default()

    def generate_default(self, event=None):
        id_info = IDGener.TypeGATXZ(self.id_type.get())
        self.ID_No.set(id_info.No)
        self.name_CH.set(id_info.name_ch)


class TWtxz(tk.Frame):
    """台湾通行证"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.label_ID_No = tk.Label(self, text="证件号码:", anchor="e")
        self.label_ID_No.grid(row=1, column=0, sticky='e')
        self.ID_No = tk.StringVar()
        self.entry_ID_No = tk.Entry(self, textvariable=self.ID_No)
        self.entry_ID_No.grid(row=1, column=1)
        self.btn_copy_ID_No = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.ID_No.get()))
        self.btn_copy_ID_No.grid(row=1, column=2)

        self.label_name_CH = tk.Label(self, text="中文名:")
        self.label_name_CH.grid(row=2, column=0, sticky='e')
        self.name_CH = tk.StringVar()
        self.entry_name_CH = tk.Entry(self, textvariable=self.name_CH)
        self.entry_name_CH.grid(row=2, column=1)
        self.btn_copy_name_CH = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.name_CH.get()))
        self.btn_copy_name_CH.grid(row=2, column=2)

        self.btn_refresh_gat = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh_gat.grid(row=3, column=0)

        self.btn_refresh_gat = tk.Button(self, text="退出", command=self.master.destroy)
        self.btn_refresh_gat.grid(row=3, column=1)

        self.generate_default()

    def generate_default(self, event=None):
        id_info = IDGener.TypeTWTXZ()
        self.ID_No.set(id_info.No)
        self.name_CH.set(id_info.name_ch)


class MainApplication(tk.Tk):
    def __init__(self, id_kinds, ):
        super().__init__()
        self.title("永居证生成器")
        self.id_kind = tk.StringVar()
        self.label_id_kinds = tk.Label(self, text="证件类型:")
        self.label_id_kinds.grid(row=0, column=0, sticky='e')
        self.combobox_id_kind = ttk.Combobox(self, textvariable=self.id_kind, values=id_kinds)
        self.combobox_id_kind.bind("<<ComboboxSelected>>", self.create_frame)
        self.combobox_id_kind.grid(row=0, column=1, sticky='w')
        self.geometry("300x500+300+200")

        # 创建不同的 Frame
        self.yjj_frame = Yjj2023(self)

        # 默认显示永居证页面
        self.id_kind.set(IDGener.IDType.FOREIGN_PERMANENT_RESIDENT2023.value)
        self.show_frame(self.yjj_frame)

    def show_frame(self, frame=None):
        # 隐藏所有 Frame
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.grid_forget()
        # 显示指定的 Frame
        if frame:
            frame.grid(row=1, column=0, columnspan=4, padx=0, pady=20)

    def create_frame(self, event):
        if IDGener.IDType.FOREIGN_PERMANENT_RESIDENT2023.value == str(self.id_kind.get()):
            self.show_frame(self.yjj_frame)
        elif IDGener.IDType.GAT_PERMANENT_RESIDENT.value == str(self.id_kind.get()):
            self.show_frame(GATJzz(self))
        elif IDGener.IDType.HKG_MAC_PERMIT.value == str(self.id_kind.get()):
            self.show_frame(GAtxz(self))
        elif IDGener.IDType.CTN_PERMIT.value == str(self.id_kind.get()):
            self.show_frame(TWtxz(self))
        elif IDGener.IDType.FOREIGN_PERMANENT_RESIDENT2017.value == str(self.id_kind.get()):
            self.show_frame(Yjj2017(self))
        else:
            self.show_frame()


if __name__ == '__main__':
    # root = tk.Tk()
    # root.title("永居证生成器")
    id_kinds_all = tuple(member.value for member in IDGener.IDType)
    # id_kind = tk.StringVar()
    # label_id_kinds = tk.Label(root, text="证件类型:")
    # label_id_kinds.grid(row=0, column=0, sticky='e')
    # combobox_id_kind = ttk.Combobox(root, text variable=id_kind, values=id_kinds)
    # combobox_id_kind.bind("<<ComboboxSelected>>", lambda e: print(id_kind.get()))
    # combobox_id_kind.grid(row=0, column=1, sticky='w')
    # # 设置窗口大小和位置,先横后纵,左上角为原点
    # root.geometry("700x700+300+200")
    # root.mainloop()
    a = MainApplication(id_kinds_all)
    a.mainloop()
