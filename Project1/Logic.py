from PyQt6.QtWidgets import *
from Final_UI_1 import *
import csv
import re

class Logic(QMainWindow, Ui_VotingBooth):
    def __init__(self) -> None:
        '''
        Method to set up the UI, and submit the data to def submit(self):
        '''
        super().__init__()
        self.setupUi(self)
        self.Submit.clicked.connect(lambda : self.submit())

    def submit(self: Ui_VotingBooth) -> None:
        """
         This makes sure self.Identificatior is a 5-digit ID, if it's not it raises the ValueError (It will
        raise the NameError if the ID has been used previously), After it makes sure
        the proper parameters are met it makes sure either radio_john or radio_jane are clicked, if not a SyntaxError
        is raised. Depending on which one was clicked upon submission john_votes or jane_votes increases by one
        and status is updated to their respective name. After this is done the Votes.csv file is open
        and a re.findall is used to look for uses of john or jane (depending on what the status is) on the row with
        who was voted for, for every time it's located john_votes or jane_votes increases by one. After this finishes
        the totals get added as the total variable, it then checks if john_votes or jane_votes has a higher score
        depending on who has the higher score the winner variable will be updated with their name, in case of a tie
        the winner variable will be updated to say draw. it will then turn the total, john_votes and jane_votes
        into strings and then self.display will be updated to say
        "John has a score of (john_string) Current votes are (total_string)" and self.Error will be updated to say
        "Jane has a score of (jane_string) Current winner is (winner)". After this is done The ID, individual voted for,
        Jane total, John total, overall total, and current winner is sent to Votes.csv

        :raise ValueError: if the Identifier is not 5-digits
        :raise NameError: If the 5-digit ID has been used previously
        :raise SyntaxError: If neither radio_jane nor radio_john was pressed

        """

        jane_votes: int = 0
        john_votes: int = 0
        try:
            ident: int = int(self.Identificator.text())
            search: str = str(ident)

            if ident < 10000:
                raise ValueError
            elif ident > 99999:
                raise ValueError

            if self.buttonGroup.checkedButton() is self.Radio_Jane:
                status: str = 'Jane'
                jane_votes: int = 1
            elif self.buttonGroup.checkedButton() is self.Radio_John:
                status: str = 'John'
                john_votes: int = 1
            else:
                raise SyntaxError

            with open('Votes.csv', 'r', newline='') as e:
                read = csv.reader(e)
                for row in read:
                    if re.findall('Jane', row[1]):
                        jane_votes += 1
                    else:
                        pass

                e.seek(0)
                read = csv.reader(e)
                for row in read:
                    if re.findall('John', row[1]):
                        john_votes += 1
                    else:
                        pass

            e.close()

            total = jane_votes + john_votes

            if john_votes > jane_votes:
                winner: str = 'John'
            elif jane_votes > john_votes:
                winner: str = 'Jane'
            else:
                winner = 'Draw'
            total_string: str = str(total)
            john_string: str = str(john_votes)
            john_text: str = 'John has a score of ' + john_string + '   Current votes are:  ' + total_string

            jane_string: str = str(jane_votes)
            jane_text: str = 'Jane has a score of ' + jane_string + '   Current winner is ' + winner

            with open('Votes.csv', 'a', newline='') as output_csv_file:
                with open('Votes.csv', 'r', newline='') as input_file:
                    read = input_file.read()
                    if search in read:
                        raise NameError
                content = csv.writer(output_csv_file)
                content.writerow([ident, status, jane_votes, john_votes, total, winner])
            output_csv_file.close()

            self.display.setText(jane_text)
            self.Error.setText(john_text)
            self.Identificator.setText('')


            if self.buttonGroup.checkedButton() is not None:
                self.buttonGroup.setExclusive(False)
                self.buttonGroup.checkedButton().setChecked(False)
                self.buttonGroup.setExclusive(True)

        except ValueError:
            self.Error.setText('Invalid ID')
            self.display.setText('')
        except SyntaxError:
            self.Error.setText('Select a candidate')
            self.display.setText('')
        except NameError:
            self.Error.setText('You already voted!')
            self.display.setText('')

        self.Identificator.setFocus()