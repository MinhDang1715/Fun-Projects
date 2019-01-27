import sys
import os
import main

from PyQt5.QtWidgets import *
from PIL import Image

input_file = ''


class App(QWidget):
    def __init__(self):
        super().__init__()
        self.title = 'Image to ASCII'
        self.left = 700
        self.top = 400
        self.width = 400
        self.height = 300
        self.window = QWidget()
        self.layout = QVBoxLayout()
        self.initUI()

    def initUI(self):
        self.window.setWindowTitle(self.title)
        self.window.setGeometry(self.left, self.top, self.width, self.height)

        btn_import = QPushButton('Import Picture', self)
        btn_import.clicked.connect(self.btn_import_click)
        btn_import.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        btn_export = QPushButton('Export Picture', self)
        btn_export.clicked.connect(self.btn_export_click)
        btn_export.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.layout.addWidget(btn_import)
        self.layout.addWidget(btn_export)
        self.window.setLayout(self.layout)
        self.window.show()

    def btn_import_click(self):
        global input_file
        dialog = QFileDialog.getOpenFileName(self, 'Picture Files',
                                             './', 'Image Files(*.png *.jpg *.gif)')
        if dialog:
            input_file = dialog[0]

    def btn_export_click(self):
        def msg_box_click():
            osCommand = 'notepad.exe ' + output_file
            os.system(osCommand)

        global input_file
        if input_file:
            file_type = input_file[len(input_file) - 3: len(input_file)]
            if file_type == 'jpg' or file_type == 'png':
                dialog = QFileDialog.getSaveFileName(self, 'Text Files',
                                                     './', 'Text Files(*.txt)')
                if dialog:
                    output_file = dialog[0]
                    if main.convertImage(input_file, output_file):
                        msgBox = QMessageBox()
                        msgBox.setIcon(QMessageBox.Information)
                        msgBox.setText("Click OK to open the file.")
                        msgBox.setWindowTitle("Convert successful")
                        msgBox.buttonClicked.connect(msg_box_click)
                        msgBox.exec_()
            else:
                dialog = QFileDialog.getSaveFileName(self, 'Gif',
                                                     './', 'Gif(*.gif)')
                if dialog:
                    output_file = dialog[0]
                    # get each frame
                    for i, frame in enumerate(main.getFrame(input_file)):
                        frame.save('gif_frame/frame%d.png' % i, **frame.info)

                    # convert all the frame to a .txt file
                    DIR = 'gif_frame/'
                    DIR_2 = 'gif_frame_text/'
                    list_file = os.listdir(DIR)
                    for i in range(len(list_file)):
                        main.convertGif(DIR + list_file[i], DIR_2 + 'frame(%d).txt' % i)

                    # process the .txt files
                    DIR_3 = 'to_image/'
                    list_file = os.listdir(DIR_2)
                    for i in range(len(list_file)):
                        main.textToImage(DIR_2 + list_file[i], DIR_3 + 'frame(%d).png' % i)

                    DIR_3 = 'to_image/'
                    # convert all the .process png to .gif
                    if main.imagesToGif(DIR_3, output_file):
                        msgBox = QMessageBox()
                        msgBox.setIcon(QMessageBox.Information)
                        msgBox.setText("Click OK to open the file.")
                        msgBox.setWindowTitle("Convert successful")
                        msgBox.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

