from yahtzeepy.die_set import DieSet
from yahtzeepy.yahtzee_game import YahtzeeGame

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QPushButton, QButtonGroup, QWidget, QTableWidget, QLabel, \
    QFrame
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QRect, QSize

import os

# This sets the task bar icon
try:
    from ctypes import windll
    myappid = 'com.mycompany'
    windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)
except ImportError:
    pass


class YahtzeeGui(object):
    def __init__(self):
        self.yahtzee_game = YahtzeeGame()
        self.resources_path = os.path.join(os.path.dirname(__file__), 'resources')
        self.die_set = DieSet()
        self.button_list = []  # list of die button objects with dieGroup icon value applied
        self.button_die_dictionary = {}  # dictionary with push button objects and corresponding die objects
        self.yahtzee_table_list = []  # master list of all yahtzee table cells that have been filled
        self.table_clicked = False  # toggle flag for knowing if rolls should be stopped because of table entry
        self.rolls_left = 3

    def setup(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(900, 830)
        icon = QIcon()
        icon.addPixmap(QPixmap(os.path.join(self.resources_path, "yahtzee.ico")), QIcon.Normal,
                       QIcon.Off)  # icon for menu bar
        main_window.setWindowIcon(icon)
        self.central_widget = QWidget(main_window)
        self.central_widget.setObjectName("centralwidget")
        # button to roll dice
        self.roll_button = QPushButton(self.central_widget)
        self.roll_button.setGeometry(QRect(170, 280, 110, 50))
        self.roll_button.setObjectName("rollButton")
        self.roll_button.clicked.connect(self.roll_dice)
        self.die_button_group = QButtonGroup()
        # makes the five dice that are push buttons
        for i in range(5):
            self.die = QPushButton(self.central_widget)
            self.die.setGeometry(QRect(50, 50 + (i * 100), 81, 81))
            self.die.setIcon(QIcon(os.path.join(self.resources_path, self.die_set.get_at(i).get_image())))
            self.die.setIconSize(QSize(81, 81))
            self.button_die_dictionary[self.die] = self.die_set.get_at(
                i)  # dictionary of pairs of die buttons and die objectss
            self.button_list.append(self.die)  # list of die buttons
            self.die_button_group.addButton(self.die, i)  # group of die buttons
        self.die_button_group.buttonClicked.connect(self.die_clicked)  # if clicked go to dieClicked
        # set up for yahtzee table of entries
        self.yahtzee_table = QTableWidget(self.central_widget)
        self.yahtzee_table.setGeometry(QRect(340, 10, 541, 775))
        self.yahtzee_table.setAutoFillBackground(False)
        self.yahtzee_table.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.yahtzee_table.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.yahtzee_table.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustToContents)
        self.yahtzee_table.setWordWrap(False)
        self.yahtzee_table.setCornerButtonEnabled(False)
        self.yahtzee_table.setRowCount(20)
        self.yahtzee_table.setColumnCount(3)
        self.yahtzee_table.setObjectName("yahtzeeTable")
        item = QTableWidgetItem()

        # sets up the 20 rows of the table
        for i in range(20):
            font = QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            if i < 7:  # first rows get icons in the header
                icon = QIcon()
                icon.addPixmap(QPixmap(os.path.join(self.resources_path, "w" + str(i) + ".jpg")), QIcon.Normal,
                               QIcon.Off)
                item.setIcon(icon)
            item = QTableWidgetItem()
            self.yahtzee_table.setVerticalHeaderItem(i, item)
        # sets up the three columns
        for i in range(4):
            font = QFont()
            font.setBold(True)
            font.setWeight(75)
            item = QTableWidgetItem()
            item.setTextAlignment(QtCore.Qt.AlignCenter)
            item.setFont(font)
            self.yahtzee_table.setHorizontalHeaderItem(i, item)
        # format the headers
        self.yahtzee_table.horizontalHeader().setVisible(True)
        self.yahtzee_table.horizontalHeader().setMinimumSectionSize(125)
        self.yahtzee_table.horizontalHeader().setStretchLastSection(True)
        self.yahtzee_table.verticalHeader().setVisible(True)
        self.yahtzee_table.verticalHeader().setStretchLastSection(True)
        # makes a label for the grand total
        self.label = QLabel(self.central_widget)
        self.label.setGeometry(QRect(60, 600, 251, 51))
        font = QFont()
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        # makes a push button that is normally hidden to start a new game
        self.play_again = QPushButton(self.central_widget)
        self.play_again.setGeometry(QRect(70, 700, 162, 49))
        self.play_again.setIcon(QIcon(os.path.join(self.resources_path, "playAgain.jpg")))
        self.play_again.setIconSize(QSize(162, 49))
        self.play_again.hide()
        self.play_again.clicked.connect(self.new_game)
        # formats lines at the top of the first row
        self.line = QFrame(self.central_widget)
        self.line.setGeometry(QRect(480, 30, 401, 20))
        self.line.setLineWidth(2)
        self.line.setFrameShape(QFrame.HLine)
        self.line.setFrameShadow(QFrame.Sunken)
        self.line.setObjectName("line")
        main_window.setCentralWidget(self.central_widget)
        self.retranslate(main_window)
        QtCore.QMetaObject.connectSlotsByName(main_window)
        self.yahtzee_table.clicked.connect(self.yahtzee_table_click)

    def retranslate(self, main_window):  # this sets up the material displayed in the widgets
        _translate = QtCore.QCoreApplication.translate
        main_window.setWindowTitle(_translate("MainWindow", "Yahtzee"))
        self.roll_button.setText(_translate("MainWindow", "Roll"))
        yahtzee_list = ["Ones", "Twos", "Threes", "Fours", "Fives", "Sixes", "Total", "Bouns", "UPPER TOTAL           ",
                        "", "Three of a Kind", "Four of a Kind", "Full House", "Small Straight", "Large Straight",
                        "Yahtzee", "Chance", "Yahtzee Bonus", "LOWER TOTAL", "GRAND TOTAL"]
        # makes 20 rows and uses the list to populate them
        for i in range(20):
            item_row = self.yahtzee_table.verticalHeaderItem(i)
            item_row.setText(_translate("MainWindow", yahtzee_list[i]))
        yahtzee_top_list = ["x1", "x2", "x3"]
        # makes three columns and uses the list to populate them
        for i in range(3):
            item_col = self.yahtzee_table.horizontalHeaderItem(i)
            item_col.setText(_translate("MainWindow", yahtzee_top_list[i]))
        self.label.setText(_translate("MainWindow", "Grand Total = 0"))

    def new_game(self):
        self.yahtzee_game.new_game()
        self.play_again.hide()  # hide the play again button
        self.label.setText("Grand Total = 0")
        for i in range(5):  # reset all of the die objects to 0 and white
            die_object = self.die_set.get_at(i)
            die_object.is_clicked = False
        self.clear_table()


    def roll_dice(self):  # GUI method to roll the dice
        self.table_clicked = False
        self.yahtzee_game.die_rolls += 1  # increment dieRolls toward three
        self.yahtzee_game.rolls_left = 3 - self.yahtzee_game.die_rolls  # rolls left will be displayed on the roll button
        if self.yahtzee_game.die_rolls < 4:  # if not past the end of dice rolls
            for i in range(10):  # we're going to go through 10 different dice values to simulate a roll
                self.yahtzee_game.roll_dice(self.die_set)
                self.show_die()

    def show_die(self):  # helper method to display the dice
        for i in range(5):
            die = self.die_set.get_at(i)
            die_icon = die.get_image()  # set the icon image
            # pip = 6 #for testing yahtzee bonus logic
            self.button_list[i].setIcon(QIcon(os.path.join(self.resources_path, die_icon)))
            QApplication.processEvents()  # again must be called to update the icon images
            die_value = die.get_pip()  # die_icon.strip('wy.jpg')
            die.pip = die_value  # set the die object's pip value to the random number for use later
        _translate = QtCore.QCoreApplication.translate
        if self.yahtzee_game.die_rolls == 2:  # if there is one roll left maKe roll singular
            self.roll_button.setText(_translate("MainWindow", (str(self.yahtzee_game.rolls_left) + " Roll Left")))
        else:  # otherwise make plural
            self.roll_button.setText(_translate("MainWindow", (str(self.yahtzee_game.rolls_left) + " Rolls Left")))

    def die_clicked(self, button):  # this is called if a die is clicked
        clicked_die = self.button_die_dictionary[
            button]  # sets clickedDie = to the die object dictionary pair to the button pressed
        if clicked_die.is_clicked == True:  # toggles the is_clicked value
            clicked_die.is_clicked = False
            clicked_die_icon = clicked_die.get_image()  # makes the die white
        else:
            clicked_die.is_clicked = True
            clicked_die_icon = clicked_die.get_image()  # makes the die yellow
        for i in range(5):
            if self.button_list[i] == button:
                self.button_list[i].setIcon(QIcon(os.path.join(self.resources_path, clicked_die_icon)))
        QApplication.processEvents()  # MUST HAVE THIS to update the dice icons

    def yahtzee_table_click(self, item):
        if self.yahtzee_game.game_over == True or self.yahtzee_game.no_rolls == True:
            return
        self.yahtzee_game.unset_dice_rolled() # Get dice ready to roll again
        self.yahtzee_game.die_rolls = 0
        _translate = QtCore.QCoreApplication.translate
        self.roll_button.setText(_translate("MainWindow", "Roll"))  # put roll back on the button
        row = item.row()
        col = item.column()
        in_table_list = False
        pip_value = 0
        if self.yahtzee_game.auto_fill == False:  # checks to see if a yahtzee bonus autofill has already occurred
            if self.yahtzee_game.yahtzee_bonus > 2 and self.die_set.get_at(0).pip == self.die_set.get_at(
                    1).pip == self.die_set.get_at(2).pip == self.die_set.get_at(3).pip == self.die_set.get_at(4).pip:
                # Note this is a yahtzee bonus situation and special rules apply to the cell to be filled
                column_list = []
                for entry in self.yahtzee_game.yahtzee_table_list:  # look at each table cell entry to see if the upper cell corresponding to pip is filled
                    pip_value = (self.die_set.get_at(0).pip - 1)
                    if entry[0] == pip_value:
                        column_list.append(entry[1])  # make a list of columns already filled in
                column_list.sort()  # sort the column numbers from 0 to 2
                length = len(column_list)
                if length < 3:  # if the column's upper section pip rows are not already all filled in
                    entry_column = 4 # set entry column to a value that cannot exist
                    if length > 0:
                        for i in range(2, -1, -1):  # step backwards through the list
                            if i not in column_list:  # pick the largest value from the list
                                entry_column = i
                                break  # get out of here
                    if entry_column == 4: # If the column_list is empty because entry_column is still 4
                        entry_column = 2 # Set the column to 2
                    bonus = self.yahtzee_game.yahtzee_bonus_list[
                        entry_column]  # see if any yahtzee bonus exists already
                    bonus += 100  # increase that value by 100
                    self.yahtzee_game.yahtzee_bonus_list[entry_column] = bonus  # update the list
                    point_value = ((pip_value + 1) * 5)  # total points to be filled in
                    self.yahtzee_game.yahtzee_table_list.append(
                        (pip_value, entry_column, point_value))  # append the tuple with row, col and total
                    item = QTableWidgetItem(str(point_value))  # make the point value 5 times the pip value
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.yahtzee_table.setItem(pip_value, entry_column, item)  # fill in the cell
                    item = QTableWidgetItem(str(bonus))  # set the yahtzee bonus value
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.yahtzee_table.setItem((17), entry_column, item)  # fill in the cell
                    self.yahtzee_game.total_up()  # total up
                    self.yahtzee_game.auto_fill = True
                else:
                    self.yahtzee_game.yahtzee_joker = True # if all the upper cells are filled then it is a yahtzee_joker
            for entry in self.yahtzee_game.yahtzee_table_list:  # look through the tuples in yTableList and see if the cell has been filled already
                if entry[0] == row and entry[1] == col:
                    in_table_list = True
            if in_table_list == False and self.yahtzee_game.auto_fill == False:
                # next line makes sure that the player didn't click on a "total" cell
                if self.table_clicked == True and row >= 0 and row <= 5 or self.table_clicked == True and row >= 10 and row <= 16:
                    last_cell = self.yahtzee_game.yahtzee_table_list[-1]  # get the last tuple in the list
                    last_row = last_cell[0]
                    last_column = last_cell[1]
                    if last_row == 15:
                        self.yahtzee_game.yahtzee_bonus -= 1
                    if self.yahtzee_game.yahtzee_joker == True:  # undo the yahtzee bonus from the last iteration
                        previous_bonus = self.yahtzee_game.yahtzee_bonus_list[last_column]
                        previous_bonus -= 100
                        self.yahtzee_game.yahtzee_bonus_list[last_column] = previous_bonus
                        item = QTableWidgetItem(str(previous_bonus))  # set the yahtzee bonus value
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.yahtzee_table.setItem((17), last_column, item)  # fill in the cell
                    self.yahtzee_game.yahtzee_table_list.pop()  # pop removes the last element in the list
                    item = QTableWidgetItem(str(""))  # put a blank fill in the formerly populated cell
                    self.yahtzee_table.setItem(last_row, last_column, item)
                die_total = 0
                if self.yahtzee_game.yahtzee_joker == True:  # if a yahtzee joker situation exists
                    bonus = self.yahtzee_game.yahtzee_bonus_list[col]  # see if any yahtzee bonus exists already
                    bonus += 100  # increase that value by 100
                    self.yahtzee_game.yahtzee_bonus_list[col] = bonus  # update the list
                    item = QTableWidgetItem(str(bonus))  # set the yahtzee bonus value
                    item.setTextAlignment(QtCore.Qt.AlignCenter)
                    self.yahtzee_table.setItem((17), col, item)  # fill in the cell
                # check to see if the selection is in the upper cells
                if row >= 0 and row <= 5:
                    for i in range(5):
                        die_pip = self.die_set.get_at(i).get_pip()
                        if die_pip == (row + 1):  # if the die pip matches the row selected
                            die_total += (row + 1)  # add that die to the total
                    self.fill_cell(row, col, die_total)
                # if the player clicked on the lower section of the table
                if row >= 10 and row <= 16:
                    # If three of a kind is selected
                    if row == 10:
                        total = self.yahtzee_game.three_of_a_kind(self.die_set)  # get the result from this function
                        self.fill_cell(row, col, total)
                    # if four of a kind is selected
                    if row == 11:
                        total = self.yahtzee_game.four_of_a_kind(self.die_set)  # get the result from this function
                        self.fill_cell(row, col, total)
                    # if full house is selected
                    if row == 12:
                        total = self.yahtzee_game.full_house(self.die_set)  # get the result from this function
                        self.fill_cell(row, col, total)
                    # if small straight is selected
                    if row == 13:
                        total = self.yahtzee_game.small_straight(self.die_set)  # get the result from this function
                        self.fill_cell(row, col, total)
                    # if large straight is selected
                    if row == 14:
                        total = self.yahtzee_game.large_straight(self.die_set)  # get the result from this function
                        self.fill_cell(row, col, total)
                    # if yahtzee is selected
                    if row == 15:
                        total = self.yahtzee_game.yahtzee(self.die_set)  # get the result from this function
                        self.fill_cell(row, col, total)
                    # if chance is selected
                    if row == 16:
                        total = self.yahtzee_game.chance(self.die_set)  # get the result from this function
                        self.fill_cell(row, col, total)

                self.label.setText("Grand Total = " + str(self.yahtzee_game.yahtzee_grand_total))
                for i in range(3):
                    for j in range(6, 9):
                        item = QTableWidgetItem(str(self.yahtzee_game.top_totals_list[i + ((j - 6) * 3)]))
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.yahtzee_table.setItem(j, i, item)

                for i in range(3):
                    for j in range(18, 20):
                        item = QTableWidgetItem(str(self.yahtzee_game.bottom_totals_list[i + ((j - 18) * 3)]))
                        item.setTextAlignment(QtCore.Qt.AlignCenter)
                        self.yahtzee_table.setItem(j, i, item)

    def fill_cell(self, row, col, total):
        item = QTableWidgetItem(str(total))
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.yahtzee_table.setItem(row, col, item)
        self.yahtzee_game.yahtzee_table_list.append((row, col, total))
        self.table_clicked = True
        self.yahtzee_game.total_up()
        self.check_end_game()

    def check_end_game(self):
        if len(self.yahtzee_game.yahtzee_table_list) == 39:
            self.yahtzee_game.end_game()
            self.play_again.show()  # show the play again button

    def clear_table(self):
        for col in range(3):  # reset each column
            for row in range(20):  # and row
                item = QTableWidgetItem(str(""))  # to blank
                self.yahtzee_table.setItem(row, col, item)
