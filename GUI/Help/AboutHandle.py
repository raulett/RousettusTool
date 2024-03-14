import os

from PyQt5.QtWidgets import QDialog

from UI.Help.AboutWindow_ui import Ui_DialogAbout


class AboutHandle(Ui_DialogAbout, QDialog):
    debug = 0
    def __init__(self, parent = None):
        super(AboutHandle, self).__init__(parent)
        self.setupUi(self)
        self.button_Close.clicked.connect(self.close)
        self.initGui()

    def initGui(self):
        current_path = os.path.dirname(os.path.abspath(__file__)).split('\\')
        root_path = '\\'.join(current_path[0: len(current_path) - 2]) + "\\"
        metadata_file = open(os.path.join(root_path, 'metadata.txt'), 'r')
        lines = metadata_file.readlines()
        metadata_file.close()
        version = lines[8].strip().split('=')[1]
        author = lines[9].strip().split('=')[1]
        email = lines[10].strip().split('=')[1]
        self.label_Author.setText(author)
        self.label_email.setText(email)
        self.label_version.setText(version)
        if self.debug:
            print(root_path)


