import sys
import os
import main

from natsort import natsorted
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
        self.initUI()

    def initUI(self):
        self.window.setWindowTitle(self.title)
        self.window.setGeometry(self.left, self.top, self.width, self.height)

        btn_import = QPushButton('Import', self)
        btn_import.clicked.connect(self.btn_import_click)
        btn_import.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        btn_export = QPushButton('Export', self)
        btn_export.clicked.connect(self.btn_export_click)
        btn_export.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        btn_cam = QPushButton('Open Webcam', self)
        # btn_cam.clicked.connect(self.btn_export_click)
        btn_cam.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)

        self.layout.addWidget(btn_import)
        self.layout.addWidget(btn_export)
        self.layout.addWidget(btn_cam)
        self.window.setLayout(self.layout)
        self.window.show()

    def btn_import_click(self):
        # get the input file
        global input_file
        dialog = QFileDialog.getOpenFileName(self, 'Import Files', './', 'Image Files(*.png *.jpg *.gif)')
        if dialog:
            input_file = dialog[0]
        else:
            pass

    def btn_export_click(self):
        def msg_box_click():
            osCommand = 'notepad.exe ' + output_file
            os.system(osCommand)

        global input_file
        if input_file:
            file_type = input_file[len(input_file) - 3: len(input_file)]
            if file_type == 'jpg' or file_type == 'png':
                # choose the output of the picture
                menu_mode = QMessageBox()
                menu_mode.setWindowTitle('Choose Mode')
                menu_mode.setText("Please select the output of the picture")
                menu_mode.setGeometry(700, 500, 800, 200)
                text_mode = QPushButton('Text')
                pic_mode = QPushButton('Picture')
                menu_mode.addButton(text_mode, QMessageBox.YesRole)
                menu_mode.addButton(pic_mode, QMessageBox.NoRole)
                ret = menu_mode.exec_()

                # get the output file
                if not ret:
                    dialog = QFileDialog.getSaveFileName(self, 'Export Text File', './', 'Text Files(*.txt)')
                    try:
                        if dialog:
                            output_file = dialog[0]
                            # txt mode
                            if main.convertImage(input_file, output_file):
                                msgBox = QMessageBox()
                                msgBox.setIcon(QMessageBox.Information)
                                msgBox.setText("Click OK to open the file.")
                                msgBox.setWindowTitle("Convert successful")
                                msgBox.buttonClicked.connect(msg_box_click)
                                msgBox.exec_()
                    except IOError as io_error:
                        pass
                else:
                    dialog = QFileDialog.getSaveFileName(self, 'Export Picture', './', 'Picture(*.png)')
                    try:
                        if dialog:
                            output_file = dialog[0]
                            if main.picToImage(input_file, output_file):
                                msgBox = QMessageBox()
                                msgBox.setIcon(QMessageBox.Information)
                                msgBox.setText("Convert successful.")
                                msgBox.setWindowTitle("Done")
                                msgBox.exec_()
                    except IOError as io_error:
                        pass

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
                try:
                    dialog = QFileDialog.getSaveFileName(self, 'Export GIF', './', 'Gif(*.gif)')
                    # notice that press detail_mode will return 0
                    # and simple mode will return 1
                    if dialog and len(dialog[0]) > 0:
                        output_file = dialog[0]
                        if not ret:
                            # get each frame
                            for i, frame in enumerate(main.getFrameDetail(input_file)):
                                frame.save('gif_frame/%d.png' % i, **frame.info)

                            # convert all the frame to a .txt file
                            DIR = 'gif_frame/'
                            DIR_2 = 'gif_frame_text/'
                            list_file = natsorted(os.listdir(DIR))
                            for i in range(len(list_file)):
                                main.convertGifDetail(DIR + list_file[i], DIR_2 + '%d.txt' % i)

                            # process the .txt files
                            DIR_3 = 'to_image/'
                            list_file = natsorted(os.listdir(DIR_2))
                            for i in range(len(list_file)):
                                main.textToImageDetail(DIR_2 + list_file[i], DIR_3 + '%d.png' % i)
                        else:
                            output_file = dialog[0]
                            # get each frame
                            for i, frame in enumerate(main.getFrameSimple(input_file)):
                                frame.save('gif_frame/%d.png' % i, **frame.info)

                            # convert all the frame to a .txt file
                            DIR = 'gif_frame/'
                            DIR_2 = 'gif_frame_text/'
                            list_file = natsorted(os.listdir(DIR))
                            for i in range(len(list_file)):
                                main.convertGifSimple(DIR + list_file[i], DIR_2 + '%d.txt' % i)

                            # process the .txt files
                            DIR_3 = 'to_image/'
                            list_file = natsorted(os.listdir(DIR_2))
                            for i in range(len(list_file)):
                                main.textToImageSimple(DIR_2 + list_file[i], DIR_3 + '%d.png' % i)
                        # convert back to images
                        DIR_3 = 'to_image/'
                        # convert all the .process png to .gif
                        if main.imagesToGif(DIR_3, output_file):
                            msgBox = QMessageBox()
                            msgBox.setIcon(QMessageBox.Information)
                            msgBox.setText("Convert successful.")
                            msgBox.setWindowTitle("Done")
                            msgBox.exec_()
                except IOError as io_error:
                    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())

