from yahtzeepy.die_set import DieSet

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QPushButton, QButtonGroup, QWidget, QTableWidget, QLabel, \
    QFrame
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtCore import QRect, QSize

import time
import os


class YahtzeeGui(object):
    def __init__(self):
        self.resources_path = os.path.join(os.path.dirname(__file__), 'resources')
        self.die_set = DieSet()
        self.button_list = []  # list of die button objects with dieGroup icon value applied
        self.button_die = {}  # dictionary with push button objects and corresponding die objects
        self.sorted_dice_list = []  # list with dice sorted from low to high
        self.y_table_list = []  # master list of all yahtzee table cells that have been filled
        self.table_clicked = False  # toggle flag for knowing if rolls should be stopped because of table entry
        self.dice_rolled = False  # toggle flag to know if any rolling has taken place
        self.die_rolls = 0  # number of times the dice have been rolled
        self.game_over = False  # variable to know if the game is over
        self.auto_fill = False  # used to prevent player cell entry if yahtzee bonus is in plan and upper section can be filled
        # if all three yahtzee cells are filled with 50's then the yahtzee must go into a upper section cell of the
        # same pip value.  If those are filled then the yahtzee can be used as a "joker" to fill in any full house,
        # small or large straight for full point values (25, 30 or 40).  The yahtzee bonus of 100 is filled into
        # the column of the score and multiplied by the column's multiple factor
        self.yahtzee_bonus = 0  # keeps track of number of yahtzees, if greater than 3 then yahtzee bonus rules apply
        self.yahtzee_bonus_list = [0, 0, 0]  # list of the yahtzee bonus values
        self.yahtzee_joker = False  # flag to know if a "joker" situation is true

    def setup(self, main_window):
        main_window.setObjectName("MainWindow")
        main_window.resize(900, 830)
        icon = QIcon()
        icon.addPixmap(QPixmap(os.path.join(self.resources_path, "y6.jpg")), QIcon.Normal,
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
            self.button_die[self.die] = self.die_set.get_at(i)  # dictionary of pairs of die buttons and die objectss
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
        item.setTextAlignment(QtCore.Qt.AlignCenter)
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
        for i in range(3):
            font = QFont()
            font.setBold(True)
            font.setWeight(75)
            item.setFont(font)
            item = QTableWidgetItem()
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

    def yahtzee_table_click(self, item):
        self.dice_rolled = False  # set to false to show that the dice rolling is over
        _translate = QtCore.QCoreApplication.translate
        self.roll_button.setText(_translate("MainWindow", "Roll"))  # put roll back on the button
        row = item.row()
        col = item.column()
        pip_value = 0
        in_table_list = False  # flag to know if the player has clicked on a cell that is already filled

        if self.auto_fill == False:  # checks to see if a yahtzee bonus autofill has already occurred
            if self.yahtzee_bonus > 2 and self.die_set.get_at(0).pip == self.die_set.get_at(
                    1).pip == self.die_set.get_at(2).pip == self.die_set.get_at(3).pip == self.die_set.get_at(4).pip:
                # Note this is a yahtzee bonus situation and special rules apply to the cell to be filled
                column_list = []
                for entry in self.y_table_list:  # look at each table cell entry to see if the upper cell corresponding to pip is filled
                    pip_value = (self.die_set.get_at(0).pip - 1)
                    if entry[0] == pip_value:
                        column_list.append(entry[1])  # make a list of columns already filled in
                column_list.sort()  # sort the column numbers from 0 to 2
                if len(column_list) < 3:  # if the column's upper section pip rows are not already all filled in
                    for i in range(2, -1, -1):  # step backwards through the list
                        if i not in column_list:  # pick the largest value from the list
                            entry_column = i
                            break  # get out of here
                    bonus = self.yahtzee_bonus_list[entry_column]  # see if any yahtzee bonus exists already
                    bonus += 100  # increase that value by 100
                    self.yahtzee_bonus_list[entry_column] = bonus  # update the list
                    point_value = ((pip_value + 1) * 5)  # total points to be filled in
                    self.y_table_list.append(
                        (pip_value, entry_column, point_value))  # append the tuple with row, col and total
                    item = QTableWidgetItem(str(point_value))  # make the point value 5 times the pip value
                    self.yahtzee_table.setItem((pip_value), entry_column, item)  # fill in the cell
                    item = QTableWidgetItem(str(bonus))  # set the yahtzee bonus value
                    self.yahtzee_table.setItem((17), entry_column, item)  # fill in the cell
                    self.auto_fill = True
                else:
                    self.yahtzee_joker = True
                    print(self.yahtzee_joker)
            for entry in self.y_table_list:  # look through the tuples in yTableList and see if the cell has been filled already
                print(self.yahtzee_joker)
                if entry[0] == row and entry[1] == col:
                    in_table_list = True
            if in_table_list == False and self.auto_fill == False:  # next line makes sure that the player didn't click on a "total" cell
                if self.table_clicked == True and row >= 0 and row <= 5 or self.table_clicked == True and row >= 10 and row <= 16:
                    last_cell = self.y_table_list[-1]  # get the last tuple in the the list
                    last_row = last_cell[0]
                    last_column = last_cell[1]
                    if self.yahtzee_joker == True:  # undo the yahtzee bonus from the last iteration
                        previous_bonus = self.yahtzee_bonus_list[last_column]
                        print(self.yahtzee_bonus_list)
                        previous_bonus -= 100
                        self.yahtzee_bonus_list[last_column] = previous_bonus
                        print(self.yahtzee_bonus_list)
                        item = QTableWidgetItem(str(previous_bonus))  # set the yahtzee bonus value
                        self.yahtzee_table.setItem((17), last_column, item)  # fill in the cell
                    self.y_table_list.pop()  # pop removes the last element in the list
                    item = QTableWidgetItem(str(""))  # put a blank fill in the formerly populated cell
                    self.yahtzee_table.setItem(last_row, last_column, item)
                die_total = 0
                if self.yahtzee_joker == True:  # if a yahtzee joker situation exists
                    print("ybl = " + str(self.yahtzee_bonus_list))
                    bonus = self.yahtzee_bonus_list[col]  # see if any yahtzee bonus exists already
                    print(bonus)
                    bonus += 100  # increase that value by 100
                    print(bonus)
                    self.yahtzee_bonus_list[col] = bonus  # update the list
                    item = QTableWidgetItem(str(bonus))  # set the yahtzee bonus value
                    self.yahtzee_table.setItem((17), col, item)  # fill in the cell

                # check to see if the selection is in the upper cells
                if row >= 0 and row <= 5:
                    for i in range(5):
                        die_pip = self.die_set.get_at(i).get_pip()
                        if die_pip == (row + 1):  # if the die pip matches the row selected
                            die_total += (row + 1)  # add that die to the total
                    item = QTableWidgetItem(str(die_total))
                    self.yahtzee_table.setItem(row, col, item)
                    self.y_table_list.append((row, col, die_total))  # append the touple with row, col and total
                    self.table_clicked = True  # set the tableClicked flag to true
                    self.total_up()  # call total up to sum the columns
                    if len(self.y_table_list) == 39:  # if all the cells are filled, end the game
                        self.end_game()
                # if the player clicked on the lower section of the table
                if row >= 10 and row <= 16:
                    self.sorted_dice_list = []
                    sorted_dice_group = self.die_set.copy()  # important to copy not set equal, copy makes the original not change
                    print("value = ")
                    print(sorted_dice_group[0].get_pip())
                    sorted_dice_group.sort(key=lambda x: x.get_pip())  # sort the group based upon pip value
                    for i in range(5):
                        print(self.die_set.get_at(i))
                    print(sorted_dice_group)
                    for i in range(5):
                        self.sorted_dice_list.append(sorted_dice_group[i].pip)  # append the die objects
                    # If three of a kind is selected
                    if row == 10:
                        total = self.three_of_a_kind()  # get the result from this function
                        item = QTableWidgetItem(str(total))
                        self.yahtzee_table.setItem(row, col, item)
                        self.y_table_list.append((row, col, total))
                        self.table_clicked = True
                        self.total_up()
                        if len(self.y_table_list) == 39:
                            self.end_game()
                    # if four of a kind is selected
                    if row == 11:
                        total = self.four_of_a_kind()  # get the result from this function
                        item = QTableWidgetItem(str(total))
                        self.yahtzee_table.setItem(row, col, item)
                        self.y_table_list.append((row, col, total))
                        self.table_clicked = True
                        self.total_up()
                        if len(self.y_table_list) == 39:
                            self.end_game()
                    # if full house is selected
                    if row == 12:
                        total = self.full_house()  # get the result from this function
                        item = QTableWidgetItem(str(total))
                        self.yahtzee_table.setItem(row, col, item)
                        self.y_table_list.append((row, col, total))
                        self.table_clicked = True
                        self.total_up()
                        if len(self.y_table_list) == 39:
                            self.end_game()
                    # if small straight is selected
                    if row == 13:
                        total = self.small_straight()  # get the result from this function
                        item = QTableWidgetItem(str(total))
                        self.yahtzee_table.setItem(row, col, item)
                        self.y_table_list.append((row, col, total))
                        self.table_clicked = True
                        self.total_up()
                        if len(self.y_table_list) == 39:
                            self.end_game()
                    # if large straight is selected
                    if row == 14:
                        total = self.large_straight()  # get the result from this function
                        item = QTableWidgetItem(str(total))
                        self.yahtzee_table.setItem(row, col, item)
                        self.y_table_list.append((row, col, total))
                        self.table_clicked = True
                        self.total_up()
                        if len(self.y_table_list) == 39:
                            self.end_game()
                    # if yahtzee is selected
                    if row == 15:
                        total = self.yahtzee()  # get the result from this function
                        item = QTableWidgetItem(str(total))
                        self.yahtzee_table.setItem(row, col, item)
                        self.y_table_list.append((row, col, total))
                        self.table_clicked = True
                        self.total_up()
                        if len(self.y_table_list) == 39:
                            self.end_game()
                    # if chance is selected
                    if row == 16:
                        total = self.chance()  # get the result from this function
                        item = QTableWidgetItem(str(total))
                        self.yahtzee_table.setItem(row, col, item)
                        self.y_table_list.append((row, col, total))
                        self.table_clicked = True
                        self.total_up()
                        if len(self.y_table_list) == 39:
                            print("End of Game")
                            self.end_game()

    # these are the helper methods for summing up the lower section totals
    def three_of_a_kind(self):
        print(self.sorted_dice_list)
        for i in range(3):  # look at the first three dice that have been sorted
            if self.sorted_dice_list[i] == self.sorted_dice_list[
                i + 2]:  # if the first is equal to the third then three of a kind
                total = 0
                for j in range(5):
                    total += int(self.sorted_dice_list[j])
                return total  # NOTE return ends the method so no need to try to break out
        return 0  # if no three of a kind return a zero

    def four_of_a_kind(self):
        for i in range(2):
            if self.sorted_dice_list[i] == self.sorted_dice_list[
                i + 3]:  # if the first is equal to the fourth then four of a kind
                total = 0
                for j in range(5):
                    total += int(self.sorted_dice_list[j])
                return total
        return 0

    def full_house(
            self):  # checks if the first three and last two are the same and first two and last three sorted dice
        if self.yahtzee_joker == True:
            return 25
        if self.sorted_dice_list[0] == self.sorted_dice_list[2] and self.sorted_dice_list[3] == self.sorted_dice_list[
            4] or self.sorted_dice_list[0] == \
                self.sorted_dice_list[1] and self.sorted_dice_list[2] == self.sorted_dice_list[4]:
            return 25
        else:
            return 0

    def small_straight(self):
        if self.yahtzee_joker == True:
            return 30
        print("sorted die list" + str(self.sorted_dice_list))
        new_list = [*set(self.sorted_dice_list)]  # sort the dice and remove duplicate pip values
        new_list.sort()  # sort the group based upon pip value
        print("new list = " + str(new_list))
        if len(new_list) < 4:  # if there are fewer than four dice in the list there can be no small straight
            return 0
        if len(new_list) < 5:  # if there are only four dice then go through the loop once (prevents read past end of list)
            step_to = 1
        else:
            step_to = 2  # otherwise go through twice to get all five dice checked out
        for i in range(step_to):  # check and see if each die is one more than the preceeding die
            print("in here")
            if int(new_list[i + 3]) == (int(new_list[i + 2]) + 1) and int(new_list[i + 2]) == (
                    int(new_list[i + 1]) + 1) and int(new_list[
                                                          i + 1]) == (int(new_list[i]) + 1):
                return 30
        return 0

    def large_straight(self):  # same logic as above but all five must be in sequence
        if self.yahtzee_joker == True:
            return 40
        if int(self.sorted_dice_list[4]) == (int(self.sorted_dice_list[3]) + 1) and int(self.sorted_dice_list[3]) == (
                int(
                        self.sorted_dice_list[2]) + 1) and \
                int(self.sorted_dice_list[2]) == (int(self.sorted_dice_list[1]) + 1) and int(
            self.sorted_dice_list[1]) == (int(
            self.sorted_dice_list[0]) + 1):
            return 40
        else:
            return 0

    def yahtzee(self):  # just checks if all die pip values are the same
        if self.sorted_dice_list[0] == self.sorted_dice_list[1] == self.sorted_dice_list[2] == self.sorted_dice_list[
            3] == self.sorted_dice_list[4]:
            self.yahtzee_bonus += 1  # if this gets to three then the yahtzee bonus rules apply
            return 50
        else:
            return 0

    def chance(self):  # just adds all five die pip values together
        total = int(self.sorted_dice_list[0]) + int(self.sorted_dice_list[1]) + int(self.sorted_dice_list[2]) + int(
            self.sorted_dice_list[
                3]) + int(self.sorted_dice_list[4])
        return total

    def die_clicked(self, button):  # this is called if a die is clicked
        clicked_die = self.button_die[
            button]  # sets clickedDie = to the die object dictionary pair to the button pressed
        if clicked_die.is_clicked == True:  # toggles the is_clicked value
            clicked_die.is_clicked = False
            print("in 1")
            clicked_die_icon = clicked_die.get_image()  # makes the die white
        else:
            clicked_die.is_clicked = True
            print("in 2")
            clicked_die_icon = clicked_die.get_image()  # makes the die yellow
        for i in range(5):
            if self.button_list[i] == button:
                self.button_list[i].setIcon(QIcon(os.path.join(self.resources_path, clicked_die_icon)))
        QApplication.processEvents()  # MUST HAVE THIS to update the dice icons

    def total_up(self):  # helper function to total up the columns
        top_total0 = 0
        top_total1 = 0
        top_total2 = 0
        bonus0 = 0
        bonus1 = 0
        bonus2 = 0
        top_grand_total0 = 0
        top_grand_total1 = 0
        top_grand_total2 = 0
        bottom_total0 = 0
        bottom_total1 = 0
        bottom_total2 = 0
        grand_total0 = 0
        grand_total1 = 0
        grand_total2 = 0
        y_grand_total = 0

        for y_tuple in self.y_table_list:  # look through the tuple list
            for i in range(3):  # look at each column
                if y_tuple[1] == i:  # if the tuple's column matches the column being summed
                    if y_tuple[0] <= 5:  # if it is in the top section
                        if y_tuple[1] == 0:  # if in the first column
                            top_total0 += y_tuple[2]  # incremet the top first column total by the value stored
                            if top_total0 >= 63:  # if the top total is > 63 then add the 35 point bonus
                                bonus0 = 35
                            else:
                                bonus0 = 0
                            top_grand_total0 = top_total0 + bonus0  # sum the top grand total
                            grand_total0 = bottom_total0 + top_grand_total0  # sum the top and bottom grand totals
                        elif y_tuple[1] == 1:  # repeat for column 1
                            top_total1 += y_tuple[2]
                            if top_total1 >= 63:
                                bonus1 = 35
                            else:
                                bonus1 = 0
                            top_grand_total1 = top_total1 + bonus1
                            grand_total1 = bottom_total1 + top_grand_total1
                        else:  # repeat for column 2
                            top_total2 += y_tuple[2]
                            if top_total2 >= 63:
                                bonus2 = 35
                            else:
                                bonus2 = 0
                            top_grand_total2 = top_total2 + bonus2
                            grand_total2 = bottom_total2 + top_grand_total2
                    else:  # we are in the lower section
                        if y_tuple[1] == 0:  # add the value to the lower total for column 0
                            bottom_total0 += y_tuple[2]
                            grand_total0 = bottom_total0 + top_grand_total0 + self.yahtzee_bonus_list[0]
                        elif y_tuple[1] == 1:  # same for column 1
                            bottom_total1 += y_tuple[2]
                            grand_total1 = bottom_total1 + top_grand_total1 + self.yahtzee_bonus_list[1]
                        else:  # same for column 2
                            bottom_total2 += y_tuple[2]
                            grand_total2 = bottom_total2 + top_grand_total2 + self.yahtzee_bonus_list[2]
        y_grand_total = grand_total2 * 3 + grand_total1 * 2 + grand_total0  # multiply col two by 3 and col two by 2, add
        self.label.setText("Grand Total = " + str(y_grand_total))
        # this section updates the table with the values generated above
        item = QTableWidgetItem(str(top_total0))
        self.yahtzee_table.setItem(6, 0, item)
        item = QTableWidgetItem(str(top_total1))
        self.yahtzee_table.setItem(6, 1, item)
        item = QTableWidgetItem(str(top_total2))
        self.yahtzee_table.setItem(6, 2, item)
        item = QTableWidgetItem(str(bonus0))
        self.yahtzee_table.setItem(7, 0, item)
        item = QTableWidgetItem(str(bonus1))
        self.yahtzee_table.setItem(7, 1, item)
        item = QTableWidgetItem(str(bonus2))
        self.yahtzee_table.setItem(7, 2, item)
        item = QTableWidgetItem(str(top_grand_total0))
        self.yahtzee_table.setItem(8, 0, item)
        item = QTableWidgetItem(str(top_grand_total1))
        self.yahtzee_table.setItem(8, 1, item)
        item = QTableWidgetItem(str(top_grand_total2))
        self.yahtzee_table.setItem(8, 2, item)
        item = QTableWidgetItem(str(bottom_total0))
        self.yahtzee_table.setItem(18, 0, item)
        item = QTableWidgetItem(str(bottom_total1))
        self.yahtzee_table.setItem(18, 1, item)
        item = QTableWidgetItem(str(bottom_total2))
        self.yahtzee_table.setItem(18, 2, item)
        item = QTableWidgetItem(str(grand_total0))
        self.yahtzee_table.setItem(19, 0, item)
        item = QTableWidgetItem(str(grand_total1))
        self.yahtzee_table.setItem(19, 1, item)
        item = QTableWidgetItem(str(grand_total2))
        self.yahtzee_table.setItem(19, 2, item)

    def end_game(self):  # helper function to end the game
        self.game_over = True  # set the flag for game over to true
        self.play_again.show()  # show the play again button

    def new_game(self):  # helper function to start a new game
        self.play_again.hide()  # hide the play again button
        self.game_over = False
        for i in range(5):  # reset all of the die objects to 0 and white
            die_object = self.die_set.get_at(i)
            die_object.is_clicked = False
            die_icon = die_object.get_image()
            self.button_list[i].setIcon(QIcon(os.path.join(self.resources_path, die_icon)))
            QApplication.processEvents()
        self.y_table_list = []  # clear the ytabledList for a new game
        self.yahtzee_bonus = 0
        for col in range(3):  # reset each column
            for row in range(20):  # and row
                item = QTableWidgetItem(str(""))  # to blank
                self.yahtzee_table.setItem(row, col, item)

    def roll_dice(self):  # helper method to roll the dice
        if self.game_over == False:  # if not in a game over state
            if self.dice_rolled == False:  # if the dice have not been rolled yet
                self.yahtzee_joker = False
                self.auto_fill = False
                self.table_clicked = False  # toggle these flag values
                self.dice_rolled = True
                self.die_rolls = 0  # reset die rolls to zero
                for i in range(5):  # since this is the first roll turn all yellow dice to white and
                    die = self.die_set.get_at(i)
                    die.is_clicked = False  # reset the is_clicked value to "w"
                    die_icon = die.get_image()
                    self.button_list[i].setIcon(QIcon(os.path.join(self.resources_path,
                                                                   die_icon)))  # update the buttons that actually display the dice
                    QApplication.processEvents()  # again without this the icons will not update
            if self.die_rolls < 3:  # if not pas the end of dice rolls
                for i in range(10):  # we're goining to go through 10 different dice values to simulate a roll
                    for j in range(5):  # go through each die
                        if self.die_set.get_at(j).is_clicked == False:  # if the die can be rolled (ie not clicked)
                            last_time = 0  # set the lastTime flag to zero
                            if i == 9:  # on the last of the 10 rolls
                                last_time = 1  # set last time to 1 to set the die button values
                            self.show_die(self.die_set.get_at(j), j, last_time)  # call show dice to display the icons
                    time.sleep(.07)  # short sleep to slow down the roll 70 ms
                self.die_rolls += 1  # increment dieRolls toward three
                rolls_left = 3 - self.die_rolls  # rolls left will be displayed on the roll button
                _translate = QtCore.QCoreApplication.translate
                if self.die_rolls == 2:  # if there is one roll left maKe roll singular
                    self.roll_button.setText(_translate("MainWindow", (str(rolls_left) + " Roll Left")))
                else:  # otherwise make plural
                    self.roll_button.setText(_translate("MainWindow", (str(rolls_left) + " Rolls Left")))

    def show_die(self, die_object, rolling_die, last_time):  # helper method to display the dice
        die = die_object
        die.roll_die()  # generate a random number between 1 and 6
        die_icon = die.get_image()  # set the icon image
        # pip = 6 #for testing yahtzee bonus logic
        self.button_list[rolling_die].setIcon(QIcon(os.path.join(self.resources_path, die_icon)))
        QApplication.processEvents()  # again must be called to update the icon images
        if last_time == 1:  # if this is the last roll then
            die_value = die.get_pip()  # die_icon.strip('wy.jpg')
            print(die_value)
            die_object.pip = die_value  # set the die object's pip value to the random number for use later
