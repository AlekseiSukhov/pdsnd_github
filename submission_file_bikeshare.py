import time
import pandas as pd
import numpy as np
import calendar

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
TIME_FRAME = {'month':'m','day':'d','both':'b','none':'n'}
MONTH_DICT = {"jan" : 1,
            "feb" : 2,
            "mar" : 3,
            "apr" : 4,
            "may" : 5,
            "jun" : 6,
            "all" : "all" }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs

    month = None
    day = None

    while True:
        try:
            city = CITY_DATA[input("Would you like to see data for Chicago, New York City or Washington?\n").lower()]
            break
        except KeyError:
            print("\nYou might have tryped in the city name wrong, please imput one of the cities from the list.")

    TIME_FRAME = {'month':'m','day':'d','both':'b','none':'n'}
# get user input for month (all, january, february, ... , june)
    while True:
        try:
            tf = TIME_FRAME[input('Would you like to filter the data by month, day, both or not at all? Type "none" for no time filter.\n').lower()]
            break
        except KeyError:
            print("\nThe time frame you have specified is not a part of the list, please choose one from the list.")


    if tf == "m":
        while True:
            try:
                month = MONTH_DICT[input("Which month? January, Febriary, March, April, May or June?\n").lower()[:3]]
                day = None
                break
            except KeyError:
                print("\nYour input is not valid, follow the instructions bellow:")


    elif tf == 'd':
        while True:
            try:
                day = int(input("Which day of the week would you like to asses? Please type your response as an integer (e.g., 0=Monday).\nEnter 7 for 'all'.\n"))
                month = None
                if day == 7:
                   day = None
                   break
                elif 0<= day <=6:
                    break
            except ValueError:
                print("\nYour input is not valid, follow the instructions bellow:")


    elif tf == 'b':
        while True:
            try:
                month = MONTH_DICT[input("Which month? January, February, March, April, May or June?\n").lower()[:3]]
                break
            except KeyError:
                print("\nYour input is not valid, follow the instructions bellow:")
        while True:
            try:
                day = int(input("Which day of the week would you like to asses? Please type your response as an integer (e.g., 0=Monday).\nEnter 7 for 'all'\n"))
                if day == 7:
                   day = None
                   break
                elif 0<= day <=6:
                    break
                else:
                    print("\nYour input is not valid, follow the instructions bellow:")
            except ValueError:
                print("\nYour input is not valid, follow the instructions bellow:")


    print("You have chosen: ",city," ", month," ", day," ")
    return city,month,day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city)
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    if month != None:
    # use the index of the months list to get the corresponding int

        df = df[df['month'] == month]
    else:
        df = df

    # filter by day of week

    if day != None:
    #filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day]
    else:
        df = df


    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    most_common_month = df['month'].mode()[0]
    print('The most common month to travel is: {}'.format(calendar.month_name[most_common_month]))

    # display the most common day of week

    most_common_day_of_week = df['day_of_week'].mode()[0]
    print('The most common day of the week to travel is: {}'.format(calendar.day_name[most_common_day_of_week]))

    # display the most common start hour

    df['hour'] = df['Start Time'].dt.hour
    most_common_day_start_hour = df['hour'].mode()[0]
    print('The most common hour of the day to travel is: {}'.format(most_common_day_start_hour))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is: {}'.format(start_station))

    # display most commonly used end station
    most_common_end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is: {}'.format(most_common_end_station))

    # display most frequent combination of start station and end station trip
    df['comb'] = df['Start Station'] + ' to ' + df['End Station']
    common_combo = df['comb'].mode()[0]
    print('Most common combination of Start and End station:{}'.format(common_combo))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('The total duration of all trips that qulaify the input createria is:{}'.format(total_travel_time))

    # display mean travel time
    avg_travel_time =np.nanmean(df['Trip Duration'])
    print('The mean duration of a trip that qulaifies for the input createria is:{}'.format(avg_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('User type and resprective count:\n{}'.format(user_types))

    # Display counts of gender
    while True:
        try:
            gender_type = df['Gender'].value_counts()
            print('The gender distribution is:\n{}'.format(gender_type))
            break
        except KeyError:
            print('Sorry there is not data about gender for this city')
            break
    # Display earliest, most recent, and most common year of birth
        try:
            earliest_yob = int(df['Birth Year'].min())
            print('The eariest year of birth is:{}'.format(earliest_yob))
            break
        except KeyError:
            print('Sorry there is not data about clients\' date of birth for this city')
            break
        try:
            most_recent_youb = int(df['Birth Year'].max())
            print('The most recent year of birth is:{}'.format(most_recent_youb))
        except KeyError:
            break
        try:
            most_common_yob = int(df['Birth Year'].mode()[0])
            print('The most common year of birth is:{}'.format(most_common_yob))
            break
        except KeyError:
            break

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):

    start_count = 0
    end_count = 5

    answ = input('\nWould you like to see the indivudual data for the user of this bycyle cervice? Type in yes or no\n').lower()
    if answ == 'yes':

        while answ == 'yes':
            print(df[start_count:end_count])
            start_count+=5
            end_count+=5
            answ = input('Would you like to see more raw data? Type in yes or no\n').lower()



def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        raw_data(df)



        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break
        else:
            print('Than you for using our algorythm to gain insight aobut bikeshare data.')


if __name__ == "__main__":
	main()
#/Users/alekesisukhov/Desktop/Udacity/Part3/pdsnd_github/submission_file_bikeshare.py
