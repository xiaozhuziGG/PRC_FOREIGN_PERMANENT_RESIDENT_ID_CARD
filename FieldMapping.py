# -*- coding: utf-8 -*-
"""
证件字段映射字典
提供证件类型、性别等枚举值到外部系统编码的映射关系
"""

from IdCardGenerator import IDKind

# 证件类型 → CSDC 证件类型编码
ID_KIND_TO_CSDC_ID_KIND: dict[str, str] = {
    IDKind.ID_CARD.value: '01',
    IDKind.FOREIGN_PERMANENT_RESIDENT2017.value: 'I',
    IDKind.FOREIGN_PERMANENT_RESIDENT2023.value: '09',
    IDKind.HKG_MAC_PERMIT.value: '07',
    IDKind.CTN_PERMIT.value: '08',
    IDKind.GAT_PERMANENT_RESIDENT.value: '15',
    IDKind.BUSINESS_LICENSE.value: '02',
}

# 性别 → CSDC 性别编码
GENDER_TO_CSDC_GENDER: dict[str, str] = {
    '男': '1',
    '女': '2',
    '非自然人': '3',
}

# 性别 → BOP 性别编码
GENDER_TO_BOP_GENDER: dict[str, str] = {
    '男': '0',
    '女': '1',
    '非自然人': '2',
}


# 证件类型 → BOP 证件类型编码
ID_KIND_TO_BOP_ID_KIND: dict[str, str] = {
    IDKind.ID_CARD.value:'0',
    IDKind.FOREIGN_PERMANENT_RESIDENT2017.value:'I',
    IDKind.FOREIGN_PERMANENT_RESIDENT2023.value:'I',
    IDKind.HKG_MAC_PERMIT.value:'G',
    IDKind.CTN_PERMIT.value:'H',
    IDKind.GAT_PERMANENT_RESIDENT.value:'l',
    IDKind.BUSINESS_LICENSE.value:'2',        
}