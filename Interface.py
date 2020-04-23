from collections import namedtuple
from datetime import date
import sys
import ast
from tokenize import String
from xmlrpc.client import Boolean

from Team import Team

def totalFees(n):
    count = 0
    for k, v in team_info.items():
        for x, z in v.items():
            if z == 'yes':
                count = count + 1
    return count * Team.fee


def nonPaidTeamsPercent(n):
    count = 0
    for k, v in team_info.items():
        for x, z in v.items():
            if z == 'no':
                count = count + 1
    try:
        percentage = (count / n) * 100
    except ZeroDivisionError:
        percentage = 0
    return str(percentage) + ' %'


class Menu:
    global team_info
    global team_data
    team_info = {}
    team_data = ['Enter City Name: ', 'Fee Paid? [yes/no]', 'Number of Players: ', 'Date of Registry:']
    Option = namedtuple('Option', 'label')
    _separator = "=" * 25
    _options = {1: Option("Add Team"), 2: Option("Select Team"),
                3: Option("Update Team"), 4: Option("Delete Team"),
                5: Option("Exit")}

    def print_header(self):
        print("{0}\n Please Select An Option\n{0}".format(self._separator))

    def print_mainMenu(self):
        totalTeams = len(team_info)
        print("\nTotal Number of Teams are: ", totalTeams)
        print("\nTotal Sum of Fees is: ", totalFees(totalTeams))
        print("\nTotal percentage of Unpaid Teams : ", nonPaidTeamsPercent(totalTeams),"\n")
        self.print_header()
        for option in sorted(self._options.keys()):
            print("{0} {1}".format(option, self._options[option].label))

    def prompt(self):
        option = int(input("Select Option: "))
        dict_options_keys = self._options.keys()
        if option in dict_options_keys:
            return option
        else:
            print('Enter Valid Option')

    def write_to_file(self):
        f = open("Teams.txt", "w")
        f.write(str(team_info))
        f.close()

    def handle_input(self, chosen_option):
        try:
            if chosen_option == 1:
                team_name = input("Enter Team Name: ")
                team_info[team_name] = {}
                for entry in team_data:
                    if entry == 'Enter City Name: ':
                        team_info[team_name][entry] = input(entry)
                    elif entry == 'Fee Paid? [yes/no]':
                        fee_paid = input(entry)
                        if fee_paid.lower() == 'no':
                            team_info[team_name][entry] = fee_paid.lower()
                        elif fee_paid.lower() == 'yes':
                            team_info[team_name][entry] = fee_paid.lower()
                        else:
                            print('You Entered Wrong Value')
                            main()
                    elif entry == 'Number of Players: ':
                        team_info[team_name][entry] = int(input(entry))
                    elif entry == 'Date of Registry:':
                        team_info[team_name][entry] = date.today()

            if chosen_option == 2:
                name = input("Enter Team Name: ")
                for k, v in team_info.items():
                    if name == k:
                        for key, value in v.items():
                            print('City Name: ' + (v['Enter City Name: ']))
                            print('Fee Paid: ' + (v['Fee Paid? [yes/no]']))
                            print('Number of Players: ' + str((v['Number of Players: '])))
                            date_one = v['Date of Registry:']
                            date_two = date.today()
                            delta = date_two - date_one
                            print("Team Registered " + str(delta.days) + " days ago.")
                            break
                    else:
                        print("Team Does Not Exist")
                    break
                main()
            if chosen_option == 3:
                name = input("Enter Team Name You Want To Update: ")
                for k, v in team_info.items():
                    if name == k:
                        team_info[k]['Enter City Name: '] = input('Enter City: ')
                        fee_paid = input('Fee paid ?')
                        if fee_paid.lower() == 'no':
                            team_info[k]['Fee Paid? [yes/no]'] = fee_paid.lower()
                        elif fee_paid.lower() == 'yes':
                            team_info[k]['Fee Paid? [yes/no]'] = fee_paid.lower()
                        else:
                            print('You Entered Wrong Value')
                            main()
                        team_info[k]['Number of Players: '] = input('Enter Players: ')
                    else:
                        print("Team Does Not Exist")
                    break
                main()
            if chosen_option == 4:
                name = input("Enter Team Name You Want To Delete: ")
                team_info_keys = list(team_info.keys())
                if name in team_info_keys:
                    for k in team_info_keys:
                        if name == k:
                            del team_info[k]
                else:
                    print("Team Does Not Exist")
            if chosen_option == 5:
                self.write_to_file()
                sys.exit()

        except KeyError:
            print("Wrong Option")





def main():
    menu = Menu()
    menu.print_mainMenu()
    menu.handle_input(menu.prompt())



    main()


if __name__ == '__main__':
    main()