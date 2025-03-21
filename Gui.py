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
import pyperclip
import Nationality
import IdCardGenerator
from abc import abstractmethod, ABC

LABEL_BG ='#80FFFF'


class BaseCardFrame(tk.Frame, ABC):
    """抽象基类，定义 generate_default 方法"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.id_info = None

    @abstractmethod
    def generate_default(self):
        """生成默认信息的抽象方法"""
        pass


class Sfz(tk.Frame):
    """身份证的页面"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # 证件信息,IDGener.TypeSFZ类型
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
        self.label_name_ch = tk.Label(self, text="中文名:", bg=LABEL_BG)
        self.label_name_ch.grid(row=2, column=0, sticky='e')
        self.name_ch = tk.StringVar()
        self.entry_name_ch = tk.Entry(self, textvariable=self.name_ch)
        self.entry_name_ch.grid(row=2, column=1)
        self.btn_copy_name_ch = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.name_ch.get()))
        self.btn_copy_name_ch.grid(row=2, column=2)

        # 创建英文名标签和输入框
        self.label_name_en = tk.Label(self, text="英文名:", bg=LABEL_BG)
        self.label_name_en.grid(row=3, column=0, sticky='e')
        self.name_en = tk.StringVar()
        self.entry_name_en = tk.Entry(self, textvariable=self.name_en)
        self.entry_name_en.grid(row=3, column=1)
        self.btn_copy_name_en = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.name_en.get()))
        self.btn_copy_name_en.grid(row=3, column=2)

        # 创建生日标签和输入框
        self.label_birthday = tk.Label(self, text="生日:", anchor="e", bg=LABEL_BG)
        self.label_birthday.grid(row=4, column=0, sticky='e')
        self.birthday = tk.StringVar()
        self.entry_birthday = tk.Entry(self, textvariable=self.birthday)
        self.entry_birthday.grid(row=4, column=1)
        self.btn_copy_birthday = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.birthday.get()))
        self.btn_copy_birthday.grid(row=4, column=2)

        # 创建性别标签和输入框
        self.label_gender = tk.Label(self, text="性别:", bg=LABEL_BG)
        self.label_gender.grid(row=5, column=0, sticky='e')
        self.gender = tk.StringVar()
        self.gender.set("")
        self.entry_gender_M = tk.Radiobutton(self, text='男', value='男', variable=self.gender)
        self.entry_gender_F = tk.Radiobutton(self, text='女', value='女', variable=self.gender)
        self.entry_gender_M.grid(row=5, column=1)
        self.entry_gender_F.grid(row=5, column=2)

        # 创建办理地区码标签和输入框
        self.label_administration_code = tk.Label(self, text="行政区代码:", bg=LABEL_BG)
        self.label_administration_code.grid(row=6, column=0, sticky='e')
        self.administration_code = tk.StringVar()
        self.entry_administration_code = tk.Entry(self, textvariable=self.administration_code)
        self.entry_administration_code.grid(row=6, column=1)
        self.btn_copy_administration_code = tk.Button(self, text="复制",
                                                      command=lambda: pyperclip.copy(self.administration_code.get()))
        self.btn_copy_administration_code.grid(row=6, column=2)

        # 创建办理省份标签和输入框
        self.label_province_name = tk.Label(self, text="省:")
        self.label_province_name.grid(row=7, column=0, sticky='e')
        self.province_name = tk.StringVar()
        self.entry_province_name = tk.Entry(self, textvariable=self.province_name)
        self.entry_province_name.grid(row=7, column=1)
        self.btn_copy_province_name = tk.Button(self, text="复制",
                                                command=lambda: pyperclip.copy(self.province_name.get()))
        self.btn_copy_province_name.grid(row=7, column=2)

        # 创建国籍编号标签和输入框
        self.label_city_name = tk.Label(self, text="市:")
        self.label_city_name.grid(row=8, column=0, sticky='e')
        self.city_name = tk.StringVar()
        self.entry_city_name = tk.Entry(self, textvariable=self.city_name)
        self.entry_city_name.grid(row=8, column=1)
        self.btn_copy_city_name = tk.Button(self, text="复制",
                                            command=lambda: pyperclip.copy(self.city_name.get()))
        self.btn_copy_city_name.grid(row=8, column=2)

        # 创建国籍标签和输入框
        self.label_county_name = tk.Label(self, text="县:")
        self.label_county_name.grid(row=9, column=0, sticky='e')
        self.county_name = tk.StringVar()
        self.entry_county_name = tk.Entry(self, textvariable=self.county_name)
        self.entry_county_name.grid(row=9, column=1)
        self.btn_copy_county_name = tk.Button(self, text="复制",
                                              command=lambda: pyperclip.copy(self.county_name.get()))
        self.btn_copy_county_name.grid(row=9, column=2)

        # 刷新按钮
        self.btn_refresh = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh.grid(row=11, column=1)

        self.button_check = tk.Button(self, text="清除信息", command=self.clear_all_fields)
        create_tooltip(self.button_check, text="清除所有输入框中的信息")
        self.button_check.grid(row=11, column=0)

        # 自定义生成按钮
        self.btn_generate = tk.Button(self, text="自定义生成", command=self.generate_by_input)
        create_tooltip(self.btn_generate, text="依据变色字段输入进行生成")
        self.btn_generate.grid(row=12, column=0)

        # 校验码计算
        self.button_check_num_calculate = tk.Button(self, text="校验位补全", command=self.check_number_complete)
        create_tooltip(self.button_check_num_calculate, text="只做校验位计算并补全")
        self.button_check_num_calculate.grid(row=12, column=1)

        self.button_quit = tk.Button(self, text="退出", command=self.master.destroy)
        self.button_quit.grid(row=12, column=2)

        self.generate_default()

    def generate_default(self):
        self.id_info = IdCardGenerator.TypeSFZ()
        self.show_info()

    def generate_by_input(self):
        name_ch = self.entry_name_ch.get() or None
        name_en = self.entry_name_en.get() or None
        birthday = self.entry_birthday.get() or None
        gender = self.gender.get() or None
        administration_code = self.entry_administration_code.get() or None
        try:
            self.id_info = IdCardGenerator.TypeSFZ(name_ch, name_en, birthday, gender, county_code=administration_code)
            self.show_info()
        except Exception as e:
            messagebox.showinfo("提示", f"输入有误,错误信息为{e}")

    def check_number_complete(self):
        ID_No_src = self.ID_No.get()
        ID_No_src = ID_No_src[0:17]
        try:
            ID_No_src = IdCardGenerator.IDNOGenerator.calculate_check_num_cls(ID_No_src)
        except ValueError as e:
            messagebox.showinfo("提示", f"输入有误,{e}")
        self.ID_No.set(ID_No_src)

    def clear_all_fields(self):
        self.ID_No.set('')
        self.name_ch.set('')
        self.name_en.set('')
        self.birthday.set('')
        self.gender.set('')
        self.administration_code.set('')
        self.province_name.set('')
        self.city_name.set('')
        self.county_name.set('')

    def show_info(self):
        self.ID_No.set(self.id_info.No)
        self.name_ch.set(self.id_info.name_ch)
        self.name_en.set(self.id_info.name_en)
        self.birthday.set(self.id_info.birthday)
        self.gender.set(self.id_info.gender)
        self.administration_code.set(self.id_info.county_code)
        self.province_name.set(self.id_info.province_name)
        self.city_name.set(self.id_info.city_name)
        self.county_name.set(self.id_info.county_name)


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
        self.label_name_ch = tk.Label(self, text="中文名:", bg=LABEL_BG)
        self.label_name_ch.grid(row=2, column=0, sticky='e')
        self.name_ch = tk.StringVar()
        self.entry_name_ch = tk.Entry(self, textvariable=self.name_ch)
        self.entry_name_ch.grid(row=2, column=1)
        self.btn_copy_name_ch = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.name_ch.get()))
        self.btn_copy_name_ch.grid(row=2, column=2)

        # 创建英文名标签和输入框
        self.label_name_en = tk.Label(self, text="英文名:", bg=LABEL_BG)
        self.label_name_en.grid(row=3, column=0, sticky='e')
        self.name_en = tk.StringVar()
        self.entry_name_en = tk.Entry(self, textvariable=self.name_en)
        self.entry_name_en.grid(row=3, column=1)
        self.btn_copy_name_en = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.name_en.get()))
        self.btn_copy_name_en.grid(row=3, column=2)

        # 创建生日标签和输入框
        self.label_birthday = tk.Label(self, text="生日:", anchor="e", bg=LABEL_BG)
        self.label_birthday.grid(row=4, column=0, sticky='e')
        self.birthday = tk.StringVar()
        self.entry_birthday = tk.Entry(self, textvariable=self.birthday)
        self.entry_birthday.grid(row=4, column=1)
        self.btn_copy_birthday = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.birthday.get()))
        self.btn_copy_birthday.grid(row=4, column=2)

        # 创建性别标签和输入框
        self.label_gender = tk.Label(self, text="性别:", bg=LABEL_BG)
        self.label_gender.grid(row=5, column=0, sticky='e')
        self.gender = tk.StringVar()
        self.gender.set("")
        self.entry_gender_M = tk.Radiobutton(self, text='男', value='男', variable=self.gender)
        self.entry_gender_F = tk.Radiobutton(self, text='女', value='女', variable=self.gender)
        self.entry_gender_M.grid(row=5, column=1)
        self.entry_gender_F.grid(row=5, column=2)

        # 创建办理地区码标签和输入框
        self.label_province_code = tk.Label(self, text="办理地区码:", bg=LABEL_BG)
        self.label_province_code.grid(row=6, column=0, sticky='e')
        self.province_code = tk.StringVar()
        self.entry_province_code = tk.Entry(self, textvariable=self.province_code)
        self.entry_province_code.grid(row=6, column=1)
        self.btn_copy_province_code = tk.Button(self, text="复制",
                                                command=lambda: pyperclip.copy(self.province_code.get()))
        self.btn_copy_province_code.grid(row=6, column=2)

        # 创建办理省份标签和输入框
        self.label_province_name = tk.Label(self, text="办理省份:", bg=LABEL_BG)
        self.label_province_name.grid(row=7, column=0, sticky='e')
        self.province_name = tk.StringVar()
        self.entry_province_name = tk.Entry(self, textvariable=self.province_name)
        self.entry_province_name.grid(row=7, column=1)
        self.btn_copy_province_name = tk.Button(self, text="复制",
                                                command=lambda: pyperclip.copy(self.province_name.get()))
        self.btn_copy_province_name.grid(row=7, column=2)

        # 创建国籍代码标签和输入框
        self.label_nationality_number = tk.Label(self, text="国籍编号:")
        self.label_nationality_number.grid(row=8, column=0, sticky='e')
        self.nationality_number = tk.StringVar()
        self.entry_nationality_number = tk.Entry(self, textvariable=self.nationality_number)
        self.entry_nationality_number.grid(row=8, column=1)
        self.btn_copy_nationality_number = tk.Button(self, text="复制",
                                                     command=lambda: pyperclip.copy(self.nationality_number.get()))
        self.btn_copy_nationality_number.grid(row=8, column=2)

        # 创建国籍代码标签和输入框
        self.label_nationality_code = tk.Label(self, text="国籍代码:", bg=LABEL_BG)
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

        # 对应其他版本永居证的号码
        self.label_ID_No_other = tk.Label(self, text="旧版号码:", anchor="e")
        self.label_ID_No_other.grid(row=11, column=0, sticky='e')
        self.ID_No_other = tk.StringVar()
        self.entry_ID_No_other = tk.Entry(self, textvariable=self.ID_No_other)
        self.entry_ID_No_other.grid(row=11, column=1)

        # 添加复制按钮
        self.btn_copy_ID_No_other = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.ID_No_other.get()))
        self.btn_copy_ID_No_other.grid(row=11, column=2)

        # 刷新按钮
        self.btn_refresh = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh.grid(row=12, column=1)

        # 合成图像按钮
        self.btn_generate_image = tk.Button(self, text="合成图像", command=self.generate_image)
        self.btn_generate_image.grid(row=12, column=2)

        self.button_check = tk.Button(self, text="清除信息", command=self.clear_all_fields)
        create_tooltip(self.button_check, text="清除所有输入框中的信息")
        self.button_check.grid(row=12, column=0)

        # 自定义生成按钮
        self.btn_generate = tk.Button(self, text="自定义生成", command=self.generate_by_input)
        create_tooltip(self.btn_generate, text="依据变色字段输入进行生成")
        self.btn_generate.grid(row=13, column=0)

        # 校验码计算
        self.button_check_num_calculate = tk.Button(self, text="校验位补全", command=self.check_number_complete)
        create_tooltip(self.button_check_num_calculate, text="只做校验位计算并补全")
        self.button_check_num_calculate.grid(row=13, column=1)

        self.button_quit = tk.Button(self, text="退出", command=self.master.destroy)
        self.button_quit.grid(row=13, column=2)

        '''
        只有本类型的页面需要调用生成号码的逻辑,否则子类在使用super调用的时候会报错,因为子类会调用子类自己的generate_default()方法
        generate_default()中在show_info()时,此时子类并未完成初始化,会报错提示子类无某个属性
        '''
        if type(self) is Yjj2023:
            self.generate_default()

    def generate_by_input(self, event=None):
        # 依据自定义输入,需要同步修改其他文件的内容
        name_ch = self.entry_name_ch.get() or None
        name_en = self.entry_name_en.get() or None
        birthday = self.entry_birthday.get() or None
        gender = self.gender.get() or None
        province_code = self.entry_province_code.get() or None
        province_name = self.entry_province_name.get() or None
        if province_name is None and province_code:
            # 名称优先级高,同时输入了代码和名称时,根据名称查不到代码才使用代码信息,下方的国籍也是一样的
            try:
                province_name = Nationality.administration_division[province_code]
            except KeyError as e:
                messagebox.showinfo("提示", f"地区码码不合法,错误信息为:{e},请重新输入")
                return
        nationality_code = self.entry_nationality_code.get() or None
        # nationality_name_cn = self.entry_nationality_name_cn.get() or None
        try:
            self.id_info = IdCardGenerator.TypeYJZ(
                name_ch=name_ch,
                name_en=name_en,
                province_name=province_name,
                birthday=birthday,
                gender=gender,
                national_code_3=nationality_code
            )
            self.show_info(self.id_info)
        except Exception as e:
            messagebox.showinfo("提示", f"自定义生成出错,错误信息为:{e}")


    def generate_default(self, event=None):  # event就是点击事件
        self.id_info = IdCardGenerator.TypeYJZ()
        # messagebox.showinfo("提示", "校验方法")
        self.show_info(self.id_info)

    def show_info(self, card_info: IdCardGenerator.TypeYJZ):
        """
        显示卡片信息。

        为所有标签绑定的变量实现赋值，以在界面上展示证件持有者的相关信息。

        参数:
        card_info (IDGener.TypeYJZ): 外国人永久居留证对象。
        """
        self.ID_No.set(card_info.No)
        self.name_en.set(card_info.name_en)
        self.name_ch.set(card_info.name_ch)
        self.birthday.set(card_info.birthday)
        self.gender.set(card_info.gender)
        self.province_code.set(card_info.province_code)
        self.province_name.set(Nationality.CODE_PROVINCE_DATA.get(int(card_info.province_code), '未知'))
        self.nationality_number.set(card_info.nationality_number)
        self.nationality_code.set(card_info.nationality_code)
        self.nationality_name_cn.set(card_info.nationality_name_ch)
        self.ID_No_other.set('有需要在2017版页面中用校验位补全的方式生成')

    def generate_image(self, event=None):
        try:
            file_path = self.id_info.generate_image()
            pyperclip.copy(file_path)
            messagebox.showinfo("提示", f"生成证件图片并复制路径到剪切板:{file_path}")
        except Exception as e:
            messagebox.showinfo("提示", f"生成证件图片出错,错误信息为:{e}")

    def clear_all_fields(self):
        """
        清除所有标签组件的值
        """
        self.ID_No.set("")
        self.name_ch.set("")
        self.name_en.set("")
        self.birthday.set("")
        self.gender.set("")
        self.province_code.set("")
        self.province_name.set("")
        self.nationality_number.set("")
        self.nationality_code.set("")
        self.nationality_name_cn.set("")
        self.ID_No_other.set('')

    def check_number_complete(self, event=None):
        ID_No_src = self.ID_No.get()
        ID_No_src = ID_No_src[0:17]
        try:
            ID_No_src = IdCardGenerator.IDNOGenerator.calculate_check_num_cls(ID_No_src)
        except ValueError as e:
            messagebox.showinfo("提示", f"输入有误,{e}")
        self.ID_No.set(ID_No_src)
        # print(type(self), event)


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
        self.label_city_code = tk.Label(self, text="办理省市码:", bg=LABEL_BG)
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
        # 对应其他版本永居证的号码
        self.label_ID_No_other = tk.Label(self, text="新版号码:", anchor="e")
        self.label_ID_No_other.grid(row=11, column=0, sticky='e')
        # 不显示合成图像按钮
        self.btn_generate_image.grid_forget()

        self.generate_default()

    def generate_default(self, event=None):  # event就是点击事件
        id_info = IdCardGenerator.TypeYJZ2017()
        # messagebox.showinfo("提示", "校验方法")
        self.show_info(id_info)

    def generate_by_input(self, event=None):
        # 依据自定义输入,需要同步修改其他文件的内容
        name_ch = self.entry_name_ch.get() or None
        name_en = self.entry_name_en.get() or None
        birthday = self.entry_birthday.get() or None
        gender = self.gender.get() or None
        nationality_code = self.entry_nationality_code.get() or None
        city_code = self.entry_city_code.get() or None
        # nationality_name_cn = self.entry_nationality_name_cn.get() or None
        try:
            self.id_info = IdCardGenerator.TypeYJZ2017(
                name_ch=name_ch,
                name_en=name_en,
                national_abbreviation=nationality_code,
                province_city_code=city_code,
                birthday=birthday,
                gender=gender,
            )
            self.show_info(self.id_info)
        except Exception as e:
            messagebox.showinfo("提示", f"自定义生成出错,错误信息为:{e}")


    def show_info(self, card_info: IdCardGenerator.TypeYJZ2017):
        """
        显示卡片信息。

        为所有标签绑定的变量实现赋值，以在界面上展示证件持有者的相关信息。

        参数:
        card_info (IDGener.TypeYJZ): 外国人永久居留证对象。
        """

        self.ID_No.set(card_info.No)
        self.name_en.set(card_info.name_en)
        self.name_ch.set(card_info.name_ch)
        self.birthday.set(card_info.birthday)
        self.gender.set(card_info.gender)
        self.city_code.set(card_info.city_code)
        province_code = card_info.city_code[0:2] + '0000'
        if province_code not in Nationality.CODE_HONGKONG_MACAO_TAIWAN:
            province_name = Nationality.administration_division.get(province_code)
        else:
            province_name = ''
        self.city_name.set(province_name + card_info.city_name)
        self.nationality_number.set(card_info.nationality_number)
        self.nationality_code.set(card_info.nationality_code)
        self.nationality_name_cn.set(card_info.nationality_name_ch)
        self.ID_No_other.set(card_info.No_2023)

    def clear_all_fields(self):
        super().clear_all_fields()
        self.city_code.set("")
        self.city_name.set("")

    def check_number_complete(self, event=None):
        ID_No_src = self.ID_No.get()
        check_num = ''
        try:
            ID_No_src = ID_No_src[0:14]
            check_num = IdCardGenerator.calculate_check_num_731(ID_No_src)
        except Exception as e:
            messagebox.showinfo("提示", f"输入有误,错误信息:{e}")
        self.ID_No.set(ID_No_src + check_num)


class GATJzz(tk.Frame):
    """港澳台居民居住证的页面"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # 行号迭代器，注意next方法返回当前值
        row_num = RowNumIterator(1)

        # 创建港澳台页面的组件
        self.id_type = tk.StringVar()
        self.label_id_type = tk.Label(self, text="证件类别:")
        self.label_id_type.grid(row=row_num.current, column=0, sticky='e')
        gat_id_type = tuple(member.value for member in IdCardGenerator.GATPermanentResident)
        self.combobox_id_type = ttk.Combobox(self, textvariable=self.id_type, values=gat_id_type)
        self.combobox_id_type.bind("<<ComboboxSelected>>", self.generate_default)
        self.combobox_id_type.grid(row=next(row_num), column=1, sticky='w')

        self.label_ID_No = tk.Label(self, text="证件号码:", anchor="e")
        self.label_ID_No.grid(row=row_num.current, column=0, sticky='e')
        self.ID_No = tk.StringVar()
        self.entry_ID_No = tk.Entry(self, textvariable=self.ID_No)
        self.entry_ID_No.grid(row=row_num.current, column=1)
        self.btn_copy_ID_No = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.ID_No.get()))
        self.btn_copy_ID_No.grid(row=next(row_num), column=2)

        self.label_name_ch = tk.Label(self, text="中文名:", bg=LABEL_BG)
        self.label_name_ch.grid(row=row_num.current, column=0, sticky='e')
        self.name_ch = tk.StringVar()
        self.entry_name_ch = tk.Entry(self, textvariable=self.name_ch)
        self.entry_name_ch.grid(row=row_num.current, column=1)
        self.btn_copy_name_ch = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.name_ch.get()))
        self.btn_copy_name_ch.grid(row=next(row_num), column=2)

        # 创建英文名标签和输入框
        self.label_name_en = tk.Label(self, text="英文名:", bg=LABEL_BG)
        self.label_name_en.grid(row=row_num.current, column=0, sticky='e')
        self.name_en = tk.StringVar()
        self.entry_name_en = tk.Entry(self, textvariable=self.name_en)
        self.entry_name_en.grid(row=row_num.current, column=1)
        self.btn_copy_name_en = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.name_en.get()))
        self.btn_copy_name_en.grid(row=next(row_num), column=2)


        # 创建生日标签和输入框
        self.label_birthday = tk.Label(self, text="生日:", anchor="e", bg=LABEL_BG)
        self.label_birthday.grid(row=row_num.current, column=0, sticky='e')
        self.birthday = tk.StringVar()
        self.entry_birthday = tk.Entry(self, textvariable=self.birthday)
        self.entry_birthday.grid(row=row_num.current, column=1)
        self.btn_copy_birthday = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.birthday.get()))
        self.btn_copy_birthday.grid(row=next(row_num), column=2)

        # 创建性别标签和输入框
        self.label_gender = tk.Label(self, text="性别:", bg=LABEL_BG)
        self.label_gender.grid(row=row_num.current, column=0, sticky='e')
        self.gender = tk.StringVar()
        self.gender.set('')
        self.entry_gender_M = tk.Radiobutton(self, text='男', value='男', variable=self.gender)
        self.entry_gender_F = tk.Radiobutton(self, text='女', value='女', variable=self.gender)
        self.entry_gender_M.grid(row=row_num.current, column=1)
        self.entry_gender_F.grid(row=next(row_num), column=2)

        # 创建办理地区码标签和输入框
        self.label_province_code = tk.Label(self, text="地区码:")
        self.label_province_code.grid(row=row_num.current, column=0, sticky='e')
        self.province_code = tk.StringVar()
        self.entry_province_code = tk.Entry(self, textvariable=self.province_code)
        self.entry_province_code.grid(row=row_num.current, column=1)
        self.btn_copy_province_code = tk.Button(self, text="复制",
                                                command=lambda: pyperclip.copy(self.province_code.get()))
        self.btn_copy_province_code.grid(row=next(row_num), column=2)

        # 创建办理省份标签和输入框
        self.label_province_name = tk.Label(self, text="地区:")
        self.label_province_name.grid(row=row_num.current, column=0, sticky='e')
        self.province_name = tk.StringVar()
        self.entry_province_name = tk.Entry(self, textvariable=self.province_name)
        self.entry_province_name.grid(row=row_num.current, column=1)
        self.btn_copy_province_name = tk.Button(self, text="复制",
                                                command=lambda: pyperclip.copy(self.province_name.get()))
        self.btn_copy_province_name.grid(row=next(row_num), column=2)

        # 清理按钮
        self.btn_clear_gat = tk.Button(self, text="清除信息", command=self.clear_all_fields)
        create_tooltip(self.btn_clear_gat, text="清除所有输入框中的信息")
        self.btn_clear_gat.grid(row=row_num.current, column=0)
        # 刷新按钮
        self.btn_refresh_gat = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh_gat.grid(row=row_num.current, column=1)

        self.button_check_gat = tk.Button(self, text="校验位补全", command=self.check_num_complete)
        self.button_check_gat.grid(row=next(row_num), column=2)
        # 生成按钮
        self.btn_generate_gat = tk.Button(self, text="自定义生成", command=self.generate_by_input)
        create_tooltip(self.btn_generate_gat, text="依据变色字段输入进行生成")
        self.btn_generate_gat.grid(row=row_num.current, column=0)

        self.button_quit_gat = tk.Button(self, text="退出", command=self.master.destroy)
        self.button_quit_gat.grid(row=next(row_num), column=2)

        # 默认显示香港居住证
        self.id_type.set(IdCardGenerator.GATPermanentResident.HKG_PERMANENT_RESIDENT.value)
        self.generate_default()

    def generate_by_input(self, event=None):
        name_ch = self.entry_name_ch.get() or None
        name_en = self.entry_name_en.get() or None
        birthday = self.entry_birthday.get() or None
        gender = self.gender.get() or None
        try:
            id_info = IdCardGenerator.TypeGATJZZ(self.id_type.get(),
                                                 name_ch=name_ch,
                                                 name_en=name_en,
                                                 birthday=birthday,
                                                 gender=gender,
                                                 )
            self.show_info(id_info)
        except Exception as e:
            messagebox.showinfo("提示", f"自定义生成出错,错误信息为:{e}")

    def generate_default(self, event=None):  # event就是点击事件
        id_info = IdCardGenerator.TypeGATJZZ(self.id_type.get())
        # messagebox.showinfo("提示", "校验方法")
        self.show_info(id_info)

    def show_info(self, card_info: IdCardGenerator.TypeGATJZZ):
        self.ID_No.set(card_info.No)
        self.name_ch.set(card_info.name_ch)
        self.name_en.set(card_info.name_en)
        self.birthday.set(card_info.birthday)
        self.gender.set(card_info.gender)
        self.province_code.set(card_info.region_code)
        self.province_name.set(card_info.province_name)

    def check_num_complete(self, event=None):
        ID_No_src = self.ID_No.get()
        ID_No_src = ID_No_src[0:17]
        try:
            ID_No_src = IdCardGenerator.IDNOGenerator.calculate_check_num_cls(ID_No_src)
        except ValueError as e:
            messagebox.showinfo("提示", f"输入有误,{e}")
        self.ID_No.set(ID_No_src)

    def clear_all_fields(self, event=None):
        self.ID_No.set("")
        self.name_ch.set("")
        self.name_en.set("")
        self.birthday.set("")
        self.gender.set("")
        self.province_code.set("")
        self.province_name.set("")


class GAtxz(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # 行号迭代器，注意next方法返回当前值
        row_num = RowNumIterator(1)

        # 创建港澳台页面的组件
        self.id_type = tk.StringVar()
        self.label_id_type = tk.Label(self, text="证件类别:")
        self.label_id_type.grid(row=row_num.current, column=0, sticky='e')
        ga_id_type = tuple(member.value for member in IdCardGenerator.HkgMacPermit)
        self.combobox_id_type = ttk.Combobox(self, textvariable=self.id_type, values=ga_id_type)
        self.combobox_id_type.bind("<<ComboboxSelected>>", self.generate_default)
        self.combobox_id_type.grid(row=next(row_num), column=1, sticky='w')

        self.label_ID_No = tk.Label(self, text="证件号码:", anchor="e")
        self.label_ID_No.grid(row=row_num.current, column=0, sticky='e')
        self.ID_No = tk.StringVar()
        self.entry_ID_No = tk.Entry(self, textvariable=self.ID_No)
        self.entry_ID_No.grid(row=row_num.current, column=1, sticky='w')
        self.btn_copy_ID_No = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.ID_No.get()))
        self.btn_copy_ID_No.grid(row=next(row_num), column=2)

        self.label_name_ch = tk.Label(self, text="中文名:")
        self.label_name_ch.grid(row=row_num.current, column=0, sticky='e')
        self.name_ch = tk.StringVar()
        self.entry_name_ch = tk.Entry(self, textvariable=self.name_ch)
        self.entry_name_ch.grid(row=row_num.current, column=1)
        self.btn_copy_name_ch = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.name_ch.get()))
        self.btn_copy_name_ch.grid(row=next(row_num), column=2)

        # 创建英文名标签和输入框
        self.label_name_en = tk.Label(self, text="英文名:")
        self.label_name_en.grid(row=row_num.current, column=0, sticky='e')
        self.name_en = tk.StringVar()
        self.entry_name_en = tk.Entry(self, textvariable=self.name_en)
        self.entry_name_en.grid(row=row_num.current, column=1)
        self.btn_copy_name_en = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.name_en.get()))
        self.btn_copy_name_en.grid(row=next(row_num), column=2)

        self.btn_refresh_gat = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh_gat.grid(row=row_num.current, column=1)

        self.btn_refresh_gat = tk.Button(self, text="退出", command=self.master.destroy)
        self.btn_refresh_gat.grid(row=row_num.current, column=2)

        # 默认显示香港通行证
        self.id_type.set(IdCardGenerator.HkgMacPermit.HKG_PERMIT.value)
        self.generate_default()

    def generate_default(self, event=None):
        id_info = IdCardGenerator.TypeGATXZ(self.id_type.get())
        self.ID_No.set(id_info.No)
        self.name_ch.set(id_info.name_ch)
        self.name_en.set(id_info.name_en)


class TWtxz(tk.Frame):
    """台湾通行证"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        # 行号迭代器，注意next方法返回当前值
        row_num = RowNumIterator(1)

        self.label_ID_No = tk.Label(self, text="证件号码:", anchor="e")
        self.label_ID_No.grid(row=row_num.current, column=0, sticky='e')
        self.ID_No = tk.StringVar()
        self.entry_ID_No = tk.Entry(self, textvariable=self.ID_No)
        self.entry_ID_No.grid(row=row_num.current, column=1)
        self.btn_copy_ID_No = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.ID_No.get()))
        self.btn_copy_ID_No.grid(row=next(row_num), column=2)

        self.label_name_ch = tk.Label(self, text="中文名:")
        self.label_name_ch.grid(row=row_num.current, column=0, sticky='e')
        self.name_ch = tk.StringVar()
        self.entry_name_ch = tk.Entry(self, textvariable=self.name_ch)
        self.entry_name_ch.grid(row=row_num.current, column=1)
        self.btn_copy_name_ch = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.name_ch.get()))
        self.btn_copy_name_ch.grid(row=next(row_num), column=2)

        # 创建英文名标签和输入框
        self.label_name_en = tk.Label(self, text="英文名:")
        self.label_name_en.grid(row=row_num.current, column=0, sticky='e')
        self.name_en = tk.StringVar()
        self.entry_name_en = tk.Entry(self, textvariable=self.name_en)
        self.entry_name_en.grid(row=row_num.current, column=1)
        self.btn_copy_name_en = tk.Button(self, text="复制", command=lambda: pyperclip.copy(self.name_en.get()))
        self.btn_copy_name_en.grid(row=next(row_num), column=2)

        self.btn_refresh_gat = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh_gat.grid(row=row_num.current, column=1)

        self.btn_refresh_gat = tk.Button(self, text="退出", command=self.master.destroy)
        self.btn_refresh_gat.grid(row=row_num.current, column=2)

        self.generate_default()

    def generate_default(self, event=None):
        id_info = IdCardGenerator.TypeTWTXZ()
        self.ID_No.set(id_info.No)
        self.name_ch.set(id_info.name_ch)
        self.name_en.set(id_info.name_en)


class ToolTip:
    def __init__(self, widget, text='widget info'):
        self.widget = widget
        self.text = text
        self.tip_window = None
        self.id = None
        self.x = self.y = 0
        self.delay = 300  # 延迟显示时间（毫秒）
        self.after_id = None

    def showtip(self):
        """延迟显示 Tooltip 窗口"""
        if self.tip_window or not self.text:
            return
        # 延迟显示
        self.after_id = self.widget.after(self.delay, self._create_tip)

    def _create_tip(self):
        """实际创建 Tooltip 窗口"""
        if self.tip_window or not self.text:
            return
        x, y, cx, cy = self.widget.bbox("insert")
        x = x + self.widget.winfo_rootx() + 25
        y = y + cy + self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # 去掉窗口边框
        tw.wm_geometry(f"+{x}+{y}")  # 设置窗口位置
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", "8", "normal"))
        label.pack(ipadx=1)

    def hidetip(self):
        """隐藏 Tooltip 窗口"""
        if self.after_id:
            self.widget.after_cancel(self.after_id)  # 取消延迟显示
            self.after_id = None
        if self.tip_window:
            self.tip_window.destroy()
            self.tip_window = None


def create_tooltip(widget, text):
    tooltip = ToolTip(widget, text)

    def enter(event):
        tooltip.showtip()

    def leave(event):
        tooltip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)

# 行号迭代器
class RowNumIterator:
    def __init__(self, start=0):
        self.current = start

    def __iter__(self):
        return self

    # 注意，返回的是当前值，是为了在循环中，每次都是从头迭代
    def __next__(self):
        value = self.current
        self.current += 1
        return value


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
        self.geometry("310x450+300+200")

        # 创建不同的 Frame 缓存
        self.frame_cache = {}

        # 默认显示永居证页面
        self.id_kind.set(IdCardGenerator.IDType.FOREIGN_PERMANENT_RESIDENT2023.value)
        self.create_frame(None)
        self.show_frame(self.frame_cache.get(IdCardGenerator.IDType.FOREIGN_PERMANENT_RESIDENT2023.value))

    def show_frame(self, frame=None):
        # 隐藏所有 Frame
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.grid_forget()
        # 显示指定的 Frame
        if frame:
            frame.grid(row=1, column=0, columnspan=4, padx=0, pady=20)

    def create_frame(self, event):
        try:
            selected_id_kind = str(self.id_kind.get())
            if selected_id_kind not in self.frame_cache.keys():
                if IdCardGenerator.IDType.ID_CARD.value == selected_id_kind:
                    self.frame_cache[selected_id_kind] = Sfz(self)
                elif IdCardGenerator.IDType.FOREIGN_PERMANENT_RESIDENT2023.value == selected_id_kind:
                    self.frame_cache[selected_id_kind] = Yjj2023(self)
                elif IdCardGenerator.IDType.GAT_PERMANENT_RESIDENT.value == selected_id_kind:
                    self.frame_cache[selected_id_kind] = GATJzz(self)
                elif IdCardGenerator.IDType.HKG_MAC_PERMIT.value == selected_id_kind:
                    self.frame_cache[selected_id_kind] = GAtxz(self)
                elif IdCardGenerator.IDType.CTN_PERMIT.value == selected_id_kind:
                    self.frame_cache[selected_id_kind] = TWtxz(self)
                elif IdCardGenerator.IDType.FOREIGN_PERMANENT_RESIDENT2017.value == selected_id_kind:
                    self.frame_cache[selected_id_kind] = Yjj2017(self)
                else:
                    self.frame_cache[selected_id_kind] = None
            self.show_frame(self.frame_cache.get(selected_id_kind))
        except Exception as e:
            messagebox.showwarning("错误", f"发生错误,错误信息为:{e}")



if __name__ == '__main__':
    # root = tk.Tk()
    # root.title("永居证生成器")
    id_kinds_all = tuple(member.value for member in IdCardGenerator.IDType)
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
