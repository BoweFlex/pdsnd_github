import time
import sys
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def month_switcher(month):
    """
    Takes an unwanted month variable as input and returns the desired month type instead

    Returns:
        (int) month - if given a string, returns the number month associated with it
        (str) month - if given an int, returns the name of the month associated with it
    """
    
    if type(month) is str:
        MONTH_SWITCH = { 'january': 1,
                        'february': 2,
                        'march': 3,
                        'april': 4,
                        'may': 5,
                        'june': 6,
                        'all': 7 }
        return MONTH_SWITCH.get(month)
    else:
        MONTH_SWITCH = { 1: 'january',
                         2: 'february',
                         3: 'march',
                         4: 'april',
                         5: 'may',
                         6: 'june',
                         7: 'all'}
        return MONTH_SWITCH.get(month)

def day_switcher(day):
    """
    Takes an unwanted day variable as input and returns the desired type instead

    Returns:
        (int) day - if given a string, returns the number day associated with it
        (str) day - if given an int, returns the name of the day associated with it
    """

    if type(day) is str:
        DAY_SWITCH = { 'monday': 0,
                   'tuesday': 1,
                   'wednesday': 2,
                   'thursday': 3,
                   'friday': 4,
                   'saturday': 5,
                   'sunday': 6,
                   'all': 7 }
        return DAY_SWITCH.get(day)
    else:
        DAY_SWITCH = { 0: 'monday',
                       1: 'tuesday',
                       2: 'wednesday',
                       3: 'thursday',
                       4: 'friday',
                       5: 'saturday',
                       6: 'sunday',
                       7: 'all' }
        return DAY_SWITCH.get(day)

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    
    #Lists for checking month & day input
    VAL_MONTHS = "january february march april may june all".split()
    VAL_DAYS = "monday tuesday wednesday thursday friday saturday sunday all".split()

    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input("Which city would you like to analyze? (chicago, new york city, washington): ").lower()
    while city not in CITY_DATA.keys():
        city = input("Please enter one of these cities (chicago, new york city, washington): ").lower()

    # get user input for month (all, january, february, ... , june)
    month = input("What month would you like to analyze? (january-june, or all): ").lower()
    while month not in VAL_MONTHS:
        month = input("Please enter one of these months (january-june, or all): ").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    day = input("What day would you like to analyze? (monday-sunday, or all): ").lower()
    while day not in VAL_DAYS:
        day = input("Please enter one of these days (monday-sunday, or all): ").lower()

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
    
    

    df = pd.read_csv(CITY_DATA.get(city), parse_dates=['Start Time'])
    month_num = month_switcher(month)
    day_num = day_switcher(day)
    if month_num < 7:
        df = df[df['Start Time'].dt.month == month_num]
    if day_num < 7:
        df = df[df['Start Time'].dt.weekday == day_num]

    df = df.dropna(axis=0)

    return df

def preview_data(df):
    """Allows previewing of dataset, 5 rows at a time."""

    preview = input("Would you like to see the first 5 rows of data? (yes or no): ").lower()
    start = 0
    stop = 0
    while preview == "yes": # continues previewing as long as they enter yes a second time
        start = stop # sets start equal to current stop, for first iteration this does not change the value
        stop += 5 # increases the top end for range by 5, both of these could be done at end of loop but this way there's no needless incrementing
        print(df.iloc[range(start, stop)])
        preview = input("Would you like to see 5 more rows of data? (yes or no): ").lower()
    
    print('-'*40)


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    try:
    # display the most common month 
        most_common_month_df = df['Start Time'].dt.month.value_counts().to_frame()
        most_common_month_name = month_switcher(most_common_month_df.index[0])
        month_count = most_common_month_df.loc[most_common_month_df.index[0]]['Start Time']
        print('\nMost common month: {}\nNumber of rides: {}'.format(most_common_month_name, month_count))
        print('-'*5)
    except KeyError as E:
        print('{} column not found'.format(E))
    except:
        E = sys.exc_info()[0]
        print('Unknown exception: {} occured'.format(E))

    try:
    # display the most common day of week
        most_common_day_df = df['Start Time'].dt.weekday.value_counts().to_frame()
        most_common_day_name = day_switcher(most_common_day_df.index[0])
        day_count = most_common_day_df.loc[most_common_day_df.index[0]]['Start Time']
        print('\nMost common day: {}\nNumber of rides: {}'.format(most_common_day_name, day_count))
        print('-'*5)
    except KeyError as E:
        print('{} column not found'.format(E))
    except:
        E = sys.exc_info()[0]
        print('Unknown exception: {} occured'.format(E))

    try:
    # display the most common start hour
        most_common_hour_df = df['Start Time'].dt.hour.value_counts().to_frame()
        most_common_hour_name = most_common_hour_df.index[0]
        hour_count = most_common_hour_df.loc[most_common_hour_df.index[0]]['Start Time']
        print('\nMost common hour: {}\nNumber of rides: {}'.format(most_common_hour_name, hour_count))
        print('-'*5)
    except KeyError as E:
        print('{} column not found'.format(E))
    except:
        E = sys.exc_info()[0]
        print('Unknown exception: {} occured'.format(E))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    try:
    # display most commonly used start station
        start_station_df = df['Start Station'].value_counts().to_frame()
        most_common_station = start_station_df.index[0]
        station_count = start_station_df.loc[start_station_df.index[0]]['Start Station']
        print('\nMost common start station: {}\nNumber of rides: {}'.format(most_common_station, station_count))
        print('-'*5)
    except KeyError as E:
        print('{} column not found'.format(E))
    except:
        E = sys.exc_info()[0]
        print('Unknown exception: {} occured'.format(E))

    try:
    # display most commonly used end station
        end_station_df = df['End Station'].value_counts().to_frame()
        most_common_station = end_station_df.index[0]
        station_count = end_station_df.loc[end_station_df.index[0]]['End Station']
        print('\nMost common end station: {}\nNumber of rides: {}'.format(most_common_station, station_count))
        print('-'*5)
    except KeyError as E:
        print('{} column not found'.format(E))
    except:
        E = sys.exc_info()[0]
        print('Unknown exception: {} occured'.format(E))

    try:
    # display most frequent combination of start station and end station trip
        trip_df = df
        trip_df['Both Stations'] = trip_df['Start Station'] + ' to ' + trip_df['End Station']
        trip_df = trip_df['Both Stations'].value_counts().to_frame()
        most_common_trip = trip_df.index[0]
        trip_count = trip_df.loc[trip_df.index[0]]['Both Stations']
        print('\nMost common Trip: {}\nNumber of rides: {}'.format(most_common_trip, trip_count))
        print('-'*5)
    except KeyError as E:
        print('{} column not found'.format(E))
    except:
        E = sys.exc_info()[0]
        print('Unknown exception: {} occured'.format(E))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    try:
    # display total travel time
        print('\nTotal time for all trips: {}'.format(df['Trip Duration'].sum()))
        print('-'*5)
    except KeyError as E:
        print('{} column not found'.format(E))
    except:
        E = sys.exc_info()[0]
        print('Unknown exception: {} occured'.format(E))

    try:
    # display mean travel time
        print('\nAverage trip duration: {}'.format(df['Trip Duration'].mean()))
        print('-'*5)
    except KeyError as E:
        print('{} column not found'.format(E))
    except:
        E = sys.exc_info()[0]
        print('Unknown exception: {} occured'.format(E))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()
    try:
        # Display counts of user types
        print('\n{}'.format(df['User Type'].value_counts().to_frame()))    
        print('-'*5)
    except KeyError as E:
        print('{} column not found'.format(E))
    except:
        E = sys.exc_info()[0]
        print('Unknown exception: {} occured'.format(E))
    
    try:
        # Display counts of gender
        print('\n{}'.format(df['Gender'].value_counts().to_frame()))
        print('-'*5)
    except KeyError as E:
        print('{} column not found'.format(E))
    except:
        E = sys.exc_info()[0]
        print('Unknown exception: {} occured'.format(E))
    
    try:
        # Display earliest, most recent, and most common year of birth
        print('\nMost recent birth year: {}'.format(df['Birth Year'].max()))
        print('\nEarliest birth year: {}'.format(df['Birth Year'].min()))
        birth_year_df = df['Birth Year'].value_counts().to_frame()
        most_common_year = birth_year_df.index[0]
        birth_year_count = birth_year_df.loc[birth_year_df.index[0]]['Birth Year']
        print('\nMost common birth year: {}\nNumber of people: {}'.format(most_common_year, birth_year_count))
        print('-'*5)
    except KeyError as E:
        print('{} column not found'.format(E))
    except:
        E = sys.exc_info()[0]
        print('Unknown exception: {} occured'.format(E))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        preview_data(df)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
