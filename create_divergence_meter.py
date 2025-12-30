"""
Tikun Olam - Divergence Meter Graphic Generator
Genera el gráfico del medidor de divergencia civilizacional al 75%
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# Configuración de la figura
fig, ax = plt.subplots(figsize=(16, 9), facecolor='#0A0E27')
ax.set_facecolor('#0A0E27')

# Título principal
ax.text(0.5, 0.85, 'CIVILIZATIONAL DIVERGENCE DETECTED',
        ha='center', va='center', fontsize=48, color='#3A86FF',
        weight='bold', transform=ax.transAxes, family='sans-serif')

# Barra de progreso - Fondo
bar_bg = FancyBboxPatch((0.15, 0.45), 0.7, 0.12,
                         boxstyle="round,pad=0.01",
                         facecolor='#333333',
                         edgecolor='#555555',
                         linewidth=2,
                         transform=ax.transAxes)
ax.add_patch(bar_bg)

# Barra de progreso - Relleno (75%)
bar_fill = FancyBboxPatch((0.15, 0.45), 0.525, 0.12,  # 0.7 * 0.75 = 0.525
                          boxstyle="round,pad=0.01",
                          facecolor='#FF006E',
                          edgecolor='none',
                          transform=ax.transAxes)
ax.add_patch(bar_fill)

# Efecto de gradiente (simulado con rectángulos semi-transparentes)
gradient_overlay = FancyBboxPatch((0.15, 0.45), 0.525, 0.06,
                                  boxstyle="round,pad=0.01",
                                  facecolor='white',
                                  alpha=0.2,
                                  edgecolor='none',
                                  transform=ax.transAxes)
ax.add_patch(gradient_overlay)

# Etiqueta 75% - Grande y centrada
ax.text(0.5, 0.51, '75%', ha='center', va='center',
        fontsize=80, color='white', weight='bold',
        transform=ax.transAxes, family='sans-serif',
        bbox=dict(boxstyle='round,pad=0.3', facecolor='#0A0E27',
                  edgecolor='none', alpha=0.7))

# Marcadores de escala debajo de la barra
scale_data = [
    (0.15, 'LOW\n0%', '#06FFA5'),
    (0.35, 'MODERATE\n25%', '#FFD60A'),
    (0.575, 'HIGH\n50%', '#FB5607'),
    (0.85, 'EXTREME\n100%', '#FF006E')
]

for pos, label, color in scale_data:
    # Marcador vertical
    ax.plot([pos, pos], [0.42, 0.45], color=color, linewidth=2,
            alpha=0.6, transform=ax.transAxes)

    # Etiqueta
    ax.text(pos, 0.38, label, ha='center', va='top',
            fontsize=16, color='#AAAAAA', transform=ax.transAxes,
            weight='bold', family='sans-serif')

# Estadísticas de blind spots
ax.text(0.5, 0.25, '16 BLIND SPOTS IDENTIFIED',
        ha='center', va='center', fontsize=36, color='white',
        weight='bold', transform=ax.transAxes, family='sans-serif')

# Desglose Western vs Eastern
ax.text(0.35, 0.17, '8', ha='center', va='center',
        fontsize=48, color='#3A86FF', weight='bold',
        transform=ax.transAxes, family='sans-serif')
ax.text(0.35, 0.11, 'WESTERN', ha='center', va='center',
        fontsize=18, color='#AAAAAA', transform=ax.transAxes)

ax.text(0.5, 0.14, '•', ha='center', va='center',
        fontsize=32, color='#AAAAAA', transform=ax.transAxes)

ax.text(0.65, 0.17, '8', ha='center', va='center',
        fontsize=48, color='#FB5607', weight='bold',
        transform=ax.transAxes, family='sans-serif')
ax.text(0.65, 0.11, 'EASTERN', ha='center', va='center',
        fontsize=18, color='#AAAAAA', transform=ax.transAxes)

# Firma discreta
ax.text(0.98, 0.02, 'Tikun Olam - Ethical AI Observatory',
        ha='right', va='bottom', fontsize=12, color='#555555',
        transform=ax.transAxes, style='italic')

# Limpiar ejes
ax.set_xlim(0, 1)
ax.set_ylim(0, 1)
ax.axis('off')

# Guardar
plt.tight_layout()
output_path = 'images/graphics/graphic_01_divergence_meter_75.png'
plt.savefig(output_path, dpi=300, bbox_inches='tight', facecolor='#0A0E27')
print(f"✅ Gráfico guardado en: {output_path}")
plt.show()
