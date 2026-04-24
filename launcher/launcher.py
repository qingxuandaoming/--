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
SQL_INIT       = os.path.join(BASE_DIR, "database", "complete_init.sql")

DB_HOST   = "127.0.0.1"
DB_PORT   = 3306
JAVA_PORT = 8080
PY_PORT   = 5000
WEB_PORT  = 5000  # Python 同时 serve 前端静态文件

DB_USER = "root"
DB_PASS = "Cycling2024!"
DB_NAME = "ljxz"

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
            subprocess.run(
                [MARIADB_ADMIN, "-u", DB_USER, f"-p{DB_PASS}",
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
def start_mariadb(log_cb):
    log_cb("▶ 正在初始化数据库目录...")

    # 首次运行：初始化数据目录
    if not os.path.isdir(os.path.join(MARIADB_DATA, "mysql")):
        os.makedirs(MARIADB_DATA, exist_ok=True)
        log_cb("  ↳ 首次运行，执行 mysql_install_db ...")
        install_db = os.path.join(MARIADB_DIR, "bin", "mysql_install_db.exe")
        if not os.path.exists(install_db):
            # MariaDB 10.x 使用 mysqld --initialize-insecure
            r = subprocess.run(
                [MARIADB_BIN,
                 f"--datadir={MARIADB_DATA}",
                 "--initialize-insecure",
                 f"--basedir={MARIADB_DIR}"],
                capture_output=True, text=True, timeout=120
            )
            log_cb(r.stdout[-500:] if r.stdout else "")
            log_cb(r.stderr[-500:] if r.stderr else "")
        else:
            r = subprocess.run(
                [install_db,
                 f"--datadir={MARIADB_DATA}",
                 f"--basedir={MARIADB_DIR}"],
                capture_output=True, text=True, timeout=120
            )
            log_cb(r.stdout[-500:] if r.stdout else "")

    my_cnf = os.path.join(BASE_DIR, "runtime", "mariadb", "my.ini")
    _write_my_cnf(my_cnf)

    log_cb("▶ 正在启动 MariaDB...")
    p = subprocess.Popen(
        [MARIADB_BIN,
         f"--defaults-file={my_cnf}",
         f"--datadir={MARIADB_DATA}",
         f"--port={DB_PORT}",
         "--console"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    _procs.append(p)

    log_cb("  ↳ 等待数据库端口就绪...")
    if not wait_for_port(DB_HOST, DB_PORT, timeout=60, label="MariaDB"):
        log_cb("✗ 数据库启动超时！")
        return False

    log_cb("  ↳ 初始化数据库账号和数据...")
    _init_db(log_cb)
    log_cb("✔ 数据库已就绪")
    return True

def _write_my_cnf(path):
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

[client]
port={DB_PORT}
default-character-set=utf8mb4
"""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

def _init_db(log_cb):
    """创建数据库、用户，导入初始数据（幂等）"""
    cmds = [
        f"ALTER USER 'root'@'localhost' IDENTIFIED BY '{DB_PASS}';",
        f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;",
        f"GRANT ALL PRIVILEGES ON `{DB_NAME}`.* TO 'root'@'%' IDENTIFIED BY '{DB_PASS}';",
        "FLUSH PRIVILEGES;",
    ]
    for cmd in cmds:
        _run_mysql_cmd(cmd, log_cb, use_auth=False)

    # 导入 SQL 文件（只在表不存在时）
    check = _run_mysql_cmd(
        f"SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='{DB_NAME}';",
        log_cb, capture=True
    )
    if check and "0" in check:
        log_cb("  ↳ 导入初始数据...")
        _import_sql(SQL_INIT, log_cb)
    else:
        log_cb("  ↳ 数据库已存在，跳过导入")

def _run_mysql_cmd(cmd, log_cb=None, use_auth=True, capture=False):
    args = [MARIADB_CLIENT,
            "-h", DB_HOST, "-P", str(DB_PORT),
            "-u", "root"]
    if use_auth:
        args += [f"-p{DB_PASS}"]
    else:
        # 初始化时 root 无密码
        args += ["--connect-expired-password"]
    args += ["-e", cmd]
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=30,
                           creationflags=subprocess.CREATE_NO_WINDOW)
        if capture:
            return r.stdout
        if r.returncode != 0 and log_cb:
            log_cb(f"  [db] {r.stderr[:200]}")
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
    args = [MARIADB_CLIENT,
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

    p = subprocess.Popen(
        [JAVA_EXE, "-jar", JAVA_JAR,
         f"--spring.datasource.url={db_url}",
         f"--spring.datasource.username={DB_USER}",
         f"--spring.datasource.password={DB_PASS}",
         "--server.port=8080",
         "--spring.jpa.hibernate.ddl-auto=update"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
        env=env,
        creationflags=subprocess.CREATE_NO_WINDOW
    )
    _procs.append(p)

    log_cb("  ↳ 等待 Java 后端端口就绪 (最多 90 秒)...")
    if not wait_for_port(DB_HOST, JAVA_PORT, timeout=90, label="Java"):
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

    p = subprocess.Popen(
        [PYTHON_BACKEND],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
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
