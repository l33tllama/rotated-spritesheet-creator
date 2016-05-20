from PIL import Image, ImageQt
import sys
from PyQt4 import QtGui, QtCore
import math

#TODO: animated preview tab (maybe later..)
#TODO: clean up prints and commented out code

class GuiMain(QtGui.QWidget):

    def __init__(self):
        super(GuiMain, self).__init__()

        self.txt_ui_base_image = "./ui_base_image.png"
        self.txt_ui_output_spritesheet = "./ui_output_spritesheet.png"
        self.loaded_filename = ""
        self.angle_divisors = [1, 2, 3, 4, 5, 6, 8, 9, 10, 12, 15, 18, 20, 24, 30, 36, 40, 45, 60, 72, 90]
        self.angle_divisors_i = 0
        self.last_slider_value = 0
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
        self.hbox_l_num_sprites = QtGui.QHBoxLayout()
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
        if self.loaded_filename == "":
            return
        self.loaded_pixmap = QtGui.QPixmap(self.loaded_filename)
        self.loaded_pixmap = self.loaded_pixmap.scaledToHeight(180)
        self.label_loaded_img.setPixmap(self.loaded_pixmap)
        self.btn_generate_sheet.setEnabled(True)

    def generate_spritesheet(self):

        if self.loaded_pixmap is None:
            msg_box = QtGui.QMessageBox()
            msg_box.setText("Trying to create spritesheet when no image loaded.")
            msg_box.exec_()
            return

        # load image into PIL image for manipulation
        pil_img_loaded = Image.open(str(self.loaded_filename))
        width, height = pil_img_loaded.size
        width_step = math.ceil(math.sqrt(self.step))

        height_step = width_step

        # if height can be 1 less then width (eg 12 = 4x3)
        if (height_step - 1) * width_step == self.step:
            height_step -=1

        if (height_step - 2) * width_step == self.step:
            height_step -= 1

        out_width, out_height = (int(width * width_step), int(height * height_step))
        self.img_out = Image.new(mode=pil_img_loaded.mode, size=(out_width, out_height))

        w_count = 0
        h_count = 0
        step_count = 0
        for rotation in range(0, 360, self.angle):
            x_pos = w_count * width
            y_pos = h_count * height
            rot = pil_img_loaded.rotate(-rotation)
            box = (x_pos, y_pos, x_pos + width, y_pos + height)
            self.img_out.paste(rot, box)

            w_count += 1
            step_count += 1

            if step_count > self.step:
                break

            if w_count > width_step - 1:
                w_count = 0
                h_count += 1

        tmp_rotate_img = Image.new(mode=pil_img_loaded.mode, size=(out_width, out_height))
        tmp_rotate_img.paste(self.img_out)
        tmp_rotate_img = tmp_rotate_img.resize((180, 180))
        out_pixmap = self.pil2qpixmap(tmp_rotate_img)
        self.label_generated_img.setPixmap(out_pixmap)

    def sliderChange(self, value):
        if value > 90: return
        if value < self.last_slider_value:
            i = 0
            for angle in self.angle_divisors:
                if angle > value:
                    self.scale_angle_step.setValue(self.angle_divisors[i - 1])
                    value = self.angle_divisors[i - 1]
                    break
                i += 1
        elif value > self.last_slider_value:
            i = 0
            for angle in sorted(self.angle_divisors):
                if angle >= value:
                    self.scale_angle_step.setValue(self.angle_divisors[i])
                    value = self.angle_divisors[i]
                    break
                i += 1

        self.textfield_angle_slider.setText(str(value))
        self.label_num_sprites_v.setText(str(360 / value))
        self.step = 360 / value
        self.angle = value
        self.last_slider_value = value

    def textFieldChanged(self, value):
        self.scale_angle_step.setValue(int(value))

    def saveGenImg(self):
        save_name = QtGui.QFileDialog.getSaveFileName(self, 'Save File', self.loaded_filename, "Image files (*.jpg *.gif *.png)")
        print "Saving file as : " + save_name
        file_ext = save_name[-3:]
        if file_ext == "png":
            self.img_out.save(str(save_name), "PNG")
        else:
            self.img_out.save(str(save_name))

    def init_ui(self):

        # --- LEFT SIDE ------
        # open, set angle rotation degrees and generate button

        # OPEN source file button
        self.btn_open.clicked.connect(self.showDialog)

        # FILE CHOOSER dialog
        self.dialog_open_img.setFileMode(QtGui.QFileDialog.AnyFile)

        # ANGLE STEP slider
        self.scale_angle_step.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scale_angle_step.setMinimum(1)
        self.scale_angle_step.setMaximum(90)
        self.scale_angle_step.valueChanged[int].connect(self.sliderChange)

        # ANGLE STEP text field
        self.textfield_angle_slider.setText("1")

        self.textfield_angle_slider.textChanged[str].connect(self.textFieldChanged)

        # LOADED IMAGE and GENERATE BUTTON
        self.loaded_pixmap = QtGui.QPixmap(self.txt_ui_base_image)
        self.label_loaded_img.setPixmap(self.loaded_pixmap)
        #self.label_loaded_img.setFixedHeight(180)
        self.btn_generate_sheet.setEnabled(False)
        self.btn_generate_sheet.clicked.connect(self.generate_spritesheet)

        # LAYOUT PACKING
        # left side - select image and angle steps
        self.vbox_l.addWidget(self.btn_open)
        self.vbox_l.addWidget(self.label_angle_step)

        # ANGLE SELECTOR HBOX
        self.hbox_l_angle_selector.addWidget(self.scale_angle_step)
        #self.hbox_l_angle_selector.addStretch(1)
        self.textfield_angle_slider.setFixedWidth(48)
        self.hbox_l_angle_selector.addWidget(self.textfield_angle_slider)

        self.vbox_l.addLayout(self.hbox_l_angle_selector)

        # NUMBER OF SPRITES HBOX

        self.hbox_l_num_sprites.addWidget(self.label_num_sprites_l)
        self.hbox_l_num_sprites.addStretch(1)
        self.hbox_l_num_sprites.addWidget(self.label_num_sprites_v)

        self.vbox_l.addLayout(self.hbox_l_num_sprites)
        self.vbox_l.addWidget(self.label_loaded_img)
        self.vbox_l.addWidget(self.btn_generate_sheet)

        self.vbox_l.addStretch(1)

        # --- RIGHT SIDE ----
        # preview and save
        self.loaded_pixmap = QtGui.QPixmap(self.txt_ui_output_spritesheet)
        self.label_generated_img.setPixmap(self.loaded_pixmap)

        self.btn_save.clicked.connect(self.saveGenImg)
        self.vbox_r.addStretch(1)
        self.vbox_r.addWidget(self.label_generated_img)
        self.vbox_r.addWidget(self.btn_save)

        self.hbox.addLayout(self.vbox_l)
        self.hbox.addLayout(self.vbox_r)

        self.setLayout(self.hbox)

        # self.setGeometry(300, 300, 800, 150)
        self.setWindowTitle('Rotated Spritesheet Creator by l33tllama')
        self.center()
        self.setFixedWidth(420)
        self.show()

def main():
    app = QtGui.QApplication(sys.argv)
    ex = GuiMain()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()