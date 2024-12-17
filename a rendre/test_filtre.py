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
    'Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 
    'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Grays', 'Greens', 'Greens_r', 'Greys', 
    'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 
    'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 
    'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 
    'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 
    'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 
    'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 
    'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 
    'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 
    'cubehelix', 'cubehelix_r', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 
    'gist_gray_r', 'gist_grey', 'gist_heat', 'gist_heat_r', 'gist_ncar', 'gist_ncar_r', 'gist_rainbow', 
    'gist_rainbow_r', 'gist_stern', 'gist_stern_r', 'gist_yarg', 'gist_yarg_r', 'gist_yerg', 'gnuplot', 
    'gnuplot2', 'gnuplot2_r', 'gnuplot_r', 'gray', 'gray_r', 'grey', 'hot', 'hot_r', 'hsv', 'hsv_r', 
    'inferno', 'inferno_r', 'jet', 'jet_r', 'magma', 'magma_r', 'nipy_spectral', 'nipy_spectral_r', 
    'ocean', 'ocean_r', 'pink', 'pink_r', 'plasma', 'plasma_r', 'prism', 'prism_r', 'rainbow', 
    'rainbow_r', 'seismic', 'seismic_r', 'spring', 'spring_r', 'summer', 'summer_r', 'tab10', 
    'tab10_r', 'tab20', 'tab20_r', 'tab20b', 'tab20b_r', 'tab20c', 'tab20c_r', 'terrain', 'terrain_r', 
    'turbo', 'turbo_r', 'twilight', 'twilight_r', 'twilight_shifted', 'twilight_shifted_r', 'viridis', 
    'viridis_r', 'winter', 'winter_r'
]


fig, ax = plt.subplots()
plt.subplots_adjust(left=0.25, right=0.9, top=0.9, bottom=0.3) 
im = ax.imshow(image, cmap='viridis')  
plt.colorbar(im, ax=ax)


slider_ax = plt.axes([0.25, 0.1, 0.6, 0.03], facecolor='lightgrey') 
slider = Slider(slider_ax, 'Index', 0, len(colormaps) - 1, valinit=0, valstep=1)


filter_text = plt.text(0.5, 0.15, f'Colormap: {colormaps[0]}', fontsize=12, ha='center', va='center', transform=fig.transFigure)


def update_colormap(val):
    cmap_index = int(slider.val)
    selected_cmap = colormaps[cmap_index]
    im.set_cmap(selected_cmap)
    filter_text.set_text(f'Colormap: {selected_cmap}')  
    plt.draw()


slider.on_changed(update_colormap)


plt.show()

