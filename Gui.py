#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time     : 2025/1/19 上午12:15
# @Author   : Admin
# @File     : Gui.py
# @Software : PRC_FOREIGN_PARTMENT_RESAIDNT_ID_CARD
# @实现功能  :
"""
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import IdCardGenerator as IDGener
import Nationality
import pyperclip


def generate_image(e):  # e就是点击事件
    messagebox.showinfo("提示", "合成图像")
    print("合成图像")


class AppYjj(tk.Frame):
    """永居证的页面"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # 创建证件号码标签和输入框
        self.label_ID_No = tk.Label(self, text="证件号码:", anchor="e", bg=None, fg=None)
        self.label_ID_No.grid(row=1, column=0, sticky='e')
        self.ID_No = tk.StringVar()
        self.entry_ID_No = tk.Entry(self, textvariable=self.ID_No)
        self.entry_ID_No.grid(row=1, column=1)
        # 添加复制按钮
        self.btn_copy_ID_No = tk.Button(self, text="复制", command=lambda :pyperclip.copy(self.ID_No.get()))
        self.btn_copy_ID_No.grid(row=1, column=2)

        # 创建中文名标签和输入框
        self.label_name_CH = tk.Label(self, text="中文名:")
        self.label_name_CH.grid(row=2, column=0, sticky='e')
        self.name_CH = tk.StringVar()
        self.entry_name_CH = tk.Entry(self, textvariable=self.name_CH)
        self.entry_name_CH.grid(row=2, column=1)
        self.btn_copy_name_CH = tk.Button(self, text="复制", command=self.copy_to_clipboard(self.name_CH))
        self.btn_copy_name_CH.grid(row=2, column=2)

        # 创建英文名标签和输入框
        self.label_name_EN = tk.Label(self, text="英文名:")
        self.label_name_EN.grid(row=3, column=0, sticky='e')
        self.name_EN = tk.StringVar()
        self.entry_name_EN = tk.Entry(self, textvariable=self.name_EN)
        self.entry_name_EN.grid(row=3, column=1)
        self.btn_copy_name_EN = tk.Button(self, text="复制", command=self.copy_to_clipboard(self.name_EN))
        self.btn_copy_name_EN.grid(row=3, column=2)

        # 创建生日标签和输入框
        self.label_birthday = tk.Label(self, text="生日:", anchor="e")
        self.label_birthday.grid(row=4, column=0, sticky='e')
        self.birthday = tk.StringVar()
        self.entry_birthday = tk.Entry(self, textvariable=self.birthday)
        self.entry_birthday.grid(row=4, column=1)
        self.btn_copy_birthday = tk.Button(self, text="复制", command=self.copy_to_clipboard(self.birthday))
        self.btn_copy_birthday.grid(row=4, column=2)

        # 创建性别标签和输入框
        self.label_gender = tk.Label(self, text="性别:")
        self.label_gender.grid(row=5, column=0, sticky='e')
        self.gender = tk.StringVar()
        self.gender.set(None)
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
        self.btn_copy_province_code = tk.Button(self, text="复制", command=self.copy_to_clipboard(self.province_code))
        self.btn_copy_province_code.grid(row=6, column=2)

        # 创建办理省份标签和输入框
        self.label_province_name = tk.Label(self, text="办理省份:")
        self.label_province_name.grid(row=7, column=0, sticky='e')
        self.province_name = tk.StringVar()
        self.entry_province_name = tk.Entry(self, textvariable=self.province_name)
        self.entry_province_name.grid(row=7, column=1)
        self.btn_copy_province_name = tk.Button(self, text="复制", command=self.copy_to_clipboard(self.province_name))
        self.btn_copy_province_name.grid(row=7, column=2)

        # 创建国籍代码标签和输入框
        self.label_nationality_number = tk.Label(self, text="国籍代码:")
        self.label_nationality_number.grid(row=8, column=0, sticky='e')
        self.nationality_number = tk.StringVar()
        self.entry_nationality_number = tk.Entry(self, textvariable=self.nationality_number)
        self.entry_nationality_number.grid(row=8, column=1)
        self.btn_copy_nationality_number = tk.Button(self, text="复制",
                                                     command=self.copy_to_clipboard(self.nationality_number))
        self.btn_copy_nationality_number.grid(row=8, column=2)

        # 创建国籍标签和输入框
        self.label_nationality_code = tk.Label(self, text="国籍:")
        self.label_nationality_code.grid(row=9, column=0, sticky='e')
        self.nationality_code = tk.StringVar()
        self.entry_nationality_code = tk.Entry(self, textvariable=self.nationality_code)
        self.entry_nationality_code.grid(row=9, column=1)
        self.btn_copy_nationality_code = tk.Button(self, text="复制",
                                                   command=self.copy_to_clipboard(self.nationality_code))
        self.btn_copy_nationality_code.grid(row=9, column=2)

        # 创建国家简称标签和输入框
        self.label_nationality_name_cn = tk.Label(self, text="国家简称:")
        self.label_nationality_name_cn.grid(row=10, column=0, sticky='e')
        self.nationality_name_cn = tk.StringVar()
        self.entry_nationality_name_cn = tk.Entry(self, textvariable=self.nationality_name_cn)
        self.entry_nationality_name_cn.grid(row=10, column=1)
        self.btn_copy_nationality_name_cn = tk.Button(self, text="复制",
                                                      command=self.copy_to_clipboard(self.nationality_name_cn))
        self.btn_copy_nationality_name_cn.grid(row=10, column=2)

        # 生成按钮
        self.btn_generate = tk.Button(self, text="自定义生成", command=self.generate_by_input)
        self.btn_generate.grid(row=11, column=0)
        # 刷新按钮
        self.btn_refresh = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh.grid(row=11, column=1)
        # 合成图像按钮
        self.btn_generate_image = tk.Button(self, text="合成图像")
        self.btn_generate_image.bind("<Button-1>", self.generate_image)
        self.btn_generate_image.grid(row=11, column=3)

        self.button_check = tk.Button(self, text="合法性校验", command=lambda: print("校验"))
        self.button_check.grid(row=11, column=4)

        self.button_cheack_gat = tk.Button(self, text="校验位补全", command=self.generate_image)
        self.button_cheack_gat.grid(row=11, column=5)


        self.button_quit = tk.Button(self, text="退出", command=self.master.destroy)
        self.button_quit.grid(row=12, column=6)

        self.generate_default()
        self.createWidget()

    def copy_to_clipboard(self, variable):
        """将变量的值复制到剪贴板"""
        pyperclip.copy(variable.get())
        # messagebox.showinfo("提示", "已复制到剪贴板")

    def print_contents(self, event):
        print("Hi. The current entry content is:",
              self.contents.get())

    def createWidget(self):
        pass

    def generate_by_input(self, event=None):
        # 依据自定义输入,需要同步修改其他文件的内容
        return
        id_info = IDGener.TypeYJZ()
        self.show_info(id_info)

    def generate_default(self, event=None):  # event就是点击事件
        id_info = IDGener.TypeYJZ()
        # messagebox.showinfo("提示", "校验方法")
        self.show_info(id_info)

    def show_info(self, card_info: IDGener.TypeYJZ):
        """
        显示卡片信息。

        为所有标签绑定的变量实现赋值，以在界面上展示证件持有者的相关信息。

        参数:
        card_info (IDGener.TypeYJZ): 外国人永久居留证对象。
        """

        # 为所有标签绑定的变量实现赋值
        self.ID_No.set(card_info.No)
        self.name_EN.set(card_info.name_EN)
        self.name_CH.set(card_info.name_CH)
        self.birthday.set(card_info.birthday)
        self.gender.set(card_info.gender)
        self.province_code.set(card_info.province_code)
        self.province_name.set(Nationality.CODE_PROVINCE_DATA.get(int(card_info.province_code), '未知'))
        self.nationality_number.set(card_info.nationality_number)
        self.nationality_code.set(card_info.nationality_code)
        self.nationality_name_cn.set(card_info.nationality_name_cn)

    def generate_image(self, event=None):
        print(type(self), event)
        messagebox.showinfo("提示", "生成证件图片在根目录下")


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
        self.combobox_id_type.bind("<<ComboboxSelected>>")
        self.combobox_id_type.grid(row=1, column=1, sticky='w')

        self.label_ID_No = tk.Label(self, text="证件号码:", anchor="e", bg=None, fg=None)
        self.label_ID_No.grid(row=3, column=0, sticky='e')
        self.ID_No = tk.StringVar()
        self.ID_No.set("77374123")
        self.entry_ID_No = tk.Entry(self, textvariable=self.ID_No)
        self.entry_ID_No.grid(row=3, column=1)
        self.btn_copy_ID_No = tk.Button(self, text="复制", command=lambda :pyperclip.copy(self.ID_No.get()))
        self.btn_copy_ID_No.grid(row=3, column=2)

        # 创建生日标签和输入框
        self.label_birthday = tk.Label(self, text="生日:", anchor="e")
        self.label_birthday.grid(row=4, column=0, sticky='e')
        self.birthday = tk.StringVar()
        self.entry_birthday = tk.Entry(self, textvariable=self.birthday)
        self.entry_birthday.grid(row=4, column=1)
        self.btn_copy_birthday = tk.Button(self, text="复制", command=lambda :pyperclip.copy(self.birthday))
        self.btn_copy_birthday.grid(row=4, column=2)

        # 创建性别标签和输入框
        self.label_gender = tk.Label(self, text="性别:")
        self.label_gender.grid(row=5, column=0, sticky='e')
        self.gender = tk.StringVar()
        self.gender.set(None)
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
        self.btn_copy_province_code = tk.Button(self, text="复制", command=lambda :pyperclip.copy(self.province_code))
        self.btn_copy_province_code.grid(row=6, column=2)

        # 创建办理省份标签和输入框
        self.label_province_name = tk.Label(self, text="办理省份:")
        self.label_province_name.grid(row=7, column=0, sticky='e')
        self.province_name = tk.StringVar()
        self.entry_province_name = tk.Entry(self, textvariable=self.province_name)
        self.entry_province_name.grid(row=7, column=1)
        self.btn_copy_province_name = tk.Button(self, text="复制", command=lambda :pyperclip.copy(self.province_name))
        self.btn_copy_province_name.grid(row=7, column=2)

        # 生成按钮
        self.btn_generate_gat = tk.Button(self, text="自定义生成", command=lambda: print("生成港澳台"))
        self.btn_generate_gat.grid(row=11, column=0)
        # 刷新按钮
        self.btn_refresh_gat = tk.Button(self, text="重新随机生成", command=lambda: print("刷新港澳台"))
        self.btn_refresh_gat.grid(row=11, column=1)

        self.button_cheack_gat = tk.Button(self, text="合法性校验", command=self.generate_image)
        self.button_cheack_gat.grid(row=11, column=4)

        self.button_cheack_gat = tk.Button(self, text="校验位补全", command=self.generate_image)
        self.button_cheack_gat.grid(row=11, column=5)

        self.button_quit_gat = tk.Button(self, text="退出", command=self.master.destroy)
        self.button_quit_gat.grid(row=11, column=6)

        # 默认显示香港居住证
        self.id_type.set(IDGener.IDGener.GATPermanentResident.HKG_PERMANENT_RESIDENT.value)
        self.show_info()

        def generate_by_input(self, event=None):
            # 依据自定义输入,需要同步修改其他文件的内容
            return
            id_info = IDGener.TypeGATJZZ()
            self.show_info(YJZ)

        def generate_default(self, event=None):  # event就是点击事件
            id_info = IDGener.TypeGATJZZ()
            # messagebox.showinfo("提示", "校验方法")
            self.show_info(id_info)

        def show_info(self, card_info: IDGener.TypeYJZ):
            pass


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
        self.geometry("700x700+300+200")

        # 创建不同的 Frame
        self.yjj_frame = AppYjj(self)
        self.gat_frame = GATJzz(self)

        # 默认显示永居证页面
        self.id_kind.set(IDGener.IDType.FOREIGN_PERMANENT_RESIDENT2023.value)
        self.show_frame(self.yjj_frame)

    def show_frame(self, frame):
        # 隐藏所有 Frame
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.grid_forget()
        # 显示指定的 Frame
        frame.grid(row=1, column=0, columnspan=4, padx=20, pady=20)

    def create_frame(self, event):
        if IDGener.IDType.FOREIGN_PERMANENT_RESIDENT2023.value == str(self.id_kind.get()):
            self.show_frame(self.yjj_frame)
        else:
            self.show_frame(self.gat_frame)


if __name__ == '__main__':
    # root = tk.Tk()
    # root.title("永居证生成器")
    id_kinds = tuple(member.value for member in IDGener.IDType)
    # id_kind = tk.StringVar()
    # label_id_kinds = tk.Label(root, text="证件类型:")
    # label_id_kinds.grid(row=0, column=0, sticky='e')
    # combobox_id_kind = ttk.Combobox(root, textvariable=id_kind, values=id_kinds)
    # combobox_id_kind.bind("<<ComboboxSelected>>", lambda e: print(id_kind.get()))
    # combobox_id_kind.grid(row=0, column=1, sticky='w')
    # # 设置窗口大小和位置,先横后纵,左上角为原点
    # root.geometry("700x700+300+200")
    # root.mainloop()
    a = MainApplication(id_kinds)
    a.mainloop()
