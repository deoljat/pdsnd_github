import time
import calendar
import pandas as pd

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (int) month - the month to filter by, or 0 if no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = ""
    while not(city in CITY_DATA.keys()):
        city = input('Would you like to see data for Chicago, New York City or Washington? \n').lower()
        if not(city in CITY_DATA.keys()):
            print('invalid input please enter Chicago, New York City or Washington')

    # TO DO: get user input for month (all, january, february, ... , june)
    months = ['all', 'jan', 'feb', 'mar', 'apr', 'may', 'jun']
    month = ""
    while month == "":
        month_input = input('Which month? All, Jan, Feb, Mar, Apr, May or Jun \n').lower()[:3]
        if month_input in months:
            month = months.index(month_input)
        else:
            print('invalid input')

    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    filter_by_day = ""
    while filter_by_day!='n' and filter_by_day!='y':
        try:
            filter_by_day = input('Would you like to filter by day? Y, N \n').lower()[0]
            if filter_by_day!='n' and filter_by_day!='y':
                print('invalid input')
        except:
            print('invalid input')
    if filter_by_day == 'y':
        days = ['m', 'tu', 'w', 'th', 'f', 'sa', 'su']
        week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        day = ""
        while day == "":
            day_input = input('Which day? Please type a day M, Tu, W, Th, F, Sa, Su\n').lower()
            if day_input in days:
                day = week[days.index(day_input)]
            else:
                print('invalid input')
    else:
        day = "all"

    print('-'*40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (int) month - the month to filter by, or 0 if no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(CITY_DATA[city])
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['month'] = df['Start Time'].dt.month
    if (int(pd.__version__.split(".")[0]) > 0) or (int(pd.__version__.split(".")[1]) > 23):
        df['day_of_week'] = df['Start Time'].dt.day_name(locale = 'English')
    else:
        df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour
    if month != 0:
        df = df[df['month'] == month]
    if day != 'all':
        df = df[df['day_of_week'] == day]

    return df


def time_stats(df, month, day):
    """
    Displays statistics on the most frequent times of travel.

    Args:
        df - Pandas DataFrame filtered by month and day
        (int) month - the month to filter by, or 0 if no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filterr
    Returns:
        The most popular month to travel, if no month is selected.
        The most popular day to travel, if no day is selected
        The most popular hour to travel.

    """

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()
    # TO DO: display the most common month
    if month == 0:
        popular_month = calendar.month_name[df['month'].mode()[0]]
        print('The most popular month to travel is:',  popular_month)
    else:
        print('The most popular month to travel is: N/A filtered on Month')

    # TO DO: display the most common day of week
    if day == 'all':
        popular_day = df['day_of_week'].mode()[0]
        print('The most popular day to travel is:',  popular_day)
    else:
        print('The most popular day to travel is: N/A filtered on Day')

    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('The most popular day to travel is:',  popular_hour)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    start_station = df['Start Station'].mode()[0]
    print('The most commonly used start station is:',  start_station)

    # TO DO: display most commonly used end station
    end_station = df['End Station'].mode()[0]
    print('The most commonly used end station is:',  end_station)


    # TO DO: display most frequent combination of start station and end station trip
    trip = df.groupby(['Start Station','End Station']).size().idxmax()
    print('The most commonly trip is from:',  trip[0],
          '\n                            to:', trip[1])

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_time = df['Trip Duration'].sum()
    print('The total travel time is:', total_time)
    # TO DO: display mean travel time
    mean_time = df['Trip Duration'].mean()
    print('The mean travel time is:', "{:.2f}".format(mean_time))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    usergroup = df.groupby(['User Type']).size()
    print('What is the breakdown of user? \n', usergroup)

    # TO DO: Display counts of gender
    print('What is the breakdown of gender?')
    if city != 'washington':
        gendergroup = df.groupby(['Gender']).size()
        print(gendergroup)
    else:
        print('No gender date to share.')

    # TO DO: Display earliest, most recent, and most common year of birth
    print('What is the earliest, most recent and most common year of birth respectively?')
    if city != 'washington':
        earliest_birth_year = int(df['Birth Year'].min())
        recent_birth_year = int(df['Birth Year'].max())
        most_common_birth_year = int(df['Birth Year'].mode())
        print('The earliest year of birth is:', earliest_birth_year, '\n The most recent year of birth is:', recent_birth_year,
              '\n The most common year of birth is:', most_common_birth_year)
    else:
        print('No birth year data to share')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def individual_trip_data(df):
    """Displays individual trip data 5 rows at a time."""

    show_data = ""
    while show_data!='n' and show_data!='y':
        try:
            show_data = input('Do you to view the first 10 rows of data? Y, N \n').lower()[0]
            if show_data!='n' and show_data!='y':
                print('invalid input')
        except:
            print('invalid input')
    if show_data =='y':
        row_num = 10
        while show_data =='y':
            show_data = ""
            print(df.iloc[(row_num-10):row_num])
            row_num += 10
            while show_data!='n' and show_data!='y':
                try:
                    show_data = input('Do you to view the next 10 rows of data?? Y, N \n').lower()[0]
                    if show_data!='n' and show_data!='y':
                        print('invalid input')
                except:
                    print('invalid input')

    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        individual_trip_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n').lower()[0]
        if restart.lower() != 'y':
            break


if __name__ == "__main__":
	main()
