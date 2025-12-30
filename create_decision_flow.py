"""
Tikun Olam - Decision Flow Diagram Generator
Genera el diagrama de flujo de decisión BinahSigma
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

# Configuración
fig, ax = plt.subplots(figsize=(14, 16), facecolor='#0A0E27')
ax.set_facecolor('#0A0E27')

# Helper para crear cajas
def create_box(ax, x, y, width, height, text, color, subtitle=''):
    box = FancyBboxPatch((x, y), width, height,
                          boxstyle="round,pad=0.02",
                          facecolor=color,
                          edgecolor='white',
                          linewidth=3,
                          transform=ax.transAxes)
    ax.add_patch(box)

    # Texto principal
    ax.text(x + width/2, y + height*0.65, text,
            ha='center', va='center', fontsize=24, color='white',
            weight='bold', transform=ax.transAxes)

    # Subtítulo
    if subtitle:
        ax.text(x + width/2, y + height*0.3, subtitle,
                ha='center', va='center', fontsize=14, color='white',
                transform=ax.transAxes, alpha=0.9)

# Helper para flechas
def create_arrow(ax, x1, y1, x2, y2, color='white', width=3):
    arrow = FancyArrowPatch((x1, y1), (x2, y2),
                            arrowstyle='->,head_width=0.6,head_length=0.4',
                            color=color, linewidth=width,
                            transform=ax.transAxes,
                            mutation_scale=30)
    ax.add_patch(arrow)

# NIVEL 1: Western y Eastern views
create_box(ax, 0.05, 0.85, 0.35, 0.12, 'WESTERN VIEW',
           '#3A86FF', 'Individual • Market Freedom')

create_box(ax, 0.6, 0.85, 0.35, 0.12, 'EASTERN VIEW',
           '#FB5607', 'Collective • Social Harmony')

# Flechas convergentes hacia BinahSigma
create_arrow(ax, 0.225, 0.85, 0.5, 0.72, '#3A86FF', 4)
create_arrow(ax, 0.775, 0.85, 0.5, 0.72, '#FB5607', 4)

# NIVEL 2: BinahSigma (destacado)
# Resplandor
glow = FancyBboxPatch((0.18, 0.62), 0.64, 0.15,
                       boxstyle="round,pad=0.03",
                       facecolor='#FF006E',
                       edgecolor='#FF006E',
                       linewidth=0,
                       alpha=0.3,
                       transform=ax.transAxes)
ax.add_patch(glow)

# Caja principal
create_box(ax, 0.2, 0.64, 0.6, 0.12, 'BinahSigma',
           '#FF006E', 'ADVERSARIAL ANALYSIS')

# Ícono sigma
ax.text(0.12, 0.7, 'Σ', ha='center', va='center',
        fontsize=64, color='#FF006E', weight='bold',
        transform=ax.transAxes, style='italic')

# Flecha hacia synthesis
create_arrow(ax, 0.5, 0.64, 0.5, 0.54, 'white', 5)

# NIVEL 3: Transcendent Synthesis
create_box(ax, 0.15, 0.43, 0.7, 0.15, 'TRANSCENDENT SYNTHESIS',
           '#8338EC', 'Competitive Dividend: $10B\nNeither West nor East Alone')

# Flecha hacia decisión
create_arrow(ax, 0.5, 0.43, 0.5, 0.33, '#06FFA5', 5)

# NIVEL 4: Final Decision
# Resplandor
glow2 = FancyBboxPatch((0.23, 0.2), 0.54, 0.12,
                        boxstyle="round,pad=0.02",
                        facecolor='#06FFA5',
                        edgecolor='#06FFA5',
                        linewidth=0,
                        alpha=0.4,
                        transform=ax.transAxes)
ax.add_patch(glow2)

create_box(ax, 0.25, 0.22, 0.5, 0.11, 'CONDITIONAL GO',
           '#06FFA5', 'Confidence: HIGH (78%)')

# Título superior
ax.text(0.5, 0.98, 'BinahSigma Decision Flow',
        ha='center', va='top', fontsize=36, color='white',
        weight='bold', transform=ax.transAxes)

# Subtítulo
ax.text(0.5, 0.94, 'Nvidia-Groq $20B M&A Analysis',
        ha='center', va='top', fontsize=18, color='#AAAAAA',
        transform=ax.transAxes)

# Información adicional (lateral)
info_texts = [
    ('75%', 'Divergence'),
    ('16', 'Blind Spots'),
    ('10.8 min', 'Duration')
]

y_start = 0.5
for value, label in info_texts:
    ax.text(0.92, y_start, value,
            ha='left', va='center', fontsize=24, color='#FF006E',
            weight='bold', transform=ax.transAxes)
    ax.text(0.92, y_start - 0.03, label,
            ha='left', va='center', fontsize=12, color='#AAAAAA',
            transform=ax.transAxes)
    y_start -= 0.12

# Firma
ax.text(0.98, 0.02, 'Tikun Olam - Ethical AI Observatory',
        ha='right', va='bottom', fontsize=10, color='#555555',
        transform=ax.transAxes, style='italic')

# Limpiar ejes
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Guardar
plt.tight_layout()
output_path = 'images/graphics/graphic_02_decision_flow.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0A0E27')
print(f"✅ Gráfico guardado en: {output_path}")
plt.show()
