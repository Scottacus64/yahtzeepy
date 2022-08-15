import time


class YahtzeeGame(object):
    def __init__(self):
        self.game = 0
        self.sorted_dice_list = []  # list with dice sorted from low to high
        self.die_rolls = 0  # number of times the dice have been rolled
        self.rolls_left = 3
        self.dice_rolled = False  # toggle flag to know if any rolling has taken place
        self.game_over = False  # variable to know if the game is over
        self.yahtzee_bonus = 0  # keeps track of number of yahtzees, if greater than 3 then yahtzee bonus rules apply
        self.yahtzee_bonus_list = [0, 0, 0]  # list of the yahtzee bonus values
        self.yahtzee_joker = False  # flag to know if a "joker" situation is true
        self.no_rolls = True  # flag to know if any die rolls have occurred in a new game
        self.yahtzee_table_list = []  # list of all table entires
        self.top_totals_list = []
        self.bottom_totals_list = []
        self.yahatzee_grand_total = 0
        self.auto_fill = False  # used to prevent player cell entry if yahtzee bonus is in play and upper section can be filled
        # if all three yahtzee cells are filled with 50's then the yahtzee must go into a upper section cell of the
        # same pip value.  If those are filled then the yahtzee can be used as a "joker" to fill in any full house,
        # small or large straight for full point values (25, 30 or 40).  The yahtzee bonus of 100 is filled into
        # the column of the score and multiplied by the column's multiple factor

    def end_game(self):  # helper function to end the game
        self.game_over = True  # set the flag for game over to true

    def new_game(self):  # helper function to start a new game
        self.game_over = False
        self.no_rolls = True
        self.yahtzee_bonus = 0
        self.yahtzee_grand_total = 0
        self.top_totals_list = []  # clear the top and bottom totals
        self.bottom_totals_list = []
        self.yahtzee_table_list = []  # clear the ytable List for a new game

    def roll_dice(self, die_set):  # helper method to roll the dice
        if self.game_over == False:  # if not in a game over state
            self.no_rolls = False
            if self.dice_rolled == False:  # if the dice have not been rolled yet
                self.auto_fill = False
                self.yahtzee_joker = False
                self.table_clicked = False  # toggle these flag values
                self.dice_rolled = True
                self.die_rolls = 1  # reset die rolls to after first roll
                for i in range(5):
                    die = die_set.get_at(i)
                    if die.is_clicked == True:  # toggles the is_clicked value
                        die.is_clicked = False

            for j in range(5):  # go through each die
                die = die_set.get_at(j)
                if die.is_clicked == False:  # if the die can be rolled (ie not clicked)
                    die.roll_die()  # generate a random number between 1 and 6
            time.sleep(.07)  # short sleep to slow down the roll 70 ms

    def sort_dice(self, die_set):
        self.sorted_dice_list = []
        sorted_dice_group = die_set.copy()  # important to copy not set equal, copy makes the original not change
        sorted_dice_group.sort(key=lambda x: x.get_pip())  # sort the group based upon pip value
        for i in range(5):
            self.sorted_dice_list.append(sorted_dice_group[i].pip)  # append the die objects

    def unset_dice_rolled(self):
        self.dice_rolled = False  # set to false to show that the dice rolling is over

    # these are the helper methods for summing up the lower section totals
    def three_of_a_kind(self, die_set):
        self.sort_dice(die_set)
        for i in range(3):  # look at the first three dice that have been sorted
            if self.sorted_dice_list[i] == self.sorted_dice_list[
                i + 2]:  # if the first is equal to the third then three of a kind
                total = 0
                for j in range(5):
                    total += int(self.sorted_dice_list[j])
                return total  # NOTE return ends the method so no need to try to break out
        return 0  # if no three of a kind return a zero

    def four_of_a_kind(self, die_set):
        self.sort_dice(die_set)
        for i in range(2):
            if self.sorted_dice_list[i] == self.sorted_dice_list[
                i + 3]:  # if the first is equal to the fourth then four of a kind
                total = 0
                for j in range(5):
                    total += int(self.sorted_dice_list[j])
                return total
        return 0

    # checks if the first three and last two are the same or the first two and last three (sorted dice)
    def full_house(self, die_set):
        self.sort_dice(die_set)
        if self.yahtzee_joker == True:
            return 25
        if self.sorted_dice_list[0] == self.sorted_dice_list[2] and self.sorted_dice_list[3] == self.sorted_dice_list[
            4] or self.sorted_dice_list[0] == \
                self.sorted_dice_list[1] and self.sorted_dice_list[2] == self.sorted_dice_list[4]:
            return 25
        else:
            return 0

    def small_straight(self, die_set):
        self.sort_dice(die_set)
        if self.yahtzee_joker == True:
            return 30
        new_list = [*set(self.sorted_dice_list)]  # sort the dice and remove duplicate pip values
        new_list.sort()  # sort the group based upon pip value
        if len(new_list) < 4:  # if there are fewer than four dice in the list there can be no small straight
            return 0
        if len(new_list) < 5:  # if there are only four dice then go through the loop once (prevents read past end of list)
            step_to = 1
        else:
            step_to = 2  # otherwise go through twice to get all five dice checked out
        for i in range(step_to):  # check and see if each die is one more than the preceeding die

            if int(new_list[i + 3]) == (int(new_list[i + 2]) + 1) and int(new_list[i + 2]) == (
                    int(new_list[i + 1]) + 1) and int(new_list[
                                                          i + 1]) == (int(new_list[i]) + 1):
                return 30
        return 0

    def large_straight(self, die_set):  # same logic as above but all five must be in sequence
        self.sort_dice(die_set)
        if self.yahtzee_joker == True:
            return 40
        if int(self.sorted_dice_list[4]) == (int(self.sorted_dice_list[3]) + 1) and int(self.sorted_dice_list[3]) == (
                int(self.sorted_dice_list[2]) + 1) and int(self.sorted_dice_list[2]) == (
                int(self.sorted_dice_list[1]) + 1) and int(self.sorted_dice_list[1]) == (
                int(self.sorted_dice_list[0]) + 1):
            return 40
        else:
            return 0

    def yahtzee(self, die_set):  # just checks if all die pip values are the same
        self.sort_dice(die_set)
        if self.sorted_dice_list[0] == self.sorted_dice_list[1] == self.sorted_dice_list[2] == self.sorted_dice_list[
            3] == self.sorted_dice_list[4]:
            self.yahtzee_bonus += 1  # if this gets to three then the yahtzee bonus rules apply
            return 50
        else:
            return 0

    def chance(self, die_set):  # just adds all five die pip values together
        self.sort_dice(die_set)
        total = int(self.sorted_dice_list[0]) + int(self.sorted_dice_list[1]) + int(self.sorted_dice_list[2]) + int(
            self.sorted_dice_list[
                3]) + int(self.sorted_dice_list[4])
        return total

    def total_up(self):  # helper function to total up the columns
        top_total0 = top_total1 = top_total2 = 0
        bonus0 = bonus1 = bonus2 = 0
        top_grand_total0 = top_grand_total1 = top_grand_total2 = 0
        bottom_total0 = bottom_total1 = bottom_total2 = 0
        grand_total0 = grand_total1 = grand_total2 = 0
        self.yahtzee_grand_total = 0
        for y_tuple in self.yahtzee_table_list:  # look through the tuple list
            for i in range(3):  # look at each column
                if y_tuple[1] == i:  # if the tuple's column matches the column being summed
                    if y_tuple[0] <= 5:  # if it is in the top section
                        if y_tuple[1] == 0:  # if in the first column
                            top_total0 += y_tuple[2]  # increment the top first column total by the value stored
                            if top_total0 >= 63:  # if the top total is > 63 then add the 35 point bonus
                                bonus0 = 35
                            else:
                                bonus0 = 0
                            top_grand_total0 = top_total0 + bonus0  # sum the top grand total
                            grand_total0 = bottom_total0 + top_grand_total0 + self.yahtzee_bonus_list[
                                0]  # sum the top and bottom grand totals
                        elif y_tuple[1] == 1:  # repeat for column 1
                            top_total1 += y_tuple[2]
                            if top_total1 >= 63:
                                bonus1 = 35
                            else:
                                bonus1 = 0
                            top_grand_total1 = top_total1 + bonus1
                            grand_total1 = bottom_total1 + top_grand_total1 + self.yahtzee_bonus_list[1]
                        else:  # repeat for column 2
                            top_total2 += y_tuple[2]
                            if top_total2 >= 63:
                                bonus2 = 35
                            else:
                                bonus2 = 0
                            top_grand_total2 = top_total2 + bonus2
                            grand_total2 = bottom_total2 + top_grand_total2 + self.yahtzee_bonus_list[2]
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
        self.yahtzee_grand_total = grand_total2 * 3 + grand_total1 * 2 + grand_total0  # multiply col two by 3 and col two by 2, add
        # this section updates the table with the values generated above
        self.top_totals_list = [top_total0, top_total1, top_total2, bonus0, bonus1, bonus2, top_grand_total0,
                                top_grand_total1,
                                top_grand_total2
                                ]
        self.bottom_totals_list = [bottom_total0, bottom_total1, bottom_total2, grand_total0, grand_total1,
                                   grand_total2]

