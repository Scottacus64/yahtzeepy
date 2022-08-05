from yahtzeepy.yahtzee_gui import YahtzeeGui
from PyQt5 import QtWidgets


def main():
    import sys

    app = QtWidgets.QApplication(sys.argv)
    main_window = QtWidgets.QMainWindow()

    gui = YahtzeeGui()
    gui.setup(main_window)

    main_window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()