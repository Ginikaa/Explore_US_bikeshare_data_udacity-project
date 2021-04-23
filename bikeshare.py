import time
import pandas as pd
import numpy as np
import datetime


#dictionary comprising of the csv files of the 3 cities to be explored
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
    print('\nHello! Let\'s explore some US bikeshare data!')

    #get the user input for city (chicago, new york city, washington)
    cities = {'1':'chicago', '2':'new york city', '3': 'washington'}
    while True:
        try:
            city_num = input('\nWhich City from the options below do you wish to explore? Enter 1 for Chicago, 2 for New York...\n1.Chicago\n2.New York City\n3.Washington\n')
            if city_num not in cities:
                raise ValueError('Oops! Invalid City')
            break
        except ValueError as ve:
            print(ve)

    print('Good choice!You have selected {}'.format(cities[city_num]))
    city = cities[city_num]



    #get user input for the month to be explored (all, january, february, ... , june)
    Months = { '1': 'January', '2': 'February', '3': 'March', '4': 'April', '5': 'May', '6': 'June', '7': 'ALL'}
    while True:
        try:
            month_num = input('\nPlease select a month to explore by inputting a number between 1 and 6 where the numbers represent January to June respectively. Input 7 if you do not want to explore a particular month: ')
            if month_num not in Months:
                raise ValueError('Oops! Invalid month')
            break
        except ValueError as ve:
            print(ve)
    if month_num == '7':
        print('You do not wish to explore a particular month')
    else:
        print('You have selected:',Months[month_num])
    month = Months[month_num]


    #get user input for the day of the week to be explored (all, monday, tuesday, ... sunday)
    Days = { '1': 'Sunday', '2': 'Monday', '3': 'Tuesday', '4': 'Wednesday', '5': 'Thursday', '6': 'Friday', '7': 'Saturday', '8':'ALL'}
    while True:
        try:
            day_num =input('\nPlease select the day of the week you wish explore by inputting a number between 1 and 7 where the numbers represent Sunday to Saturday respectively. Input 8 if you do not want to explore a particular day: ')
            if day_num not in Days:
                raise ValueError('Oops! Invalid day')
            break
        except ValueError as ve:
            print(ve)
    if day_num == '8':
        print('You do not wish to explore a particular day of the week')
    else:
        print('You have selected:',Days[day_num])
    day = Days[day_num]



    #display the selections made
    if month_num!='7' and day_num != '8':
        print('\nThanks for your selections!You have chosen to explore {} in the month of {} for {}'.format(day, month, city.title()))
    elif month_num == '7' and day_num != '8':
        print('\nThanks for your selections!You have chosen to explore {}s for {}'.format(day, city.title()))
    elif month_num != '7' and day_num == '8':
        print('\nThanks for your selections!You have chosen to explore the month of {} for {}'.format(month, city.title()))
    elif month_num == '7' and day_num == '8':
        print('\nThanks for your selections!You have chosen to explore {}'.format(city.title()))


    #asks the user if they would like to change their selections
    
    while True:
        reselect = input('\nWould you like to make a different selection? Enter yes or no.\n').lower()
        if reselect != 'yes' and reselect != 'no':
            print('Oops! invalid input')
            continue
        elif reselect == 'yes':
            get_filters()
        else:
            break
        break







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
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract month, day of week and hour from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    if month != 'ALL':
        # use the index of the months list to get the corresponding int
        months = ['January', 'February', 'March', 'April', 'May', 'June']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'ALL':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]


    return df

def display_raw_data(df):
    """
    Asks the user if they want to see 5 random rows of the raw data.
    Displays 5 random rows if user enters yes until the user enters no

    """

    #get user input to determine if the user wants to display 5 random rows of data
    while True:
        try:
            display = input('\nPlease enter yes if you wish to see 5 random rows of the data you want to explore and no if you dont: ').lower()
            if display == 'yes':
                print(df.sample(n = 5))

            elif display == 'no':
                break
            else:
                raise ValueError('Oops! invalid input')


        except ValueError as ve:
            print(ve)





def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    #display the most common month if applicable
    if df.month.nunique() > 1:
        most_popular_month = str(df['month'].mode()[0])
        most_popular_month_name = datetime.datetime.strptime(most_popular_month, '%m').strftime("%B")
        print('Most Common Month: ', most_popular_month_name)


    #display the most common day of week if applicable
    if df.day_of_week.nunique() > 1:
        most_popular_day = df['day_of_week'].mode()[0]
        print('Most Common Day of Week: ', most_popular_day)

    #display the most common start hour
    popular_hour = df['hour'].mode()[0]
    print('Most Popular Start Hour: ', popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    #Dsiplay most commonly used start station
    most_common_startstation = df['Start Station'].mode()[0]
    print('Most Commonly Used Start Station: ', most_common_startstation)



    #display most commonly used end station
    most_common_endstation = df['End Station'].mode()[0]
    print('Most Commonly Used End Station: ', most_common_endstation)


    #display most frequent combination of start station and end station trip
    most_frequent_combination = (df['Start Station'] +'  TO  ' + df['End Station']).mode()[0]
    print('Most Common trips from start to end station: ', most_frequent_combination)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    #display total travel time
    total_travel_time = df['Trip Duration'].sum()
    print('Total travel time: {}s '.format(total_travel_time))


    #display mean travel time
    mean_travel_time = df['Trip Duration'].mean()
    print('Average travel time: {}s '.format(mean_travel_time))


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    #display counts of user types
    user_types = df['User Type'].value_counts()
    print('Count of each user type:\n{}'.format(user_types))


    #display counts of gender
    if city != 'washington':
        gender_count = df['Gender'].value_counts()
        print('\n\nCount of each gender:\n{}'.format(gender_count))


    #display earliest, most recent, and most common year of birth
    if city != 'washington':
        #display earliest year of birth
        earliest_birth = df['Birth Year'].min()
        print('\n\nEarliest Birth Year:',int(earliest_birth))

        #display most recent year of birth
        latest_birth = df['Birth Year'].max()
        print('Most Recent Birth Year:',int(latest_birth))

        #display most common year of birth
        most_common_birth = df['Birth Year'].mode()[0]
        print('Most Common Birth Year:',int(most_common_birth))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        display_raw_data(df)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
