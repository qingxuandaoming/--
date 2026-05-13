# -*- mode: python ; coding: utf-8 -*-
# PyInstaller spec for Python Backend (python_backend.exe)
# 入口使用 start.py，以同时启动 Flask 应用和任务调度器
import os, sys

block_cipher = None

# 收集需要打包的数据目录
added_files = [
    ('services', 'services'),
    ('models', 'models'),
    ('config', 'config'),
]
# 加入 .env 示例（运行时由启动器覆写）
if os.path.exists('.env'):
    added_files.append(('.env', '.'))

a = Analysis(
    ['start.py'],  # 使用 start.py 作为入口，包含 Flask + Scheduler
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
        'pandas._libs.tslibs.base',
        'pandas._libs.tslibs.np_datetime',
        'pandas._libs.tslibs.nattype',
        'pandas._libs.tslibs.timezones',
        'numpy',
        'scipy',
        'sklearn',
        'sklearn.utils._cython_blas',
        'sklearn.utils._weight_vector',
        'sklearn.neighbors._partition_nodes',
        'sklearn.neighbors._quad_tree',
        'sklearn.tree._utils',
        'apscheduler',
        'apscheduler.schedulers.background',
        'apscheduler.executors.pool',
        'apscheduler.jobstores.sqlalchemy',
        'apscheduler.jobstores.memory',
        'apscheduler.triggers.cron',
        'apscheduler.triggers.interval',
        'apscheduler.triggers.date',
        'requests',
        'bs4',
        'lxml',
        'lxml.etree',
        'lxml.html',
        'PIL',
        'PIL._imagingtk',
        'PIL._tkinter_finder',
        'marshmallow',
        'email_validator',
        'validators',
        'fake_useragent',
        'fuzzywuzzy',
        'Levenshtein',
        'psutil',
        'httpx',
        'cryptography',
        'cryptography.hazmat.primitives.kdf.pbkdf2',
        'services.crawler_service',
        'services.advanced_crawler_service',
        'services.equipment_service',
        'services.data_analysis_service',
        'services.crawler_config_service',
        'services.crawler_monitor_service',
        'services.crawler_queue_service',
        'services.data_validation_service',
        'services.recommendation_service',
        'services.price_alert_service',
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
