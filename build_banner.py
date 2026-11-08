"""Build the self-contained profile SVG; no runtime JavaScript or remote assets."""
from pathlib import Path
from base64 import b64encode
from html import escape
from PIL import Image, ImageFont
from random import Random

ROOT = Path(__file__).resolve().parent
NAME = 'Priyadharsan D'
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
# Sample the silhouette to anchor vector particles to the actual portrait edge.
# The original photo stays intact; only the surrounding SVG dots move.
source = Image.open(ROOT / 'assets/ME.png').convert('RGB')
random = Random(14)
particles = []
for row in range(125, source.height - 40, 27):
    lit = [col for col in range(source.width)
           if max(source.getpixel((col, row))) > 100]
    if len(lit) < 4:
        continue
    for edge, direction in [(lit[0], -1), (lit[-1], 1)]:
        px = 690 + edge / source.width * 454
        py = -17 + row / source.height * 406
        if not (725 < px < 1120 and 8 < py < 334):
            continue
        red, green, blue = source.getpixel((edge, row))
        color = '#ff3333' if red > green * 1.5 else '#d9d9df'
        particles.append(
            f'<circle class="particle" cx="{px:.2f}" cy="{py:.2f}" '
            f'r="{random.uniform(.55, 1.25):.2f}" fill="{color}" '
            f'style="--dx:{direction * random.uniform(9, 29):.2f}px; '
            f'--dy:{random.uniform(-22, -6):.2f}px; '
            f'animation-delay:-{random.uniform(0, 5):.2f}s"/>'
        )
bot_shapes = [
    ('#ff493d', 'M0 -25 C14 -25 25 -14 25 0 C25 14 14 25 0 25 C-14 25 -25 14 -25 0 C-25 -14 -14 -25 0 -25 Z'),
    ('#00bba8', 'M0 -25 C24 -25 25 -24 25 0 C25 24 24 25 0 25 C-24 25 -25 24 -25 0 C-25 -24 -24 -25 0 -25 Z'),
    ('#ff2d9c', 'M0 -27 C6 -27 20 -4 25 13 C30 25 11 25 0 25 C-11 25 -30 25 -25 13 C-20 -4 -6 -27 0 -27 Z'),
    ('#ff9800', 'M0 -24 C18 -33 22 -9 26 0 C36 17 12 18 0 26 C-16 32 -21 13 -25 0 C-32 -17 -15 -28 0 -24 Z'),
    ('#9355ff', 'M0 -28 C6 -28 28 -6 28 0 C28 6 6 28 0 28 C-6 28 -28 6 -28 0 C-28 -6 -6 -28 0 -28 Z'),
    ('#1485ff', 'M0 -24 C19 -24 27 -15 27 0 C27 15 19 24 0 24 C-19 24 -27 15 -27 0 C-27 -15 -19 -24 0 -24 Z'),
]
bot_frames = []
for index, (color, shape) in enumerate(bot_shapes):
    bot_frames.append(f'{index / 6 * 100:.3f}%, {(index + .72) / 6 * 100:.3f}% '
                      f'{{ fill: {color}; d: path("{shape}"); }}')
bot_frames.append(f'100% {{ fill: {bot_shapes[0][0]}; d: path("{bot_shapes[0][1]}"); }}')
bot_styles = '''
    .bot-motion { animation: bot-react var(--cycle) ease-in-out infinite; }
    .bot-body { animation: bot-morph var(--cycle) ease-in-out infinite; }
    .bot-eye { fill: #fff; transform-box: fill-box; transform-origin: center; }
    .bot-eye-left { animation: eye-left var(--cycle) ease-in-out infinite; }
    .bot-eye-right { animation: eye-right var(--cycle) ease-in-out infinite; }
    .bot-mouth { fill: #fff; transform-box: fill-box; transform-origin: center;
      animation: mouth-react var(--cycle) ease-in-out infinite; }
    @keyframes bot-react {
      0%,100% { transform: translateY(0) rotate(0deg); }
      16.667% { transform: translateY(-4px) rotate(-9deg); }
      33.333% { transform: translateY(0) rotate(7deg); }
      50% { transform: translateY(-5px) rotate(-5deg); }
      66.667% { transform: translateY(1px) rotate(8deg); }
      83.333% { transform: translateY(-4px) rotate(-7deg); }
    }
    @keyframes eye-left {
      0%,12%,100% { transform: scaleY(1); }
      17%,29% { transform: scaleY(.35) rotate(-12deg); }
      34%,46% { transform: scale(1.2); }
      51%,62% { transform: scaleY(.15); }
      67%,79% { transform: scaleY(.55) rotate(12deg); }
      84%,96% { transform: scaleY(.45) rotate(-18deg); }
    }
    @keyframes eye-right {
      0%,12%,100% { transform: scaleY(1); }
      17%,29% { transform: scaleY(.35) rotate(12deg); }
      34%,46% { transform: scale(1.2); }
      51%,62% { transform: scaleY(1); }
      67%,79% { transform: scaleY(.55) rotate(-12deg); }
      84%,96% { transform: scaleY(.45) rotate(18deg); }
    }
    @keyframes mouth-react {
      0%,12%,100% { transform: scale(.8,.5); }
      17%,29% { transform: scale(1.6,.55); }
      34%,46% { transform: scale(1,1.8); }
      51%,62% { transform: scale(1.2,.5); }
      67%,79% { transform: scale(.6,.4); }
      84%,96% { transform: scale(1.5,1.1); }
    }
'''
tech_labels = []
tech_styles = []
tech_font = ImageFont.truetype('C:/Windows/Fonts/consola.ttf', 13)
tech_x = 40.0
for index, label in enumerate(['EMBEDDED FIRMWARE', 'EDGE AI/ML', 'RTOS', 'VLSI']):
    tech_labels.append(f'<text class="tech-label" x="{tech_x:.2f}" y="316" '
                       f'style="animation-name:tech-{index}">{label}</text>')
    start = 6 + index * 10
    tech_styles.append(f'@keyframes tech-{index} {{ '
                       f'0%, {start}%, {start + 24}%, 100% {{ transform: translateY(0); fill: #eeeeef; }} '
                       f'{start + 10}% {{ transform: translateY(-5px); fill: #ff5555; }} }}')
    tech_x += tech_font.getlength(label) + len(label) * .8 + 12
    if index < 3:
        tech_labels.append(f'<text x="{tech_x:.2f}" y="316" fill="#ff3333">/</text>')
        tech_x += tech_font.getlength('/') + .8 + 12
svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1144" height="344" viewBox="0 0 1144 344" role="img" aria-labelledby="title description">
  <title id="title">{NAME} — Electronics Engineering</title>
  <desc id="description">{escape(DESCRIPTION)}</desc>
  <style>
    svg {{ --cycle: 5s; }}
    {bot_styles.strip()}
    {''.join(tech_styles)}
    .greeting-mask {{ animation: greeting-type var(--cycle) steps(7, end) infinite; }}
    @keyframes greeting-type {{
      0%, 100% {{ width: 0; }}
      20%, 84% {{ width: 130px; }}
    }}
    .profile-name {{ transform-origin: 37px 99px;
      animation: name-reveal var(--cycle) cubic-bezier(.16,1,.3,1) infinite; }}
    @keyframes name-reveal {{
      0%,100% {{ opacity: .35; transform: translateY(7px) scale(.98); }}
      16%,82% {{ opacity: 1; transform: translateY(0) scale(1); }}
    }}
    .name-ink {{ animation: name-shine var(--cycle) ease-in-out infinite; }}
    @keyframes name-shine {{
      0%,42%,78%,100% {{ fill: #f5f5f7; }}
      60% {{ fill: #ff7373; }}
    }}
    .tech-label {{ animation-duration: var(--cycle); animation-timing-function: ease-in-out;
      animation-iteration-count: infinite; }}
    @keyframes bot-morph {{ {''.join(bot_frames)} }}
    .word {{ font: 19px 'Segoe UI', sans-serif; fill: #c3c3ca;
      animation: enter var(--cycle) cubic-bezier(.16,1,.3,1) infinite both; }}
    @keyframes enter {{
      0% {{ opacity: 0; transform: translateY(10px); }}
      10%, 82% {{ opacity: 1; transform: translateY(0); }}
      94%, 100% {{ opacity: 0; transform: translateY(-8px); }}
    }}
    .particle {{ opacity: 0; animation: float-out var(--cycle) ease-in-out infinite; }}
    @keyframes float-out {{
      0% {{ opacity: 0; transform: translate(0,0); }}
      22% {{ opacity: .75; }}
      100% {{ opacity: 0; transform: translate(var(--dx), var(--dy)); }}
    }}
    @media (prefers-reduced-motion: reduce) {{
      .word {{ animation: none; opacity: 1; }}
      .particle {{ animation: none; opacity: 0; }}
      .bot-motion, .bot-body, .bot-eye, .bot-mouth {{ animation: none; }}
      .greeting-mask {{ animation: none; width: 130px; }}
      .profile-name, .name-ink, .tech-label {{ animation: none; }}
    }}
  </style>
  <defs><clipPath id="greeting-clip"><rect class="greeting-mask" x="80" y="19" width="130" height="20"/></clipPath></defs>
  <rect width="1144" height="344" fill="#000"/>
  <image x="690" y="-17" width="454" height="406" href="data:image/png;base64,{photo}"/>
  <g aria-hidden="true">{''.join(particles)}</g>
  <rect x="40" y="28" width="27" height="3" rx="1.5" fill="#ff3333"/>
  <text clip-path="url(#greeting-clip)" x="80" y="34" fill="#a8a8ad" font-family="Consolas, monospace" font-size="12" letter-spacing="2">HI, I'M</text>
  <g class="profile-name"><text class="name-ink" x="37" y="99" fill="#f5f5f7" font-family="Segoe UI, sans-serif" font-size="53" font-weight="700" letter-spacing="-1.7">{NAME}<tspan fill="#ff3333">.</tspan></text></g>
  <g id="bot" transform="translate(645 70)" aria-hidden="true">
    <g class="bot-motion">
      <path class="bot-body" fill="{bot_shapes[0][0]}" d="{bot_shapes[0][1]}"/>
      <rect class="bot-eye bot-eye-left" x="-12" y="-9" width="6" height="14" rx="3"/>
      <rect class="bot-eye bot-eye-right" x="6" y="-9" width="6" height="14" rx="3"/>
      <ellipse class="bot-mouth" cx="0" cy="12" rx="3" ry="2"/>
    </g>
  </g>
  {''.join(words)}
  <line x1="40" y1="285" x2="684" y2="285" stroke="#292929"/>
  <g fill="#eeeeef" font-family="Consolas, monospace" font-size="13" letter-spacing="0.8">{''.join(tech_labels)}</g>
</svg>
'''
(ROOT / 'assets/intro.svg').write_text(svg, encoding='utf-8')
(ROOT / 'README.md').write_text(
    '<p align="center">\n'
    f'  <img src="assets/intro.svg" alt="{NAME}. {escape(DESCRIPTION, quote=True)}" width="1144">\n'
    '</p>\n', encoding='utf-8'
)
print(f'Built 1144 x 344 banner; {len(words)} words; {len(particles)} edge particles.')
