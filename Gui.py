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

_SENTINEL = object()
LABEL_BG = '#80FFFF'
LABEL_BG_NO = '#1CE47A'
LABEL_BG_OLD_NO = '#90FFA7'

IDKIND_TO_CSDC_ID_KIND = {
    IdCardGenerator.IDKind.ID_CARD.value:'01',
    IdCardGenerator.IDKind.FOREIGN_PERMANENT_RESIDENT2017.value:'09',
    IdCardGenerator.IDKind.FOREIGN_PERMANENT_RESIDENT2023.value:'-9',
    IdCardGenerator.IDKind.HKG_MAC_PERMIT.value:'07',
    IdCardGenerator.IDKind.CTN_PERMIT.value:'08',
    IdCardGenerator.IDKind.GAT_PERMANENT_RESIDENT.value:'15',
    IdCardGenerator.IDKind.BUSINESS_LICENSE.value:'02',        
}

GENDER_TO_CSDC_GENDER ={
    '男':'1',
    '女':'2',
    '非自然人':'3'
}

GENDER_TO_BOP_GENDER ={
    '男':'0',
    '女':'1',
    '非自然人':'2'
}

class WidgetGroupDescriptor:
    """描述符：管理 WidgetGroup/GenderGroup 属性，实现子类赋值时更新而非覆盖"""

    def __init__(self, attr_name: str):
        """
        初始化描述符

        :param attr_name: 属性名，对应 instance.__dict__ 中的 key
        """
        self.attr_name = attr_name

    def __get__(self, instance, owner):
        """
        获取属性值

        :param instance: 拥有该属性的实例
        :param owner: 拥有该描述符的类
        :return: instance.__dict__ 中的 WidgetGroup/GenderGroup 或描述符自身
        """
        if instance is None:
            return self
        return instance.__dict__.get(self.attr_name)

    def __set__(self, instance, value: 'WidgetGroup | GenderGroup'):
        """
        设置属性值：若已有同名组件则更新而非覆盖

        :param instance: 拥有该属性的实例
        :param value: 新的 WidgetGroup 或 GenderGroup；非组件类型直接存入 __dict__
        """
        if not isinstance(value, (WidgetGroup, GenderGroup)):
            instance.__dict__[self.attr_name] = value
            return
        existing = instance.__dict__.get(self.attr_name)
        if existing is not None:
            # 仅传递子类显式提供的参数，更新已有组件
            if isinstance(value, WidgetGroup):
                kwargs = {}
                if value._has_name:
                    kwargs['name'] = value.name
                if value._has_bg:
                    kwargs['bg'] = value._bg
                if value._has_bindings and value._bindings:
                    kwargs['bindings'] = value._bindings
                if kwargs:
                    existing.configure(**kwargs)
                if value._has_row_num:
                    existing.row_num = value.row_num
            elif isinstance(value, GenderGroup):
                kwargs = {}
                if value._has_name:
                    kwargs['name'] = value.name
                if value._has_bg:
                    kwargs['bg'] = value._bg
                if kwargs:
                    existing.configure(**kwargs)
                if value._has_row_num:
                    existing.row_num = value.row_num
            value.destroy()
        else:
            instance.__dict__[self.attr_name] = value

    def __delete__(self, instance):
        """
        删除属性

        :param instance: 拥有该属性的实例
        """
        if self.attr_name in instance.__dict__:
            del instance.__dict__[self.attr_name]


class BaseCardFrame(tk.Frame, ABC):
    """抽象基类，用描述符管理 13 个公共字段，子类无需重复赋值"""

    name_ch = WidgetGroupDescriptor('name_ch')
    ID_No = WidgetGroupDescriptor('ID_No')
    name_en = WidgetGroupDescriptor('name_en')
    birthday = WidgetGroupDescriptor('birthday')
    gender = WidgetGroupDescriptor('gender')
    begin_date = WidgetGroupDescriptor('begin_date')
    end_date = WidgetGroupDescriptor('end_date')
    phone_number = WidgetGroupDescriptor('phone_number')
    landline_number = WidgetGroupDescriptor('landline_number')
    fax_number = WidgetGroupDescriptor('fax_number')
    email_address = WidgetGroupDescriptor('email_address')
    zipcode = WidgetGroupDescriptor('zipcode')
    id_address = WidgetGroupDescriptor('id_address')

    @staticmethod
    def _common_field_names():
        return [
            'name_ch', 'ID_No', 'name_en', 'birthday', 'gender',
            'begin_date', 'end_date', 'phone_number', 'landline_number',
            'fax_number', 'email_address', 'zipcode', 'id_address'
        ]

    def __init__(self, master=None, start_row_num: int = 1):
        """
        初始化抽象基类，预创建所有公共字段组件

        :param master: 父级 tk 容器
        :param start_row_num: 公共字段的起始行号，子类可在前面插入自有字段后传入更大值
        """
        super().__init__(master)
        self.master = master
        self.id_info:IdCardGenerator.IDNOGenerator = None
        self._init_common_widgets(start_row_num)

    def _init_common_widgets(self, start_row_num: int):
        """
        预创建 13 个公共字段组件，行号由迭代器管理，调整顺序即可调整排布

        :param start_row_num: 组件起始行号
        """
        r = RowNumIterator(start_row_num)
        self.__dict__['name_ch'] = WidgetGroup(self, name="中文名:", row_num=next(r))
        self.__dict__['ID_No'] = WidgetGroup(self, name="证件号码:", row_num=next(r))
        self.__dict__['name_en'] = WidgetGroup(self, name="英文名:", row_num=next(r))
        self.__dict__['birthday'] = WidgetGroup(self, name="生日:", row_num=next(r))
        self.__dict__['gender'] = GenderGroup(self, name="性别:", row_num=next(r))
        self.__dict__['begin_date'] = WidgetGroup(self, name="起始日期:", row_num=next(r))
        self.__dict__['end_date'] = WidgetGroup(self, name="到期日期:", row_num=next(r))
        self.__dict__['phone_number'] = WidgetGroup(self, name="联系电话:", row_num=next(r))
        self.__dict__['landline_number'] = WidgetGroup(self, name="固定电话:", row_num=next(r))
        self.__dict__['fax_number'] = WidgetGroup(self, name="传真号码:", row_num=next(r))
        self.__dict__['email_address'] = WidgetGroup(self, name="电子邮箱:", row_num=next(r))
        self.__dict__['zipcode'] = WidgetGroup(self, name="邮政编码:", row_num=next(r))
        self.__dict__['id_address'] = WidgetGroup(self, name="证件地址:", row_num=next(r))
        self._next_row = r.current

    @abstractmethod
    def generate_default(self):
        """生成默认证件信息并填充到界面，子类必须实现"""
        self.show_info()

    def show_info(self):
        """
        将 self.id_info 中的公共字段数据填充到对应组件中

        若 self.id_info 为 None 则直接返回
        """
        if not self.id_info:
            return
        info = self.id_info
        d = self.__dict__
        _set_if = lambda name, val: d[name].set(val) if d.get(name) else None
        _set_if('name_ch', info.name_ch)
        _set_if('ID_No', info.No)
        _set_if('name_en', info.name_en)
        _set_if('birthday', info.birthday)
        _set_if('gender', info.gender)
        _set_if('begin_date', info.begin_date)
        _set_if('end_date', info.end_date)
        _set_if('phone_number', info.phone_number)
        _set_if('landline_number', info.landline_number)
        _set_if('fax_number', info.fax_number)
        _set_if('email_address', info.email_address)
        _set_if('zipcode', info.zipcode)
        _set_if('id_address', getattr(info, 'address', ''))

    def clear_all_fields(self):
        """清空所有 WidgetGroup 和 GenderGroup 字段（含子类特有字段）"""
        for widget in self.__dict__.values():
            if isinstance(widget, (WidgetGroup, GenderGroup)):
                widget.set('')

    def refresh_default(self) -> tk.Frame:
        """
        重新生成默认信息并返回自身 Frame

        :return: 当前 BaseCardFrame 实例
        """
        self.generate_default()
        return self

    def show_id_info_by_sql(self):
        """将证件信息格式化为sql语句"""
        if self.id_info:
            CSDC_ID_NO = self.id_info.No
            CSDC_ID_BEGINDATE = self.id_info.begin_date
            CSDC_ID_ENDDATE = self.id_info.end_date
            CSDC_FULL_NAME = self.id_info.name_ch
            CSDC_BIRTHDAY = self.id_info.birthday
            CSDC_MOBILEPHONE = self.id_info.phone_number
            CSDC_NATIONALITY = self.id_info.nationality_code
            CSDC_ID_KIND = IDKIND_TO_CSDC_ID_KIND.get(self.id_info.id_kind, ' ')
            CSDC_CLIENT_GENDER = GENDER_TO_CSDC_GENDER.get(self.id_info.gender, ' ')
            insert_sql = f"""insert into hs_tstp.tpidinfo (BRANCH_NO, CSDC_ID_KIND, CSDC_ID_NO, CSDC_ID_BEGINDATE, CSDC_ID_ENDDATE, CSDC_FULL_NAME, CSDC_NATIONALITY, CSDC_CLIENT_GENDER, CSDC_BIRTHDAY, CSDC_OPENORGAN_CODE, CSDC_OPENNET_CODE, CSDC_MOBILEPHONE, CSDC_QUERY_FLAG, CSDC_FILE_NAME, CSDC_FILE_LENGTH, CSDC_RESERVE1, CSDC_RESERVE2, REVIEW_FLAG)
    values (1111, '{CSDC_ID_KIND}', '{CSDC_ID_NO}', {CSDC_ID_BEGINDATE}, {CSDC_ID_ENDDATE}, '{CSDC_FULL_NAME}', '{CSDC_NATIONALITY}', '{CSDC_CLIENT_GENDER}', {CSDC_BIRTHDAY}, ' ', ' ', '{CSDC_MOBILEPHONE}', '0', ' ', ' ', ' ', ' ', '1');
    """
            show_sql(insert_sql)
        else:
            messagebox.showinfo("提示", "当前没有证件信息")


class WidgetGroup:
    """自定义组件的组合，定义 get 和 set 方法"""

    def __init__(self, frame: BaseCardFrame, name=_SENTINEL, row_num=_SENTINEL,
                 bg=_SENTINEL, bindings=_SENTINEL):
        self._has_name = name is not _SENTINEL
        self._has_row_num = row_num is not _SENTINEL
        self._has_bg = bg is not _SENTINEL
        self._has_bindings = bindings is not _SENTINEL
        self.name = name if self._has_name else None
        self.row_num = row_num if self._has_row_num else 0
        self._bg = bg if self._has_bg else None
        self._bindings = bindings if self._has_bindings else None

        self.__widget_list: list[tk.Widget] = []
        if self._has_name and self._has_row_num:
            self._label = tk.Label(frame, text=name, anchor="e", bg=bg if self._has_bg else None)
            self._label.grid(row=row_num, column=0, sticky='e')
            self.__widget_list.append(self._label)
            self.__entry_value = tk.StringVar()
            self._entry = tk.Entry(frame, textvariable=self.__entry_value)
            if bindings is not _SENTINEL and bindings:
                for sequence, func in bindings:
                    self._entry.bind(sequence, func)
            self._entry.grid(row=row_num, column=1)
            self.__widget_list.append(self._entry)
            self._btn_copy = tk.Button(frame, text="复制", command=lambda: pyperclip.copy(self.get()))
            self._btn_copy.grid(row=row_num, column=2, sticky="w")
            self.__widget_list.append(self._btn_copy)
        else:
            self._label = None
            self.__entry_value = None
            self._entry = None
            self._btn_copy = None

    def get(self):
        """
        获取输入框中的值
        :return: (str) 输入框中的值
        """
        return self.__entry_value.get()

    def set(self, value):
        """
        设置输入框中的值
        :param value: (str) 输入框中的值
        :return:
        """
        self.__entry_value.set(value)

    def clear_entry(self):
        """
        将输入框清空
        :return:
        """
        self.set("")

    def label_configure(self, **kwargs):
        """
        配置label组件
        :param kwargs: (dict) label组件的配置参数
        :return:
        """
        self._label.configure(**kwargs)

    def entry_bind(self, sequence, func):
        """
        绑定 Entry 输入框的事件

        :param sequence: 事件序列字符串，如 "<FocusOut>"
        :param func: 事件回调函数
        """
        self._entry.bind(sequence, func)

    def configure(self, **kwargs):
        """
        依据入参更新已有 WidgetGroup，不销毁重建

        :keyword name: (str) 新的字段名
        :keyword bg: (str) label 背景色，None 表示清除
        :keyword bindings: (list[tuple[str, callable]]) 事件绑定列表
        """
        if 'name' in kwargs:
            self.name = kwargs['name']
            self._label.configure(text=kwargs['name'])
        if 'bg' in kwargs:
            self._bg = kwargs['bg']
            self._label.configure(bg=kwargs['bg'] if kwargs['bg'] else 'SystemButtonFace')
        if 'bindings' in kwargs:
            self._bindings = kwargs['bindings']
            if kwargs['bindings']:
                for sequence, func in kwargs['bindings']:
                    self._entry.bind(sequence, func)

    def grid_forget(self):
        """
        隐藏控件组中的所有子组件
        :return:  - (int)控件组在frame组件中所在行
        """
        for single_widget in self.__widget_list:
            single_widget.grid_forget()
        return self.row_num

    def destroy(self):
        """
        销毁控件组中的所有子组件
        :return: - (int)控件组在frame组件中所在行
        """
        for single_widget in self.__widget_list:
            single_widget.destroy()
        return self.row_num

    def grid_info(self):
        """
        获取组件的基本信息
        :return: 字典对象
        """
        return {'name': self.name, 'row_num': self.row_num}

    def grid_at(self, row_num: int):
        """
        将组件重新定位到指定行

        :param row_num: 目标行号
        """
        self.row_num = row_num
        self._label.grid(row=row_num, column=0, sticky='e')
        self._entry.grid(row=row_num, column=1)
        self._btn_copy.grid(row=row_num, column=2, sticky='w')


class GenderGroup:
    """性别选择组件"""

    def __init__(self, frame: BaseCardFrame, name=_SENTINEL, row_num=_SENTINEL, bg=_SENTINEL):
        """
        性别选择组件（Label + 两个 Radiobutton）

        :param frame: 父级 tk 容器
        :param name: 字段名（如 "性别:"），仅描述符更新时可不传
        :param row_num: 所在行号，仅描述符更新时可不传
        :param bg: label 背景色
        """
        self._has_name = name is not _SENTINEL
        self._has_row_num = row_num is not _SENTINEL
        self._has_bg = bg is not _SENTINEL
        self.name = name if self._has_name else None
        self.row_num = row_num if self._has_row_num else 0
        self._bg = bg if self._has_bg else None

        if self._has_name and self._has_row_num:
            self._label = tk.Label(frame, text=name, bg=bg if self._has_bg else None)
            self._label.grid(row=row_num, column=0, sticky='e')
            self.__gender = tk.StringVar()
            self._radio_m = tk.Radiobutton(frame, text='男', value='男', variable=self.__gender)
            self._radio_f = tk.Radiobutton(frame, text='女', value='女', variable=self.__gender)
            self._radio_m.grid(row=row_num, column=1)
            self._radio_f.grid(row=row_num, column=2, sticky="w")
            self.__widget_list = [self._label, self._radio_m, self._radio_f]
        else:
            self._label = None
            self.__gender = None
            self._radio_m = None
            self._radio_f = None
            self.__widget_list = []

    def get(self):
        """
        获取当前选中的性别值

        :return: (str) 选中的性别 -- "男" 或 "女"
        """
        return self.__gender.get()

    def set(self, value):
        """
        设置性别选中值

        :param value: (str) "男" 或 "女"
        """
        self.__gender.set(value)

    def configure(self, name=_SENTINEL, bg=_SENTINEL):
        """
        更新已有 GenderGroup 的配置，仅更新显式传入的参数

        :param name: 新的字段名
        :param bg: label 背景色，None 表示清除
        """
        if name is not _SENTINEL:
            self.name = name
            self._label.configure(text=name)
        if bg is not _SENTINEL:
            self._bg = bg
            self._label.configure(bg=bg if bg else 'SystemButtonFace')

    def destroy(self):
        """
        销毁控件组中的所有子组件

        :return: (int) 控件组在 frame 中所在行号
        """
        for widget in self.__widget_list:
            widget.destroy()
        return self.row_num

    def grid_forget(self):
        """
        隐藏控件组中的所有子组件

        :return: (int) 控件组在 frame 中所在行号
        """
        for widget in self.__widget_list:
            widget.grid_forget()
        return self.row_num

    def grid_info(self):
        """
        获取组件的基本信息

        :return: (dict) 包含 name 和 row_num 的字典
        """
        return {'name': self.name, 'row_num': self.row_num}

    def grid_at(self, row_num: int):
        """
        将组件重新定位到指定行

        :param row_num: 目标行号
        """
        self.row_num = row_num
        self._label.grid(row=row_num, column=0, sticky='e')
        self._radio_m.grid(row=row_num, column=1)
        self._radio_f.grid(row=row_num, column=2, sticky='w')


class Sfz(BaseCardFrame):
    """身份证的页面"""

    def __init__(self, master=None):
        """
        初始化身份证页面，创建特有字段和按钮

        :param master: 父级 tk 容器
        """
        super().__init__(master)
        self.id_info: IdCardGenerator.TypeSFZ = None

        # 通过描述符仅传入需要更新的参数
        self.name_ch = WidgetGroup(self, bg=LABEL_BG)
        self.ID_No = WidgetGroup(self, bg=LABEL_BG_NO,
                                 bindings=[("<FocusOut>", self.id_no_parse),
                                           ("<Return>", self.id_no_parse)])
        self.birthday = WidgetGroup(self, bg=LABEL_BG)
        self.gender = GenderGroup(self, bg=LABEL_BG)
        self.begin_date = WidgetGroup(self, bg=LABEL_BG)

        # 子类特有字段，从 _next_row(14) 开始
        r = RowNumIterator(self._next_row)
        self.administration_code = WidgetGroup(self, name="行政区代码:", row_num=next(r), bg=LABEL_BG)
        self.province_name = WidgetGroup(self, name="省:", row_num=next(r))
        self.city_name = WidgetGroup(self, name="市:", row_num=next(r))
        self.county_name = WidgetGroup(self, name="县:", row_num=next(r))
        self.ID_No_old = WidgetGroup(self, name="旧版号码:", row_num=next(r), bg=LABEL_BG_OLD_NO)

        # 按钮
        self.btn_refresh = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh.grid(row=r.current, column=1)
        self.button_upgrade = tk.Button(self, text="升位", command=self.upgrade_ID_number, bg=LABEL_BG_OLD_NO)
        create_tooltip(self.button_upgrade, text="15位号码升位为18位")
        self.button_upgrade.grid(row=r.current, column=2, sticky="w")

        self.button_check = tk.Button(self, text="清除信息", command=self.clear_all_fields)
        create_tooltip(self.button_check, text="清除所有输入框中的信息")
        self.button_check.grid(row=next(r), column=0, sticky="e")

        self.btn_generate = tk.Button(self, text="自定义生成", command=self.generate_by_input, bg=LABEL_BG)
        create_tooltip(self.btn_generate, text="依据变色字段输入进行生成")
        self.btn_generate.grid(row=r.current, column=0, sticky="e")

        self.button_check_num_calculate = tk.Button(self, text="校验位补全", command=self.check_number_complete,
                                                    bg=LABEL_BG_NO)
        create_tooltip(self.button_check_num_calculate, text="只做校验位计算并补全")
        self.button_check_num_calculate.grid(row=r.current, column=1)

        self.button_insert_database_sql = tk.Button(self, text="同步福研", command=self.show_id_info_by_sql)
        self.button_insert_database_sql.grid(row=next(r), column=2)

        self.button_quit = tk.Button(self, text="退出", command=self.master.destroy)
        self.button_quit.grid(row=next(r), column=2, sticky="w")

        self.generate_default()

    def generate_default(self):
        self.id_info = IdCardGenerator.TypeSFZ()
        self.show_info()

    def upgrade_ID_number(self):
        """
        给15位旧版身份证号码做升位并显示在证件号码lable中
        :return:
        """
        ID_no_old = self.ID_No_old.get()
        if (length := len(ID_no_old)) != 15:
            messagebox.showinfo("提示", f"输入{ID_no_old}为{length}位,请输入15位旧版身份证号码")
            return
        ID_No_src = ID_no_old[0:6] + "19" + ID_no_old[6:]
        try:
            ID_no_new = IdCardGenerator.IDNOGenerator.calculate_check_num_cls(ID_No_src)
            self.ID_No.set(ID_no_new)
            # 升位的同时解析新的身份证号码
            self.id_no_parse()
        except ValueError as e:
            messagebox.showinfo("提示", f"输入有误,{e}")

    def generate_by_input(self):
        name_ch = self.name_ch.get() or None
        name_en = self.name_en.get() or None
        birthday = self.birthday.get() or None
        gender = self.gender.get() or None
        administration_code = self.administration_code.get() or None
        begin_date = self.begin_date.get() or None
        try:
            self.id_info = IdCardGenerator.TypeSFZ(name_ch, name_en, birthday, gender, county_code=administration_code,
                                                   begin_date=begin_date)
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

    def show_info(self):
        super().show_info()
        self.administration_code.set(self.id_info.county_code)
        self.province_name.set(self.id_info.province_name)
        self.city_name.set(self.id_info.city_name)
        self.county_name.set(self.id_info.county_name)
        self.id_address.set(self.id_info.address)
        self.ID_No_old.set(self.id_info.No[0:6] + self.id_info.No[8:-1])

    def refresh_default(self):
        self.generate_default()
        return self

    def id_no_parse(self, event=None):
        """
        解析身份证号码并填充到对应字段

        :param event: tk 事件对象（失焦或回车事件的 Event，可为 None）
        """
        print(f"{event}事件触发的解析身份证号码...")
        try:
            id_no = self.ID_No.get()
            id_info: dict = IdCardGenerator.TypeSFZ.id_no_parse(id_no)
            self.gender.set(id_info.get('gender', ''))
            self.birthday.set(id_info.get('birthday', ''))
            self.administration_code.set(id_info.get('county_code', ''))
            self.province_name.set(id_info.get('province_name', ''))
            self.city_name.set(id_info.get('city_name', ''))
            self.county_name.set(id_info.get('county_name', ''))
            self.id_address.set(id_info.get('address', ''))
            self.ID_No_old.set(id_no[0:6] + id_no[8:-1])
        except Exception as e:
            messagebox.showinfo("提示", f"证件号码解析出错,错误信息为:{e}")


class Yjj2023(BaseCardFrame):
    """2023年版永居证的页面"""

    def __init__(self, master=None):
        """
        初始化 2023 版永居证页面，创建特有字段和按钮

        :param master: 父级 tk 容器
        """
        super().__init__(master)
        self.id_info = None

        # 通过描述符仅传入需要更新的参数
        self.name_ch = WidgetGroup(self, bg=LABEL_BG)
        self.ID_No = WidgetGroup(self, bg=LABEL_BG_NO,
                                 bindings=[("<FocusOut>", self.id_no_parse),
                                           ("<Return>", self.id_no_parse)])
        self.name_en = WidgetGroup(self, bg=LABEL_BG)
        self.birthday = WidgetGroup(self, bg=LABEL_BG)
        self.gender = GenderGroup(self, bg=LABEL_BG)
        self.begin_date = WidgetGroup(self, bg=LABEL_BG)
        # 子类特有字段，从 _next_row(14) 开始
        r = RowNumIterator(self._next_row)
        self.province_code = WidgetGroup(self, name="办理地区码:", row_num=next(r), bg=LABEL_BG)
        self.province_name = WidgetGroup(self, name="办理省份:", row_num=next(r), bg=LABEL_BG)
        self.nationality_number = WidgetGroup(self, name="国籍编号:", row_num=next(r))
        self.nationality_code = WidgetGroup(self, name="国籍代码:", row_num=next(r), bg=LABEL_BG)
        self.nationality_name_cn = WidgetGroup(self, name="国家简称:", row_num=next(r))
        self.ID_No_other = WidgetGroup(self, name="旧版号码:", row_num=next(r))

        # 按钮
        self.button_clear = tk.Button(self, text="清除信息", command=self.clear_all_fields)
        create_tooltip(self.button_clear, text="清除所有输入框中的信息")
        self.button_clear.grid(row=r.current, column=0, sticky="e")
        self.btn_refresh = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh.grid(row=r.current, column=1)

        self.btn_generate_image = tk.Button(self, text="合成图像", anchor="e", command=self.generate_image)
        self.btn_generate_image.grid(row=next(r), column=2, sticky="w")

        self.btn_generate = tk.Button(self, text="自定义生成", command=self.generate_by_input, bg=LABEL_BG)
        create_tooltip(self.btn_generate, text="依据变色字段输入进行生成")
        self.btn_generate.grid(row=r.current, column=0, sticky="e")

        self.button_check_num_calculate = tk.Button(self, text="校验位补全", command=self.check_number_complete,
                                                    bg=LABEL_BG_NO)
        create_tooltip(self.button_check_num_calculate, text="只做校验位计算并补全")
        self.button_check_num_calculate.grid(row=r.current, column=1)

        self.button_insert_database_sql = tk.Button(self, text="同步福研", command=self.show_id_info_by_sql)
        self.button_insert_database_sql.grid(row=next(r), column=2)

        self.button_quit = tk.Button(self, text="退出", command=self.master.destroy)
        self.button_quit.grid(row=r.current, column=2, sticky="w")

        if type(self) is Yjj2023:
            self.generate_default()

    def generate_by_input(self, event=None):
        """
        依据变色字段的输入值生成证件信息

        :param event: tk 事件对象（可为 None）
        """
        # 依据自定义输入,需要同步修改其他文件的内容
        name_ch = self.name_ch.get() or None
        name_en = self.name_en.get() or None
        birthday = self.birthday.get() or None
        gender = self.gender.get() or None
        province_code = self.province_code.get() or None
        province_name = self.province_name.get() or None
        begin_date = self.begin_date.get() or None
        if province_name is None and province_code:
            # 名称优先级高,同时输入了代码和名称时,根据名称查不到代码才使用代码信息,下方的国籍也是一样的
            try:
                province_name = Nationality.administration_division[province_code]
            except KeyError as e:
                messagebox.showinfo("提示", f"地区码码不合法,错误信息为:{e},请重新输入")
                return
        nationality_code = self.nationality_code.get() or None
        # nationality_name_cn = self.entry_nationality_name_cn.get() or None
        try:
            self.id_info = IdCardGenerator.TypeYJZ(
                name_ch=name_ch,
                name_en=name_en,
                province_name=province_name,
                birthday=birthday,
                gender=gender,
                national_code_3=nationality_code,
                begin_date=begin_date
            )
            self.show_info()
        except Exception as e:
            messagebox.showinfo("提示", f"自定义生成出错,错误信息为:{e}")

    def generate_default(self, event=None):
        """
        随机生成新版永居证信息并填充到界面

        :param event: tk 事件对象（可为 None）
        """
        self.id_info = IdCardGenerator.TypeYJZ()
        self.show_info()

    def id_no_parse(self, event=None):
        """
        解析永居证号码并填充到对应字段

        :param event: tk 事件对象（可为 None）
        """
        print(f"{event}事件触发的解析新版永居证号码...")
        try:
            id_no = self.ID_No.get()
            id_info: dict = IdCardGenerator.TypeYJZ.id_no_parse(id_no)
            self.gender.set(id_info.get('gender', ''))
            self.birthday.set(id_info.get('birthday', ''))
            self.province_code.set(id_info.get('province_code', ''))
            self.province_name.set(id_info.get('province_name', ''))
            self.nationality_code.set(id_info.get('nationality_code', ''))
            self.nationality_number.set(id_info.get('nationality_number', ''))
            self.nationality_name_cn.set(id_info.get('nationality_name_ch', ''))
        except Exception as e:
            messagebox.showinfo("提示", f"证件号码解析出错,错误信息为:{e}")

    def show_info(self):
        super().show_info()
        self.province_code.set(self.id_info.province_code)
        self.province_name.set(Nationality.CODE_PROVINCE_DATA.get(int(self.id_info.province_code), '未知'))
        self.nationality_number.set(self.id_info.nationality_number)
        self.nationality_code.set(self.id_info.nationality_code)
        self.nationality_name_cn.set(self.id_info.nationality_name_ch)
        self.ID_No_other.set('有需要在2017版页面中用校验位补全的方式生成')

    def generate_image(self, event=None):
        try:
            file_path = self.id_info.generate_image()
            pyperclip.copy(file_path)
            messagebox.showinfo("提示", f"生成证件图片并复制路径到剪切板:{file_path}")
        except Exception as e:
            messagebox.showinfo("提示", f"生成证件图片出错,错误信息为:{e}")

    def check_number_complete(self, event=None):
        ID_No_src = self.ID_No.get()
        ID_No_src = ID_No_src[0:17]
        try:
            ID_No_src = IdCardGenerator.IDNOGenerator.calculate_check_num_cls(ID_No_src)
        except ValueError as e:
            messagebox.showinfo("提示", f"输入有误,{e}")
        self.ID_No.set(ID_No_src)
        # print(__type(self), event)


class Yjj2017(Yjj2023):
    """2017年版永居证的页面"""

    def __init__(self, master=None):
        """
        初始化 2017 版永居证页面，隐藏办理省份字段并创建办理省市字段

        :param master: 父级 tk 容器
        """
        super().__init__(master)

        # 隐藏不需要的字段，在相同位置创建替代字段；清除不使用的背景色
        num1 = self.province_code.grid_forget()
        num2 = self.province_name.grid_forget()
        self.city_code = WidgetGroup(self, name="办理省市码:", row_num=num1, bg=LABEL_BG)
        self.city_name = WidgetGroup(self, name="办理省市:", row_num=num2)

        # 描述符自动检测已有 ID_No_other，调用 configure 更新名称
        self.ID_No_other = WidgetGroup(self, name="新版号码:", row_num=self.ID_No_other.row_num)

        self.btn_generate_image.grid_forget()

        self.generate_default()

    def generate_default(self, event=None):  # event就是点击事件
        self.id_info = IdCardGenerator.TypeYJZ2017()
        # messagebox.showinfo("提示", "校验方法")
        self.show_info()

    def generate_by_input(self, event=None):
        # 依据自定义输入,需要同步修改其他文件的内容
        name_ch = self.name_ch.get() or None
        name_en = self.name_en.get() or None
        birthday = self.birthday.get() or None
        gender = self.gender.get() or None
        nationality_code = self.nationality_code.get() or None
        city_code = self.city_code.get() or None
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
            self.show_info()
        except Exception as e:
            messagebox.showinfo("提示", f"自定义生成出错,错误信息为:{e}")

    def show_info(self):
        BaseCardFrame.show_info(self)
        self.city_code.set(self.id_info.city_code)
        province_code = self.id_info.city_code[0:2] + '0000'
        if province_code not in Nationality.CODE_HONGKONG_MACAO_TAIWAN:
            province_name = Nationality.administration_division.get(province_code)
        else:
            province_name = ''
        self.city_name.set(province_name + self.id_info.city_name)
        self.nationality_number.set(self.id_info.nationality_number)
        self.nationality_code.set(self.id_info.nationality_code)
        self.nationality_name_cn.set(self.id_info.nationality_name_ch)
        self.ID_No_other.set(self.id_info.No_2023)

    def check_number_complete(self, event=None):
        ID_No_src = self.ID_No.get()
        check_num = ''
        try:
            ID_No_src = ID_No_src[0:14]
            check_num = IdCardGenerator.calculate_check_num_731(ID_No_src)
        except Exception as e:
            messagebox.showinfo("提示", f"输入有误,错误信息:{e}")
        self.ID_No.set(ID_No_src + check_num)

    def id_no_parse(self, event=None):
        print(f"{event}事件触发的解析旧版永居证号码...")
        try:
            id_no = self.ID_No.get()
            id_info: dict = IdCardGenerator.TypeYJZ2017.id_no_parse(id_no)
            self.gender.set(id_info.get('gender', ''))
            self.birthday.set(id_info.get('birthday', ''))
            self.city_code.set(id_info.get('province_city_code', ''))
            self.city_name.set(id_info.get('province_city_name', ''))
            self.nationality_number.set(id_info.get('nationality_number', ''))
            self.nationality_code.set(id_info.get('nationality_code', ''))
            self.nationality_name_cn.set(id_info.get('nationality_name_ch', ''))
            self.ID_No_other.set(id_info.get('ID_No_other', ''))
        except Exception as e:
            messagebox.showinfo("提示", f"证件号码解析出错,错误信息为:{e}")


class GATJzz(BaseCardFrame):
    """港澳台居民居住证的页面"""

    def __init__(self, master=None):
        """
        初始化港澳台居住证页面，在公共字段前插入证件类别下拉框

        :param master: 父级 tk 容器
        """
        super().__init__(master, start_row_num=2)
        r = RowNumIterator(1)

        # 子类特有：证件类别下拉框（公共字段之前）
        self.id_type = tk.StringVar()
        self.label_id_type = tk.Label(self, text="证件类别:")
        self.label_id_type.grid(row=r.current, column=0, sticky='e')
        gat_id_type = tuple(member.value for member in IdCardGenerator.GATPermanentResident)
        self.combobox_id_type = ttk.Combobox(self, textvariable=self.id_type, values=gat_id_type)
        self.combobox_id_type.bind("<<ComboboxSelected>>", self.generate_default)
        self.combobox_id_type.grid(row=next(r), column=1, sticky='w')

        # 通过描述符仅传入需要更新的参数
        self.name_ch = WidgetGroup(self, bg=LABEL_BG)
        self.ID_No = WidgetGroup(self, bg=LABEL_BG_NO,
                                 bindings=[("<FocusOut>", self.id_no_parse),
                                           ("<Return>", self.id_no_parse)])
        self.name_en = WidgetGroup(self, bg=LABEL_BG)
        self.birthday = WidgetGroup(self, bg=LABEL_BG)
        self.gender = GenderGroup(self, bg=LABEL_BG)
        self.begin_date = WidgetGroup(self, bg=LABEL_BG)
        # 子类特有字段，从 _next_row(16) 开始
        r2 = RowNumIterator(self._next_row)
        self.province_code = WidgetGroup(self, name="地区码:", row_num=next(r2))
        self.province_name = WidgetGroup(self, name="地区:", row_num=next(r2))
        self.nationality_code = WidgetGroup(self, name="国籍代码:", row_num=next(r2))
        # 按钮
        self.btn_clear_gat = tk.Button(self, text="清除信息", command=self.clear_all_fields)
        create_tooltip(self.btn_clear_gat, text="清除所有输入框中的信息")
        self.btn_clear_gat.grid(row=r2.current, column=0, sticky="e")
        self.btn_refresh_gat = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh_gat.grid(row=r2.current, column=1)
        self.button_insert_database_sql = tk.Button(self, text="同步福研", command=self.show_id_info_by_sql)
        self.button_insert_database_sql.grid(row=next(r2), column=2)

        self.btn_generate_gat = tk.Button(self, text="自定义生成", command=self.generate_by_input, bg=LABEL_BG)
        create_tooltip(self.btn_generate_gat, text="依据变色字段输入进行生成")
        self.btn_generate_gat.grid(row=r2.current, column=0, sticky="e")
        self.button_check_gat = tk.Button(self, text="校验位补全", command=self.check_num_complete, bg=LABEL_BG_NO)
        self.button_check_gat.grid(row=r2.current, column=1)

        self.button_quit_gat = tk.Button(self, text="退出", command=self.master.destroy)
        self.button_quit_gat.grid(row=next(r2), column=2, sticky="w")

        self.id_type.set(IdCardGenerator.GATPermanentResident.HKG_PERMANENT_RESIDENT.value)
        self.generate_default()

    def generate_by_input(self, event=None):
        name_ch = self.name_ch.get() or None
        name_en = self.name_en.get() or None
        birthday = self.birthday.get() or None
        gender = self.gender.get() or None
        begin_date = self.begin_date.get() or None
        try:
            self.id_info = IdCardGenerator.TypeGATJZZ(self.id_type.get(), name_ch=name_ch, name_en=name_en,
                                                      birthday=birthday, gender=gender, begin_date=begin_date, )
            self.show_info()
        except Exception as e:
            messagebox.showinfo("提示", f"自定义生成出错,错误信息为:{e}")

    def generate_default(self, event=None):  # event就是点击事件
        self.id_info = IdCardGenerator.TypeGATJZZ(self.id_type.get())
        # messagebox.showinfo("提示", "校验方法")
        self.show_info()

    def show_info(self):
        super().show_info()
        self.province_code.set(self.id_info.region_code)
        self.province_name.set(self.id_info.province_name)
        self.nationality_code.set(self.id_info.nationality_code)        

    def check_num_complete(self, event=None):
        ID_No_src = self.ID_No.get()
        ID_No_src = ID_No_src[0:17]
        try:
            ID_No_src = IdCardGenerator.IDNOGenerator.calculate_check_num_cls(ID_No_src)
        except ValueError as e:
            messagebox.showinfo("提示", f"输入有误,{e}")
        self.ID_No.set(ID_No_src)

    def id_no_parse(self, event=None):
        print(f"{event}事件触发的解析港澳台居住证号码...")
        try:
            id_no = self.ID_No.get()
            id_info: dict = IdCardGenerator.TypeGATJZZ.id_no_parse(id_no)
            self.id_type.set(id_info.get('id_type', ''))
            self.gender.set(id_info.get('gender', ''))
            self.birthday.set(id_info.get('birthday', ''))
            self.province_name.set(id_info.get('province_name', ''))
            self.province_code.set(id_info.get('region_code', ''))

        except Exception as e:
            messagebox.showinfo("提示", f"证件号码解析出错,错误信息为:{e}")


class GAtxz(BaseCardFrame):
    """港澳居民来往内地通行证"""

    def __init__(self, master=None):
        """
        初始化港澳通行证页面，在公共字段前插入证件类别下拉框

        :param master: 父级 tk 容器
        """
        super().__init__(master, start_row_num=2)
        r = RowNumIterator(1)

        # 子类特有：证件类别下拉框（公共字段之前）
        self.id_type = tk.StringVar()
        self.label_id_type = tk.Label(self, text="证件类别:")
        self.label_id_type.grid(row=r.current, column=0, sticky='e')
        ga_id_type = tuple(member.value for member in IdCardGenerator.HkgMacPermit)
        self.combobox_id_type = ttk.Combobox(self, textvariable=self.id_type, values=ga_id_type)
        self.combobox_id_type.bind("<<ComboboxSelected>>", self.generate_default)
        self.combobox_id_type.grid(row=next(r), column=1, sticky='w')
        r2 = RowNumIterator(self._next_row)
        self.nationality_code = WidgetGroup(self, name="国籍代码:", row_num=next(r2))
        # 按钮
        self.button_insert_database_sql = tk.Button(self, text="同步福研", command=self.show_id_info_by_sql)
        self.button_insert_database_sql.grid(row=r2.current, column=0)

        self.btn_refresh_gat = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh_gat.grid(row=r2.current, column=1)

        self.btn_quit = tk.Button(self, text="退出", command=self.master.destroy)
        self.btn_quit.grid(row=next(r2), column=2, sticky="w")
        self._next_row = r2.current
        self.id_type.set(IdCardGenerator.HkgMacPermit.HKG_PERMIT.value)
        self.generate_default()

    def generate_default(self, event=None):
        self.id_info = IdCardGenerator.TypeGATXZ(self.id_type.get())
        self.show_info()

    def show_info(self):
        super().show_info()
        self.nationality_code.set(self.id_info.nationality_code)        


class TWtxz(BaseCardFrame):
    """台湾居民来往内地通行证"""

    def __init__(self, master=None):
        """
        初始化台湾通行证页面，无需额外子类字段

        :param master: 父级 tk 容器
        """
        super().__init__(master)

        r2 = RowNumIterator(self._next_row)
        self.nationality_code = WidgetGroup(self, name="国籍代码:", row_num=next(r2))
        # 按钮
        self.button_insert_database_sql = tk.Button(self, text="同步福研", command=self.show_id_info_by_sql)
        self.button_insert_database_sql.grid(row=r2.current, column=0)

        self.btn_refresh_gat = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh_gat.grid(row=r2.current, column=1)

        self.btn_quit = tk.Button(self, text="退出", command=self.master.destroy)
        self.btn_quit.grid(row=next(r2), column=2, sticky="w")

        self.generate_default()

    def generate_default(self, event=None):
        self.id_info = IdCardGenerator.TypeTWTXZ()
        self.show_info()

    def show_info(self):
        super().show_info()
        self.nationality_code.set(self.id_info.nationality_code)

class BusinessLicense(BaseCardFrame):
    """营业执照的页面"""

    def __init__(self, master=None):
        """
        初始化营业执照页面，重命名字段并创建统一信用代码等特有字段

        :param master: 父级 tk 容器
        """
        super().__init__(master)
        self.id_info: IdCardGenerator.TypeYYZZ = None

        # 通过描述符仅传入需要更新的参数（name 需要传是因为要改名）
        self.name_ch = WidgetGroup(self, name="企业名称:", bg=LABEL_BG)
        self.name_en = WidgetGroup(self, name="英文名称:", bg=LABEL_BG)
        self.birthday = WidgetGroup(self, name="成立日期:", bg=LABEL_BG)
        self.begin_date = WidgetGroup(self, bg=LABEL_BG)

        # 子类特有字段（与公共字段共存）
        self.credit_code = WidgetGroup(self, name="统一信用代码:", row_num=2,
                                       bg=LABEL_BG_NO,
                                       bindings=[("<FocusOut>", self.credit_code_parse),
                                                 ("<Return>", self.credit_code_parse)])

        # 子类特有字段，从 _next_row(14) 开始
        r = RowNumIterator(self._next_row)
        self.dept_code = WidgetGroup(self, name="部门代码:", row_num=next(r))
        self.org_type_code = WidgetGroup(self, name="机构类别:", row_num=next(r))
        self.admin_division_code = WidgetGroup(self, name="行政区划码:", row_num=next(r))
        self.admin_division_name = WidgetGroup(self, name="登记机关:", row_num=next(r))
        self.org_code = WidgetGroup(self, name="组织机构码:", row_num=next(r))
        self.check_code = WidgetGroup(self, name="校验码:", row_num=next(r))

        # 营业执照不需要性别
        self.gender.grid_forget()

        # 按钮
        self.button_clear = tk.Button(self, text="清除信息", command=self.clear_all_fields)
        create_tooltip(self.button_clear, text="清除所有输入框中的信息")
        self.button_clear.grid(row=r.current, column=0, sticky="e")

        self.btn_refresh = tk.Button(self, text="重新随机生成", command=self.generate_default)
        self.btn_refresh.grid(row=r.current, column=1)

        self.button_insert_database_sql = tk.Button(self, text="同步福研", command=self.show_id_info_by_sql)
        self.button_insert_database_sql.grid(row=next(r), column=2)

        self.btn_generate = tk.Button(self, text="自定义生成", command=self.generate_by_input, bg=LABEL_BG)
        create_tooltip(self.btn_generate, text="依据变色字段输入进行生成")
        self.btn_generate.grid(row=r.current, column=0, sticky="e")
        self.button_check_num_calculate = tk.Button(self, text="校验位补全", command=self.check_number_complete,
                                                    bg=LABEL_BG_NO)
        create_tooltip(self.button_check_num_calculate, text="只做校验位计算并补全")
        self.button_check_num_calculate.grid(row=r.current, column=1)

        self.button_quit = tk.Button(self, text="退出", command=self.master.destroy)
        self.button_quit.grid(row=r.current, column=2, sticky="w")

        self.generate_default()

    def generate_default(self):
        self.id_info = IdCardGenerator.TypeYYZZ()
        self.show_info()

    def generate_by_input(self):
        name_ch = self.name_ch.get() or None
        name_en = self.name_en.get() or None
        birthday = self.birthday.get() or None
        begin_date = self.begin_date.get() or None
        try:
            self.id_info = IdCardGenerator.TypeYYZZ(name_ch=name_ch, name_en=name_en,
                                                    birthday=birthday, begin_date=begin_date)
            self.show_info()
        except Exception as e:
            messagebox.showinfo("提示", f"输入有误,错误信息为{e}")

    def check_number_complete(self):
        credit_code_src = self.credit_code.get()
        if len(credit_code_src) < 17:
            messagebox.showinfo("提示", "输入的统一社会信用代码不足17位")
            return
        credit_code_src = credit_code_src[0:17]
        try:
            complete_code = IdCardGenerator.TypeYYZZ.calculate_check_num_cls(credit_code_src)
            self.credit_code.set(credit_code_src + complete_code)
            self.check_code.set(complete_code)
        except ValueError as e:
            messagebox.showinfo("提示", f"输入有误,{e}")

    def show_info(self):
        super().show_info()
        self.credit_code.set(self.id_info.No)
        self.dept_code.set(self.id_info.MANAGEMENT_DEPARTMENT_CODE)
        self.org_type_code.set(self.id_info.ORGANIZATION_TYPE_CODE)
        self.admin_division_code.set(self.id_info.county_code)
        self.org_code.set(self.id_info.organization_code)
        self.check_code.set(self.id_info.check_num)
        self.admin_division_name.set(self.id_info.county_name)

    def refresh_default(self):
        self.generate_default()
        return self

    def credit_code_parse(self, event=None):
        print(f"{event}事件触发的解析统一社会信用代码...")
        try:
            credit_code = self.credit_code.get()
            # 输入17位的时候可能要做校验位补全
            if len(credit_code) == 17:
                return
            if len(credit_code) != 18:
                messagebox.showinfo("提示", f"输入的统一社会信用代码长度不正确: {len(credit_code)}位，应为18位")
                return

            # 解析各部分
            dept_code = credit_code[0]
            org_type_code = credit_code[1]
            admin_division_code = credit_code[2:8]
            org_code = credit_code[8:17]
            check_code = credit_code[17]

            self.dept_code.set(dept_code)
            self.org_type_code.set(org_type_code)
            self.admin_division_code.set(admin_division_code)
            self.org_code.set(org_code)
            self.check_code.set(check_code)

            # 获取行政区划名称
            admin_division_name = ''
            if admin_division_code in Nationality.administration_division:
                admin_division_name = Nationality.administration_division[admin_division_code]
            elif admin_division_code + '00' in Nationality.administration_division:
                admin_division_name = Nationality.administration_division[admin_division_code + '00']

            self.admin_division_name.set(admin_division_name)

        except Exception as e:
            messagebox.showinfo("提示", f"统一信用代码解析出错,错误信息为:{e}")


class ToolTip:
    """悬浮提示窗"""

    def __init__(self, widget, text='widget info'):
        """
        悬浮标签组件
        :param widget: (tk.Widget)tkinter中的widget组件
        :param text:  (str)悬浮标签中需要显示的文字内容
        """
        self.widget: tk.Widget = widget
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
        # x, y, cx, cy = self.widget.bbox()
        x = self.widget.winfo_rootx() + 25
        y = self.widget.winfo_rooty() + 25
        self.tip_window = tw = tk.Toplevel(self.widget)
        tw.wm_overrideredirect(True)  # 去掉窗口边框
        tw.wm_geometry(f"+{x}+{y}")  # 设置窗口位置
        label = tk.Label(tw, text=self.text, justify=tk.LEFT,
                         background="#ffffe0", relief=tk.SOLID, borderwidth=1,
                         font=("tahoma", 8, "normal"))
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
    """创建悬浮提示窗"""
    tooltip = ToolTip(widget, text)

    def enter(event):
        tooltip.showtip()

    def leave(event):
        tooltip.hidetip()

    widget.bind('<Enter>', enter)
    widget.bind('<Leave>', leave)


def show_sql(sql_text:str):
    """
    弹出一个窗口显示插入数据库的sql语句

    :param sql_text: 要显示的ID信息对象或字典
    """
    # 创建顶层窗口
    dialog = tk.Toplevel()
    dialog.title("插入福研数据库的语句")
    dialog.geometry("600x300")
    dialog.transient()  # 设置为临时窗口
    dialog.grab_set()  # 模态窗口

    # 配置窗口的行权重，让文本框可以扩展
    dialog.grid_rowconfigure(0, weight=1)
    dialog.grid_columnconfigure(0, weight=1)

    # 创建文本框框架
    text_frame = tk.Frame(dialog)
    text_frame.grid(row=0, column=0, sticky='nsew', padx=10, pady=(10, 5))

    # 配置text_frame的行权重
    text_frame.grid_rowconfigure(0, weight=1)
    text_frame.grid_columnconfigure(0, weight=1)

    # 创建滚动条
    scrollbar = tk.Scrollbar(text_frame)
    scrollbar.grid(row=0, column=1, sticky='ns')

    # 创建文本框
    text_widget = tk.Text(text_frame, wrap=tk.WORD, yscrollcommand=scrollbar.set,
                          font=("Microsoft YaHei", 10), padx=5, pady=5)
    text_widget.grid(row=0, column=0, sticky='nsew')

    # 配置滚动条
    scrollbar.config(command=text_widget.yview)
    # 插入文本
    text_widget.insert(tk.END, sql_text)

    # 设置文本框为只读
    text_widget.config(state=tk.DISABLED)

    # 创建按钮框架
    button_frame = tk.Frame(dialog)
    button_frame.grid(row=1, column=0, pady=(5, 10))

    # 确认并复制按钮的回调函数
    def confirm_and_copy():
        try:
            # 获取文本内容
            content = text_widget.get(1.0, tk.END).strip()
            # 复制到剪贴板
            pyperclip.copy(content)
            messagebox.showinfo("成功", "信息已复制到剪贴板！", parent=dialog)
        except Exception as e:
            messagebox.showerror("错误", f"复制失败: {str(e)}", parent=dialog)

    # 关闭按钮的回调函数
    def close_window():
        dialog.destroy()

    # 创建按钮
    confirm_button = tk.Button(button_frame, text="确认并复制", command=confirm_and_copy,
                               width=12, height=1)
    confirm_button.pack(side=tk.LEFT, padx=10)

    close_button = tk.Button(button_frame, text="关闭", command=close_window,
                             width=12, height=1)
    close_button.pack(side=tk.LEFT, padx=10)

    # 绑定ESC键关闭窗口
    dialog.bind('<Escape>', lambda event: close_window())

    # 等待窗口关闭
    dialog.wait_window()


# 行号迭代器
class RowNumIterator:
    """
    行号迭代器，调用 next() 返回当前行号后自增

    >>> r = RowNumIterator(1)
    >>> next(r)  # 返回 1
    1
    >>> next(r)  # 返回 2
    2
    """

    def __init__(self, start=0):
        """
        初始化迭代器

        :param start: 起始行号
        """
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        """
        返回当前行号并自增

        :return: (int) 当前行号
        """
        value = self.current
        self.current += 1
        return value


class MainApplication(tk.Tk):
    """主应用程序窗口，包含证件类型选择下拉框和缓存的 Frame 页面"""

    def __init__(self, id_kinds):
        """
        初始化主窗口

        :param id_kinds: 证件类型列表，用于下拉框
        """
        super().__init__()
        self.title("号码生成器")
        self.id_kind = tk.StringVar()
        self.label_id_kinds = tk.Label(self, text="证件类型:")
        self.label_id_kinds.grid(row=0, column=0, sticky='e')
        self.combobox_id_kind = ttk.Combobox(self, textvariable=self.id_kind, values=id_kinds)
        self.combobox_id_kind.bind("<<ComboboxSelected>>", self.create_frame)
        self.combobox_id_kind.grid(row=0, column=1, sticky='w')
        self.geometry("280x490+300+200")

        # 创建不同的 Frame 缓存
        self.frame_cache: dict[str, BaseCardFrame] = {}

        # 默认显示身份证页面
        self.id_kind.set(IdCardGenerator.IDKind.ID_CARD.value)
        self.create_frame(None)
        self.show_frame(self.frame_cache.get(IdCardGenerator.IDKind.ID_CARD.value))

    def show_frame(self, frame: BaseCardFrame = None):
        """
        隐藏当前 Frame 并显示指定 Frame

        :param frame: 要显示的 BaseCardFrame 实例，为 None 则隐藏所有
        """
        # 隐藏所有 Frame
        for widget in self.winfo_children():
            if isinstance(widget, tk.Frame):
                widget.grid_forget()
        # 显示指定的 Frame
        if frame:
            frame.grid(row=1, column=0, columnspan=4, padx=0, pady=20)
            #  根据组件多少调整窗口大小
            self.update()
            self.geometry(f"{self.winfo_reqwidth()}x{self.winfo_reqheight()}+{self.winfo_x()}+{self.winfo_y()}")

    def create_frame(self, event):
        """
        根据选中的证件类型创建或切换 Frame 页面（使用缓存避免重复创建）

        :param event: Combobox 选择事件（可为 None）
        """
        # 如果缓存中没有该 Frame，则创建并添加到缓存中
        try:
            selected_id_kind = str(self.id_kind.get())
            if selected_id_kind not in self.frame_cache.keys():
                if IdCardGenerator.IDKind.ID_CARD.value == selected_id_kind:
                    self.frame_cache[selected_id_kind] = Sfz(self)
                elif IdCardGenerator.IDKind.FOREIGN_PERMANENT_RESIDENT2023.value == selected_id_kind:
                    self.frame_cache[selected_id_kind] = Yjj2023(self)
                elif IdCardGenerator.IDKind.GAT_PERMANENT_RESIDENT.value == selected_id_kind:
                    self.frame_cache[selected_id_kind] = GATJzz(self)
                elif IdCardGenerator.IDKind.HKG_MAC_PERMIT.value == selected_id_kind:
                    self.frame_cache[selected_id_kind] = GAtxz(self)
                elif IdCardGenerator.IDKind.CTN_PERMIT.value == selected_id_kind:
                    self.frame_cache[selected_id_kind] = TWtxz(self)
                elif IdCardGenerator.IDKind.FOREIGN_PERMANENT_RESIDENT2017.value == selected_id_kind:
                    self.frame_cache[selected_id_kind] = Yjj2017(self)
                elif IdCardGenerator.IDKind.BUSINESS_LICENSE.value == selected_id_kind:
                    self.frame_cache[selected_id_kind] = BusinessLicense(self)
                else:
                    messagebox.showwarning("错误", f"当前输入的证件类型{selected_id_kind}不支持")

                frame = self.frame_cache.get(selected_id_kind, None)

            # 缓存中有该 Frame，则直接刷新并显示该 Frame
            else:
                frame = self.frame_cache.get(selected_id_kind, None).refresh_default()
            self.show_frame(frame)

        except Exception as e:
            messagebox.showwarning("错误", f"发生错误,错误信息为:{e}")


if __name__ == '__main__':
    # root = tk.Tk()
    # root.title("永居证生成器")
    id_kinds_all = tuple(member.value for member in IdCardGenerator.IDKind)
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
