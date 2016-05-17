from PIL import Image
import sys
from PyQt4 import QtGui, QtCore
import math


def pil2qpixmap(pil_image):
    w, h = pil_image.size
    data = pil_image.tostring("raw", "BGRX")
    qimage = QtGui.QImage(data, w, h, QtGui.QImage.Format_RGB32)
    qpixmap = QtGui.QPixmap(w, h)
    pix = QtGui.QPixmap.fromImage(qimage)
    return pix


class GuiMain(QtGui.QWidget):
    def __init__(self):
        super(GuiMain, self).__init__()

        self.loadedFilename = ""
        self.step = 1
        self.dialog_open_img = QtGui.QFileDialog()
        self.textfield_angle_slider = QtGui.QLineEdit()
        self.btn_open = QtGui.QPushButton("Select image")
        self.scale_angle_step = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.btn_save = QtGui.QPushButton("Save")
        self.label_angle_step = QtGui.QLabel("Select angle steps (deg)")
        self.label_num_sprites_l = QtGui.QLabel("Number of sprites: ")
        self.label_num_sprites_v = QtGui.QLabel("0")
        self.btn_generate_sheet = QtGui.QPushButton("Generate")

        self.vbox_l = QtGui.QVBoxLayout()
        self.hbox_l_angle_selector = QtGui.QHBoxLayout()
        self.vbox_r = QtGui.QVBoxLayout()
        self.hbox = QtGui.QHBoxLayout()
        self.img_out = None
        self.loaded_pixmap = None

        self.init_ui()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def showDialog(self):
        self.loaded_filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '~', "Image files (*.jpg *.gif)")
        print "Loaded: " + self.loadedFilename
        self.loaded_pixmap = QtGui.QPixmap(self.loaded_filename)
        self.loaded_pixmap = self.loaded_pixmap.scaledToHeight(100)
        self.label_loaded_img.setPixmap(self.loaded_pixmap)

    def generate_spritesheet(self):

        if self.loaded_pixmap is None:
            msg_box = QtGui.QMessageBox()
            msg_box.setText("Trying to create spritesheet when no image loaded.")
            msg_box.exec_()
            return

        # load image into PIL image for manipulation
        pil_img_loaded = Image.open(self.loadedFilename)
        x, y = 0, 0
        width, height = pil_img_loaded.size
        width_step = math.floor(math.sqrt(self.step))

        height_step = width_step
        if math.sqrt(self.step) - width_step > 0:
            height_step = height_step + 1

        out_width, out_height = (width * width_step, height * height_step)
        self.img_out = Image.new(mode="RGBA", size=(out_width, out_height))

        w_count = 0
        h_count = 0
        for i in range(0, 360, self.step):
            tmpImg = pil_img_loaded.copy()
            tmpImg.rotate(i)

            x_pos = w_count * width
            y_pos = h_count * height

            self.img_out.paste(tmpImg, (x_pos, y_pos, width, height))

            w_count += 1
            h_count += 1

            if w_count > width_step:
                w_count = 0

    def onClick(self):
        print "Hi"

    def sliderChange(self, value):
        self.textfield_angle_slider.setText(str(value))
        self.label_num_sprites_v.setText(str(360 / value))
        self.step = 360 / value
        #self.generate_spritesheet(360 / value)

    def textFieldChanged(self, value):
        self.scale_angle_step.setValue(int(value))

    def init_ui(self):

        # open source file button
        self.btn_open.clicked.connect(self.showDialog)

        # file chooser dialog
        self.dialog_open_img.setFileMode(QtGui.QFileDialog.AnyFile)

        # angle step slider
        self.scale_angle_step.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scale_angle_step.setMinimum(1)
        self.scale_angle_step.setMaximum(90)
        #self.scale_angle_step.setGeometry(30, 40, 100, 30)
        self.scale_angle_step.valueChanged[int].connect(self.sliderChange)

        # angle step text field
        self.textfield_angle_slider.setText("1")
        self.textfield_angle_slider.textChanged[str].connect(self.textFieldChanged)

        # loaded image
        self.label_loaded_img = QtGui.QLabel("Image goes here.")
        self.label_loaded_img.setFixedHeight(100)

        self.btn_generate_sheet.clicked.connect(self.generate_spritesheet)

        # left side - select image and angle steps
        self.vbox_l.addWidget(self.btn_open)
        self.vbox_l.addWidget(self.label_angle_step)

        self.hbox_l_angle_selector.addWidget(self.scale_angle_step)
        self.hbox_l_angle_selector.addWidget(self.textfield_angle_slider)
        self.hbox_l_angle_selector.addStretch(1)

        #self.hbox_l_num_sprites = QtGui.QHBoxLayout()
        #self.hbox_l_num_sprites.addWidget()

        self.vbox_l.addLayout(self.hbox_l_angle_selector)

        self.vbox_l.addWidget(self.label_num_sprites_l)
        self.vbox_l.addWidget(self.label_num_sprites_v)
        self.vbox_l.addWidget(self.label_loaded_img)
        self.vbox_l.addWidget(self.btn_generate_sheet)


        self.vbox_l.addStretch(1)

        # right side - preview and save
        self.vbox_r.addStretch(1)
        self.vbox_r.addWidget(self.btn_save)

        self.hbox.addLayout(self.vbox_l)
        self.hbox.addLayout(self.vbox_r)

        self.setLayout(self.hbox)

        # self.setGeometry(300, 300, 800, 150)
        self.setWindowTitle('Rotated Spritesheet Creator by l33tllama')
        self.center()
        self.show()


def main():
    app = QtGui.QApplication(sys.argv)
    ex = GuiMain()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
