# This program asks the user which state of the US it wants to check for the cases of COVID-19.
# The user gives the state name , the statistic (i.e positive, negative) it wants to check.
# The user can optionally give the start or end date.
# If the user don't want to provide start or end date, results will be shown from beginning to day today

# All the required modules are imported firstly
import json, urllib.request
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt
import sys


# We are using the Object oriented approach to make our code more professional
class DataAnalyzer():
    # This function is used to do main job of the program. It takes 5 parameters.
    def date_not_exists(self, data, state, statistic, start_date, end_date):
        dates = []
        count = []
        print("Date\t\t\t" + statistic.capitalize())
        for o_dict in data:     # This loop is calling the dictionary one by one
            abc_dict = dict((k.lower(), v) for k, v in o_dict.items())  # Converting dictionary keys to small alphabets
            if state.upper() in o_dict.values():                        # Checking if the state exists in our dictionary
                if abc_dict['state'] == state.upper():                  # if state name matches
                    if (abc_dict['date'] >= start_date) and (abc_dict['date'] <= end_date):  # and date is between range
                        if statistic.lower() in abc_dict.keys():        # if statistic is present in current dictionary
                            if abc_dict[statistic.lower()] is not None:  # only if there are some numbers present
                                print(str(abc_dict['date']) + "\t\t" + str(abc_dict[statistic.lower()]))
                                dates.append(abc_dict['date'])
                                count.append(abc_dict[statistic.lower()])
                            elif abc_dict[statistic.lower()] is None:  # if the value is null, do nothing
                                pass

        if len(count) == 0 and len(dates) == 0:     # this condition is used to check if some record is found
            print("No Record Found. Please Try Again")
        else:
            y_pos = np.arange(len(dates))
            plt.bar(y_pos, count, align='center', alpha=0.5)
            plt.xticks(y_pos, dates, rotation='vertical',  ha="right")
            plt.ylabel(statistic.upper())
            plt.xlabel("DATES")
            plt.title("Coronavirus in " + state.upper() + " between " + str(dates[-1]) + " and " + str(dates[0]))
            plt.show()
        self.re_analyze()

    # this function checks if the user wants to perform another analysis
    def re_analyze(self):
        re_analysis = input("Perform another analysis (yes/no)? ")
        if re_analysis.lower() == 'yes':
            main()
        elif re_analysis.lower() == 'no':
            sys.exit()
        else:
            print("Kindly Enter Correct Choice")
            self.re_analyze()


# this is main fucntion controlling the flow of program
def main():
    try:        # try except is used to check if the data is available
        data = urllib.request.urlopen("https://covidtracking.com/api/v1/states/daily.json").read()
        output = json.loads(data)
        data = output
    except:
        print("Can't Get Data Currently. Check Your Internet Connection And Try Again.")
        sys.exit()
    print("Welcome to the coronavirus (COVID-19) live data analyzer!")
    in_state = input("Which location would you like to search? ")
    in_statistic = input("Which statistic would you like to search? ")
    in_start = input("Would you like to add a start date (yes/no)? ")
    if in_start.lower() == 'yes':
        try:
            in_start_date = int(input("Which start date would you like to use (YYYYMMDD)? "))
        except ValueError:
            print("You Entered Wrong Date. Results will be shown from beginning")
            in_start_date = -99999999
    elif in_start.lower() == 'no':
        in_start_date = -99999999
    else:
        print("You Entered Wrong Choice. Results will be shown from beginning")
        in_start_date = -99999999

    in_end = input("Would you like to add an end date (yes/no)? ")
    if in_end.lower() == 'yes':
        try:
            in_end_date = int(input("Which end date would you like to use (YYYYMMDD)?"))
        except ValueError:
            print("You Entered Wrong Date. Results will be shown until today")
            in_end_date = 99999999
    elif in_end.lower() == 'no':
        in_end_date = 99999999
    else:
        print("You Entered Wrong Choice. Results will be shown until today")
        in_end_date = 99999999
    # making instance of class and calling its function
    da = DataAnalyzer()
    da.date_not_exists(data, in_state, in_statistic, in_start_date, in_end_date)


main()