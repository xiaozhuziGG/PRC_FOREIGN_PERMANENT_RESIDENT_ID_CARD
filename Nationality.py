#!/usr/bin/python3
# -*- coding: utf-8 -*-
"""
# @Time     : 2024/9/28 下午4:01
# @Author   : Admin
# @File     : Nationality.py
# @Software : Nationality.py
# @实现功能  : 存储国籍信息
"""
import pandas as pd
import re
import os

# 依据国籍编号的国籍信息字典
nationality_dict_by_number = {}
# 依据两位国籍代码的国籍信息字典
nationality_dict_by_code_2 = {}
# 依据三位国籍代码的国籍信息字典
nationality_dict_by_code_3 = {}
# 省市代码
administrative_division = {}
# 永久居留证国编代码和国籍缩写,可能没用了先留着吧
CODE_NATIONALITY_DATA = {
    "008": "ALB",
    "012": "DZA",
    "004": "AFG",
    "032": "ARG",
    "784": "ARE",
    "533": "ABW",
    "512": "OMN",
    "031": "AZE",
    "818": "EGY",
    "231": "ETH",
    "372": "IRL",
    "233": "EST",
    "020": "AND",
    "024": "AGO",
    "660": "AIA",
    "028": "ATG",
    "040": "AUT",
    "248": "ALA",
    "036": "AUS",
    "446": "MAC",
    "052": "BRB",
    "598": "PNG",
    "044": "BHS",
    "586": "PAK",
    "600": "PRY",
    "275": "PSE",
    "048": "BHR",
    "591": "PAN",
    "076": "BRA",
    "112": "BLR",
    "060": "BMU",
    "100": "BGR",
    "580": "MNP",
    "807": "MKD",
    "204": "BEN",
    "056": "BEL",
    "352": "ISL",
    "630": "PRI",
    "070": "BIH",
    "616": "POL",
    "068": "BOL",
    "084": "BLZ",
    "535": "BES",
    "072": "BWA",
    "064": "BTN",
    "854": "BFA",
    "108": "BDI",
    "074": "BVT",
    "408": "PRK",
    "226": "GNQ",
    "208": "DNK",
    "276": "DEU",
    "626": "TLS",
    "768": "TGO",
    "214": "DOM",
    "212": "DMA",
    "643": "RUS",
    "218": "ECU",
    "232": "ERI",
    "250": "FRA",
    "234": "FRO",
    "258": "PYF",
    "254": "GUF",
    "260": "ATF",
    "336": "VAT",
    "608": "PHL",
    "242": "FJI",
    "246": "FIN",
    "132": "CPV",
    "238": "FLK",
    "270": "GMB",
    "178": "COG",
    "180": "COD",
    "170": "COL",
    "188": "CRI",
    "308": "GRD",
    "304": "GRL",
    "268": "GEO",
    "831": "GGY",
    "192": "CUB",
    "312": "GLP",
    "316": "GUM",
    "328": "GUY",
    "398": "KAZ",
    "332": "HTI",
    "410": "KOR",
    "528": "NLD",
    "334": "HMD",
    "449": "MNE",
    "340": "HND",
    "296": "KIR",
    "262": "DJI",
    "417": "KGZ",
    "324": "GIN",
    "624": "GNB",
    "124": "CAN",
    "288": "GHA",
    "266": "GAB",
    "116": "KHM",
    "203": "CZE",
    "716": "ZWE",
    "120": "CMR",
    "634": "QAT",
    "136": "CYM",
    "166": "CCK",
    "174": "COM",
    "384": "CIV",
    "414": "KWT",
    "191": "HRV",
    "404": "KEN",
    "184": "COK",
    "531": "CUW",
    "428": "LVA",
    "426": "LSO",
    "418": "LAO",
    "422": "LBN",
    "440": "LTU",
    "430": "LBR",
    "434": "LBY",
    "438": "LIE",
    "638": "REU",
    "442": "LUX",
    "646": "RWA",
    "642": "ROU",
    "450": "MDG",
    "833": "IMN",
    "462": "MDV",
    "470": "MLT",
    "454": "MWI",
    "458": "MYS",
    "466": "MLI",
    "584": "MHL",
    "474": "MTQ",
    "175": "MYT",
    "480": "MUS",
    "478": "MRT",
    "840": "USA",
    "581": "UMI",
    "016": "ASM",
    "850": "VIR",
    "496": "MNG",
    "500": "MSR",
    "050": "BGD",
    "604": "PER",
    "583": "FSM",
    "104": "MMR",
    "498": "MDA",
    "504": "MAR",
    "492": "MCO",
    "508": "MOZ",
    "484": "MEX",
    "516": "NAM",
    "710": "ZAF",
    "010": "ATA",
    "239": "SGS",
    "728": "SSD",
    "520": "NRU",
    "524": "NPL",
    "558": "NIC",
    "562": "NER",
    "566": "NGA",
    "570": "NIU",
    "578": "NOR",
    "574": "NFK",
    "585": "PLW",
    "612": "PCN",
    "620": "PRT",
    "392": "JPN",
    "752": "SWE",
    "756": "CHE",
    "222": "SLV",
    "882": "WSM",
    "688": "SRB",
    "694": "SLE",
    "686": "SEN",
    "196": "CYP",
    "690": "SYC",
    "682": "SAU",
    "652": "BLM",
    "162": "CXR",
    "678": "STP",
    "654": "SHN",
    "659": "KNA",
    "662": "LCA",
    "663": "MAF",
    "534": "SXM",
    "674": "SMR",
    "666": "SPM",
    "670": "VCT",
    "144": "LKA",
    "703": "SVK",
    "705": "SVN",
    "744": "SJM",
    "748": "SWZ",
    "729": "SDN",
    "740": "SUR",
    "090": "SLB",
    "706": "SOM",
    "762": "TJK",
    "158": "TWN",
    "764": "THA",
    "834": "TZA",
    "776": "TON",
    "796": "TCA",
    "780": "TTO",
    "788": "TUN",
    "798": "TUV",
    "792": "TUR",
    "795": "TKM",
    "772": "TKL",
    "876": "WLF",
    "548": "VUT",
    "320": "GTM",
    "862": "VEN",
    "096": "BRN",
    "800": "UGA",
    "804": "UKR",
    "858": "URY",
    "860": "UZB",
    "724": "ESP",
    "732": "ESH",
    "300": "GRC",
    "344": "HKG",
    "702": "SGP",
    "540": "NCL",
    "554": "NZL",
    "348": "HUN",
    "760": "SYR",
    "388": "JAM",
    "051": "ARM",
    "887": "YEM",
    "368": "IRQ",
    "364": "IRN",
    "376": "ISR",
    "380": "ITA",
    "356": "IND",
    "360": "IDN",
    "826": "GBR",
    "092": "VGB",
    "086": "IOT",
    "400": "JOR",
    "704": "VNM",
    "894": "ZMB",
    "832": "JEY",
    "148": "TCD",
    "292": "GIB",
    "152": "CHL",
    "140": "CAF",
    "156": "CHN",
}
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
    path_xlsx = r"./resource/GBT2659.1-2022.xlsx"

    if not os.path.exists(path_csv):
        nationality_read = pd.read_excel(path_xlsx, engine='openpyxl', header=0, index_col=None,
                                         sheet_name=0)
        nationality_read_new = nationality_read.applymap(replace_newline)
        nationality_read_new.to_csv(path_csv, index=True, encoding="utf-8")
    else:
        nationality_read_new = pd.read_csv(path_csv, encoding="utf-8", dtype={'阿拉伯数字代码': str})
    # 逐行解析
    for index, row in nationality_read_new.iterrows():
        name = row['中文和英文简称']
        name_cn = name.split(" ")[0]
        # 英文简称
        name_en = name.split(" ")[1]
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
    try:
        admin_division = r"./resource/administrative_division.csv"
        region_info = pd.read_csv(admin_division, encoding="utf-8", dtype={'行政区代码': str})
        for index, row in region_info.iterrows():
            administrative_division[row['行政区代码']] = row['行政区名称']
    except FileNotFoundError:
        print(f'文件{admin_division}不存在')


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
    print(nationality_dict_by_number)
