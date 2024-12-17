from astropy.io import fits
import matplotlib.pyplot as plt

#Charger le fichier FITS
data=fits.getdata('Tarantula-20241216/Tarantula/Tarantula_Nebula-halpha.fit')

#Afficher l’image
plt.imshow(data, cmap = 'flag_r')
plt.colorbar()
plt.show()