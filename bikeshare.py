import time
import calendar
import datetime as dt
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def hms(seconds):
    """calculate hours, minutes, seconds from seconds"""
    a=str(seconds//3600)
    b=str((seconds%3600)//60)
    c=str((seconds%3600)%60)
    d="{} hours {} mins {} seconds".format(a, b, c)
    return d

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
    while True:
        try:
            city = input("Please enter one of the following cities: Chicago, New York City, Washington\n")
            if city.lower() in CITY_DATA:
                city = city.lower()
                break
            else:
                print("{} is not in the list of cities.\n".format(city))
                start_again = input("Would you like to try again? yes or no\n")
                if start_again.lower() != "yes":
                    exit()
        except (KeyboardInterrupt, ValueError):
            print("Incorrect input")

    # get user input for month (all, january, february, ... , june)
    while True:
        try:
            month = input("Which month? All, January, February, March, April, May or June\n")
            valid_month = ['all','january','february','march','april','may','june']
            if month.lower() in valid_month:
                month = month.lower()
                break
            else:
                print("{} is not in the list of months.\n".format(month))
                start_again = input("Would you like to try again? yes or no\n")
                if start_again.lower() != "yes":
                    exit()
        except (KeyboardInterrupt, ValueError):
            print("Incorrect input")

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while True:
        try:
            day = input("Which day of the week? All, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday or Sunday\n")
            valid_day= ['all','monday','tuesday','wednesday','thursday','friday','saturday','sunday']
            if day.lower() in valid_day:
                day = day.lower()
                break
            else:
                print("{} is not in the list of months.\n".format(day))
                start_again = input("Would you like to try again? yes or no\n")
                if start_again.lower() != "yes":
                    exit()
        except (KeyboardInterrupt, ValueError):
            print("Incorrect input")

    print('-'*40)
    return city, month, day


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
    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from the Start Time column to create a month, day of week and hour column
    df['month'] = df['Start Time'].dt.month
    df['day of week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour

    # display the most common month
    common_month = df['month'].mode()[0]
    print('Most common month: ', calendar.month_name[common_month], '\n( Count:',df['month'].value_counts().max(),')')

    # display the most common day of week
    common_weekday = df['day of week'].mode()[0]
    print('\nMost common day of week: ', common_weekday, '\n( Count:',df['day of week'].value_counts().max(),')')

    # display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('\nMost common start hour: ', common_hour, '\n( Count:',df['hour'].value_counts().max(),')')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('\nMost common start station: ', start_station, '\n( Count:', (df['Start Station'] == start_station).sum(),')')

    # display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('\nMost common end station: ', end_station, '\n( Count:', (df['End Station'] == end_station).sum(),')')

    # display most frequent combination of start station and end station trip
    start_end_station = df[['Start Station','End Station']].value_counts().idxmax()
    print('\nMost frequent combination of start station and end station: ', start_end_station[0],' / ',start_end_station[1], '\n( Count:', df[['Start Station','End Station']].value_counts().max(),')')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    total_travel_time = int(df['Trip Duration'].sum())
    print('\nTotal travel time: ', hms(total_travel_time))

    # display mean travel time
    mean_travel_time = int(df['Trip Duration'].mean())
    print('\nMean travel time: ', hms(mean_travel_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # fill NaN (missing values) with 0
    df.fillna('na')

    # Display counts of user types
    count_user_type = df['User Type'].value_counts()
    print('\nCounts of user types:\n\n', count_user_type)

    if 'Gender' in df.columns:
    # Display counts of gender
        gender = df['Gender'].value_counts()
        print('\nCounts of gender:\n\n', gender)
    else:
        print('\nCounts of gender: no data available')
    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        min_birth_year = int(df['Birth Year'].min())
        max_birth_year = int(df['Birth Year'].max())
        common_birth_year = int(df['Birth Year'].mode()[0])

        print('\nEaliest year of birth:', min_birth_year)
        print('\nMost recent year of birth:', max_birth_year)
        print('\nMost common year of birth:', common_birth_year, '\n( Count:', (df['Birth Year'] == common_birth_year).sum(),')')
    else:
        print('\nEaliest year of birth: no data available')
        print('\nMost recent year of birth: no data available')
        print('\nMost common year of birth: no data available')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def show_data(df):
    """Prompt the user if they want to see 5 lines of raw data"""
    data_display = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
    if data_display.lower() != 'yes':
        exit()
    else:
        start = 0
        end = 5
        # get number of rows
        total_rows = df.shape[0]
        while end < total_rows:
                print(df.iloc[start:end,:])
                start_again = input("\nWould you like to see more? yes or no\n")
                if start_again.lower() != "yes":
                    break
                else:
                    start += 5
                    end += 5

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        show_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
