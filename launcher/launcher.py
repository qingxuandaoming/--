# -*- coding: utf-8 -*-
"""
骑行装备数据分析系统 - 一键启动器
自动启动 MariaDB、Java 后端、Python 后端，并打开浏览器
"""

import sys
import os
import subprocess
import threading
import time
import socket
import webbrowser
import shutil
import signal
import tkinter as tk
from tkinter import ttk, scrolledtext
import ctypes

# ─────────────────────────────────────────────
# 路径工具
# ─────────────────────────────────────────────
def get_base_dir():
    """获取程序根目录（兼容 PyInstaller --onedir）"""
    if getattr(sys, 'frozen', False):
        # PyInstaller 打包后，_MEIPASS 是解压目录，exe 在其上级
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

BASE_DIR = get_base_dir()

# 各组件路径
MARIADB_DIR    = os.path.join(BASE_DIR, "runtime", "mariadb")
MARIADB_BIN    = os.path.join(MARIADB_DIR, "bin", "mysqld.exe")
MARIADB_CLIENT = os.path.join(MARIADB_DIR, "bin", "mysql.exe")
MARIADB_ADMIN  = os.path.join(MARIADB_DIR, "bin", "mysqladmin.exe")
MARIADB_DATA   = os.path.join(BASE_DIR, "data", "mysql")

JRE_DIR        = os.path.join(BASE_DIR, "runtime", "jre")
JAVA_EXE       = os.path.join(JRE_DIR, "bin", "java.exe")
JAVA_JAR       = os.path.join(BASE_DIR, "java-backend", "app.jar")

PYTHON_BACKEND = os.path.join(BASE_DIR, "python-backend", "python_backend.exe")
VUE_DIST       = os.path.join(BASE_DIR, "vue-dist")
# SQL 文件：打包后在 BASE_DIR/database/，开发时在上级目录 database/
_sql_candidate = os.path.join(BASE_DIR, "database", "complete_init.sql")
if not os.path.exists(_sql_candidate):
    _sql_candidate = os.path.join(os.path.dirname(BASE_DIR), "database", "complete_init.sql")
SQL_INIT = _sql_candidate

DB_HOST   = "127.0.0.1"
DB_PORT   = 33306       # 捆绑 MariaDB 端口；若用系统 MySQL 则动态切换为 3306
JAVA_PORT = 8080
PY_PORT   = 5000
WEB_PORT  = 5000  # Python 同时 serve 前端静态文件

DB_USER = "root"
DB_PASS = "Cycling2024!"
DB_NAME = "ljxz"

# 系统 MySQL/MariaDB 常见端口（探测顺序）
SYSTEM_DB_PORTS = [3306, 3307]

# ─────────────────────────────────────────────
# 全局进程列表（退出时统一清理）
# ─────────────────────────────────────────────
_procs = []

def cleanup():
    for p in reversed(_procs):
        try:
            p.terminate()
            p.wait(timeout=5)
        except Exception:
            try:
                p.kill()
            except Exception:
                pass
    # 停止 MariaDB
    if os.path.exists(MARIADB_ADMIN):
        try:
            my_cnf = os.path.join(BASE_DIR, "runtime", "mariadb", "my.ini")
            subprocess.run(
                [MARIADB_ADMIN, f"--defaults-file={my_cnf}", "-u", DB_USER, f"-p{DB_PASS}",
                 "-P", str(DB_PORT), "-h", DB_HOST, "shutdown"],
                timeout=10, capture_output=True
            )
        except Exception:
            pass

# ─────────────────────────────────────────────
# 网络工具
# ─────────────────────────────────────────────
def wait_for_port(host, port, timeout=120, label="服务"):
    """阻塞等待端口可达，返回 True/False"""
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            with socket.create_connection((host, port), timeout=2):
                return True
        except OSError:
            time.sleep(1)
    return False

# ─────────────────────────────────────────────
# 启动 MariaDB
# ─────────────────────────────────────────────
def _detect_system_mysql(log_cb):
    """探测系统已安装的 MySQL/MariaDB，返回 (host, port) 或 None"""
    import socket as _sock
    for port in SYSTEM_DB_PORTS:
        try:
            with _sock.create_connection((DB_HOST, port), timeout=1):
                log_cb(f"  ↳ 检测到系统 MySQL/MariaDB 运行在端口 {port}")
                return (DB_HOST, port)
        except OSError:
            pass
    return None


def start_mariadb(log_cb):
    global DB_PORT, MARIADB_CLIENT, MARIADB_ADMIN
    log_cb("▶ 正在初始化数据库目录...")

    # ── 优先探测系统已运行的 MySQL/MariaDB ──────────────────
    sys_db = _detect_system_mysql(log_cb)
    if sys_db:
        DB_PORT = sys_db[1]
        # 同步更新 client/admin 路径到系统 MySQL（若存在）
        import glob as _glob
        for candidate in [
            r"C:\Program Files\MySQL\MySQL Server 9.7\bin",
            r"C:\Program Files\MySQL\MySQL Server 8.0\bin",
            r"C:\Program Files\MariaDB 10.11\bin",
            r"C:\Program Files\MariaDB 10.6\bin",
        ]:
            if os.path.exists(os.path.join(candidate, "mysql.exe")):
                MARIADB_CLIENT = os.path.join(candidate, "mysql.exe")
                MARIADB_ADMIN  = os.path.join(candidate, "mysqladmin.exe")
                log_cb(f"  ↳ 使用系统 MySQL 客户端: {candidate}")
                break
        log_cb(f"✔ 复用系统数据库 (端口 {DB_PORT})，跳过捆绑 MariaDB 启动")
        log_cb("  ↳ 初始化数据库账号和数据...")
        _init_db(log_cb)
        log_cb("✔ 数据库已就绪")
        return True

    # ── 无系统数据库，尝试启动捆绑 MariaDB ──────────────────
    if not os.path.exists(MARIADB_BIN):
        log_cb(f"✗ 找不到捆绑 MariaDB: {MARIADB_BIN}")
        log_cb("  请安装 MySQL/MariaDB 或将 MariaDB 放入 runtime/mariadb 目录")
        return False

    log_dir = os.path.join(BASE_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)
    mariadb_log_path = os.path.join(log_dir, "mariadb.log")
    my_cnf = os.path.join(BASE_DIR, "runtime", "mariadb", "my.ini")
    _write_my_cnf(my_cnf, mariadb_log_path)

    # 首次运行：初始化数据目录
    if not os.path.isdir(os.path.join(MARIADB_DATA, "mysql")):
        os.makedirs(MARIADB_DATA, exist_ok=True)
        log_cb("  ↳ 首次运行，正在初始化数据库（约需 1~2 分钟）...")
        install_db = os.path.join(MARIADB_DIR, "bin", "mysql_install_db.exe")
        if not os.path.exists(install_db):
            # MariaDB 10.4+ 使用 mysqld --initialize-insecure
            r = subprocess.run(
                [MARIADB_BIN,
                 f"--defaults-file={my_cnf}",
                 "--initialize-insecure",
                 "--skip-test-db"],
                capture_output=True, timeout=180,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        else:
            r = subprocess.run(
                [install_db,
                 f"--defaults-file={my_cnf}",
                 f"--datadir={MARIADB_DATA}",
                 f"--basedir={MARIADB_DIR}",
                 "--skip-test-db"],
                capture_output=True, timeout=180,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
        out = r.stdout.decode("utf-8", errors="ignore") if r.stdout else ""
        err = r.stderr.decode("utf-8", errors="ignore") if r.stderr else ""
        if out.strip(): log_cb(f"  [init] {out[-400:]}")
        if err.strip(): log_cb(f"  [init] {err[-400:]}")
        if r.returncode != 0:
            log_cb(f"  ⚠ 初始化返回码 {r.returncode}，若数据目录已存在可忽略")

    log_cb("▶ 正在启动捆绑 MariaDB...")
    log_cb(f"  ↳ 日志文件: {mariadb_log_path}")
    mariadb_log_fh = open(mariadb_log_path, "w", encoding="utf-8", errors="ignore")
    p = subprocess.Popen(
        [MARIADB_BIN,
         f"--defaults-file={my_cnf}"],
        stdout=mariadb_log_fh,
        stderr=mariadb_log_fh,
        stdin=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    _procs.append(p)

    log_cb("  ↳ 等待数据库端口就绪（最多 120 秒）...")
    deadline = time.time() + 120
    started = False
    while time.time() < deadline:
        if p.poll() is not None:   # 进程已退出 = 崩溃
            log_cb(f"  ✗ MariaDB 进程意外退出 (code={p.returncode})")
            break
        try:
            with socket.create_connection((DB_HOST, DB_PORT), timeout=1):
                started = True
                break
        except OSError:
            time.sleep(1)

    if not started:
        log_cb("✗ 数据库启动超时！错误日志：")
        try:
            mariadb_log_fh.flush()
            with open(mariadb_log_path, encoding="utf-8", errors="ignore") as f:
                lines = [l.rstrip() for l in f if l.strip()]
            for line in (lines[-20:] if len(lines) > 20 else lines):
                log_cb(f"    {line}")
        except Exception:
            pass
        log_cb(f"  完整日志: {mariadb_log_path}")
        return False

    log_cb("  ↳ 初始化数据库账号和数据...")
    _init_db(log_cb)
    log_cb("✔ 数据库已就绪")
    return True

def _write_my_cnf(path, log_error_path=None):
    log_error_line = (
        f"log-error={log_error_path.replace(os.sep, '/')}"
        if log_error_path else "log-error=mariadb.err"
    )
    content = f"""[mysqld]
basedir={MARIADB_DIR.replace(os.sep, '/')}
datadir={MARIADB_DATA.replace(os.sep, '/')}
port={DB_PORT}
character-set-server=utf8mb4
collation-server=utf8mb4_unicode_ci
skip-networking=0
bind-address=127.0.0.1
max_connections=100
innodb_buffer_pool_size=64M
{log_error_line}

[client]
port={DB_PORT}
default-character-set=utf8mb4
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def _init_db(log_cb):
    """创建数据库、用户，导入初始数据（幂等）"""
    # 探测连接方式：优先试配置密码（系统 MySQL 已有密码），再试无密码（MariaDB 首次初始化）
    check_with_pass = _run_mysql_cmd("SELECT 1;", log_cb=None, use_auth=True, capture=True)
    if check_with_pass.strip():
        # 用配置密码可以连接（系统 MySQL 已设密码，或捆绑 MariaDB 已初始化）
        needs_pass = True
        log_cb("  ↳ 数据库连接验证成功（使用配置密码）")
    else:
        # 配置密码失败，试无密码（MariaDB --initialize-insecure 首次）
        check_no_pass = _run_mysql_cmd("SELECT 1;", log_cb=None, use_auth=False, capture=True)
        needs_pass = False if check_no_pass.strip() else True
        if not check_no_pass.strip():
            log_cb("  ↳ 警告：无法连接到数据库，请检查密码配置")

    # MySQL 8+/9+ 不支持 PASSWORD() 函数，改用 ALTER USER
    # MariaDB 10.x 兼容 ALTER USER 语法
    init_sql = f"""
        CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
        CREATE USER IF NOT EXISTS 'root'@'%' IDENTIFIED BY '{DB_PASS}';
        GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' WITH GRANT OPTION;
        ALTER USER 'root'@'localhost' IDENTIFIED BY '{DB_PASS}';
        FLUSH PRIVILEGES;
    """
    _run_mysql_cmd(init_sql, log_cb, use_auth=needs_pass)

    # 导入 SQL 文件：检查目标表是否存在（用新密码连接）
    check = _run_mysql_cmd(
        f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='{DB_NAME}';",
        log_cb, capture=True, use_auth=True
    )
    # check 为空或包含 '0' → 表不存在，需要导入
    table_count = "".join(c for c in check if c.isdigit())
    if not table_count or table_count == "0":
        log_cb("  ↳ 导入初始数据...")
        _import_sql(SQL_INIT, log_cb)
    else:
        log_cb(f"  ↳ 数据库已存在（{table_count} 张表），跳过导入")

def _run_mysql_cmd(cmd, log_cb=None, use_auth=True, capture=False):
    my_cnf = os.path.join(BASE_DIR, "runtime", "mariadb", "my.ini")
    args = [MARIADB_CLIENT]
    # 仅当捆绑 MariaDB 的 my.ini 实际存在时才加载（系统 MySQL 不需要此选项）
    if os.path.exists(my_cnf):
        args.append(f"--defaults-file={my_cnf}")
    args += ["-h", DB_HOST, "-P", str(DB_PORT), "-u", "root"]
    if use_auth:
        args += [f"-p{DB_PASS}"]
    args += ["-e", cmd]
    try:
        # 使用 bytes 模式避免 Windows 编码导致 text=True 时 stderr=None
        r = subprocess.run(
            args,
            capture_output=True,
            stdin=subprocess.DEVNULL,   # PyInstaller 无控制台模式必须显式设置
            timeout=30,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        stdout = r.stdout.decode('utf-8', errors='ignore') if r.stdout else ""
        stderr = r.stderr.decode('utf-8', errors='ignore') if r.stderr else ""
        if capture:
            return stdout
        if r.returncode != 0 and log_cb and stderr:
            log_cb(f"  [db] {stderr[:300]}")
    except Exception as e:
        if log_cb:
            log_cb(f"  [db err] {e}")
    return ""

def _import_sql(sql_file, log_cb):
    if not os.path.exists(sql_file):
        log_cb(f"  ✗ 找不到 SQL 文件: {sql_file}")
        return
    with open(sql_file, "rb") as f:
        data = f.read()
    my_cnf = os.path.join(BASE_DIR, "runtime", "mariadb", "my.ini")
    args = [MARIADB_CLIENT,
            f"--defaults-file={my_cnf}",
            "-h", DB_HOST, "-P", str(DB_PORT),
            "-u", "root", f"-p{DB_PASS}",
            DB_NAME]
    try:
        r = subprocess.run(args, input=data, capture_output=True, timeout=120,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        if r.returncode != 0:
            log_cb(f"  [sql warn] {r.stderr.decode('utf-8','ignore')[:300]}")
    except Exception as e:
        log_cb(f"  [sql err] {e}")

# ─────────────────────────────────────────────
# 启动 Java 后端
# ─────────────────────────────────────────────
def start_java(log_cb):
    if not os.path.exists(JAVA_EXE):
        log_cb(f"✗ 找不到 JRE: {JAVA_EXE}")
        return False
    if not os.path.exists(JAVA_JAR):
        log_cb(f"✗ 找不到 JAR: {JAVA_JAR}")
        return False

    log_cb("▶ 正在启动 Java 后端...")
    db_url = (f"jdbc:mysql://{DB_HOST}:{DB_PORT}/{DB_NAME}"
              "?useUnicode=true&characterEncoding=utf8&useSSL=false"
              "&serverTimezone=Asia/Shanghai&allowPublicKeyRetrieval=true")
    env = os.environ.copy()
    env["SPRING_DATASOURCE_URL"] = db_url
    env["SPRING_DATASOURCE_USERNAME"] = DB_USER
    env["SPRING_DATASOURCE_PASSWORD"] = DB_PASS

    # 将 Java 日志写到文件，方便排查启动失败原因
    log_dir = os.path.join(BASE_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)
    java_log = open(os.path.join(log_dir, "java.log"), "w", encoding="utf-8", errors="ignore")

    p = subprocess.Popen(
        [JAVA_EXE,
         "-Xms128m", "-Xmx512m",      # 限制堆内存，启动更快
         "-jar", JAVA_JAR,
         f"--spring.datasource.url={db_url}",
         f"--spring.datasource.username={DB_USER}",
         f"--spring.datasource.password={DB_PASS}",
         "--server.port=8080",
         "--spring.jpa.hibernate.ddl-auto=update",
         "--logging.level.root=WARN",    # 减少日志量，加快启动
         "--logging.level.com.ljxz=INFO"],
        stdout=java_log,
        stderr=java_log,
        stdin=subprocess.DEVNULL,
        env=env,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    _procs.append(p)

    log_cb("  ↳ 等待 Java 后端端口就绪 (最多 120 秒)...")
    if not wait_for_port(DB_HOST, JAVA_PORT, timeout=120, label="Java"):
        # 读取日志尾部帮助诊断
        try:
            java_log.flush()
            log_path = os.path.join(log_dir, "java.log")
            with open(log_path, encoding="utf-8", errors="ignore") as f:
                tail = f.readlines()
            last = [l.strip() for l in tail if l.strip()][-10:]
            log_cb("✗ Java 后端启动失败，最后 10 行日志:")
            for line in last:
                log_cb(f"  {line}")
            log_cb(f"  完整日志: {log_path}")
        except Exception:
            log_cb("✗ Java 后端启动超时！")
        return False
    log_cb("✔ Java 后端已就绪 (http://localhost:8080)")
    return True

# ─────────────────────────────────────────────
# 启动 Python 后端
# ─────────────────────────────────────────────
def start_python(log_cb):
    if not os.path.exists(PYTHON_BACKEND):
        log_cb(f"✗ 找不到 Python 后端: {PYTHON_BACKEND}")
        return False

    log_cb("▶ 正在启动 Python 后端...")
    env = os.environ.copy()
    env["DB_HOST"]      = DB_HOST
    env["DB_PORT"]      = str(DB_PORT)
    env["DB_USER"]      = DB_USER
    env["DB_PASSWORD"]  = DB_PASS
    env["DB_NAME"]      = DB_NAME
    env["DATABASE_URL"] = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    env["HOST"]         = "0.0.0.0"
    env["PORT"]         = str(PY_PORT)
    env["DEBUG"]        = "False"
    env["FLASK_DEBUG"]  = "0"
    env["VUE_DIST_DIR"] = VUE_DIST  # 让 Python 后端 serve 前端

    py_log = open(os.path.join(BASE_DIR, "logs", "python.log"), "w",
                  encoding="utf-8", errors="ignore")
    p = subprocess.Popen(
        [PYTHON_BACKEND],
        stdout=py_log,
        stderr=py_log,
        stdin=subprocess.DEVNULL,
        env=env,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    _procs.append(p)

    log_cb("  ↳ 等待 Python 后端端口就绪 (最多 60 秒)...")
    if not wait_for_port(DB_HOST, PY_PORT, timeout=60, label="Python"):
        log_cb("✗ Python 后端启动超时！")
        return False
    log_cb("✔ Python 后端已就绪 (http://localhost:5000)")
    return True

# ─────────────────────────────────────────────
# GUI 主窗口
# ─────────────────────────────────────────────
class LauncherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("骑行装备数据分析系统 — 启动器")
        self.geometry("680x520")
        self.resizable(False, False)
        self.configure(bg="#1a1a2e")
        self.protocol("WM_DELETE_WINDOW", self._on_close)

        self._setup_ui()
        # 启动后自动开始
        threading.Thread(target=self._launch_all, daemon=True).start()

    # ── UI 布局 ──────────────────────────────
    def _setup_ui(self):
        # 标题
        header = tk.Frame(self, bg="#16213e", pady=12)
        header.pack(fill="x")
        tk.Label(header, text="🚴 骑行装备数据分析系统",
                 font=("Microsoft YaHei UI", 16, "bold"),
                 bg="#16213e", fg="#e94560").pack()
        tk.Label(header, text="正在启动各项服务，请稍候…",
                 font=("Microsoft YaHei UI", 9),
                 bg="#16213e", fg="#8892a4").pack()

        # 状态指示器
        status_frame = tk.Frame(self, bg="#1a1a2e", pady=8)
        status_frame.pack(fill="x", padx=20)
        self._status_vars = {}
        services = [
            ("db",     "📦 MariaDB 数据库"),
            ("java",   "☕ Java 后端"),
            ("python", "🐍 Python 后端"),
            ("web",    "🌐 前端界面"),
        ]
        for key, label in services:
            row = tk.Frame(status_frame, bg="#1a1a2e")
            row.pack(fill="x", pady=2)
            var = tk.StringVar(value="⏳ 等待中")
            self._status_vars[key] = var
            tk.Label(row, text=label, width=20, anchor="w",
                     font=("Microsoft YaHei UI", 10),
                     bg="#1a1a2e", fg="#c0c0c0").pack(side="left")
            tk.Label(row, textvariable=var,
                     font=("Microsoft YaHei UI", 10),
                     bg="#1a1a2e", fg="#8892a4").pack(side="left")

        # 进度条
        self._progress = ttk.Progressbar(self, orient="horizontal",
                                         length=640, mode="determinate",
                                         maximum=4)
        self._progress.pack(pady=(4, 8), padx=20)

        # 日志框
        log_frame = tk.Frame(self, bg="#1a1a2e")
        log_frame.pack(fill="both", expand=True, padx=20, pady=(0, 8))
        tk.Label(log_frame, text="启动日志", anchor="w",
                 font=("Microsoft YaHei UI", 9, "bold"),
                 bg="#1a1a2e", fg="#e94560").pack(anchor="w")
        self._log_box = scrolledtext.ScrolledText(
            log_frame, height=14, wrap="word",
            bg="#0f3460", fg="#e0e0e0",
            font=("Consolas", 9),
            insertbackground="white",
            state="disabled"
        )
        self._log_box.pack(fill="both", expand=True)

        # 底部按钮
        btn_frame = tk.Frame(self, bg="#1a1a2e", pady=6)
        btn_frame.pack(fill="x", padx=20)
        self._open_btn = tk.Button(
            btn_frame, text="打开浏览器",
            font=("Microsoft YaHei UI", 10, "bold"),
            bg="#e94560", fg="white",
            activebackground="#c73652",
            relief="flat", padx=12, pady=6,
            state="disabled",
            command=self._open_browser
        )
        self._open_btn.pack(side="left")
        tk.Button(
            btn_frame, text="关闭所有服务",
            font=("Microsoft YaHei UI", 10),
            bg="#444", fg="white",
            activebackground="#666",
            relief="flat", padx=12, pady=6,
            command=self._on_close
        ).pack(side="right")

    # ── 日志回调 ────────────────────────────
    def _log(self, msg):
        def _do():
            self._log_box.configure(state="normal")
            self._log_box.insert("end", msg + "\n")
            self._log_box.see("end")
            self._log_box.configure(state="disabled")
        self.after(0, _do)

    def _set_status(self, key, text, color="#8892a4"):
        def _do():
            self._status_vars[key].set(text)
        self.after(0, _do)

    def _step_progress(self):
        def _do():
            self._progress.step(1)
        self.after(0, _do)

    # ── 主启动流程 ───────────────────────────
    def _launch_all(self):
        ok = True

        # 1. MariaDB
        self._set_status("db", "🔄 启动中…", "#f5a623")
        if start_mariadb(self._log):
            self._set_status("db", "✔ 已就绪", "#7ed321")
        else:
            self._set_status("db", "✗ 启动失败", "#d0021b")
            ok = False
        self._step_progress()

        # 2. Java
        self._set_status("java", "🔄 启动中…", "#f5a623")
        if ok and start_java(self._log):
            self._set_status("java", "✔ 已就绪", "#7ed321")
        else:
            self._set_status("java", "✗ 启动失败", "#d0021b")
            ok = False
        self._step_progress()

        # 3. Python
        self._set_status("python", "🔄 启动中…", "#f5a623")
        if ok and start_python(self._log):
            self._set_status("python", "✔ 已就绪", "#7ed321")
        else:
            self._set_status("python", "✗ 启动失败", "#d0021b")
            ok = False
        self._step_progress()

        # 4. Web
        if ok:
            self._set_status("web", "✔ http://localhost:5000", "#7ed321")
            self._log("=" * 50)
            self._log("✅ 所有服务已就绪！")
            self._log(f"   前端地址: http://localhost:{WEB_PORT}")
            self._log(f"   Java API: http://localhost:{JAVA_PORT}/api")
            self._log(f"   Python API: http://localhost:{PY_PORT}/api")
            self._log("=" * 50)
            self.after(0, lambda: self._open_btn.configure(state="normal"))
            # 延迟 1 秒自动打开浏览器
            time.sleep(1)
            self._open_browser()
        else:
            self._set_status("web", "✗ 服务异常", "#d0021b")
            self._log("❌ 部分服务启动失败，请查看上方日志")
        self._step_progress()

    def _open_browser(self):
        webbrowser.open(f"http://localhost:{WEB_PORT}")

    def _on_close(self):
        self._log("正在关闭所有服务...")
        threading.Thread(target=cleanup, daemon=True).start()
        time.sleep(2)
        self.destroy()


# ─────────────────────────────────────────────
# 入口
# ─────────────────────────────────────────────
if __name__ == "__main__":
    # 请求管理员权限（可选，用于绑定低端口）
    if sys.platform == "win32":
        try:
            is_admin = ctypes.windll.shell32.IsUserAnAdmin()
        except Exception:
            is_admin = False
        # 不强制提权，直接运行

    app = LauncherApp()
    app.mainloop()
