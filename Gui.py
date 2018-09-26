import sys
from PyQt5.QtWidgets import QApplication, QFileDialog
from PyQt5.QtGui import QImage, QPixmap
from PyQt5 import uic, QtCore
import threading
import ImageProcessor

main_page_ui = 'gui/MainWindow.ui'
main_page_form, main_page_base = uic.loadUiType(main_page_ui)

image_processor = ImageProcessor.ImageProcessor()

def format_image(image):
    qformat = QImage.Format_Indexed8
    if len(image.shape) == 3:  # rows, cols, channels
        if image.shape[2] == 4:  # 4 channels
            qformat = QImage.Format_RGBA8888
        else:
            qformat = QImage.Format_RGB888

    output = QImage(image, image.shape[1], image.shape[0], image.strides[0], qformat)
    return output.rgbSwapped()


class MainWindow(main_page_base, main_page_form):
    def __init__(self):
        super(main_page_base, self).__init__()
        self.setupUi(self)

        self.load_btn.clicked.connect(self.load_source)

        self.btn_channel.setDisabled(True)
        self.btn_depth.setDisabled(True)
        self.btn_horizont.setDisabled(True)
        self.btn_vertical.setDisabled(True)
        self.save_btn.setDisabled(True)

        self.btn_channel.clicked.connect(self.get_channel)
        self.btn_depth.clicked.connect(self.change_depth)
        self.btn_horizont.clicked.connect(self.flip_image)
        self.btn_vertical.clicked.connect(self.flop_image)
        self.save_btn.clicked.connect(self.save)
        self.btn_exit.clicked.connect(self.exit_app)

    def load_source(self):
        self.file_name, filter = QFileDialog.getOpenFileName(self, 'Open file', __file__, "Image Files (*.jpg *png)")
        if self.file_name:
            self.btn_channel.setDisabled(False)
            self.btn_depth.setDisabled(False)
            self.btn_horizont.setDisabled(False)
            self.btn_vertical.setDisabled(False)
            self.save_btn.setDisabled(False)


            image = format_image(image_processor.load_image(self.file_name))
            self.input_picture_label.setPixmap(QPixmap.fromImage(image))
            self.input_picture_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

            image = format_image(image_processor.original_image)
            self.output_picture_label.setPixmap(QPixmap.fromImage(image))
            self.output_picture_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)

    def draw_output(self, output_image):
        if output_image is not None:
            image = format_image(output_image)
            self.output_picture_label.setPixmap(QPixmap.fromImage(image))
            self.output_picture_label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        else:
            self.output_picture_label.setText("Err: Žiadny výstup, zlé parametre")

    def get_channel(self):
        channel = self.channel_edit_line.text()
        self.draw_output(image_processor.get_color_channel(channel))

    def change_depth(self):
        depth = int(self.depth_edit_line.text())
        th = threading.Thread(target=image_processor.decrease_color_depth, args=([depth, self.draw_output]))
        th.start()
        self.output_picture_label.setText("Prepočítavam...")

        # processed_image = image_processor.decrease_color_depth(depth)
        # if processed_image is not None:
        #     self.draw_output(processed_image)
        # else:
        #     print("error")

    def flip_image(self):
        self.draw_output(image_processor.flip_image())

    def flop_image(self):
        self.draw_output(image_processor.flop_image())

    def save(self):
        filename = QFileDialog.getSaveFileName(self, 'Ulož', self.file_name, filter="Images (*.jpg *png)")
        print(filename)
        image_processor.save(filename[0])

    def exit_app(self):
        sys.exit(1)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())