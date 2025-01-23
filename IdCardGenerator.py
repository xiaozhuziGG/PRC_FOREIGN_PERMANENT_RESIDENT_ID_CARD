"""
# @Time     : 2024/2/27 14:31
# @Author   : wanggz38530
# @File     : 18位外国人永久居留证.py
# @Software :
"""
# -*- coding: utf-8 -*-
# !/usr/bin/python3.6/
import random
import datetime
from abc import abstractmethod
from enum import Enum
import Nationality
from os import path, makedirs


class IDType(Enum):
    """证件类型枚举"""
    ID_CARD = "居民身份证0"
    BUSINESS_LICENSE = "营业执照0"
    FOREIGN_PERMANENT_RESIDENT2023 = "2023版外国人永久居留证"
    FOREIGN_PERMANENT_RESIDENT2017 = "2017版外国人永久居留证"
    GAT_PERMANENT_RESIDENT = "港澳台居民居住证"
    CTN_PERMIT = "台湾居民来往内地通行证"
    HKG_MAC_PERMIT = "港澳居民来往内地通行证"


class GATPermanentResident(Enum):
    """港澳台居民居住证"""
    HKG_PERMANENT_RESIDENT = "香港居民居住证"
    MAC_PERMANENT_RESIDENT = "澳门居民居住证"
    CTN_PERMANENT_RESIDENT = "台湾居民居住证"


class HkgMacPermit(Enum):
    """港澳居民来往内地通行证"""
    HKG_PERMIT = "香港居民来往内地通行证"
    MAC_PERMIT = "澳门居民来往内地通行证"


def get_sex(num: str) -> str:
    """校验性别"""
    return '女' if int(num) % 2 == 0 else '男'


def generate_date():
    """生成随机日期,1920-01-01到2020-01-01"""
    # 设置日期范围
    start_date = datetime.date(1920, 1, 1)
    end_date = datetime.date(2020, 1, 1)

    # 计算日期范围的天数
    days_between = (end_date - start_date).days

    # 生成随机天数并加上起始日期
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
    items = list(Nationality.administrative_division.items())
    """过滤掉省级行政区"""
    while True:
        selected_item = random.sample(items, 1)[0]
        name = selected_item[1]
        if '省' not in name or '台湾省' == name:
            # 行政区划格式为 330108,滨江区
            city_code = selected_item[0][0:4]
            break
    city_name = Nationality.administrative_division[city_code + '00']
    return city_code, city_name


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
            return "输入证件号码有误，只能以数字和字母组合"
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


def word_to_pinyin(chinese_text: str) -> list:
    from pypinyin import lazy_pinyin
    # 使用lazy_pinyin函数获取不带声调的拼音
    pinyin_without_tone = lazy_pinyin(chinese_text)
    return pinyin_without_tone


# 个人证件父类
class IDNOGenerator(object):
    # 权重参数
    WEIGHT = (7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2)

    def __init__(self, birthday: str = None, gender: str = None, name_length: int = 3, sequence_code: str = None):
        """
        birthday :生日
        gender :性别，男或者女
        """
        # 证件类别
        self.__type = ' '
        # 姓名
        self.name_CH = generate_chinese_name(name_length)
        # 生日
        if birthday is None:
            self.birthday = generate_date()
        else:
            try:
                # 判断字符串是不是合法日期
                birthday_time = datetime.datetime.strptime(birthday, "%Y%m%d")
                # 生日时间转换为生日日期
                self.birthday = birthday_time.date().strftime("%Y%m%d")
            except ValueError:
                raise "输入的生日格式不正确"
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
            self.gender = get_sex(self.sequence_code)
        # 校验位
        self.last_num = ' '
        # 证件号码
        self.No = ' '
        # 起始日期
        self.begin_date = ' '
        # 终止日期
        self.end_date = ' '

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
        """计算最后一位校验位,返回有校验位的证件号码"""
        if 17 != len(str_number):
            raise ValueError("输入代码不是17位")
        sum_all = 0
        for i in range(0, 17):
            # 加权运算的和
            sum_all = int(str_number[i]) * cls.WEIGHT[i] + sum_all
        # 加权运算的和对11取余，12-余数的差再对11取余
        check_num = (12 - sum_all % 11) % 11
        # 校验位是10，则换成X
        if 10 == check_num:
            last_num = 'X'
        else:
            last_num = str(check_num)
        return str_number + last_num


# 居民身份证
class TypeSFZ(IDNOGenerator):
    def __str__(self):
        return self.type

    def print_info(self):
        pass

    def __init__(self):
        super().__init__()
        self.type = "居民身份证"
        self.province_code = IDNOGenerator.get_province_code()


# 23新版外国人永久居留证
class TypeYJZ(IDNOGenerator):
    # 外国人永居证都是9为开头
    PREFIX_NUM = '9'

    def __init__(self, province_name: str = None, national_code_3: str = None, birthday: str = None,
                 gender: str = None, name_length: int = 4):
        """
        初始化外国人信息类。

        参数:
        - province_name (str): 省份名称。默认为None。
        - national_abbreviation (str): 三位拉丁文国家缩写。默认为None。
        - birthday (str): 出生日期。默认为None。
        - gender (str): 性别，支持输入男或女。默认为None。
        - name_length (int): 名字长度。默认为4个汉字。

        该构造函数允许创建时指定个人信息的各个属性，如省份、国家缩写、出生日期和性别等。
        """
        super().__init__(birthday, gender, name_length)
        self.type = IDType.FOREIGN_PERMANENT_RESIDENT2023.value
        # 英文名
        self.name_EN = TypeYJZ.get_english_name(self.name_CH)
        # 地区码
        if province_name is None:
            self.province_code = IDNOGenerator.get_province_code()
        elif isinstance(province_name, str):
            try:
                reverse_index_province = {v: k for k, v in Nationality.CODE_PROVINCE_DATA.items()}
                self.province_code = str(reverse_index_province[province_name])
            except KeyError:
                print("输入的省名无对应代码 请确认")
        else:
            raise TypeError("输入省份名称不是字符串")
        # 国籍码
        if national_code_3 is None:
            list_nationality = [str(nationality) for nationality in Nationality.nationality_dict_by_number.keys()]
            self.nationality_number = random.choice(list_nationality)
        elif isinstance(national_code_3, str):
            try:
                self.nationality_number = Nationality.nationality_dict_by_code_3[national_code_3]
                self.nationality_code = national_code_3
            except KeyError:
                print("输入的国家简称无对应代码,请确认")
        else:
            raise TypeError("输入的国家简称不是字符串")
        # 拉丁字母国籍码
        self.nationality_code = Nationality.nationality_dict_by_number.get(self.nationality_number).code_3
        # 中文简称
        self.nationality_name_cn = Nationality.nationality_dict_by_number.get(self.nationality_number).name_cn
        # 拼接成没校验位的
        self.No = f"{str(TypeYJZ.PREFIX_NUM)}{self.province_code}{self.nationality_number}{self.birthday}\
{self.sequence_code}"
        self.calculate_check_num()
        # 拼接上校验位
        self.No += self.last_num
        # 既往版本外国人永久居留证件号码关联项，前两位为市代，后一位为顺序号
        self.related_item = None
        self.NO_2017 = None

    # 依据新版永居证计算旧版永居证信息
    def get_old_foreign_permanent_resident_info(self):
        # 2017版的永居证
        yjz_old = TypeYJZ2017()
        self.NO_2017 = yjz_old.NO

    # 根据证件信息生成证件图像
    def generate_image(self, image_src: str = None, image_dest: str = None):
        from PIL import Image, ImageDraw, ImageFont
        # 打开png
        # image = Image.open(image_path).convert("RGBA")
        # 打开jpeg
        path_src = r"./resource"
        path_result = r"./result/"
        if image_src is None:
            image_src = path.join(path_src, "YJJ_IDInfo.jpg")
        if image_dest is None:
            image_dest = path_result
        try:
            image = Image.open(image_src).convert("RGB")
        except FileNotFoundError:
            print("底稿文件不存在,渲染方法退出")
            return
        color = (0, 0, 0)  # 文字颜色，RGB 格式
        # 字体为黑体
        type_face = "simhei.ttf"
        # type_face = "msyhl.ttc"
        font = ImageFont.truetype(type_face, 76)  # 字体类型和大小
        # 尺寸是2024 * 1280 ,一毫米对应24像素 ,每次上下端会留15个像素的边
        # 英文名 横向：35:428 竖向19:90
        # 中文名
        # 性别 横向：35:428 竖向23.9：54
        # 出生日期 横线 26:54 竖向：23.9：54
        # 国籍  横线：35:428  竖向31.7：54
        # 有效期 横线：35:428  竖向39.8：54
        # 证件号 横线：26:85.6  竖向44.6：54
        draw = ImageDraw.Draw(image)
        # 英文名 横向：35:428 竖向19:90 9P黑体
        draw.text((166, 230), self.name_EN, font=font, fill=color)
        # 中文名 9P黑体
        draw.text((166, 345), self.name_CH, font=font, fill=color)
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
        draw.text((166, 745), f'{self.nationality_name_cn}/{self.nationality_code}', font=font, fill=color)
        # 有效期 横线：35:428  竖向39.8：54  8P黑体
        font = ImageFont.truetype(type_face, 68)
        draw.text((166, 943), '2021.01.01 - 2031.01.01', font=font, fill=color)
        # 证件号码 横线：26:85.6  竖向44.6：54  12P OCR-B10 BT字体 纵坐标1057-1123
        font_path = path.join(path_src, 'OCR-B 10 BT.ttf')
        font = ImageFont.truetype(font_path, 102)
        draw.text((614, 1050), self.No, font=font, fill=color)
        # 写头像 头像大小为644*758
        # image.paste(head_portrait, (1314, 166,1929, 960)) #废弃原因，图像范围和图像大小不匹配
        image.paste(head_portrait, (1314, 150,), head_portrait)
        # 展示图像
        # image.show()
        # 设置新的分辨率（例如，将图像缩小到原来的一半）
        new_width = int(image.width / 2)
        new_height = int(image.height / 2)

        # 调整图像大小
        resized_image = image.resize((new_width, new_height), Image.Resampling.BILINEAR)
        # 压缩保存
        if not path.exists(image_dest):
            makedirs(image_dest)
        resized_image.save(path.join(image_dest, '{}-{}.jpg'.format(self.name_CH, self.No)), format='JPEG',
                           optimize=True, quality=20)

    @classmethod
    # 中文名转换成英文名
    def get_english_name(cls, name_ch):
        pinyin_list = word_to_pinyin(name_ch)
        if len(pinyin_list) > 2:
            pinyin_str = "".join(pinyin_list[0:-2]) + ", " + "".join(pinyin_list[-2:])
        else:
            pinyin_str = "".join(pinyin_list)
        return pinyin_str.upper()

    def __str__(self):
        return (
            f"证件类型：{self.type}\n"
            f"证件号码：{self.No}\n"
            f"中文名：{self.name_CH}\n"
            f"英文名：{self.name_EN}\n"
            f"生日：{self.birthday}\n"
            f"性别：{self.gender}\n"
            f"办理地区：{self.province_code}, 对应的省份：\
{Nationality.CODE_PROVINCE_DATA.get(int(self.province_code), '未知')}\n"
            f"国籍代码：{self.nationality_number}, 国籍：\
{self.nationality_code}, 国家简称:{self.nationality_name_cn}\n"
        )


# 17旧版外国人永久居留证
class TypeYJZ2017(IDNOGenerator):
    def __init__(self, national_abbreviation: str = None, province_city_code: str = None,
                 birthday: str = None, gender: str = None, sequence_code: str = None):
        """
        national_abbreviation :三位拉丁国籍代码
        province_city_code :省市代码
        birthday :生日
        gender :性别,输入性别时,随机生成顺序码
        sequence_code :顺序码,同时输入性别和顺序码,以顺序码为准
        """
        super().__init__(birthday, gender, sequence_code=sequence_code)
        self.type = IDType.FOREIGN_PERMANENT_RESIDENT2017.value
        self.sequence_code = str(int(self.sequence_code) % 10)
        if national_abbreviation is None:
            list_nationality = [str(nationality) for nationality in Nationality.nationality_dict_by_code_3.keys()]
            # 三位拉丁国籍代码
            self.nationality_code = random.choice(list_nationality)
            # 国籍数字编号
            self.nationality_number = Nationality.nationality_dict_by_code_3[self.nationality_code].number
            # 中文简称
            self.name_cn = Nationality.nationality_dict_by_code_3[self.nationality_code].name_cn
        else:
            try:
                dict_ret = Nationality.nationality_dict_by_code_3[national_abbreviation]
                self.nationality_code = national_abbreviation
                # 国籍数字编号
                self.nationality_number = dict_ret.number
                # 中文简称
                self.name_cn = dict_ret.nationality_name_cn
            except KeyError:
                print("输入的国家简称无对应代码,请确认")
        if province_city_code is None:
            city_info = get_province_city_code()
            self.city_code = city_info[0]
            self.city_name = city_info[1]
        else:
            try:
                self.city_name = Nationality.administrative_division[province_city_code + '00']
                self.city_code = province_city_code
            except KeyError:
                print("输入的省市代码无对应省份,请确认")
        self.NO = self.nationality_code + self.city_code + self.birthday[2:] + self.sequence_code
        self.last_num = calculate_check_num_731(self.NO)
        self.NO = self.NO + self.last_num

    def __str__(self):
        return (
            f"证件类别：{self.type}\n"
            f"证件号码：{self.NO}\n"
            f"生日：{self.birthday}\n"
            f"性别：{self.gender}\n"
            f"办理地区：{self.city_code},对应地区名称：{self.city_name},\
对应省份={Nationality.administrative_division[self.city_code[0:2] + '0000']}\n"
            f"国籍：{self.nationality_code},国籍代码：{self.nationality_number},国家简称：{self.name_cn}\n"
        )


# 港澳台居住证
class TypeGATJZZ(IDNOGenerator):
    def __str__(self):
        return (
            f"证件类别：{self.__kind}\n"
            f"证件类型：{self.__type}\n"
            f"证件号码：{self.No}\n"
            f"生日：{self.birthday}\n"
            f"性别：{self.gender}\n"
            f"地区码：{self.region_code}, 地区：{self.province_name}\n"
        )

    def __init__(self, id_type: str):
        super().__init__()
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
            raise "输入证件类型错误,输入证件类型不为港澳台居住证"
        self.No = f"{str(self.region_code)}{self.birthday}{self.sequence_code}"
        self.calculate_check_num()
        # 拼接上校验位
        self.No += self.last_num


# 港澳通行证
class TypeGATXZ(IDNOGenerator):
    def __init__(self, id_type: IDType):
        super().__init__()
        self.__kind = id_type.HKG_MAC_PERMIT.value
        self.type = id_type.value
        if id_type == HkgMacPermit.HKG_PERMIT:
            self.PREFIX_CODE = 'H'
        elif id_type == HkgMacPermit.MAC_PERMIT:
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
    wgr = TypeYJZ()
    # wgr.generate_image()
    print(wgr)
    HKG_card = TypeGATJZZ(GATPermanentResident.HKG_PERMANENT_RESIDENT)
    print(HKG_card)
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
    d = TypeYJZ2017()
    print(d)
    # name = generate_chinese_name()
    # pinyin = word_to_pinyin(name)
    # print(pinyin)
