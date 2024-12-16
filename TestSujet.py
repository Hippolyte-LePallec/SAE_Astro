from astropy.io import fits
import matplotlib.pyplot as plt

#Charger le fichier FITS
data=fits.getdata('./Tarantula_Nebula-oiii.fit')

#Afficher l’image
plt.imshow(data, cmap = 'gray')
plt.colorbar()
plt.show()