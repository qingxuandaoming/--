# -*- coding: utf-8 -*-
"""
软著源代码文档生成脚本
生成符合中国版权保护中心要求的源代码提交文档

要求：
1. 代码总量超过3000行的，提交前30页和后30页
2. 每页50行代码
3. 页眉包含软件名称和版本号
4. 页脚包含页码
5. 不包含爬虫相关代码
"""

import os
from fpdf import FPDF

# ============== 配置 ==============
SOFTWARE_NAME = "驭见东方"
SOFTWARE_NAME_EN = "Intangible_Cultural_Heritage_Cycling_Tour"
VERSION = "V1.0"
LINES_PER_PAGE = 50
PAGES_FRONT = 30
PAGES_BACK = 30
OUTPUT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.join(OUTPUT_DIR, "..", "..")

# ============== 前30页文件配置 ==============
# 格式: (相对路径, 起始行, 结束行)
FRONT_FILES = [
    # 前端基础架构 (667行)
    ("vue-cycling-app/src/main.js", 1, 14),
    ("vue-cycling-app/src/App.vue", 1, 39),
    ("vue-cycling-app/src/router/index.js", 1, 109),
    ("vue-cycling-app/src/utils/auth.js", 1, 62),
    ("vue-cycling-app/src/config/api.js", 1, 149),
    ("vue-cycling-app/src/services/api.js", 1, 294),

    # Java后端认证核心 (664行)
    ("java-backend/src/main/java/com/ljxz/cycling/CyclingRouteApplication.java", 1, 29),
    ("java-backend/src/main/java/com/ljxz/cycling/config/SecurityConfig.java", 1, 134),
    ("java-backend/src/main/java/com/ljxz/cycling/config/JwtAuthenticationFilter.java", 1, 72),
    ("java-backend/src/main/java/com/ljxz/cycling/controller/AuthController.java", 1, 132),
    ("java-backend/src/main/java/com/ljxz/cycling/service/AuthService.java", 1, 163),
    ("java-backend/src/main/java/com/ljxz/cycling/util/JwtUtil.java", 1, 134),

    # Python数据模型 (169行)
    ("python-backend/models/equipment.py", 1, 169),
]

# ============== 后30页文件配置 ==============
BACK_FILES = [
    # Python数据模型续 (105行)
    ("python-backend/models/equipment.py", 170, 274),

    # Java后端业务核心 (1035行)
    ("java-backend/src/main/java/com/ljxz/cycling/controller/RouteController.java", 1, 451),
    ("java-backend/src/main/java/com/ljxz/cycling/service/RouteService.java", 1, 334),
    ("java-backend/src/main/java/com/ljxz/cycling/service/AmapService.java", 1, 250),

    # 前端核心页面 (360行，到</script>结束)
    ("vue-cycling-app/src/views/Home.vue", 1, 360),
]

# ============== 文件注释生成 ==============
def get_file_comment(rel_path):
    """根据文件路径生成文件标识注释"""
    ext = os.path.splitext(rel_path)[1].lower()
    
    # 确定技术栈
    if ext == '.vue':
        stack = "Vue 3 + JavaScript"
        prefix = "//"
    elif ext == '.js':
        if 'router' in rel_path:
            stack = "Vue 3 + Vue Router"
        else:
            stack = "JavaScript (ES6+)"
        prefix = "//"
    elif ext == '.java':
        if 'config' in rel_path and 'Security' in rel_path:
            stack = "Java + Spring Boot + Spring Security"
        elif 'JwtAuthenticationFilter' in rel_path:
            stack = "Java + Spring Boot + JWT Filter"
        elif 'controller' in rel_path:
            stack = "Java + Spring Boot (REST API)"
        elif 'service' in rel_path:
            stack = "Java + Spring Boot (Service Layer)"
        elif 'util' in rel_path:
            stack = "Java + Spring Boot (JWT Utility)"
        else:
            stack = "Java + Spring Boot"
        prefix = "//"
    elif ext == '.py':
        stack = "Python + Flask-SQLAlchemy"
        prefix = "#"
    else:
        stack = "未知技术栈"
        prefix = "//"
    
    comment = f"{prefix} ====== 文件: {rel_path} | 技术栈: {stack} ======\n"
    return comment


# ============== 读取代码 ==============
def read_code_lines(file_configs):
    """按配置读取代码行，并在每部分代码前插入文件标识注释"""
    lines = []
    for rel_path, start_line, end_line in file_configs:
        full_path = os.path.join(PROJECT_ROOT, rel_path)
        full_path = os.path.normpath(full_path)
        if not os.path.exists(full_path):
            print(f"警告: 文件不存在 {full_path}")
            continue

        # 插入文件标识注释
        lines.append(get_file_comment(rel_path))

        with open(full_path, 'r', encoding='utf-8') as f:
            file_lines = f.readlines()

        # 提取指定行范围
        start_idx = max(0, start_line - 1)
        end_idx = min(len(file_lines), end_line)

        for i in range(start_idx, end_idx):
            line = file_lines[i]
            # 确保每行以换行符结尾
            if not line.endswith('\n'):
                line += '\n'
            lines.append(line)

    return lines

# ============== 分页分布计算 ==============
def get_page_distribution(total_lines, target_pages):
    """
    将总行数均匀分配到指定页数，保证每页至少50行。
    前 remainder 页每页 base+1 行，其余每页 base 行。
    """
    base = total_lines // target_pages
    remainder = total_lines % target_pages
    return [base + 1] * remainder + [base] * (target_pages - remainder)


# ============== 生成 Markdown ==============
def generate_markdown(front_lines, back_lines):
    """生成 Markdown 文档"""
    md_path = os.path.join(OUTPUT_DIR, f"软著源代码_{SOFTWARE_NAME}.md")

    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# {SOFTWARE_NAME} 源代码文档\n\n")
        f.write(f"**软件名称**: {SOFTWARE_NAME}\n\n")
        f.write(f"**英文名称**: {SOFTWARE_NAME_EN}\n\n")
        f.write(f"**版本号**: {VERSION}\n\n")
        f.write(f"**提交说明**: 本软件代码总量超过3000行，按软著要求提交前30页和后30页，每页不少于50行。\n\n")
        f.write("---\n\n")

        # 前30页
        f.write("## 第一部分：源代码前30页\n\n")
        front_dist = get_page_distribution(len(front_lines), PAGES_FRONT)
        line_idx = 0
        page_num = 1
        for page_lines_count in front_dist:
            f.write(f"<!-- 第 {page_num} 页 (本页{page_lines_count}行) -->\n\n")
            f.write("```text\n")
            page_lines = front_lines[line_idx:line_idx + page_lines_count]
            for line in page_lines:
                # Markdown 代码块中需要转义 ```
                stripped = line.strip()
                if stripped.startswith('```') and not stripped.startswith('```text'):
                    line = line.replace('```', '`` `')
                f.write(line)
            f.write("```\n\n")
            f.write("---\n\n")
            line_idx += page_lines_count
            page_num += 1

        # 后30页
        f.write("## 第二部分：源代码后30页\n\n")
        back_dist = get_page_distribution(len(back_lines), PAGES_BACK)
        page_num = 31
        line_idx = 0
        for page_lines_count in back_dist:
            f.write(f"<!-- 第 {page_num} 页 (本页{page_lines_count}行) -->\n\n")
            f.write("```text\n")
            page_lines = back_lines[line_idx:line_idx + page_lines_count]
            for line in page_lines:
                stripped = line.strip()
                if stripped.startswith('```') and not stripped.startswith('```text'):
                    line = line.replace('```', '`` `')
                f.write(line)
            f.write("```\n\n")
            f.write("---\n\n")
            line_idx += page_lines_count
            page_num += 1

    print(f"Markdown 已生成: {md_path}")
    return md_path

# ============== 生成 PDF ==============
def generate_pdf(front_lines, back_lines):
    """生成 PDF 文档"""

    class SourceCodePDF(FPDF):
        def __init__(self):
            super().__init__('P', 'mm', 'A4')
            self.set_auto_page_break(False)
            self.set_left_margin(15)
            self.set_right_margin(15)

        def header(self):
            # 页眉：软件名称和版本号
            self.set_y(10)
            self.set_font('SimSun', '', 9)
            self.cell(0, 5, f"{SOFTWARE_NAME}  {VERSION}", align='C')
            # 页眉下划线
            self.set_draw_color(128, 128, 128)
            self.line(15, 16, 195, 16)

        def footer(self):
            # 页脚：页码
            self.set_y(-10)
            self.set_font('SimSun', '', 9)
            self.cell(0, 5, f"第 {self.page_no()} 页", align='C')

    pdf = SourceCodePDF()

    # 添加中文字体
    font_paths = [
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/simfang.ttf",
        "/usr/share/fonts/truetype/wqy/wqy-zenhei.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
    ]

    font_added = False
    for font_path in font_paths:
        if os.path.exists(font_path):
            try:
                pdf.add_font('SimSun', '', font_path)
                pdf.add_font('SimSun', 'B', font_path)
                font_added = True
                print(f"使用字体: {font_path}")
                break
            except Exception as e:
                print(f"字体加载失败 {font_path}: {e}")
                continue

    if not font_added:
        print("错误: 未找到中文字体，PDF可能显示乱码")
        return None

    def add_pages(lines, start_page_num, target_pages):
        """添加代码页面，均匀分布行数，保证每页至少50行"""
        dist = get_page_distribution(len(lines), target_pages)
        line_idx = 0
        page_num = start_page_num
        for i, page_lines_count in enumerate(dist):
            pdf.add_page()
            pdf.set_font('SimSun', '', 8)
            pdf.set_xy(15, 20)

            page_lines = lines[line_idx:line_idx + page_lines_count]
            for j, line in enumerate(page_lines):
                # 移除换行符
                line = line.rstrip('\n').rstrip('\r')
                # 替换制表符为空格
                line = line.replace('\t', '    ')
                # 截断过长的行（A4纸大约能放110个7.5pt字符）
                if len(line) > 115:
                    line = line[:112] + '...'

                y = 18 + j * 5.0  # 每行5.0mm，从18mm处开始
                pdf.set_xy(15, y)
                try:
                    pdf.cell(0, 5.0, line)
                except Exception as e:
                    # 如果某些字符无法编码，替换为?
                    safe_line = line.encode('latin-1', 'replace').decode('latin-1')
                    pdf.cell(0, 5.0, safe_line)

            line_idx += page_lines_count
            page_num += 1

    add_pages(front_lines, 1, PAGES_FRONT)
    add_pages(back_lines, 31, PAGES_BACK)

    pdf_path = os.path.join(OUTPUT_DIR, f"软著源代码_{SOFTWARE_NAME}.pdf")
    try:
        pdf.output(pdf_path)
    except PermissionError:
        pdf_path = os.path.join(OUTPUT_DIR, f"软著源代码_{SOFTWARE_NAME}_new.pdf")
        pdf.output(pdf_path)
        print(f"原文件被占用，已输出到新文件")
    print(f"PDF 已生成: {pdf_path}")
    return pdf_path

# ============== 主程序 ==============
def main():
    print("=" * 60)
    print(f"软著源代码文档生成工具 - {SOFTWARE_NAME}")
    print("=" * 60)

    # 读取代码
    print("\n[1/4] 读取前30页代码...")
    front_lines = read_code_lines(FRONT_FILES)
    print(f"      前30页代码行数: {len(front_lines)}")

    print("\n[2/4] 读取后30页代码...")
    back_lines = read_code_lines(BACK_FILES)
    print(f"      后30页代码行数: {len(back_lines)}")

    total_lines = len(front_lines) + len(back_lines)
    front_dist = get_page_distribution(len(front_lines), PAGES_FRONT)
    back_dist = get_page_distribution(len(back_lines), PAGES_BACK)
    print(f"\n      总代码行数: {total_lines}")
    print(f"      前{PAGES_FRONT}页分布: {len(front_dist)}页, 每页行数 {set(front_dist)}")
    print(f"      后{PAGES_BACK}页分布: {len(back_dist)}页, 每页行数 {set(back_dist)}")
    print(f"      总页数: {PAGES_FRONT + PAGES_BACK} (每页不少于{LINES_PER_PAGE}行)")

    # 校验
    if len(front_lines) < PAGES_FRONT * LINES_PER_PAGE:
        print(f"\n警告: 前30页代码行数为 {len(front_lines)}，不足最少要求 {PAGES_FRONT * LINES_PER_PAGE}")
    if len(back_lines) < PAGES_BACK * LINES_PER_PAGE:
        print(f"\n警告: 后30页代码行数为 {len(back_lines)}，不足最少要求 {PAGES_BACK * LINES_PER_PAGE}")

    # 生成 Markdown
    print("\n[3/4] 生成 Markdown 文档...")
    generate_markdown(front_lines, back_lines)

    # 生成 PDF
    print("\n[4/4] 生成 PDF 文档...")
    generate_pdf(front_lines, back_lines)

    print("\n" + "=" * 60)
    print("生成完成！")
    print(f"输出目录: {OUTPUT_DIR}")
    print("=" * 60)

if __name__ == '__main__':
    main()
