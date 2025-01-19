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
import IdCardGenerator


def generate_image(e):  # e就是点击事件
    messagebox.showinfo("提示", "合成图像")
    print("合成图像")


class AppYjj(tk.Frame):
    """永居证的页面"""

    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.grid(columnspan=4, padx=20, pady=20)

        # self.entrythingy = tk.Entry()
        # self.entrythingy.pack()
        #
        # # Create the application variable.
        # self.contents = tk.StringVar()
        # # Set it to some value.
        # self.contents.set("this is a variable")
        # # Tell the entry widget to watch this variable.
        # self.entrythingy["textvariable"] = self.contents
        #
        # # Define a callback for when the user hits return.
        # # It prints the current value of the variable.
        # self.entrythingy.bind('<Key-Return>',
        #                       self.print_contents)
        self.createWidget()

    def print_contents(self, event):
        print("Hi. The current entry content is:",
              self.contents.get())

    def createWidget(self):
        # 创建证件号码标签和输入框
        self.label_name_EN = tk.Label(self, text="证件号码:", anchor="e", bg='red')
        self.label_name_EN.grid(row=1, column=0, sticky='e')
        name_EN = tk.StringVar()
        self.entry_name_EN = tk.Entry(self, textvariable=name_EN)
        self.entry_name_EN.grid(row=1, column=1)

        # 创建英文名标签和输入框
        self.label_name_EN = tk.Label(self, text="英文名:", bg='red')
        self.label_name_EN.grid(row=2, column=0, sticky='e')
        name_EN = tk.StringVar()
        self.entry_name_EN = tk.Entry(self, textvariable=name_EN)
        self.entry_name_EN.grid(row=2, column=1)

        # 创建中文名标签和输入框
        self.label_name_CH = tk.Label(self, text="中文名:")
        self.label_name_CH.grid(row=3, column=0, sticky='e')
        name_CH = tk.StringVar()
        self.entry_name_CH = tk.Entry(self, textvariable=name_CH)
        self.entry_name_CH.grid(row=3, column=1)

        # 创建生日标签和输入框
        self.label_birthday = tk.Label(self, text="生日:", anchor="e")
        self.label_birthday.grid(row=4, column=0, sticky='e')
        birthday = tk.StringVar()
        self.entry_birthday = tk.Entry(self, textvariable=birthday)
        self.entry_birthday.grid(row=4, column=1)

        # 创建性别标签和输入框
        self.label_gender = tk.Label(self, text="性别:")
        self.label_gender.grid(row=5, column=0, sticky='e')
        gender = tk.StringVar()
        self.entry_gender = tk.Entry(self, textvariable=gender)
        self.entry_gender.grid(row=5, column=1)

        # 创建办理地区标签和输入框
        self.label_province_code = tk.Label(self, text="办理地区码:")
        self.label_province_code.grid(row=6, column=0, sticky='e')
        province_code = tk.StringVar()
        self.entry_province_code = tk.Entry(self, textvariable=province_code)
        self.entry_province_code.grid(row=6, column=1)

        # 创建办理省份标签和输入框
        self.label_province_name = tk.Label(self, text="办理省份:")
        self.label_province_name.grid(row=7, column=0, sticky='e')
        province_name = tk.StringVar()
        self.entry_province_name = tk.Entry(self, textvariable=province_name)
        self.entry_province_name.grid(row=7, column=1)

        # 创建国籍代码标签和输入框
        self.label_nationality_number = tk.Label(self, text="国籍代码:")
        self.label_nationality_number.grid(row=8, column=0, sticky='e')
        nationality_number = tk.StringVar()
        self.entry_nationality_number = tk.Entry(self, textvariable=nationality_number)
        self.entry_nationality_number.grid(row=8, column=1)

        # 创建国籍标签和输入框
        self.label_nationality_code = tk.Label(self, text="国籍:")
        self.label_nationality_code.grid(row=9, column=0, sticky='e')
        nationality_code = tk.StringVar()
        self.entry_nationality_code = tk.Entry(self, textvariable=nationality_code)
        self.entry_nationality_code.grid(row=9, column=1)

        # 创建国家简称标签和输入框
        self.label_nationality_name_cn = tk.Label(self, text="国家简称:")
        self.label_nationality_name_cn.grid(row=10, column=0, sticky='e')
        nationality_name_cn = tk.StringVar()
        self.entry_nationality_name_cn = tk.Entry(self, textvariable=nationality_name_cn)
        self.entry_nationality_name_cn.grid(row=10, column=1)

        # 生成按钮
        self.btn_generate = tk.Button(self, text="生成", command=lambda: print("生成"))
        self.btn_generate.grid(row=11, column=0)
        # 刷新按钮
        self.btn_refresh = tk.Button(self, text="刷新", command=lambda: print("刷新"))
        self.btn_refresh.grid(row=11, column=1)
        # 合成图像按钮
        self.btn_generate_image = tk.Button(self, text="合成图像")
        self.btn_generate_image.bind("<Button-1>", self.generate_image)
        self.btn_generate_image.grid(row=11, column=3)

        self.button_cheack = tk.Button(self, text="校验", command=self.generate_image)
        self.button_cheack.grid(row=11, column=4)
        self.button_quit = tk.Button(self, text="退出", command=self.master.destroy)
        self.button_quit.grid(row=11, column=5)

    def generate_image(self, event=None):  # e就是点击事件
        messagebox.showinfo("提示", "校验方法")
        print("类中合成图像")


class GAT(tk.Frame):
    """港澳台的页面"""
    pass


if __name__ == '__main__':
    root = tk.Tk()
    root.title("永居证生成器")
    id_kinds = tuple(member.value for member in IdCardGenerator.IDType)
    id_kind = tk.StringVar()
    label_id_kinds = tk.Label(root, text="证件类型:")
    label_id_kinds.grid(row=0, column=0, sticky='e')
    combobox_id_kind = ttk.Combobox(root, textvariable=id_kind, values=id_kinds)
    combobox_id_kind.grid(row=0, column=1, sticky='w')
    # 设置窗口大小和位置,先横后纵,左上角为原点
    root.geometry("700x700+300+200")
    myapp = AppYjj(root)
    root.mainloop()
