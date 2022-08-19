## Edit streamlit text

import streamlit

streamlit.title('My Mom\'s New Healthy Corner')

streamlit.header('Breakfast Favourites')

streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


## Import table using pandas

import pandas

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")

# Set 'Fruit' as index
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list so they can pick the fruit they want
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index))
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on page
streamlit.dataframe(fruits_to_show)


## Display Fruityvice API response

streamlit.header('Fruityvice Fruit Advice!')

fruit_choice = streamlit.text_imput('What fruit would you like information about?', 'Kiwi')
streamlit.write('The user entered', fruit_choice)

import requests

# API call
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + "kiwi")

# Take de .json version of the response and normalize it
fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())

# Display the table on page
streamlit.dataframe(fruityvice_normalized)

