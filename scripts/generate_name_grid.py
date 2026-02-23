import os
import hashlib

NAME = os.getenv("NAME", "Kevin Rivera")

W, H = 1200, 320
CELL = 24
MARGIN = 12

FONT = "Fira Code, ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, 'Liberation Mono', 'Courier New', monospace"
FONT_SIZE = 72

# Aproximación del ancho de cada caracter en monospace (se ve bien en práctica)
CHAR_W = FONT_SIZE * 0.62
TEXT_W = max(320, int(len(NAME) * CHAR_W))

START_X = int((W - TEXT_W) / 2)
BASELINE_Y = int(H / 2 + FONT_SIZE * 0.35)

def cell_color(cx, cy):
    # Patrón determinístico para que parezca "grid viva" sin random real
    h = hashlib.md5(f"{cx},{cy}".encode()).hexdigest()
    v = int(h[:2], 16)
    if v % 23 == 0:
        return "#1a1a1a"  # highlight ocasional
    return "#101010" if (cx + cy) % 2 == 0 else "#121212"

cols = (W - 2*MARGIN) // CELL
rows = (H - 2*MARGIN) // CELL

grid_rects = []
for r in range(rows):
    for c in range(cols):
        x = MARGIN + c * CELL
        y = MARGIN + r * CELL
        fill = cell_color(c, r)
        grid_rects.append(
            f'<rect x="{x}" y="{y}" width="{CELL-2}" height="{CELL-2}" rx="4" fill="{fill}" stroke="#1e1e1e" stroke-width="1" />'
        )

# Animación tipo "escritura": revelamos el texto con un clip que crece
DUR = "6s"
HOLD = "0.82"  # cuánto tiempo se queda mostrado antes de reset
TYPE = "0.34"  # porcentaje en el que termina de "escribirse"

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{NAME}">
  <defs>
    <linearGradient id="vignette" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="#000" stop-opacity="0.35"/>
      <stop offset="0.5" stop-color="#000" stop-opacity="0"/>
      <stop offset="1" stop-color="#000" stop-opacity="0.35"/>
    </linearGradient>

    <clipPath id="reveal">
      <rect x="{START_X}" y="{BASELINE_Y - FONT_SIZE}" width="0" height="{int(FONT_SIZE*1.35)}" rx="10">
        <animate attributeName="width"
                 dur="{DUR}" repeatCount="indefinite"
                 values="0;{TEXT_W};{TEXT_W};0"
                 keyTimes="0;{TYPE};{HOLD};1"
                 calcMode="linear" />
      </rect>
    </clipPath>

    <filter id="softGlow" x="-20%" y="-50%" width="140%" height="200%">
      <feGaussianBlur stdDeviation="2" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="#0b0b0b"/>
  {"".join(grid_rects)}
  <rect width="{W}" height="{H}" fill="url(#vignette)"/>

  <!-- Texto -->
  <g clip-path="url(#reveal)">
    <text x="{START_X}" y="{BASELINE_Y}"
          font-family="{FONT}" font-size="{FONT_SIZE}" font-weight="700"
          fill="#ffffff" filter="url(#softGlow)">{NAME}</text>
  </g>

  <!-- Cursor -->
  <rect x="{START_X}" y="{BASELINE_Y - int(FONT_SIZE*0.90)}" width="10" height="{int(FONT_SIZE*1.05)}" rx="3" fill="#ffffff">
    <animate attributeName="x"
             dur="{DUR}" repeatCount="indefinite"
             values="{START_X};{START_X + TEXT_W};{START_X + TEXT_W};{START_X}"
             keyTimes="0;{TYPE};{HOLD};1"
             calcMode="linear" />
    <animate attributeName="opacity"
             dur="0.9s" repeatCount="indefinite"
             values="1;0;1" />
  </rect>

  <!-- Borde suave -->
  <rect x="6" y="6" width="{W-12}" height="{H-12}" rx="18" fill="none" stroke="#1f1f1f" stroke-width="2"/>
</svg>
'''

os.makedirs("dist", exist_ok=True)
with open("dist/name-grid.svg", "w", encoding="utf-8") as f:
    f.write(svg)

print("Generated dist/name-grid.svg")
