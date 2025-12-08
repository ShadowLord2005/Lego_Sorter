import cv2
import numpy as np
from pylibdmtx.pylibdmtx import decode
from PyQt6.QtCore import Qt, QThread, pyqtSignal, pyqtSlot
from PyQt6.QtGui import QImage, QPixmap
from PyQt6.QtWidgets import QGridLayout, QLabel, QWidget


#Creates Thread to hold video updating to ensure other GUI operations can still run
class VideoThread(QThread):
    #Declares Signal linked to ndarray
    update_frame_signal = pyqtSignal(np.ndarray)

    def __init__(self, index:int = 0):
        #Adds Camera Index for use in later steps
        super().__init__()
        self.index = index

    #When Thread is run loads a video feed from specified index and then if there is a new frame emits the above signal with the frame associated
    def run(self):
        self.is_running=True
        self.camera = cv2.VideoCapture(self.index, cv2.CAP_DSHOW)
        while self.is_running:
            has_new_frame, frame = self.camera.read()
            if has_new_frame:
                self.update_frame_signal.emit(frame)

    def stop(self):
        self.is_running=False
        self.camera.release()
        self.quit()
        self.terminate()

class CameraFeed(QWidget):
    def __init__(self, index:int):
        super().__init__()
        self.image_width = 640
        self.image_height = 480
        self.index = index
        label = "Camera " + str(index)
        self.camera_frame = QLabel(self)
        self.camera_label = QLabel(label)

        #Adds the camera feed and the index number to the layout one above the other.
        layout = QGridLayout()
        layout.addWidget(self.camera_frame,0,0)
        layout.addWidget(self.camera_label,1,0)
        self.setLayout(layout)

        #Create the instance of the thread, connect it to the update image function below and then start it
        self.thread = VideoThread(self.index)
        self.thread.update_frame_signal.connect(self.updateFrame)
        self.thread.start()

    def closeEvent(self, event):
        #Ensures that the camera properly closes when the app exits
        self.thread.stop()
        event.accept()

    @pyqtSlot(np.ndarray)
    def updateFrame(self, cv2_img):
        #This updates the frame shown on the QLabel with a new one from the cv2 camera after first converting it into an appropriate format for pyqt
        qt_img = self.convertCv2Qt(cv2_img)
        self.camera_frame.setPixmap(qt_img)


    def convertCv2Qt(self, cv2_img):
        #Converts the image from cv2 format to qt format
        rgb_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
        height, width, channels = rgb_img.shape #Gets Array properties
        bytes_per_line = channels * width
        qt_format = QImage(rgb_img.data, width, height, bytes_per_line, QImage.Format.Format_RGB888) #Formats as QImage
        pixmap = qt_format.scaled(self.image_width, self.image_height, Qt.AspectRatioMode.KeepAspectRatio) #Scales to the specified size
        return QPixmap.fromImage(pixmap) #Creates pixmap to apply to label

if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    window = QMainWindow()
    window.setWindowTitle("Camera Test")
    window.setCentralWidget(CameraFeed(1))
    window.show()

    sys.exit(app.exec())
