import os
from PyQt6.QtWidgets import QLabel, QWidget
from PyQt6.QtGui import QPixmap, QPalette, QColor
from PyQt6.QtCore import QMimeData, Qt
from PIL import Image, ImageQt

class Color(QWidget):

    def __init__(self, color):
        super(Color, self).__init__()
        self.setAutoFillBackground(True)
        
        palette = self.palette()
        
        if (isinstance(color, str)):
          self.str_color = True
          self.color = QColor(color)
          palette.setColor(QPalette.ColorRole.Window, self.color)
        else:
          self.str_color = False
          self.color = QColor(color[0], color[1], color[2], 255)
          palette.setColor(QPalette.ColorRole.Window, self.color)
        
        self.setPalette(palette)
    
    def setColor(self, color):
        palette = self.palette()
        
        if (isinstance(color, str)):
          self.str_color = True
          self.color = QColor(color)
          palette.setColor(QPalette.ColorRole.Window, self.color)
        else:
          self.str_color = False
          self.color = QColor(color[0], color[1], color[2], 255)
          palette.setColor(QPalette.ColorRole.Window, self.color)
        
        self.setPalette(palette)
    
    def getColor(self):
      return self.color.getRgb()
        
class GraphicsBucket(QLabel):
    def __init__(self, title, parent=None):
        super().__init__(title, None)
        self.setAcceptDrops(True)
        self.original_image = None
        self.alt_image = None
        self.using_original = True
        self.parent = parent
    
    def dragEnterEvent(self, e : QMimeData):
        # check to support drag/drop from MIME/web access
        if e.mimeData().hasImage():
            self.mime_type = 0 #web image
            e.accept()

        # check to support drag/drop from file system  
        elif e.mimeData().hasUrls() and len(e.mimeData().urls()) == 1:
            self.url = e.mimeData().urls()[0].toLocalFile()
            path, ext = os.path.splitext(self.url)
            if ext in ['.bmp', '.jpg', '.jpeg', '.png']:
                self.mime_type = 1 #from local file system
                e.accept()
            else:
                e.ignore()
        else:
            e.ignore()

    def dropEvent(self, e):
        if self.mime_type == 0:
            pixmap = QPixmap(e.mimeData().imageData())
            self.setPixmap(pixmap.scaled(self.width(), self.height(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
            self.original_image = ImageQt.fromqimage(pixmap.toImage())
            self.using_original = True
            self.parent.gfx_button_callback(True)
        elif self.mime_type == 1:
            try:
                image = Image.open(self.url)
                qtim = ImageQt.ImageQt(image)
                pixmap = QPixmap.fromImage(qtim)
                # eventually revisit this to scale based on the limiting dimension rather than warp the image entirely
                self.setPixmap(pixmap.scaled(self.width(), self.height(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
                self.original_image = image
                self.using_original = True
                self.parent.gfx_button_callback(True)
            except:
                return
      
    # add further support for user interaction triggers to change the displayed file
    def swap_images(self):
        to_use = self.alt_image if self.using_original else self.original_image
        qtim = ImageQt.ImageQt(to_use)
        pixmap = QPixmap.fromImage(qtim)
        # eventually revisit this to scale based on the limiting dimension rather than warp the image entirely
        self.setPixmap(pixmap.scaled(self.width(), self.height(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
        self.using_original = not self.using_original
        
    def clear_alt_image(self):
        self.alt_image = None
        if not self.using_original:
            qtim = ImageQt.ImageQt(self.original_image)
            pixmap = QPixmap.fromImage(qtim)
            # eventually revisit this to scale based on the limiting dimension rather than warp the image entirely
            self.setPixmap(pixmap.scaled(self.width(), self.height(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
            self.using_original = True
        
    def load_alt_image(self, image):
        self.alt_image = image
        qtim = ImageQt.ImageQt(self.alt_image)
        pixmap = QPixmap.fromImage(qtim)
        # eventually revisit this to scale based on the limiting dimension rather than warp the image entirely
        self.setPixmap(pixmap.scaled(self.width(), self.height(), aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio))
        self.using_original = False
      
if __name__ == '__main__':
  print('hello world')