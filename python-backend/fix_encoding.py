import re

# 读取当前 app.py（用替换模式）
with open('app.py', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 逐行处理：找到包含 PUA 字符的 docstring 行，直接替换整行
lines = content.split('\n')
out = []
for line in lines:
    # 检查是否含 PUA 字符（E000-F8FF）或替换字符
    has_pua = any(0xE000 <= ord(c) <= 0xF8FF or ord(c) == 0xFFFD for c in line)
    if has_pua:
        stripped = line.lstrip()
        indent = line[:len(line) - len(stripped)]
        if stripped.startswith('"""') and stripped.endswith('"""'):
            # 单行 docstring，直接替换
            line = indent + '"""API endpoint."""'
        elif stripped.startswith('#'):
            # 注释行，只删 PUA 字符
            line = ''.join('' if (0xE000 <= ord(c) <= 0xF8FF or ord(c) == 0xFFFD) else c for c in line)
        elif "'" in stripped:
            # 字符串字面量中含 PUA，删掉 PUA 字符
            line = ''.join('' if (0xE000 <= ord(c) <= 0xF8FF or ord(c) == 0xFFFD) else c for c in line)
        else:
            # 其他情况，删掉 PUA 字符
            line = ''.join('' if (0xE000 <= ord(c) <= 0xF8FF or ord(c) == 0xFFFD) else c for c in line)
    out.append(line)

content = '\n'.join(out)

with open('app.py', 'w', encoding='utf-8') as f:
    f.write(content)

import py_compile
try:
    py_compile.compile('app.py', doraise=True)
    print('PASS')
except py_compile.PyCompileError as e:
    msg = str(e)
    print('FAIL (first error):')
    # Find remaining bad lines
    ls = open('app.py', encoding='utf-8', errors='replace').readlines()
    bad = [(i+1, l) for i, l in enumerate(ls) if any(0xE000 <= ord(c) <= 0xF8FF or ord(c) == 0xFFFD for c in l)]
    print('Remaining bad lines:', len(bad))
    for bn, bl in bad[:10]:
        print(' L' + str(bn) + ': ' + repr(bl[:80]))
