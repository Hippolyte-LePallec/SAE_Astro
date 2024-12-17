from astropy.io import fits
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import numpy as np


image1 = './Tarantula-20241216/Tarantula/Tarantula_Nebula-halpha.fit'
image2 = './Tarantula-20241216/Tarantula/Tarantula_Nebula-oiii.fit'
image3 = './Tarantula-20241216/Tarantula/Tarantula_Nebula-sii.fit'

data1 = fits.getdata(image1)
data2 = fits.getdata(image2)
data3 = fits.getdata(image3)


vmin_r, vmax_r = np.percentile(data1, (1, 99))
data1_norm = np.clip((data1 - vmin_r) / (vmax_r - vmin_r), 0, 1)

vmin_g, vmax_g = np.percentile(data2, (1, 99))
data2_norm = np.clip((data2 - vmin_g) / (vmax_g - vmin_g), 0, 1)

vmin_b, vmax_b = np.percentile(data3, (1, 99))
data3_norm = np.clip((data3 - vmin_b) / (vmax_b - vmin_b), 0, 1)


image = np.stack([data1_norm, data2_norm, data3_norm], axis=-1)


colormaps = [
    'viridis', 'plasma', 'inferno', 'magma', 'cividis', 'Greys', 'Purples', 'Blues', 
    'Greens', 'Oranges', 'Reds', 'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu', 
    'GnBu', 'PuBu', 'YlGnBu', 'BuGn', 'YlGn'
]


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, right=0.9, top=0.9, bottom=0.3)
im = ax.imshow(image, cmap=colormaps[0]) 
plt.colorbar(im, ax=ax)


filter_text = plt.text(
    0.5, 0.15, f'Colormap: {colormaps[0]}', fontsize=12, ha='center', va='center', transform=fig.transFigure
)


slider_ax = plt.axes([0.25, 0.1, 0.6, 0.03], facecolor='lightgrey')  
slider = Slider(slider_ax, 'Index', 0, len(colormaps) - 1, valinit=0, valstep=1)  


def update_colormap(val):
    """Met à jour la colormap en fonction de la valeur du slider."""
    cmap_index = int(slider.val)
    selected_cmap = colormaps[cmap_index]
    im.set_cmap(selected_cmap)
    filter_text.set_text(f'Colormap: {selected_cmap}')  
    plt.draw()


slider.on_changed(update_colormap)  

plt.show()



#on a remarquer que ce n'etais pas possible de modifier la colormap d'une image en 3D comme celle-ci on vas donc reflechir a une autre approche 