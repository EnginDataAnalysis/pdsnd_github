import time
import pandas as pd
import numpy as np


CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    city = ""
    month = ""
    day = ""
    valid_city = {"chicago", "washington", "new york city"}
    valid_month = {"all", "january", "february", "march", "april", "may", "june"}
    valid_day = {"all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"}

    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    while (city not in valid_city):
        city = input("What city would you like to explore? (Chicago, New York City or Washington?)" ).lower()

    # get user input for month (all, january, february, ... , june)
    while (month not in valid_month):
        month = input("What month would you like to explore? (all, january, february, ... , june)").lower()

    # get user input for day of week (all, monday, tuesday, ... sunday)
    while (day not in valid_day):
        day = input("What day would you like to explore? (all, monday, tuesday, ... sunday)").lower()

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
    df['day_of_week'] = df['Start Time'].dt.weekday_name


# filter by month if applicable
    if month != 'all':
    # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month)+1

    # filter by month to create the new dataframe
        df = df[df['month'] == month]


# filter by day of week if applicable
    if day != 'all':
    # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

# fill NaN values

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel.
    Prints most common month for travel, most common day for travel and most common day of week for travel
    """
    month_list = {1:"January", 2:"February", 3:"March", 4:"April", 5:"May", 6:"June"}

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month

    print('The most common month for travel is: ', month_list[df['month'].mode()[0]])

    # display the most common day of week
    print('The most common day of week for travel is: ', df['day_of_week'].mode()[0])

    # display the most common start hour
    df['hour'] = df['Start Time'].dt.hour
    print('The most common day of start hour for travel is: ', df['hour'].mode()[0])


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # display most commonly used start station
    print("The most popular starting station is: {}".format(df['Start Station'].value_counts().index[0]))

    # display most commonly used end station
    print("The most popular ending station is: {}".format(df['End Station'].mode()[0]))

    # display most frequent combination of start station and end station trip
    df_grouped2 = df.groupby(['Start Station','End Station'], as_index=False).count()
    df_group_sorted = df_grouped2.sort_values('Start Time', ascending=False)
    top_start = df_group_sorted.iloc[0,0]
    top_end = df_group_sorted.iloc[0,1]
    print ('The most frequent combination of start station and end station trip is: ',top_start, '&', top_end)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration.
    Prints total travel time for the period specified, prints average travel time for this period."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('The total travel time for this period is: {} minutes'.format(df['Trip Duration'].sum()/60))
    print('The total travel time for this period is: {} hours'.format(df['Trip Duration'].sum()/360))
    # display mean travel time
    print('The average travel time for this period is: {} minutes'.format(df['Trip Duration'].mean()/60))
    print('The average travel time for this period is: {} hours'.format(df['Trip Duration'].mean()/360))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df["User Type"].value_counts()
    print('The types of users for this period is as follows: \n', user_types)

    # Display counts of gender
    if 'Gender' in df.columns:
        user_gender = df["Gender"].value_counts()
        print('\nThe gender breakdown for this period is as follows: \n', user_gender)
    else:
        print('No gender data Exists for this city.')


    # Display earliest, most recent, and most common year of birth
    if 'Birth Year' in df.columns:
        print("\nThe earliest year of birth is: {}".format(df['Birth Year'].min()))
        print("The most recent year of birth is: {}".format(df['Birth Year'].max()))
        print("The most common year of birth is: {}".format(df['Birth Year'].mode()[0]))
    else:
        print('No birth year data Exists for this city.')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """Displays raw data, 5 lines at a time."""

    valid_answer = {"yes", "no"}
    answer = ""
    start = 1

    while (answer not in valid_answer):
        answer = input("Would you like to see (more) raw trip data? (yes/no)" ).lower()
        if answer == 'yes':
            for i in range(start,start+5):
                print(df.loc[i])
            start = start + 5
            answer =""
        else:
            print('ok')


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        input("Press Enter to continue...")
        station_stats(df)
        input("Press Enter to continue...")
        trip_duration_stats(df)
        input("Press Enter to continue...")
        user_stats(df)
        input("Press Enter to continue...")
        raw_data(df)
        input("Press Enter to continue...")

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
