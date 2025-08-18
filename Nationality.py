#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time     : 2024/9/28 下午4:01
# @Author   : Admin
# @File     : Nationality.py
# @Software : Nationality.py
# @实现功能  : 存储国籍信息
"""
import csv
import re
import os
import sys


def resource_path(relative_path):
    """
    获取资源的绝对路径。
    该函数用于确定资源文件的绝对路径，特别是在使用PyInstaller等工具将Python脚本打包为可执行文件时。
    当程序被打包为可执行文件并运行时，资源文件可能不在原始的相对路径位置，此时该函数能确保正确找到资源文件。

    :param relative_path: (str)资源文件相对于程序的路径。

    返回:
    str: 资源文件的绝对路径。
    """
    # 是否Bundle Resource
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


BASE_DIR = str(resource_path(''))

# 依据国籍编号的国籍信息字典，键为国籍编号（字符串类型），值为国籍信息（字符串类型）
nationality_dict_by_number: dict[str, "NationalityInfo"] = {}
# 依据两位国籍代码的国籍信息字典，键为两位国籍代码（字符串类型），值为国籍信息（字符串类型）
nationality_dict_by_code_2 = {}
# 依据三位国籍代码的国籍信息字典，键为三位国籍代码（字符串类型），值为国籍信息（字符串类型）
nationality_dict_by_code_3 = {}
# 省市代码
administration_division = {}
# 旧版行政区划
administration_division_old = {}
# 省级行政单位列表
CODE_PROVINCE_DATA = {
    11: "北京",
    12: "天津",
    13: "河北",
    14: "山西",
    15: "内蒙古",
    21: "辽宁",
    22: "吉林",
    23: "黑龙江",
    31: "上海",
    32: "江苏",
    33: "浙江",
    34: "安徽",
    35: "福建",
    36: "江西",
    37: "山东",
    41: "河南",
    42: "湖北",
    43: "湖南",
    44: "广东",
    45: "广西",
    46: "海南",
    50: "重庆",
    51: "四川",
    52: "贵州",
    53: "云南",
    54: "西藏",
    61: "陕西",
    62: "甘肃",
    63: "青海",
    64: "宁夏",
    65: "新疆",
    71: "台湾",
    81: "香港",
    82: "澳门"
}
# 港澳台行政区代码
CODE_HONGKONG_MACAO_TAIWAN = ('810000', '820000', '710000')


# 国籍信息
class NationalityInfo:
    def __init__(self, name_cn="", name_en="", number="", code_2="", code_3="", full_name_cn="", full_name_en=""):
        """
        初始化国籍信息对象。

        :param name_cn: (str) 中文简称
        :param name_en: (str) 英文简称
        :param number: (str) 国籍编号
        :param code_2: (str) 两位国籍代码
        :param code_3: (str) 三位国籍代码
        :param full_name_cn: (str) 中文全称
        :param full_name_en: (str) 英文全称
        """
        self.name_cn = name_cn
        self.name_en = name_en
        self.number = number
        self.code_2 = code_2
        self.code_3 = code_3
        self.full_name_cn = full_name_cn
        self.full_name_en = full_name_en

    def __str__(self):
        return f"NationalityInfo:\n中文简称={self.name_cn}, 英文简称={self.name_en}, 国籍编号={self.number}, " \
               f"两位国籍代码={self.code_2}, 三位国籍代码={self.code_3}, 中文全称={self.full_name_cn}, " \
               f"英文全称={self.full_name_en}"


# 文件中读取信息
def get_nationality_info() -> None:
    # print("开始解析国籍信息...")

    # 此处写从文件读取国籍信息的代码
    path_csv = r"./resource/GBT2659.1-2022.CSV"
    path_csv = os.path.join(BASE_DIR, path_csv)
    path_csv = os.path.normpath(path_csv)
    # path_xlsx = r"./resource/GBT2659.1-2022.xlsx"

    if not os.path.exists(path_csv):
        # nationality_read = pd.read_excel(path_xlsx, engine='openpyxl', header=0, index_col=None,
        #                                  sheet_name=0)
        # nationality_read_new = nationality_read.applymap(replace_newline)
        # nationality_read_new.to_csv(path_csv, index=True, encoding="utf-8")
        raise FileNotFoundError("找不到文件：" + path_csv)
    else:
        with open(path_csv, mode='r', encoding='utf-8') as file:
            csv_reader = csv.DictReader(file)
            # 逐行解析
            for row in csv_reader:
                name = row['中文和英文简称']
                name_cn = name.split(" ")[0]
                # 英文简称
                name_en_parts = name.split(" ")[1:]
                name_en = ' '.join(name_en_parts) if name_en_parts else ''
                # 国籍编号
                number = row['阿拉伯数字代码']
                number = number.zfill(3)
                # 两位国籍代码
                code_2 = row['两字符拉丁字母代码']
                # 三位国籍代码
                code_3 = row['三字符拉丁字母代码']
                full_name = row['中文和英文全称']
                # 没有中文全称和英文全称
                try:
                    # 中文全称
                    full_name_cn = full_name.split(" ")[0]
                    # 英文全称
                    full_name_en = ' '.join(full_name.split(" ")[1:])
                except AttributeError:
                    full_name_cn = ""
                    full_name_en = ""
                nationality_info = NationalityInfo(name_cn, name_en, number, code_2, code_3, full_name_cn, full_name_en)
                nationality_dict_by_number[nationality_info.number] = nationality_info
                nationality_dict_by_code_2[nationality_info.code_2] = nationality_info
                nationality_dict_by_code_3[nationality_info.code_3] = nationality_info


# 获取省市代码
def get_province_code() -> None:
    # print("开始解析行政区划信息...")
    admin_division = r"./resource/administrative_division.csv"
    admin_division = os.path.join(BASE_DIR, admin_division)
    admin_division = os.path.normpath(admin_division)
    admin_division_old = r"./resource/administrative_division_old.csv"
    admin_division_old = os.path.join(BASE_DIR, admin_division_old)
    admin_division_old = os.path.normpath(admin_division_old)
    try:
        with open(admin_division, mode='r', encoding='utf-8') as file, \
                open(admin_division_old, mode='r', encoding='utf-8') as file_old:
            csv_reader = csv.DictReader(file)
            csv_reader_old = csv.DictReader(file_old)
            for row in csv_reader:
                administration_division[row['行政区代码']] = row['行政区名称']
            for row_old in csv_reader_old:
                administration_division_old[row_old['行政区代码']] = row_old['行政区名称']
    except FileNotFoundError as e:
        raise FileNotFoundError(f'新版或者旧版行政区划文件未找到:{e}')
    except Exception as e:
        raise Exception(f"{__name__}发生错误: {e}")


# 替换换行符
def replace_newline(data_info: str):
    # 判断是否为字符串类型，不是的则直接原样返回
    if not isinstance(data_info, str):
        return data_info
    while "\n" in data_info or "\r\n" in data_info:
        # 替换以换行开头的换行符
        result = re.match(r"^\n.*", data_info, re.DOTALL)
        if result:
            data_info = re.sub(r"\n", "", data_info, count=1)
        # 替换中文字符前的换行符
        result = re.match(r"^.+\n[\u4e00-\u9fa5]+.*", data_info, re.DOTALL)
        if result:
            data_info = re.sub(r"\n", "", data_info, count=1)
        # 替换英文字符前的换行符
        result = re.match(r"^.+\n[A-Za-z]*", data_info, re.DOTALL)
        if result:
            data_info = re.sub(r"\n", " ", data_info, count=1)
    return data_info


get_nationality_info()
get_province_code()

if __name__ == '__main__':
    print(administration_division_old)
