"""
# @Time     : 2026/6/11 17:29
# @Author   : wanggz38530
# @File     : YamlParse.py
# @Software : PRC_FOREIGN_PERMANENT_RESIDENT_ID_CARD
# @Purpose  :YAML 解析模块
            提供对机构开户 YAML 配置文件的解析功能，
            将 YAML 结构转换为层级分明的 Python 数据类型。
"""


from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import yaml
from pathlib import Path
import json


# ── 自定义数据类型 ──────────────────────────────────────────────
@dataclass
class OrganrelatedInfo:
    """各个关联人的字段信息，包含一个类型标识和一组字段映射。"""

    organrelated_type: str | None
    """该行的类型标识，如 '客户主体', '经办人' 等。对应 YAML 中的 organrelated_type 值。"""

    field_mapping: dict
    """该行包含的字段映射列表。"""


@dataclass
class SheetInfo:
    """Sheet 页信息，包含 sheet 名称和其下的所有数据行。"""

    sheet_name: str
    """Sheet 页名称。"""

    organrelated_list: list[OrganrelatedInfo]
    """该 sheet 下的关联人列表。"""


@dataclass
class YamlConfig:
    """YAML 配置文件的完整解析结果。"""

    sheets: list[SheetInfo]
    """所有 sheet 页的列表。"""


def load_yaml_file(file_path: str | Path) -> dict:
    """
    加载并解析 YAML 文件。

    :param file_path: YAML 文件路径
    :return: 解析后的字典数据
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def parse_organrelated_info(data: dict) -> OrganrelatedInfo:
    """
    解析单个关联人信息。

    :param data: 包含关联人信息的字典
    :return: OrganrelatedInfo 对象
    """
    organrelated_type: str | None = data.get('organrelated_type')
    field_mapping: dict = {}

    for key, value in data.items():
        if key != 'organrelated_type':
            # 在yaml文件中未加引号的No会被解析为False
            if 'no' in key and value is False:
                value = 'No'
            field_mapping[key] = value

    return OrganrelatedInfo(
        organrelated_type=organrelated_type,
        field_mapping=field_mapping
    )


def parse_sheet(sheet_data: list) -> SheetInfo:
    """
    解析单个 sheet 页的数据。

    :param sheet_data: sheet 页的数据列表
    :return: SheetInfo 对象
    """
    sheet_name: str = ""
    organrelated_list: list[OrganrelatedInfo] = []

    for item in sheet_data:
        if not isinstance(item, dict):
            continue

        # 检查是否为 sheet_name
        if 'sheet_name' in item:
            sheet_name = item['sheet_name']
        # 检查是否为 organrelated 信息
        elif 'organrelated_type' in item or any(
            k != 'sheet_name' for k in item.keys()
        ):
            organrelated_info = parse_organrelated_info(item)
            organrelated_list.append(organrelated_info)

    return SheetInfo(
        sheet_name=sheet_name,
        organrelated_list=organrelated_list
    )


def parse_yaml_config(data: dict) -> YamlConfig:
    """
    解析完整的 YAML 配置数据。

    :param data: YAML 解析后的字典数据
    :return: YamlConfig 对象
    """
    sheets: list[SheetInfo] = []

    sheets_data = data.get('sheets', [])

    for sheet_item in sheets_data:
        if not isinstance(sheet_item, dict):
            continue

        sheet_list = sheet_item.get('sheet', [])

        if isinstance(sheet_list, list):
            sheet_info = parse_sheet(sheet_list)
            sheets.append(sheet_info)

    return YamlConfig(sheets=sheets)


def config_to_dict(config: YamlConfig) -> dict:
    """
    将 YamlConfig 对象转换为字典格式（用于 JSON 序列化）。

    :param config: YamlConfig 对象
    :return: 字典格式的配置数据
    """
    return {
        'sheets': [
            {
                'sheet_name': sheet.sheet_name,
                'organrelated_list': [
                    {
                        'organrelated_type': org.organrelated_type,
                        'field_mapping': org.field_mapping
                    }
                    for org in sheet.organrelated_list
                ]
            }
            for sheet in config.sheets
        ]
    }


def main(file_path: str | Path) -> None:
    """
    主函数：解析 YAML 文件并打印 JSON 结果。

    :param file_path: YAML 文件路径
    """
    data = load_yaml_file(file_path)
    config = parse_yaml_config(data)
    result_dict = config_to_dict(config)
    print(json.dumps(result_dict, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    yaml_file_path = Path(__file__).parent / 'resource' / 'organ_open.yaml'
    main(yaml_file_path)