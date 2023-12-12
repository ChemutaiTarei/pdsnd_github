import time
import pandas as pd
import numpy as np

#Index the global CITY_DATA dictionary object to get the corresponding filename for the given city name
CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters(city, month, day):
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # TO DO: get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
    while city not in ['chicago', 'new york city', 'washington']:
        print('Invalid city. Please try again.')
        city = input('Would you like to see data for Chicago, New York City, or Washington?\n').lower()
    
    
    # TO DO: get user input for month (all, january, february, ... , june)
    month = input('Which month? January, February, March, April, May, June, or all?\n').lower()
    while month not in ['january', 'february', 'march', 'april', 'may', 'june', 'all']:
        print('Invalid month. Please try again.')
        month = input('Which month? January, February, March, April, May, June, or all?\n').lower()


    # TO DO: get user input for day of week (all, monday, tuesday, ... sunday)
    day = input('Which day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all?\n').lower()
    while day not in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday', 'all']:
        print('Invalid day of the week. Please try again.')
        day = input('Which day of the week? Monday, Tuesday, Wednesday, Thursday, Friday, Saturday, Sunday, or all?\n').lower()
    
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

    ## convert the Start Time and End Time columns to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])
        
    ## extract hour, day, month from the Start Time column to create an hour, day, month columns
    df['hour'] = df['Start Time'].dt.hour
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['month'] = df['Start Time'].dt.month

       
    # TO DO: display the most common month
    popular_month = df['month'].mode()[0]
    print('Most Popular Start Month:', popular_month)

    # TO DO: display the most common day of week
    popular_day = df['day_of_week'].value_counts().idxmax()
    print('Most Popular Start Day:', popular_day)
    
    # TO DO: display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour:', popular_hour)
    
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    
    # TO DO: display most commonly used start station
    # Group the data by start station and count the occurrences
    station_counts = df.groupby('Start Station')['Start Station'].count()
    # Find the most common start station
    popular_start_station = station_counts.idxmax()
    print("popular_start_station is: ", popular_start_station)
    
    # TO DO: display most commonly used end station
    # Group the data by end station and count the occurrences
    end_station_counts = df.groupby('End Station')['End Station'].count()
    # Find the most common end station
    popular_end_station = end_station_counts.idxmax()
    print("popular_end_station is: ", popular_end_station)

    # TO DO: display most frequent combination of start station and end station trip

    # Group the data by start station and end station and count the occurrences
    station_combinations = df.groupby(['Start Station', 'End Station'])['Start Station'].count()
    # Find the most frequent combination of start and end stations
    popular_trip =  station_combinations.idxmax()
    print("popular_trip is: ", popular_trip)
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print("total_travel_time: ", total_travel_time)
    
    # TO DO: display mean travel time
    average_travel_time = df['Trip Duration'].mean()
    print("average_travel_time: ", average_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    
    # TO DO: Display counts of user types
    user_types = df['User Type'].value_counts()
    print("user_types_counts: ", user_types)
    

    # TO DO: Display counts of gender
    try:
        gender_counts = df['Gender'].value_counts()
        print("Gender Counts:\n", gender_counts)
    except KeyError:
        print("No gender data available for the city of Washington.")
    

    # TO DO: Display earliest, most recent, and most common year of birth
    try:
        earlier_birth_year = df['Birth Year'].min()
        print("earlier_birth_year: ", earlier_birth_year)
    except KeyError:
        print("No birth year data available for the city of Washington.")
    
    try:
        most_recent_birth_year = df['Birth Year'].max()
        print("most_recent_birth_year: ", most_recent_birth_year)
    except KeyError:
        print("No birth year data available for the city of Washington.")
        
    try:
        most_common_birth_year = df['Birth Year'].mode()[0]
        print("most_common_birth_year: ", most_common_birth_year)
    except KeyError:
        print("No birth year data available for the city of Washington.")

    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_raw_data(df):
    """"  displays 5 lines of raw data from a DataFrame """
    
    row_index = 0
    while True:
        show_raw_data = input('\nWould you like to see 5 lines of raw data? Enter yes or no.\n')
        if show_raw_data.lower() == 'yes':
            for i in range(row_index, row_index + 5):
                if i < len(df):
                    print(df.iloc[i])
            row_index += 5
        else:
            break
  
    
    

def main():
    city = None
    month = None
    day = None
    
    while True:
        city, month, day = get_filters(city, month, day)
        df = load_data(city, month, day)
        
        if city.lower() in CITY_DATA:
            df = load_data(city, month, day)
        

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_raw_data(df)  

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break

                

if __name__ == "__main__":
	main()

    
 