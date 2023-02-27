import qrcode
import qdarkstyle
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QPushButton, QSystemTrayIcon, QMenu, QAction, qApp
from PyQt5.QtGui import QIcon, QPixmap, QGuiApplication
from PyQt5.QtCore import Qt
from PyQt5 import QtCore



class QRCodeGenerator(QWidget):
    def __init__(self):
        super().__init__()

        # Create widgets for the UI
        link_label = QLabel("Enter Link:", self)
        link_label.setStyleSheet("color: white; font-size: 16px; font-weight: bold;")
        link_label.move(20, 20)
        self.link_entry = QLineEdit(self)
        self.link_entry.setGeometry(20, 50, 360, 30)
        self.link_entry.setStyleSheet("font-size: 16px; font-weight: normal;")
        generate_button = QPushButton("Generate", self)
        generate_button.setGeometry(20, 90, 100, 30)
        generate_button.setStyleSheet("background-color: #007bff; color: white; border-radius: 5px; font-size: 16px; font-weight: bold;")
        generate_button.clicked.connect(self.generate_qr)

        # Add system tray icon
        self.tray_icon = QSystemTrayIcon(self)
        self.tray_icon.setIcon(QIcon('logo.png'))
        self.tray_icon.setVisible(True)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint | QtCore.Qt.WindowMinimizeButtonHint)

        # Create menu for system tray icon
        self.tray_menu = QMenu(self)
        show_action = QAction("Show", self)
        show_action.triggered.connect(self.show)
        self.tray_menu.addAction(show_action)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(qApp.quit)
        self.tray_menu.addAction(exit_action)

        # Set window properties
        self.setWindowTitle("QR Code Generator")
        self.setWindowIcon(QIcon('logo.png'))
        self.setStyleSheet(qdarkstyle.load_stylesheet(qt_api='pyqt5'))
        self.resize(400, 130)

        # Center the window on the screen
        self.move_center()

    def move_center(self):
        qr_code_generator_rect = self.frameGeometry()
        center_point = QGuiApplication.primaryScreen().availableGeometry().center()
        qr_code_generator_rect.moveCenter(center_point)
        self.move(qr_code_generator_rect.topLeft())

    def generate_qr(self):
        link = self.link_entry.text()
        qr = qrcode.QRCode(
            version=1,
            box_size=10,
            border=5
        )
        qr.add_data(link)
        qr.make(fit=True)
        img = qr.make_image(fill='black', back_color='white')
        img.save('qrcode.png')
        pixmap = QPixmap('qrcode.png')
        pixmap_resized = pixmap.scaledToHeight(200)
        qr_label = QLabel(self)
        qr_label.setPixmap(pixmap_resized)
        qr_label.setGeometry(220, 20, 200, 200)
        qr_label.show()

if __name__ == '__main__':
    app = QApplication([])
    qr_code_generator = QRCodeGenerator()
    qr_code_generator.show()
    app.exec_()
