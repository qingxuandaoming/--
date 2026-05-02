# build_release.ps1 - 一键打包脚本
# 用法：在 launcher 目录下以 PowerShell 运行
# 生成完整发布包到 release\ 目录

$ErrorActionPreference = "Stop"
$LAUNCHER_DIR = $PSScriptRoot
$SYSTEM_DIR   = Split-Path $LAUNCHER_DIR -Parent
$RELEASE_DIR  = Join-Path $LAUNCHER_DIR "release"

Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan
Write-Host " 骑行装备系统 - 发布包构建脚本" -ForegroundColor Cyan
Write-Host "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━" -ForegroundColor Cyan

# ── Step 1: PyInstaller 构建 launcher ────────────────────
Write-Host "`n[1/5] 构建启动器 exe..." -ForegroundColor Yellow
Set-Location $LAUNCHER_DIR
pyinstaller launcher.spec --noconfirm
if ($LASTEXITCODE -ne 0) { Write-Error "PyInstaller 构建失败"; exit 1 }

# ── Step 2: 清理并建立 release 目录 ──────────────────────
Write-Host "`n[2/5] 准备 release 目录..." -ForegroundColor Yellow
if (Test-Path $RELEASE_DIR) { Remove-Item $RELEASE_DIR -Recurse -Force }
New-Item -ItemType Directory -Path $RELEASE_DIR | Out-Null

# 复制 exe
Copy-Item "$LAUNCHER_DIR\dist\启动系统.exe" "$RELEASE_DIR\启动系统.exe"

# ── Step 3: 复制运行时目录 ────────────────────────────────
Write-Host "`n[3/5] 复制运行时组件..." -ForegroundColor Yellow

function Copy-IfExists($src, $dst) {
    if (Test-Path $src) {
        Write-Host "  复制: $src" -ForegroundColor Gray
        Copy-Item $src $dst -Recurse -Force
    } else {
        Write-Warning "  跳过（不存在）: $src"
    }
}

# runtime/mariadb - 捆绑 MariaDB（需要提前放好）
Copy-IfExists "$LAUNCHER_DIR\runtime"      "$RELEASE_DIR\runtime"

# java-backend/app.jar
$jarSrc = "$SYSTEM_DIR\java-backend\target\app.jar"
if (-not (Test-Path $jarSrc)) {
    # 尝试其他位置
    $jarSrc = Get-ChildItem "$SYSTEM_DIR\java-backend\target" -Filter "*.jar" -ErrorAction SilentlyContinue |
              Where-Object { $_.Name -notlike "*sources*" -and $_.Name -notlike "*javadoc*" } |
              Select-Object -First 1 -ExpandProperty FullName
}
if ($jarSrc -and (Test-Path $jarSrc)) {
    New-Item -ItemType Directory -Path "$RELEASE_DIR\java-backend" -Force | Out-Null
    Copy-Item $jarSrc "$RELEASE_DIR\java-backend\app.jar"
    Write-Host "  复制 JAR: $jarSrc" -ForegroundColor Gray
} else {
    Write-Warning "  未找到 java-backend app.jar，请先执行 mvn package"
}

# python-backend/python_backend.exe
Copy-IfExists "$SYSTEM_DIR\python-backend\dist\python_backend" "$RELEASE_DIR\python-backend"
# 如果是 onefile 打包，可能是单文件
$pyExe = "$SYSTEM_DIR\python-backend\dist\python_backend.exe"
if (Test-Path $pyExe) {
    New-Item -ItemType Directory -Path "$RELEASE_DIR\python-backend" -Force | Out-Null
    Copy-Item $pyExe "$RELEASE_DIR\python-backend\python_backend.exe"
    Write-Host "  复制 Python 后端 exe" -ForegroundColor Gray
}

# vue-dist
$vueDist = "$SYSTEM_DIR\vue-cycling-app\dist"
Copy-IfExists $vueDist "$RELEASE_DIR\vue-dist"

# database SQL
$dbDir = "$SYSTEM_DIR\database"
Copy-IfExists $dbDir "$RELEASE_DIR\database"

# ── Step 4: 检查关键文件 ──────────────────────────────────
Write-Host "`n[4/5] 检查发布包完整性..." -ForegroundColor Yellow
$checks = @(
    @{ Path = "$RELEASE_DIR\启动系统.exe";                  Name = "启动器 exe" }
    @{ Path = "$RELEASE_DIR\runtime\mariadb\bin\mysqld.exe"; Name = "MariaDB 服务端" }
    @{ Path = "$RELEASE_DIR\runtime\mariadb\bin\mysql.exe";  Name = "MariaDB 客户端" }
    @{ Path = "$RELEASE_DIR\runtime\jre\bin\java.exe";       Name = "JRE" }
    @{ Path = "$RELEASE_DIR\java-backend\app.jar";           Name = "Java 后端 JAR" }
    @{ Path = "$RELEASE_DIR\python-backend\python_backend.exe"; Name = "Python 后端 exe" }
    @{ Path = "$RELEASE_DIR\vue-dist\index.html";            Name = "Vue 前端" }
    @{ Path = "$RELEASE_DIR\database\complete_init.sql";     Name = "初始化 SQL" }
)
$allOk = $true
foreach ($c in $checks) {
    if (Test-Path $c.Path) {
        Write-Host "  ✔ $($c.Name)" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $($c.Name) 缺失: $($c.Path)" -ForegroundColor Red
        $allOk = $false
    }
}

# ── Step 5: 计算大小 ──────────────────────────────────────
Write-Host "`n[5/5] 发布包统计..." -ForegroundColor Yellow
$size = (Get-ChildItem $RELEASE_DIR -Recurse -File | Measure-Object -Property Length -Sum).Sum
$sizeMB = [math]::Round($size / 1MB, 1)
$fileCount = (Get-ChildItem $RELEASE_DIR -Recurse -File).Count
Write-Host "  位置: $RELEASE_DIR"
Write-Host "  大小: $sizeMB MB ($fileCount 个文件)"

Write-Host ""
if ($allOk) {
    Write-Host "✅ 发布包构建完成！" -ForegroundColor Green
    Write-Host "   将 release\ 目录整体复制到目标机器即可运行" -ForegroundColor Cyan
} else {
    Write-Host "⚠  部分组件缺失，请补充后重新打包" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "需要手动准备的目录结构：" -ForegroundColor Cyan
    Write-Host "  release\"
    Write-Host "  ├── 启动系统.exe"
    Write-Host "  ├── runtime\"
    Write-Host "  │   ├── mariadb\   <- 解压 MariaDB ZIP（免安装版）"
    Write-Host "  │   └── jre\       <- 解压 JRE（免安装版）"
    Write-Host "  ├── java-backend\app.jar"
    Write-Host "  ├── python-backend\python_backend.exe"
    Write-Host "  ├── vue-dist\"
    Write-Host "  └── database\complete_init.sql"
}
