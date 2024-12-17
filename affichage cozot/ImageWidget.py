# uHDR: HDR image editing software
#   Copyright (C) 2022  remi cozot 
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
# hdrCore project 2020-2024
# author: remi.cozot@univ-littoral.fr

# import 
# -----------------------------------------------------------------------------
from __future__ import annotations
from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QPixmap, QImage, QResizeEvent
from PyQt6.QtCore import Qt
import numpy as np

# ------------------------------------------------------------------------------------------
# --- class ImageWidget(QWidget) -------------------------------------------------------
# ------------------------------------------------------------------------------------------
class ImageWidget(QWidget):

    def __init__(self: ImageWidget, colorData : np.ndarray|None = None) -> None:
        super().__init__()

        self.label : QLabel = QLabel(self)   # create a QtLabel for pixmap
        self.label.setAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignVCenter)

        if not isinstance(colorData, np.ndarray): colorData = ImageWidget.emptyImageColorData()
        self.imagePixmap : QPixmap
        self.setPixmap(colorData)  

    # methods
    # -------------------------------------------------- 
    def resize(self : ImageWidget)-> None:
        self.label.resize(self.size())
        self.label.setPixmap(self.imagePixmap.scaled(self.size(),Qt.AspectRatioMode.KeepAspectRatio))

    # -------------------------------------------------- 
    def resizeEvent(self : ImageWidget, event :QResizeEvent)-> None:
        self.resize()
        super().resizeEvent(event)

    # -------------------------------------------------- 
    def setPixmap(self: ImageWidget, colorData :  np.ndarray|None = None) -> QPixmap:
        if not isinstance(colorData, np.ndarray): colorData = ImageWidget.emptyImageColorData()

        height, width , channel  = colorData.shape   
        bytesPerLine = channel * width

        # clip
        colorData[colorData>1.0] = 1.0
        colorData[colorData<0.0] = 0.0

        qImg : QImage= QImage(bytes((colorData*255).astype(np.uint8)), width, height, bytesPerLine, QImage.Format.Format_RGB888) # QImage
        self.imagePixmap : QPixmap = QPixmap.fromImage(qImg)
        self.resize()

        return self.imagePixmap

    # -------------------------------------------------- 
    def setQPixmap(self: ImageWidget, qPixmap : QPixmap)-> None:
        self.imagePixmap = qPixmap
        self.resize()

    # -------------------------------------------------- 
    @staticmethod
    def emptyImageColorData()-> np.ndarray: return np.ones((90,160,3))*(220/255) 

# -------------------------------------------------------------------------------------------
if __name__ == '__main__':
    import sys
    from PyQt6.QtWidgets import QApplication
    
    import colour, imageio

    imageio.plugins.freeimage.download()


    img : np.ndarray = colour.read_image('./image.jpg', bit_depth='float32', method='Imageio')/1.0
    
    app : QApplication = QApplication(sys.argv)
    iW : ImageWidget = ImageWidget(img)
    iW.setMinimumHeight(200)
    iW.show()

    sys.exit(app.exec())