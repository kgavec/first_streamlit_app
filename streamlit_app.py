import streamlit
import pandas 
import requests
import snowflake.connector
from urllib.error import URLError

##add title
streamlit.title('My Parents New Healthy Diner')

##add header 
streamlit.header('Breakfast Favorites')
##add text
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

##another header
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

##adding data from S3 bucket using pandas
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)

#create a function
def get_fruityvice_data(this_fruit_choice):
     ##Add API conection
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    #streamlit.text(fruityvice_response.json()) #writes data to screen in Json format
    # transform data to pandas df
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

##New section for API response
streamlit.header("Fruityvice Fruit Advice!")

try:
     ##select fruit
     fruit_choice = streamlit.text_input('What fruit would you like information about?')
     if not fruit_choice:
          streamlit.error("Please select a fruit to get information.")
     else:
          back_from_function = get_fruityvice_data(fruit_choice)
          streamlit.dataframe(back_from_function)

except URLError as e:
     streamlit.error()


streamlit.header("The fruit load list contains:")
#snowflake related functions
def get_fruit_load_list():
     with my_cnx.cursor() as my_cur:
          my_cur.execute("SELECT * from fruit_load_list")
          return my_cur.fetchall()

# Add button to load the fruit
if streamlit.button('Get Fruit Load List'):
     ##setup snowflake connection
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])   
     my_data_rows = get_fruit_load_list()
     streamlit.dataframe(my_data_rows)

#command that stop running anithing past here
#streamlit.stop()
    
def insert_row_snowflake(new_fruit):
     with my_cnx.cursor() as my_cur:
          my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
          return 'Thanks for adding '+ new_fruit
     
##text input a fruit to add
add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button('Add a Fruit to the List'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])  
     back_from_function = insert_row_snowflake(add_my_fruit)
     streamlit.text(back_from_function)



