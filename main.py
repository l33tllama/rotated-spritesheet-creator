from PIL import Image
import sys

from PyQt4 import QtGui, QtCore

def pil2qpixmap(pil_image):
    w, h = pil_image.size
    data = pil_image.tostring("raw", "BGRX")
    qimage = QtGui.QImage(data, w, h, QtGui.QImage.Format_RGB32)
    qpixmap = QtGui.QPixmap(w,h)
    pix = QtGui.QPixmap.fromImage(qimage)
    return pix

class Example(QtGui.QWidget):

    def __init__(self):
        super(Example, self).__init__()

        self.initUI()

    def center(self):
        frameGm = self.frameGeometry()
        screen = QtGui.QApplication.desktop().screenNumber(QtGui.QApplication.desktop().cursor().pos())
        centerPoint = QtGui.QApplication.desktop().screenGeometry(screen).center()
        frameGm.moveCenter(centerPoint)
        self.move(frameGm.topLeft())

    def showDialog(self):

        text, ok = QtGui.QInputDialog.getText(self, 'Input Dialog',
            'Enter your name:')

        if ok:
            self.le.setText(str(text))

    def onClick(self):
        print "Hi"

    def sliderChange(self, value):
        self.textfield_angle_slider.setText(str(value))

    def textFieldChanged(self, value):
        self.scale_angle_step.setValue(int(value))


    def initUI(self):

        btn_open = QtGui.QPushButton("Select image")
        btn_open.clicked.connect(self.showDialog)
        label_angle_step = QtGui.QLabel("Select angle steps (deg)")
        self.textfield_angle_slider = QtGui.QLineEdit()

        self.scale_angle_step = QtGui.QSlider(QtCore.Qt.Horizontal, self)
        self.scale_angle_step.setFocusPolicy(QtCore.Qt.NoFocus)
        self.scale_angle_step.setMinimum(1)
        self.scale_angle_step.setMaximum(90)
        self.scale_angle_step.setGeometry(30, 40, 100, 30)
        self.scale_angle_step.valueChanged[int].connect(self.sliderChange)

        self.textfield_angle_slider.setText("1")
        self.textfield_angle_slider.textChanged[str].connect(self.textFieldChanged)


        btn_save = QtGui.QPushButton("Save")


        # left side - select image and angle steps
        vbox_l = QtGui.QVBoxLayout()
        vbox_l.addWidget(btn_open)
        vbox_l.addWidget(label_angle_step)

        hbox_l_angle_selector = QtGui.QHBoxLayout()
        hbox_l_angle_selector.addWidget(self.scale_angle_step)
        hbox_l_angle_selector.addWidget(self.textfield_angle_slider)
        hbox_l_angle_selector.addStretch(1)

        vbox_l.addLayout(hbox_l_angle_selector)
        vbox_l.addStretch(1)

        # right side - preview and save
        vbox_r = QtGui.QVBoxLayout()

        vbox_r.addStretch(1)
        vbox_r.addWidget(btn_save)


        hbox = QtGui.QHBoxLayout()
        hbox.addLayout(vbox_l)
        hbox.addLayout(vbox_r)

        self.setLayout(hbox)

        #self.setGeometry(300, 300, 800, 150)
        self.setWindowTitle('Buttons')
        self.center()
        self.show()

def main():

    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()