from astropy.io import fits
import matplotlib.pyplot as plt
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

plt.imshow(image, origin='lower')
plt.colorbar()
plt.show()
