"""Build the self-contained profile SVG; no runtime JavaScript or remote assets."""
from pathlib import Path
from base64 import b64encode
from html import escape
from PIL import ImageFont

ROOT = Path(__file__).resolve().parent
DESCRIPTION = (
    'Electronics Engineering student specializing in Embedded Firmware, '
    'Edge AI/ML, and RTOS, with hands-on work in MCU development, FPGA '
    'acceleration, neural network optimization, real-time systems, and '
    'hardware-software co-design.'
)
font = ImageFont.truetype('C:/Windows/Fonts/segoeui.ttf', 19)
words = []
x, y = 40.0, 143
for index, word in enumerate(DESCRIPTION.split()):
    width = font.getlength(word)
    if word in {'Edge', 'FPGA'} or (word == 'and' and DESCRIPTION.split()[index + 1] == 'hardware-software'):
        x, y = 40.0, y + 28
    assert x + width <= 692, 'Description exceeds its line width'
    words.append(
        f'<text class="word" x="{x:.2f}" y="{y}" '
        f'style="animation-delay:{0.2 + index * 0.026:.3f}s">'
        f'{escape(word)}</text>'
    )
    x += width + font.getlength(' ')
assert y <= 255, 'Description exceeds its layout area'
photo = b64encode((ROOT / 'assets/ME.png').read_bytes()).decode('ascii')
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1144" height="344" viewBox="0 0 1144 344" role="img" aria-labelledby="title description">
  <title id="title">Priyadarsan D — Electronics Engineering</title>
  <desc id="description">{escape(DESCRIPTION)}</desc>
  <style>
    .word {{ font: 19px 'Segoe UI', sans-serif; fill: #c3c3ca;
      animation: enter 600ms cubic-bezier(.16,1,.3,1) both; }}
    @keyframes enter {{ from {{ opacity: 0; transform: translateY(10px); }}
      to {{ opacity: 1; transform: translateY(0); }} }}
    @media (prefers-reduced-motion: reduce) {{ .word {{ animation: none; }} }}
  </style>
  <rect width="1144" height="344" fill="#000"/>
  <image x="690" y="-17" width="454" height="406" href="data:image/png;base64,{photo}"/>
  <rect x="40" y="28" width="27" height="3" rx="1.5" fill="#ff3333"/>
  <text x="80" y="34" fill="#a8a8ad" font-family="Consolas, monospace" font-size="12" letter-spacing="2">HI, I'M</text>
  <text x="37" y="99" fill="#f5f5f7" font-family="Segoe UI, sans-serif" font-size="53" font-weight="700" letter-spacing="-1.7">Priyadarsan D<tspan fill="#ff3333">.</tspan></text>
  {''.join(words)}
  <line x1="40" y1="285" x2="684" y2="285" stroke="#292929"/>
  <text x="40" y="316" fill="#eeeeef" font-family="Consolas, monospace" font-size="13" letter-spacing="0.8">EMBEDDED FIRMWARE <tspan fill="#ff3333">/</tspan> EDGE AI/ML <tspan fill="#ff3333">/</tspan> RTOS <tspan fill="#ff3333">/</tspan> VLSI</text>
</svg>
'''
(ROOT / 'assets/intro.svg').write_text(svg, encoding='utf-8')
(ROOT / 'README.md').write_text(
    '<p align="center">\n'
    f'  <img src="assets/intro.svg" alt="{escape(DESCRIPTION, quote=True)}" width="1144">\n'
    '</p>\n', encoding='utf-8'
)
print(f'Built 1144 x 344 banner; {len(words)} words; last line at y={y}.')
