"""
# @Time     : 2024/2/27 14:31
# @Author   : wanggz38530
# @File     : 18位外国人永久居留证.py
# @Software :
"""
# -*- coding: utf-8 -*-
# !/usr/bin/python3.6/
import random
import string
import datetime
from abc import abstractmethod, ABC
from enum import Enum
import Nationality
from os import path, makedirs

# 资源文件的绝对路径
BASE_DIR = Nationality.BASE_DIR
# 当前日期
DATE_TODAY = datetime.date.today()


# 证件类型枚举
class IDType(Enum):
    ID_CARD = "居民身份证"
    # BUSINESS_LICENSE = "营业执照"
    FOREIGN_PERMANENT_RESIDENT2023 = "2023版外国人永久居留证"
    FOREIGN_PERMANENT_RESIDENT2017 = "2017版外国人永久居留证"
    HKG_MAC_PERMIT = "港澳居民来往内地通行证"
    CTN_PERMIT = "台湾居民来往大陆通行证"
    GAT_PERMANENT_RESIDENT = "港澳台居民居住证"


# 港澳台居民居住证枚举
class GATPermanentResident(Enum):
    HKG_PERMANENT_RESIDENT = "香港居民居住证"
    MAC_PERMANENT_RESIDENT = "澳门居民居住证"
    CTN_PERMANENT_RESIDENT = "台湾居民居住证"


# 港澳居民来往内地通行证枚举
class HkgMacPermit(Enum):
    HKG_PERMIT = "香港居民来往内地通行证"
    MAC_PERMIT = "澳门居民来往内地通行证"


def get_gender(num: str) -> str:
    """校验性别"""
    return '女' if int(num) % 2 == 0 else '男'


def generate_date():
    """生成随机日期,1920-01-01到当前日期"""
    # 设置日期范围
    start_date = datetime.date(1920, 1, 1)
    end_date = DATE_TODAY

    # 计算日期范围的天数
    days_between = (end_date - start_date).days

    # 生成随机天数并加上起始日期，randint包含起止区间
    random_days = random.randint(0, days_between)
    random_date = start_date + datetime.timedelta(days=random_days)
    return datetime.date.strftime(random_date, '%Y%m%d')


def generate_sequence_code(start, end) -> str:
    """
    生成指定范围内序列的代码字符串。

    本函数的目的是为了创建一个代码字符串，该字符串包含一个用于打印从start到end（包含start和end）范围内所有整数的Python代码片段。

    参数:
    - start (int): 序列的起始整数值。
    - end (int): 序列的结束整数值。

    返回:
    - str: 一个包含序列打印代码的字符串。
    """
    sequence_num = random.randint(start, end)
    length = len(str(end))
    sequence_code = str(sequence_num).zfill(length)
    return sequence_code


def convert_ten_tox(last_num: int) -> str:
    """校验位是10，则换成X"""
    if 10 == last_num:
        return 'X'
    else:
        return str(last_num)


# 获取省市代码
def get_province_city_code() -> tuple:
    items = list(Nationality.administration_division.items())
    while True:
        selected_item = random.sample(items, 1)[0]
        code = selected_item[0]
        name = selected_item[1]
        # 过滤掉省级行政区,包括省，自治区，直辖市,但不包括港澳台.
        if not (code.endswith('0000') and code not in Nationality.CODE_HONGKONG_MACAO_TAIWAN):
            # 行政区划格式为 330108,滨江区
            city_code = selected_item[0][0:4]
            break
    city_name = Nationality.administration_division.get(city_code + '00', name)
    return city_code, city_name


# 获取省市县代码
def get_province_city_county_code() -> tuple:
    items = list(Nationality.administration_division.items())

    while True:
        selected_item = random.sample(items, 1)[0]
        # 行政区划格式为 330108,滨江区
        code = selected_item[0]
        name = selected_item[1]
        # 过滤掉省市一级行政区,但不包括港澳台,例如810000
        if code in Nationality.CODE_HONGKONG_MACAO_TAIWAN or '00' != code[-2:]:
            break
    return code, name


# 七三一算法
def calculate_check_num_731(id_no: str) -> str:
    def cyclic_generator():
        values = [7, 3, 1]
        while True:
            for value in values:
                yield value

    gen = cyclic_generator()
    the_sum = 0
    for i in range(len(id_no)):
        if (id_no[i]).isupper():
            the_sum += (ord(id_no[i]) - ord('A') + 10) * next(gen)
        elif (id_no[i]).isdigit():
            the_sum += int(id_no[i]) * next(gen)
        else:
            raise ValueError("输入证件号码有误,只能以数字和字母组合")
    return str(the_sum % 10)


def generate_chinese_name(length=3):
    # 常见中文姓氏列表
    surnames = ['赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱',
                '秦', '尤', '许',
                '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏',
                '水', '窦', '章',
                '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞',
                '任', '袁', '柳',
                '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝',
                '邬', '安', '常',
                '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和',
                '穆', '萧', '尹']
    # 常见中文名字列表
    names = ['伟', '刚', '勇', '毅', '俊', '峰', '强', '军', '平', '保', '东', '文', '辉', '力', '明', '永', '健', '世',
             '广', '志', '义',
             '兴', '良', '海', '山', '仁', '波', '宁', '贵', '福', '生', '龙', '元', '全', '国', '胜', '学', '祥', '才',
             '发', '武', '新',
             '利', '清', '飞', '彪', '宏', '德', '光', '天', '达', '安', '岩', '中', '茂', '进', '林', '有', '坚', '和',
             '彬', '柏', '义',
             '柏', '枝', '汝', '树', '正', '萱', '涵', '鹏', '煊', '昊', '泽', '煜', '祺', '振', '鹤', '轩', '哲', '瀚',
             '烁', '杉', '琪',
             '煜', '城', '昊', '天', '思', '聪', '展', '鹏', '笑', '愚', '志', '强', '炫', '明', '雪', '松', '思', '源',
             '智', '渊', '思',
             '淼', '晓', '啸', '天', '宇', '浩', '然', '文', '轩', '鹭', '洋', '振', '家', '乐', '韬', '晓', '博', '文',
             '昊', '哲', '来',
             '思', '翰', '瑞', '博', '昊', '强', '俊', '驰', '雨', '泽', '烨', '伟', '旭', '尧', '俊', '楠', '鸿', '涛',
             '浩', '宇', '瑾',
             '瑜', '皓', '轩', '擎', '宇', '君', '昊', '子', '轩', '睿', '思', '博', '鸿', '煊', '煜', '祺', '智', '宸',
             '正', '豪', '昊',
             '然', '明', '轩', '磊', '晟', '睿', '文', '博', '昊', '焱', '立', '果', '金', '鑫', '锦', '程', '嘉', '熙',
             '鹏', '君', '楠',
             '睿', '思', '哲', '宇', '瀚', '海', '天', '宇', '博', '瀚', '栋', '梁', '维', '新', '恒', '德', '圣', '杰',
             '俊', '楠', '鸿',
             '博', '弘', '文', '烨', '伟', '智', '渊', '思', '淼', '晓', '啸', '天', '宇', '浩', '然', '文', '轩', '鹭',
             '洋', '振', '家',
             '乐', '韬', '晓', '博', '文', '昊', '哲', '来', '思', '翰', '瑞', '博', '昊', '强', '俊', '驰', '金', '鑫',
             '锦', '程', '嘉',
             '熙', '鹏', '君', '楠', '睿', '思', '哲', '旭', '鹏', '达', '智', '强', '鹤', '轩', '绍', '元', '俊', '豪',
             '宇', '达', '俊',
             '驰', '炎', '彬', '越', '彬', '风', '华', '振', '国', '志', '豪', '星', '野', '七', '星', '天', '逸', '宏',
             '韬', '智', '渊',
             '思', '齐', '翰', '飞', '天', '赋', '骏', '桀', '爵', '璟', '桦', '鸿', '叶', '曜', '晖', '翰', '运', '翊',
             '运', '诚', '建',
             '义', '兴', '良', '飞', '白', '平', '保', '东', '文', '辉', '力', '明', '永', '健', '世', '广', '志', '义',
             '兴', '良', '海',
             '山', '仁', '波', '宁', '贵', '福', '生', '龙', '元', '全', '国', '胜', '学', '祥', '才', '发', '武', '新',
             '利', '清', '飞']
    name = random.choice(surnames)
    for i in range(length - 1):
        name += random.choice(names)
    return name


def word_to_pinyin(chinese_text: str) -> list[str]:
    """
    将中文文本转换为不带声调的拼音
    :param chinese_text: 中文文本字符串
    :return: (list[str])拼音列表，每个汉字的拼音为一个元素
    """
    from pypinyin import lazy_pinyin
    # 使用lazy_pinyin函数获取不带声调的拼音
    pinyin_without_tone = lazy_pinyin(chinese_text)
    return pinyin_without_tone


def generate_china_phone_number():
    """
    生成电话号码
    :return: 11位的字符串格式的电话号码
    """
    # 选择中国大陆手机号码常见的前两位
    prefix = random.choice(['13', '14', '15', '17', '18', '19'])
    # 生成后 9 位数字
    suffix = ''.join(random.choices('0123456789', k=9))
    # 拼接成完整的 11 位手机号码
    return prefix + suffix


def generate_email_address(username=None, domain=None, domains_list=None):
    """
    生成一个电子邮箱地址

    :param username: (str) 用户名
    :param domain: (str) 域名
    :param domains_list: (list[str]) 备选域名列表

    :return: （str）电子邮箱地址
    """
    # 默认域名列表
    if domains_list is None:
        domains_list = ['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'qq.com', '163.com', 'foxmail.com', '126.com','yeah.net',
                        'sina.com', 'sina.cn', 'aliyun.com','139.com','189.com']

    # 如果没有提供用户名，则生成一个随机用户名
    if username is None:
        username_length = random.randint(5, 12)
        username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))

    # 如果没有提供域名，则从域名列表中随机选择一个
    if domain is None:
        domain = random.choice(domains_list)

    # 返回生成的邮箱地址
    return f"{username}@{domain}"


def generate_china_fax_number(area_code):
    """
    生成传真号码
    :return: 区号-传真号格式的字符串
    """

    if area_code is None:
        area_code = '010'
    # 生成后 9 位数字
    suffix = ''.join(random.choices('0123456789', k=8))
    # 拼接成完整传真号码
    return area_code + '-' + suffix


# 个人证件父类
class IDNOGenerator(ABC):
    # 权重参数
    WEIGHT = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)
    # 详细地址信息,精确到街道和门牌号
    ADDRESSES = (
        "江南大道159号",
        "中关村大街58号",
        "张江路123号",
        "科技南路88号",
        "中山路99号",
        "人民南路四段789号",
        "解放大道1234号",
        "长安中路456号",
        "梅溪湖路7890号",
        "长江一路234号"
    )

    def __init__(self, name_ch: str = None, name_en: str = None, birthday: str = None,
                 gender: str = None, name_length: int = 3, sequence_code: str = None, begin_date: str = None):
        """
        个人证件父类,生成基本的信息。

        :param name_ch: (str)中文名
        :param name_en: (str)英文名
        :param birthday: (str)生日
        :param gender: (str)性别，男或者女
        :param name_length: (str)中文名长度,未输入中文名时自动生成用
        :param sequence_code: (str) 序列号,同时输入性别和序列号,以序列号为准
        :param begin_date: (str)证件有效期起始日期
        """
        # 证件类别
        self.__type = ' '
        # 姓名
        if name_ch is None:
            self.name_ch = generate_chinese_name(name_length)
        else:
            self.name_ch = name_ch
        if name_en is None:
            self.name_en = IDNOGenerator.get_english_name(self.name_ch)
        else:
            self.name_en = name_en
        # 生日
        if birthday is None:
            self.birthday = generate_date()
        else:
            try:
                # 判断字符串是不是合法日期
                birthday_time = datetime.datetime.strptime(birthday, "%Y%m%d")
                # 生日时间转换为生日日期
                self.birthday = birthday_time.strftime("%Y%m%d")
            except ValueError:
                raise ValueError(f"输入的生日格式不正确：{birthday}")
        # 顺序码
        if sequence_code is None:
            self.sequence_code = generate_sequence_code(0, 999)
        else:
            self.sequence_code = sequence_code
        # 性别
        # 判断性别入参是否有用,性别和序列号入参都不为空，以序列号为准
        flag = True
        if (gender is not None) and (sequence_code is not None):
            flag = False
        # 如果生成的顺序码和性别预期不一致,要重新生成
        if gender is not None and flag:
            if gender in ('男', '女'):
                self.gender = gender
            else:
                raise ValueError("性别值不合法")
            if ('男' == gender and int(self.sequence_code) % 2 == 0) or \
                    ('女' == gender and int(self.sequence_code) % 2 == 1):
                if int(self.sequence_code) == 999:
                    # +3
                    self.sequence_code = str(int(self.sequence_code) + 3).zfill(3)
                else:
                    # +1
                    self.sequence_code = str(int(self.sequence_code) + 1).zfill(3)
        # 通过序列号计算性别
        else:
            self.gender = get_gender(self.sequence_code)
        # 校验位
        self.last_num = ''
        # 证件号码
        self.No = ''
        # 起始日期
        self.begin_date = ''
        # 终止日期
        self.end_date = ''
        self.generate_valid_dates(begin_date)
        self.phone_number = generate_china_phone_number()
        self.email_address = generate_email_address()
        self.zipcode = None
        self.fax_number = generate_china_fax_number()

    def calculate_check_num(self):
        """计算最后一位校验位,ISO 7064:1983.MOD 11-2校验码算法。"""
        if 17 != len(self.No):
            raise ValueError("输入代码不是17位")
        sum_all = 0
        for i in range(0, 17):
            # 加权运算的和
            sum_all = int(self.No[i]) * IDNOGenerator.WEIGHT[i] + sum_all
        # 加权运算的和对11取余，12-余数的差再对11取余
        check_num = (12 - sum_all % 11) % 11
        # 校验位是10，则换成X
        if 10 == check_num:
            self.last_num = 'X'
        else:
            self.last_num = str(check_num)

    def generate_valid_dates(self, begin_date: str = None):
        """
        生成证件的起始日期和终止日期,起始日期在生日和当前日期之间,终止日期根据起始日期时年龄确定有效期。
        如果传入了初始日期，则允许证件到期日期在当前日期之前，因为存在已过期的证件，否则到期日期不允许超过今天。
        :param begin_date: (str)证件有效期起始日期
        """

        # 生日字符串转换为日期对象
        birthday_date = datetime.datetime.strptime(self.birthday, "%Y%m%d").date()
        if begin_date:
            try:
                # 将起始日期转换为日期对象,判断字符串是不是合法日期
                begin_date_obj = datetime.datetime.strptime(begin_date, "%Y%m%d").date()
                self.begin_date = begin_date
                end_date = self.generate_valid_dates_by_birthday(birthday=birthday_date, begin_date=begin_date_obj)
                if isinstance(end_date, datetime.date):
                    self.end_date = end_date.strftime("%Y%m%d")
                else:
                    self.end_date = end_date
            except ValueError:
                raise ValueError(f"输入的证件起始日期格式不正确：{begin_date}")
        else:
            while True:
                # 确定起始日期（生日到今天的闭区间内）
                days_between = (DATE_TODAY - birthday_date).days
                random_days = random.randint(0, days_between)
                begin_date_obj = birthday_date + datetime.timedelta(days=random_days)
                end_date = self.generate_valid_dates_by_birthday(birthday=birthday_date, begin_date=begin_date_obj)
                # print(end_date)
                # 如果未输入起始日期，则终止日期要在今天之后
                if isinstance(end_date, datetime.date) and end_date >= DATE_TODAY:
                    self.begin_date = begin_date_obj.strftime("%Y%m%d")
                    self.end_date = end_date.strftime("%Y%m%d")
                    break
                elif isinstance(end_date, str):
                    self.begin_date = begin_date_obj.strftime("%Y%m%d")
                    self.end_date = end_date
                    break

    @staticmethod
    def generate_valid_dates_by_birthday(birthday: datetime.date, begin_date: datetime.date) -> str | datetime.date:
        """
        根据生日和起始日期生成终止日期,起始日期在生日和当前日期之间,终止日期根据起始日期时年龄确定有效期。
        :param birthday: (datetime.date)生日,date对象
        :param begin_date: (datetime.date)证件有效期起始日期,date对象
        :returns:
            - 如果年龄大于等于 46 岁，返回固定字符串 "30001231"
            - 否则返回计算得到的终止日期(datetime.date)对象
        :rtype: str or datetime.date
        """
        # 计算从生日到起始日期的年龄（精确计算）
        age_at_begin_date = begin_date.year - birthday.year - (
                (begin_date.month, begin_date.day) < (birthday.month, birthday.day))
        # 根据领证年龄计算终止日期，身份证有效期的逻辑
        if age_at_begin_date < 16:
            valid_years = 5
        elif 16 <= age_at_begin_date < 26:
            valid_years = 10
        elif 26 <= age_at_begin_date < 46:
            valid_years = 20
        else:
            return "30001231"
        # 计算终止日期（处理闰年问题）
        try:
            end_date = begin_date.replace(year=begin_date.year + valid_years)
        except ValueError:
            # 如果起始日期是闰年的2月29日，调整为2月28日
            end_date = begin_date.replace(year=begin_date.year + valid_years, day=28)
        return end_date

    @abstractmethod
    def __str__(self):
        pass

    @classmethod
    def get_province_code(cls, ) -> str:
        """获取省级地区码"""
        list_province = [str(province) for province in Nationality.CODE_PROVINCE_DATA]
        index_province = random.randint(0, len(list_province) - 1)
        return str(list_province[index_province])

    @classmethod
    def calculate_check_num_cls(cls, str_number: str) -> str:
        """
            计算最后一位校验位,返回有校验位的证件号码
            适用证件类型,身份证和新版永居证
        """
        if 17 != len(str_number):
            raise ValueError("输入代码不是17位")
        sum_all = 0
        for i in range(0, 17):
            # 加权运算的和
            try:
                sum_all = int(str_number[i]) * cls.WEIGHT[i] + sum_all
            except Exception as e:
                raise ValueError(f"{e},输入的证件号码可能不是纯数字")
        # 加权运算的和对11取余，12-余数的差再对11取余
        check_num = (12 - sum_all % 11) % 11
        # 校验位是10，则换成X
        if 10 == check_num:
            last_num = 'X'
        else:
            last_num = str(check_num)
        return str_number + last_num

    @classmethod
    def get_english_name(cls, name_ch):
        """
        中文名转换成英文名，
        :param name_ch:(str, unicode编码)中文名
        :return:(str)大写英文字母
        """
        pinyin_list = word_to_pinyin(name_ch)
        if len(pinyin_list) > 2:
            pinyin_str = "".join(pinyin_list[0:-2]) + ", " + "".join(pinyin_list[-2:])
        else:
            pinyin_str = "".join(pinyin_list)
        return pinyin_str.upper()

    @classmethod
    def id_no_parse(cls, id_no):
        pass


# 居民身份证
class TypeSFZ(IDNOGenerator):
    ID_NO_LENGTH: int = 18

    def __init__(self, name_ch: str = None, name_en: str = None, birthday: str = None, gender: str = None,
                 sequence_code: str = None,
                 county_code: str = None, begin_date: str = None):
        """
        生成身份证基本信息。

        :param name_ch: (str)中文名
        :param name_en: (str)英文名
        :param birthday: (str)生日
        :param gender: (str)性别,男或者女
        :param sequence_code: (str) 序列号,同时输入性别和序列号,以序列号为准
        :param county_code: (str)到县一级的行政区代码
        :param begin_date: (str)证件有效期起始日期
        """
        super().__init__(name_ch, name_en, birthday, gender, sequence_code=sequence_code, begin_date=begin_date)
        self.type = IDType.ID_CARD.value
        self.province_name = None
        self.city_name = None
        self.county_code = None
        self.county_name = None
        # 随机生成
        if not county_code:
            self.county_code, self.county_name = get_province_city_county_code()
            self.get_province_city_county_name()
        else:
            # 新版行政区划，剔除市一级但是保留港澳台
            if (county_name := Nationality.administration_division.get(county_code)) \
                    and ((county_code in Nationality.CODE_HONGKONG_MACAO_TAIWAN)
                         or ('00' != county_code[-2:])):
                self.county_code = county_code
                self.county_name = county_name
                self.get_province_city_county_name()
            # 旧版行政区划，剔除市一级
            elif (county_name := Nationality.administration_division_old.get(county_code)) and '00' != county_code[-2:]:
                self.county_code = county_code
                self.county_name = county_name
                self.get_province_city_county_name(is_new=False)
            else:
                raise ValueError(f"输入的行政区代码{county_code}错误,需要输入县一级的行政区划代码")
        self.No = f"{self.county_code}{self.birthday}{self.sequence_code}"
        self.calculate_check_num()
        # 拼接上校验位
        self.No += self.last_num
        self.address = f"{self.province_name}{self.city_name}{self.county_name}{random.choice(self.ADDRESSES)}" \
            .replace('None', '')

    def __str__(self):
        return self.type

    def get_province_city_county_name(self, is_new=True):
        """
        获取省市县的名称
        :param is_new: (bool)True-新版行政区代码，False-旧版行政区代码
        """
        if is_new:
            self.province_name = Nationality.administration_division.get(self.county_code[0:2] + '0000')
            self.city_name = Nationality.administration_division.get(self.county_code[0:4] + '00')
            # 港澳台
            if self.province_name == self.city_name == self.county_name:
                self.city_name = None
                self.county_name = None
            # 存在有市无县的情况，市代县的情况，例如429004,仙桃市
            elif None is self.city_name:
                self.city_name = self.county_name
                self.county_name = None
        else:
            self.province_name = Nationality.administration_division_old.get(self.county_code[0:2] + '0000')
            self.city_name = Nationality.administration_division_old.get(self.county_code[0:4] + '00')

    @classmethod
    def id_no_parse(cls, id_no):
        """
        身份证号解析器,将身份证号码进行解码
        :param id_no:
        :return: id_info: (dict[str,str])
        """
        if len(id_no) == cls.ID_NO_LENGTH:
            # 创建实例
            # instance = cls()
            # 创建空的类对象,未进行初始化
            instance = cls.__new__(cls)
            instance.county_code = id_no[0:6]
            birthday = id_no[6:14]
            gender_number = id_no[16]
            if (county_name := Nationality.administration_division.get(instance.county_code)) \
                    and ((instance.county_code in Nationality.CODE_HONGKONG_MACAO_TAIWAN)
                         or ('00' != instance.county_code[-2:])):
                instance.county_name = county_name
                instance.get_province_city_county_name()
            # 旧版行政区划，剔除市一级
            elif (county_name := Nationality.administration_division_old.get(
                    instance.county_code)) and '00' != instance.county_code[-2:]:
                instance.county_name = county_name
                instance.get_province_city_county_name(is_new=False)
            else:
                raise ValueError(f"输入的证件号码{id_no}中行政区代码{instance.county_code}错误")
            gender = get_gender(gender_number)
            return {
                'birthday': birthday,
                'gender': gender,
                'county_code': instance.county_code,
                'province_name': instance.province_name,
                'city_name': instance.city_name,
                'county_name': instance.county_name,
                'address': f"{instance.province_name}{instance.city_name}{instance.county_name}"
                           f"{random.choice(cls.ADDRESSES)}".replace('None', ''),
            }
        else:
            raise ValueError(f"证件号码{id_no}长度错误,长度为:{len(id_no)}")


# 23新版外国人永久居留证
class TypeYJZ(IDNOGenerator):
    # 外国人永居证都是9为开头
    PREFIX_NUM = '9'
    # 号码长度
    ID_NO_LENGTH = 18

    def __init__(self, name_ch: str = None, name_en: str = None, province_name: str = None, national_code_3: str = None,
                 birthday: str = None, gender: str = None, name_length: int = 4, sequence_code: str = None,
                 begin_date: str = None):
        """
        初始化外国人永居证信息,此构造函数用于初始化外国人永久居留身份证信息对象。。

        :param name_ch: (str)中文姓名，默认为None。
        :param name_en: (str)英文姓名，默认为None。
        :param province_name: (str): 所属省份名称，默认为None。
        :param national_code_3: (str): 三位拉丁文国家代码,例如USA，默认为None。
        :param birthday: (str)出生日期，默认为None。
        :param gender: (str)性别，默认为None。
        :param name_length: (int)名字长度，默认为4。
        :param sequence_code: (str)顺序码,仅在依据旧版信息生成新版永居证号码时有用
        :param begin_date: (str)证件有效期起始日期
        """
        super().__init__(name_ch, name_en, birthday, gender, name_length, sequence_code, begin_date)
        self.type = IDType.FOREIGN_PERMANENT_RESIDENT2023.value
        # 地区码
        if province_name is None:
            self.province_code = IDNOGenerator.get_province_code()
        elif isinstance(province_name, str):
            try:
                reverse_index_province = {v: k for k, v in Nationality.CODE_PROVINCE_DATA.items()}
                self.province_code = str(reverse_index_province[province_name])
            except KeyError as e:
                raise KeyError(f"输入的省名无对应代码,请确认.错误信息:{e}")
        else:
            raise TypeError("输入省份名称不是字符串")
        # 国籍码
        if national_code_3 is None:
            list_nationality = [str(nationality) for nationality in Nationality.nationality_dict_by_number.keys()]
            self.nationality_number = random.choice(list_nationality)
        elif isinstance(national_code_3, str):
            try:
                national_code_3 = national_code_3.upper()
                self.nationality_number = Nationality.nationality_dict_by_code_3[national_code_3].number
                self.nationality_code = national_code_3
            except KeyError:
                raise KeyError(f"输入国籍代码{national_code_3}无对应代码,请确认")
        else:
            raise TypeError("输入的国家简称不是字符串")
        # 拉丁字母国籍码
        self.nationality_code = Nationality.nationality_dict_by_number.get(self.nationality_number).code_3
        # 中文简称
        self.nationality_name_ch = Nationality.nationality_dict_by_number.get(self.nationality_number).name_cn
        # 拼接成没校验位的
        self.No = f"{str(TypeYJZ.PREFIX_NUM)}{self.province_code}{self.nationality_number}{self.birthday}\
{self.sequence_code}"
        self.calculate_check_num()
        # 拼接上校验位
        self.No += self.last_num
        # 既往版本外国人永久居留证件号码关联项，前两位为市代码，后一位为顺序号
        self.related_item = None
        self.No_2017 = None

    # 依据新版永居证计算旧版永居证信息
    def get_old_foreign_permanent_resident_info(self):
        # 2017版的永居证
        yjz_old = TypeYJZ2017()
        self.No_2017 = yjz_old.No

    # 根据证件信息生成证件图像
    def generate_image(self, image_src: str = None, image_dest: str = None):
        from PIL import Image, ImageDraw, ImageFont
        # 打开png
        # image = Image.open(image_path).convert("RGBA")
        # 打开jpeg
        path_src = r"./resource"
        path_src = path.join(BASE_DIR, path_src)
        path_src = path.normpath(path_src)
        path_result = r"./result/"
        path_result = path.join(BASE_DIR, path_result)
        path_result = path.normpath(path_result)
        if image_src is None:
            image_src = path.join(path_src, "YJJ_IDInfo.jpg")
        if image_dest is None:
            image_dest = path_result
        try:
            image = Image.open(image_src).convert("RGBA")
        except FileNotFoundError:
            raise FileNotFoundError(f"输入的底稿文件不存在")
        color = (0, 0, 0)  # 文字颜色为黑色，RGB 格式
        type_face = "simhei.ttf"  # 字体为黑体
        font = ImageFont.truetype(type_face, 76)  # 字体类型和大小
        # 尺寸是2024 * 1280 ,一毫米对应24像素 ,每次上下端会留15个像素的边
        # 英文名 横向：35:428 竖向19:90
        # 中文名
        # 性别 横向：35:428 竖向23.9：54
        # 出生日期 横线 26:54 竖向：23.9：54
        # 国籍  横线：35:428  竖向31.7：54
        # 有效期 横线：35:428  竖向39.8：54
        # 证件号 横线：26:85.6  竖向44.6：54

        # 创建一个透明的图层用于绘制水印，也可以不创建，直接在原图上绘制
        watermark = Image.new('RGBA', image.size, (0, 0, 0, 0))
        draw_watermark = ImageDraw.Draw(watermark, 'RGBA')

        # 水印文本
        watermark_text = "OCR测试使用"
        # 水印颜色和透明度
        watermark_color = (127, 127, 127, 60)  # 中性灰，25% 透明度

        # 计算水印位置
        bbox = draw_watermark.textbbox((0, 0), watermark_text, font=font, align="left")
        position1 = (10, 10)  # 左上角
        position2 = (image.width - bbox[2] - 10, image.height - bbox[3] - 10)  # 右下角

        # 绘制水印
        draw_watermark.text(position1, watermark_text, font=font, fill=watermark_color)
        draw_watermark.text(position2, watermark_text, font=font, fill=watermark_color)
        # watermark.show()
        # 将水印图层与原图合并
        watermarked_image = Image.alpha_composite(image, watermark)

        # 继续绘制其他信息
        draw = ImageDraw.Draw(watermarked_image, "RGBA")
        # draw = ImageDraw.Draw(image)
        # 英文名 横向：35:428 竖向19:90 9P黑体
        draw.text((166, 230), self.name_en, font=font, fill=color)
        # 中文名 9P黑体
        draw.text((166, 345), self.name_ch, font=font, fill=color)
        # 性别 横向：35:428 竖向23.9：54 8P黑体
        font = ImageFont.truetype(type_face, 68)
        if self.gender == '男':
            gender = '男/M'
            head_portrait = Image.open(path.join(path_src, "male.png")).convert("RGBA")
        else:
            gender = '女/F'
            head_portrait = Image.open(path.join(path_src, "female.png")).convert("RGBA")
        draw.text((166, 560), gender, font=font, fill=color)
        # 出生日期 横线 26:85.6 竖向：23.9：54  8P黑体
        font = ImageFont.truetype(type_face, 68)
        draw.text((614, 560), f'{self.birthday[:4]}.{self.birthday[4:6]}.{self.birthday[6:8]}', font=font, fill=color)
        # 国籍 横线：35:428  竖向31.7：54  8P黑体
        font = ImageFont.truetype(type_face, 68)
        draw.text((166, 745), f'{self.nationality_name_ch}/{self.nationality_code}', font=font, fill=color)
        # 有效期 横线：35:428  竖向39.8：54  8P黑体
        font = ImageFont.truetype(type_face, 68)
        draw.text((166, 943), '2021.01.01 - 2031.01.01', font=font, fill=color)
        # 证件号码 横线：26:85.6  竖向44.6：54  12P OCR-B10 BT字体 纵坐标1057-1123
        font_path = path.join(path_src, 'OCR-B 10 BT.ttf')
        font = ImageFont.truetype(font_path, 102)
        draw.text((614, 1050), self.No, font=font, fill=color)
        # 写头像 头像大小为644*758
        # image.paste(head_portrait, (1314, 166,1929, 960)) #废弃原因，图像范围和图像大小不匹配
        watermarked_image.paste(head_portrait, (1314, 150,), head_portrait)
        # 展示原尺寸图像
        # watermarked_image.show()
        # 设置新的分辨率（例如，将图像缩小到原来的一半）
        new_width = int(watermarked_image.width / 2)
        new_height = int(watermarked_image.height / 2)

        # 调整图像大小
        resized_image = watermarked_image.resize((new_width, new_height), Image.Resampling.BILINEAR)
        # 压缩保存
        if not path.exists(image_dest):
            makedirs(image_dest)
        file_path = path.join(image_dest, '{}-{}.jpg'.format(self.name_ch, self.No))
        resized_image = resized_image.convert("RGB")
        # resized_image.show()
        resized_image.save(file_path, format='JPEG', optimize=True, quality=20)
        return path.abspath(file_path)

    def __str__(self):
        return (
            f"证件类型：{self.type}\n"
            f"证件号码：{self.No}\n"
            f"中文名：{self.name_ch}\n"
            f"英文名：{self.name_en}\n"
            f"生日：{self.birthday}\n"
            f"性别：{self.gender}\n"
            f"办理地区：{self.province_code}, 对应的省份：\
{Nationality.CODE_PROVINCE_DATA.get(int(self.province_code), '未知')}\n"
            f"国籍代码：{self.nationality_number}, 国籍：\
{self.nationality_code}, 国家简称:{self.nationality_name_ch}\n"
        )

    @classmethod
    def id_no_parse(cls, id_no):
        """
        证件号码解析器,将证件号码进行解码
        :param id_no:
        :return: id_info: (dict[str,str])
        """
        if len(id_no) == cls.ID_NO_LENGTH:
            province_code = id_no[1:3]
            nationality_number = id_no[3:6]
            birthday = id_no[6:14]
            gender_number = id_no[16]
            province_name = Nationality.CODE_PROVINCE_DATA.get(int(province_code), '未知')
            nationality_info = Nationality.nationality_dict_by_number.get(nationality_number, '未知')
            nationality_number = nationality_info.number
            nationality_name_ch = nationality_info.name_cn
            nationality_code = nationality_info.code_3
            gender = get_gender(gender_number)
            return {
                'province_code': province_code,
                'province_name': province_name,
                'nationality_number': nationality_number,
                'nationality_name_ch': nationality_name_ch,
                'nationality_code': nationality_code,
                'birthday': birthday,
                'gender': gender
            }
        else:
            raise ValueError(f"证件号码{id_no}长度错误len:{len(id_no)}")


# 2017旧版外国人永久居留证
class TypeYJZ2017(IDNOGenerator):
    ID_NO_LENGTH = 15

    def __init__(self, name_ch: str = None, name_en: str = None, national_abbreviation: str = None,
                 province_city_code: str = None, birthday: str = None, gender: str = None, sequence_code: str = None):
        """
        2017版永居证

        :param name_ch: (str)中文姓名，默认为None。
        :param name_en: (str)英文姓名，默认为None。
        :param national_abbreviation: (str)国家简写，三位拉丁国籍代码,例如CHN,默认为None。
        :param province_city_code: (str)省市代码
        :param birthday :(str)生日
        :param gender: (str)性别,输入性别时,随机生成顺序码
        :param sequence_code: (str)顺序码,同时输入性别和顺序码,以顺序码为准
        """
        super().__init__(name_ch=name_ch, name_en=name_en, birthday=birthday, gender=gender, name_length=4)
        self.type = IDType.FOREIGN_PERMANENT_RESIDENT2017.value
        if sequence_code:
            self.sequence_code = str(int(sequence_code) % 10)
        else:
            self.sequence_code = str(int(self.sequence_code) % 10)
        if national_abbreviation is None:
            list_nationality = [str(nationality) for nationality in Nationality.nationality_dict_by_code_3.keys()]
            # 三位拉丁国籍代码
            self.nationality_code = random.choice(list_nationality)
            # 国籍数字编号
            self.nationality_number = Nationality.nationality_dict_by_code_3[self.nationality_code].number
            # 中文简称
            self.nationality_name_ch = Nationality.nationality_dict_by_code_3[self.nationality_code].name_cn
        else:
            try:
                national_abbreviation = national_abbreviation.upper()
                dict_ret: Nationality.NationalityInfo = Nationality.nationality_dict_by_code_3[national_abbreviation]
                self.nationality_code = national_abbreviation
                # 国籍数字编号
                self.nationality_number = dict_ret.number
                # 中文简称
                self.nationality_name_ch = dict_ret.name_cn
            except KeyError as e:
                raise KeyError(f"输入的国籍代码：{e}无对应代码,请确认")
        if province_city_code is None:
            city_info = get_province_city_code()
            self.city_code = city_info[0]
            self.city_name = city_info[1]
        else:
            try:
                if len(province_city_code) != 4 or (province_city_code.endswith('00') and (province_city_code + '00')
                                                    not in Nationality.CODE_HONGKONG_MACAO_TAIWAN):
                    raise ValueError(f"输入的省市代码:{province_city_code}不合法,请确认")
                self.city_name = Nationality.administration_division[province_city_code + '00']
                self.city_code = province_city_code
            except KeyError as e:
                raise KeyError(f"输入的省市代码{province_city_code}无对应省市,请确认;发生错误的查询信息为{e}")
        self.No = self.nationality_code + self.city_code + self.birthday[2:] + self.sequence_code
        self.last_num = calculate_check_num_731(self.No)
        self.No = self.No + self.last_num
        province_name = Nationality.CODE_PROVINCE_DATA.get(int(self.city_code[0:2]))
        sequence_code = self.sequence_code.zfill(3)
        # 推算出的2023年版永居证号码
        self.No_2023 = TypeYJZ(name_ch=self.name_ch, name_en=self.name_en, province_name=province_name,
                               national_code_3=self.nationality_code, birthday=self.birthday,
                               gender=self.gender, sequence_code=sequence_code).No

    def __str__(self):
        return (
            f"证件类别：{self.type}\n"
            f"证件号码：{self.No}\n"
            f"中文名：{self.name_ch}\n"
            f"英文名：{self.name_en}\n"
            f"生日：{self.birthday}\n"
            f"性别：{self.gender}\n"
            f"办理地区：{self.city_code},对应地区名称：{self.city_name},\
对应省份={Nationality.administration_division[self.city_code[0:2] + '0000']}\n"
            f"国籍：{self.nationality_code},国籍代码：{self.nationality_number},国家简称：{self.nationality_name_ch}\n"
        )

    @classmethod
    def id_no_parse(cls, id_no):
        """
        旧版永居证号码解析器,将证件号码进行解码
        :param id_no:
        :return: id_info: (dict[str,str])
        """
        if len(id_no) == cls.ID_NO_LENGTH:
            nationality_code = id_no[0:3]
            province_city_code = id_no[3:7]
            province_code = province_city_code[0:2]
            birthday = '19' + id_no[7:13]
            gender_number = id_no[13]
            sequence_code = gender_number.zfill(3)

            city_name = Nationality.administration_division[province_city_code + '00']
            if province_code not in Nationality.CODE_HONGKONG_MACAO_TAIWAN:
                province_name = Nationality.administration_division.get(province_code + '0000', '')
            else:
                province_name = ''
            province_city_name = province_name + city_name
            nationality_info = Nationality.nationality_dict_by_code_3[nationality_code]
            nationality_number = nationality_info.number
            nationality_info = Nationality.nationality_dict_by_number.get(nationality_number, '未知')
            nationality_name_ch = nationality_info.name_cn
            gender = get_gender(gender_number)
            province_name = Nationality.CODE_PROVINCE_DATA.get(int(province_code))
            ID_No_other = TypeYJZ(name_ch=None, name_en=None, province_name=province_name,
                                  national_code_3=nationality_code, birthday=birthday,
                                  gender=gender, sequence_code=sequence_code).No
            return {
                'birthday': birthday,
                'gender': gender,
                'province_city_code': province_city_code,
                'province_city_name': province_city_name,
                'nationality_number': nationality_number,
                'nationality_name_ch': nationality_name_ch,
                'nationality_code': nationality_code,
                'ID_No_other': ID_No_other,
            }
        else:
            raise ValueError(f"证件号码{id_no}长度错误len:{len(id_no)}")


# 港澳台居住证
class TypeGATJZZ(IDNOGenerator):
    ID_NO_LENGTH = 18

    def __init__(self, id_type: str, name_ch: str = None, name_en: str = None, birthday: str = None,
                 gender: str = None, begin_date: str = None):
        super().__init__(name_ch=name_ch, name_en=name_en, birthday=birthday, gender=gender, begin_date=begin_date)
        self.__kind = IDType.GAT_PERMANENT_RESIDENT.value
        self.__type = id_type
        if id_type == GATPermanentResident.HKG_PERMANENT_RESIDENT.value:
            self.region_code = '810000'
            self.province_name = '香港'
        elif id_type == GATPermanentResident.MAC_PERMANENT_RESIDENT.value:
            self.region_code = '820000'
            self.province_name = '澳门'
        elif id_type == GATPermanentResident.CTN_PERMANENT_RESIDENT.value:
            self.region_code = '830000'
            self.province_name = '台湾'
        else:
            raise ValueError("输入证件类型错误,输入证件类型不为港澳台居住证")
        self.No = f"{str(self.region_code)}{self.birthday}{self.sequence_code}"
        self.calculate_check_num()
        # 拼接上校验位
        self.No += self.last_num

    def __str__(self):
        return (
            f"证件类别：{self.__kind}\n"
            f"证件类型：{self.__type}\n"
            f"证件号码：{self.No}\n"
            f"生日：{self.birthday}\n"
            f"性别：{self.gender}\n"
            f"地区码：{self.region_code}, 地区：{self.province_name}\n"
        )

    @classmethod
    def id_no_parse(cls, id_no):
        """
        港澳台居住证解析器,将港澳台居住证号码进行解码
        :param id_no:
        :return: id_info: (dict[str,str])
        """
        if len(id_no) == cls.ID_NO_LENGTH:
            region_code = id_no[0:6]
            birthday = id_no[6:14]
            gender_number = id_no[16]
            if region_code == '810000':
                id_type = GATPermanentResident.HKG_PERMANENT_RESIDENT.value
                province_name = '香港'
            elif region_code == '820000':
                id_type = GATPermanentResident.MAC_PERMANENT_RESIDENT.value
                province_name = '澳门'
            elif region_code == '830000':
                id_type = GATPermanentResident.CTN_PERMANENT_RESIDENT.value
                province_name = '台湾'
            gender = get_gender(gender_number)

            return {
                'id_type': id_type,
                'birthday': birthday,
                'gender': gender,
                'region_code': region_code,
                'province_name': province_name,
            }
        else:
            raise ValueError(f"证件号码{id_no}长度错误,长度为:{len(id_no)}")


# 港澳通行证
class TypeGATXZ(IDNOGenerator):
    def __init__(self, id_type: str):
        super().__init__()
        self.__kind = IDType.HKG_MAC_PERMIT.value
        self.type = id_type
        if id_type == HkgMacPermit.HKG_PERMIT.value:
            self.PREFIX_CODE = 'H'
        elif id_type == HkgMacPermit.MAC_PERMIT.value:
            self.PREFIX_CODE = 'M'
        else:
            raise ValueError("输入证件类型错误,输入证件类型不为香港或者澳门通行证")
        # 前半段
        self.sequence_code_forepart = str(random.randint(0, 99999)).zfill(5)
        # 证件号码
        self.No = f"{self.PREFIX_CODE}{self.sequence_code_forepart}{self.sequence_code}"

    # 字母加上八位数字
    def __str__(self):
        return (
            f"证件类别：{self.__kind}\n"
            f"证件类型：{self.type}\n"
            f"证件号码：{self.No}\n"
            f"生日：{self.birthday}\n"
            f"性别：{self.gender}\n"
        )


# 台湾通行证
class TypeTWTXZ(IDNOGenerator):
    def __init__(self):
        super(TypeTWTXZ, self).__init__()
        # 台湾居民来往内地通行证
        self.type = IDType.CTN_PERMIT.value
        # 前半段
        self.sequence_code_forepart = str(random.randint(0, 99999)).zfill(5)
        # 证件号码
        self.No = f"{self.sequence_code_forepart}{self.sequence_code}"

    # 八位数字
    def __str__(self):
        return (
            f"证件类型：{self.type}\n"
            f"证件号码：{self.No}\n"
            f"生日：{self.birthday}\n"
            f"性别：{self.gender}\n"
        )


if __name__ == '__main__':
    # wgr = TypeYJZ(gender='男')
    # wgr = TypeYJZ()
    # wgr.generate_image()
    # print(wgr)
    # HKG_card = TypeGATJZZ(GATPermanentResident.HKG_PERMANENT_RESIDENT.value)
    # print(HKG_card)
    # MAC_card = TypeGATJZZ(IDType.MAC_PERMANENT_RESIDENT)
    # print(MAC_card)
    # HKG_pass_card = TypeGATXZ(IDType.HKG_PERMIT)
    # print(HKG_pass_card)
    # MAC_pass_card = TypeGATXZ(IDType.MAC_PERMIT)
    # print(MAC_pass_card)
    # CTN_pass_card = TypeTWTXZ()
    # print(CTN_pass_card)
    # wgr1 = TypeYJZ(province_name="北京", national_abbreviation="MAC", birthday="19961207", gender="男")
    # print(wgr1)
    # abc = get_province_city_code()
    # c = generate_sequence_code(0, 999)
    # d = TypeYJZ2017()
    # print(d)
    # name = generate_chinese_name()
    # pinyin = word_to_pinyin(name)
    # print(pinyin)
    # print(IDNOGenerator.calculate_check_num_cls('11011519980811051'))
    a = TypeSFZ(birthday='20000229', begin_date='20200229')
    pass
