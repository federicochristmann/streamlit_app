# Import resources
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

## Edit streamlit text

#import streamlit

streamlit.title('My Mom\'s New Healthy Corner')

streamlit.header('Breakfast Favourites')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


## Import table using pandas

#import pandas

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Set 'Fruit' as index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list so they can pick the fruit they want
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on page
streamlit.dataframe(fruits_to_show)


## Display Fruityvice API response

#import requests

# Create the repeatable code block (function)
def get_fruityvice_data(this_fruit_choice):
# API call
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)    
# Take de .json version of the response and normalize it
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# Display API response
streamlit.header('Fruityvice Fruit Advice!')
try:
# Set a fruit imput variable
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a fruit to get information.")
  else: 
    back_from_function = get_fruityvice_data(fruit_choice)
# Display the table on page
    streamlit.dataframe(back_from_function)
  
except URLError as e:
  streamlit.error()

## Add Snowflake

#import snowflake.connector

streamlit.header("View Our Fruit List-Add Your Favourites!")

# Add a function to query the table
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
# Query our Snowflake fruit data from Rivery
        my_cur.execute("SELECT * FROM FRUIT_LOAD_LIST")
        return my_cur.fetchall() #or ".fetchone" for the first element
    
# Add a button to load the fruit list
if streamlit.button('Get fruit list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx.close()
# Display the table on page
    streamlit.dataframe(my_data_rows)

# Add a function that allows the user to add a fruit to the list
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
# Insert new fruits in the table
        my_cur.execute("INSERT INTO FRUIT_LOAD_LIST VALUES ('" + new_fruit + "')")
        return 'Thanks for adding ' + new_fruit

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
# Add a button to include the fruit in the list
if streamlit.button('Add a fruit to the list'):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        back_from_function = insert_row_snowflake(add_my_fruit)
        my_cnx.close()
# Display the table on page
        streamlit.text(back_from_function)

#streamlit.stop()
