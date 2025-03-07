# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['Gui.py'],
             pathex=['F:\\GitHub\\my_python\\PRC_FOREIGN_PERMANENT_RESIDENT_ID_CARD'],
             binaries=[],
             datas=[('.\\resource\\','.\\resource\\')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)

exe = EXE(pyz,
          a.scripts,
          a.binaries,
          a.zipfiles,
          a.datas,  
          [],
          name='永居证生成器',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          upx_exclude=[],
          runtime_tmpdir=None,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
		  version='app_version_info.txt',
          entitlements_file=None,
		  icon='ID.ico',)
