# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Python Backend (python_backend.exe)
import os, sys

block_cipher = None

# 收集所有子目录
added_files = [
    ('services', 'services'),
    ('models', 'models'),
    ('config', 'config'),
]
# 加入 .env 示例（运行时由启动器覆写）
if os.path.exists('.env'):
    added_files.append(('.env', '.'))

a = Analysis(
    ['app.py'],
    pathex=['.'],
    binaries=[],
    datas=added_files,
    hiddenimports=[
        'flask',
        'flask_cors',
        'flask_sqlalchemy',
        'sqlalchemy',
        'sqlalchemy.dialects.mysql',
        'sqlalchemy.dialects.sqlite',
        'pymysql',
        'loguru',
        'dotenv',
        'pandas',
        'numpy',
        'scipy',
        'sklearn',
        'sklearn.utils._cython_blas',
        'sklearn.neighbors._partition_nodes',
        'apscheduler',
        'apscheduler.schedulers.background',
        'apscheduler.executors.pool',
        'apscheduler.jobstores.sqlalchemy',
        'requests',
        'bs4',
        'lxml',
        'lxml.etree',
        'PIL',
        'marshmallow',
        'email_validator',
        'validators',
        'fake_useragent',
        'fuzzywuzzy',
        'Levenshtein',
        'psutil',
        'httpx',
        'cryptography',
        'services.crawler_service',
        'services.advanced_crawler_service',
        'services.equipment_service',
        'services.data_analysis_service',
        'services.crawler_config_service',
        'services.crawler_monitor_service',
        'services.crawler_queue_service',
        'services.data_validation_service',
        'models.equipment',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['redis', 'matplotlib', 'seaborn'],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='python_backend',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,  # 无控制台窗口
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='python_backend',
)
