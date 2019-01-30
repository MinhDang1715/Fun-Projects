import sys
import os
import main

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

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
        self.setWindowIcon(QIcon("C:/Users/Minh Dang/Desktop/Pic_to_ASCII/icon.png"))
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
                dialog = QFileDialog.getSaveFileName(self, 'Text Files', './', 'Text Files(*.txt)')
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
                # choose between detail or simple mode
                menu_mode = QMessageBox()
                menu_mode.setWindowTitle('Choose Mode')
                menu_mode.setText("Please select the desire mode for the converted gif")
                menu_mode.setGeometry(700, 500, 800, 200)
                detail_mode = QPushButton('Detail Mode')
                simple_mode = QPushButton('Simple Mode')
                menu_mode.addButton(detail_mode, QMessageBox.YesRole)
                menu_mode.addButton(simple_mode, QMessageBox.NoRole)
                ret = menu_mode.exec_()

                dialog = QFileDialog.getSaveFileName(self, 'Gif', './', 'Gif(*.gif)')

                # notice that press detail_mode will return 0
                # and simple mode will return 1
                if not ret:
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
                            main.convertGifDetail(DIR + list_file[i], DIR_2 + 'frame(%d).txt' % i)

                        # process the .txt files
                        DIR_3 = 'to_image/'
                        list_file = os.listdir(DIR_2)
                        for i in range(len(list_file)):
                            main.textToImageDetail(DIR_2 + list_file[i], DIR_3 + 'frame(%d).png' % i)
                    else:
                        pass
                else:
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
                            main.convertGifSimple(DIR + list_file[i], DIR_2 + 'frame(%d).txt' % i)

                        # process the .txt files
                        DIR_3 = 'to_image/'
                        list_file = os.listdir(DIR_2)
                        for i in range(len(list_file)):
                            main.textToImageSimple(DIR_2 + list_file[i], DIR_3 + 'frame(%d).png' % i)
                    else:
                        pass

                DIR_3 = 'to_image/'
                # convert all the .process png to .gif
                if main.imagesToGif(DIR_3, output_file):
                    msgBox = QMessageBox()
                    msgBox.setIcon(QMessageBox.Information)
                    msgBox.setText("Convert successful.")
                    msgBox.setWindowTitle("Done")
                    msgBox.exec_()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

