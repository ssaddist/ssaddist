#!/usr/bin/env python3
import html
import os

# Пути к файлам
ASCII_ART_FILE = os.path.join(os.path.dirname(__file__), 'ascii_art.txt')
OUTPUT_SVG = os.path.join(os.path.dirname(__file__), 'card.svg')

with open(ASCII_ART_FILE, 'r', encoding='utf-8') as f:
    ascii_lines = [l.rstrip('\r\n') for l in f]

# Сбалансированная геометрия SVG карточки (симметричные отступы)
svg_w = 950
svg_h = 530

# Позиционирование ASCII арта (слева)
art_x = 22
art_y_start = 24
art_line_h = 7.42
art_text_len = 430

# Позиционирование терминальной информации (справа)
text_x = 480
text_y_start = 78
text_line_h = 32
TARGET_LINE_LEN = 44

def esc(s):
    return html.escape(str(s))

def make_tspan(key, val, target=TARGET_LINE_LEN):
    prefix_len = 2 + len(key) + 1  # '. ' + key + ':'
    needed = target - prefix_len - len(val) - 2  # пробелы вокруг точек
    if needed < 2:
        needed = 2
    dots = '.' * needed

    if '.' in key:
        k1, k2 = key.split('.', 1)
        key_html = f'<tspan class="key">{esc(k1)}</tspan>.<tspan class="key">{esc(k2)}</tspan>'
    else:
        key_html = f'<tspan class="key">{esc(key)}</tspan>'

    return f'<tspan class="cc">. </tspan>{key_html}:<tspan class="cc"> {dots} </tspan><tspan class="value">{esc(val)}</tspan>'

# Данные для карточки
DATA = [
    ('header', 'ssaddist@github', TARGET_LINE_LEN),
    ('kv', 'OS', 'macOS'),
    ('kv', 'Kernel', 'Software Engineer'),
    ('kv', 'IDE', 'VS Code'),
    ('gap',),
    ('header', '- Languages', TARGET_LINE_LEN),
    ('kv', 'Languages.Web', 'JS / TS'),
    ('kv', 'Languages.Backend', 'C#, Java, Python'),
    ('gap',),
    ('header', '- Contact', TARGET_LINE_LEN),
    ('kv', 'Email.Personal', 'alexkholin09@gmail.com'),
    ('kv', 'Telegram', '@s_s_a_d_d'),
    ('kv', 'Discord', 'ssadd.'),
]

svg = []
svg.append('<?xml version="1.0" encoding="UTF-8"?>')
svg.append(f'<svg xmlns="http://www.w3.org/2000/svg" font-family="ConsolasFallback, Consolas, ui-monospace, SFMono-Regular, Menlo, Monaco, monospace" width="{svg_w}px" height="{svg_h}px" viewBox="0 0 {svg_w} {svg_h}">')
svg.append('<style>')
svg.append('''
@font-face {
  src: local('Consolas'), local('Consolas Bold'), local('Menlo'), local('Monaco');
  font-family: 'ConsolasFallback';
  font-display: swap;
}
.key { fill: #ffa657; }
.value { fill: #a5d6ff; }
.cc { fill: #616e7f; }
.header { fill: #c9d1d9; font-weight: bold; }
.dash { fill: #616e7f; }
.ascii { font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace; font-size: 7.2px; fill: #c9d1d9; }
.info { font-family: ConsolasFallback, Consolas, ui-monospace, SFMono-Regular, Menlo, Monaco, monospace; font-size: 14.5px; fill: #c9d1d9; }
text, tspan { white-space: pre; }
''')
svg.append('</style>')

# Прямоугольник БЕЗ скруглений (прямые углы)
svg.append(f'<rect width="{svg_w}px" height="{svg_h}px" fill="#161b22" stroke="#30363d" stroke-width="1.5" />')

# ASCII Art слева
svg.append('<text class="ascii" xml:space="preserve">')
for i, line in enumerate(ascii_lines):
    y = art_y_start + i * art_line_h
    svg.append(f'  <tspan x="{art_x}" y="{y:.1f}" textLength="{art_text_len}" lengthAdjust="spacing">{esc(line)}</tspan>')
svg.append('</text>')

# Информация справа
svg.append('<text class="info" xml:space="preserve">')
curr_y = text_y_start
for item in DATA:
    if item[0] == 'gap':
        curr_y += text_line_h * 0.4
        continue
    elif item[0] == 'header':
        title = item[1]
        target = item[2]
        dashes = '-' * (target - len(title) - 1)
        svg.append(f'  <tspan x="{text_x}" y="{curr_y:.1f}"><tspan class="header">{esc(title)}</tspan> <tspan class="dash">{dashes}</tspan></tspan>')
    elif item[0] == 'kv':
        line_content = make_tspan(item[1], item[2], TARGET_LINE_LEN)
        svg.append(f'  <tspan x="{text_x}" y="{curr_y:.1f}">{line_content}</tspan>')
    curr_y += text_line_h
svg.append('</text>')
svg.append('</svg>')

with open(OUTPUT_SVG, 'w', encoding='utf-8') as f:
    f.write('\n'.join(svg))

print(f"Generated {OUTPUT_SVG} ({svg_w}x{svg_h}) successfully!")
