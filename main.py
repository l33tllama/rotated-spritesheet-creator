from PIL import Image, ImageQt
import sys
from PyQt4 import QtGui, QtCore
import math

class GuiMain(QtGui.QWidget):

    def __init__(self):
        super(GuiMain, self).__init__()

        self.loaded_filename = ""
        self.step = 1
        self.angle = 0
        self.dialog_open_img = QtGui.QFileDialog()
        self.textfield_angle_slider = QtGui.QLineEdit()
        self.btn_open = QtGui.QPushButton("Select image")
        self.scale_angle_step = QtGui.QSlider(QtCore.Qt.Horizontal, self)

        self.label_angle_step = QtGui.QLabel("Select angle steps (deg)")
        self.label_num_sprites_l = QtGui.QLabel("Number of sprites: ")
        self.label_num_sprites_v = QtGui.QLabel("0")
        self.label_loaded_img = QtGui.QLabel("Image goes here.")
        self.btn_generate_sheet = QtGui.QPushButton("Generate")

        self.label_generated_img = QtGui.QLabel("end result goes here")
        self.btn_save = QtGui.QPushButton("Save")

        self.vbox_l = QtGui.QVBoxLayout()
        self.hbox_l_angle_selector = QtGui.QHBoxLayout()
        self.vbox_r = QtGui.QVBoxLayout()
        self.hbox = QtGui.QHBoxLayout()
        self.img_out = None
        self.loaded_pixmap = None

        self.init_ui()

    def pil2qpixmap(self, im):
        myQtImage = ImageQt.ImageQt(im)
        pixmap = QtGui.QPixmap.fromImage(myQtImage)
        return pixmap

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def showDialog(self):
        self.loaded_filename = QtGui.QFileDialog.getOpenFileName(self, 'Open File', '~', "Image files (*.jpg *.gif *.png)")
        print "Loaded: " + self.loaded_filename
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
        pil_img_loaded = Image.open(str(self.loaded_filename))
        x, y = 0, 0
        width, height = pil_img_loaded.size
        print "width, height: " + str((width, height))
        width_step = math.floor(math.sqrt(self.step))

        height_step = width_step
        print "width step: " + str(width_step)
        if math.sqrt(self.step) - width_step > 0:
            print "remainder"
            height_step = height_step + 1
        print "height step: " + str(height_step)

        out_width, out_height = (int(width * width_step), int(height * height_step))
        print "Mode: " + pil_img_loaded.mode
        print "Size: " + str((out_width, out_height))
        self.img_out = Image.new(mode=pil_img_loaded.mode, size=(out_width, out_height))

        w_count = 0
        h_count = 0
        rot_count = 0
        for i in range(0, 360, self.angle):
            #tmpImg = pil_img_loaded.copy()
            print "Rotation: " + str(i)
            rot = pil_img_loaded.rotate(rot_count)

            x_pos = w_count * width
            y_pos = h_count * height

            box = (x_pos, y_pos, x_pos + width, y_pos + height)
            print "This box :" + str(box)
            #box = (0, 0)

            self.img_out.paste(rot, box)

            w_count += 1

            if w_count > width_step:
                w_count = 0
                h_count += 1

            rot_count += self.angle

        #self.loaded_pixmap = QtGui.QPixmap(self.loaded_filename)
        #self.loaded_pixmap = self.loaded_pixmap.scaledToHeight(100)
        #self.label_loaded_img.setPixmap(self.loaded_pixmap)
        print "Converting PIL image to pixmap.."
        out_pixmap = self.pil2qpixmap(self.img_out)
        print "Reszing.."
        #out_pixmap = out_pixmap.scaledToHeight(200)
        print "Done\n updating label.."
        self.label_generated_img.setPixmap(out_pixmap)

        #self.img_out.save("/home/leo/Pictures/rot_out.png")

    def onClick(self):
        print "Hi"

    def sliderChange(self, value):
        self.textfield_angle_slider.setText(str(value))
        self.label_num_sprites_v.setText(str(360 / value))
        self.step = 360 / value
        self.angle = value
        #self.generate_spritesheet(360 / value)

    def textFieldChanged(self, value):
        self.scale_angle_step.setValue(int(value))

    def saveGenImg(self):
        save_name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', '~', "Image files (*.jpg *.gif *.png)")
        self.img_out.save(save_name)

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
        #self.vbox_r.addStretch(1)
        self.btn_save.clicked.connect(self.saveGenImg)
        self.vbox_r.addWidget(self.label_generated_img)
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