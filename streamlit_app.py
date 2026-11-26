# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests



# Write directly to the app
st.title(f"Customize Your Smoothie :cup_with_straw: {st.__version__}")
st.write(
  """Choose the fruits you want in your custom Smoothie!
  """
)

if st.session_state.get("clear_form"):
    st.session_state["product_name"]= ""
    st.session_state["list_of_ingredients"]= []
    st.session_state["clear_form"]= False

# For using functions - select specific column from the table
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.PUBLIC.FRUIT_OPTIONS").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)

# name box
name_on_order = st.text_input('Name of Smoothie:', key="product_name").upper()
st.write(f"The name of Smoothie will be:\n{name_on_order}")   

ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:', 
    my_dataframe,
    key="list_of_ingredients"
)


if ingredients_list:
    # st.write(
    #     f"{ingredients_list}"
    # )
    # st.text(ingredients_list)

    if len(ingredients_list) <=5:

        # looping threw ingredients list and adding in a string
        ingredients_string = ''
        for fruit_chosen in ingredients_list:
            ingredients_string += fruit_chosen + ', '
            
            smoothiefroot_response = requests.get(url= "https://my.smoothiefroot.com/api/fruit/watermelon")
            sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)
    
    
        ingredients_finish = ingredients_string[:-2]
        
    
        my_insert_stmt = """insert into smoothies.public.orders(ingredients, name_on_order)
                    values ('"""+ ingredients_finish +"""', '"""+ name_on_order +"""')"""
    
        #check how the insert looks like before adding it
        # st.write(my_insert_stmt)
        
        if st.button("Submit order"):
            session.sql(my_insert_stmt).collect()
            st.session_state["order_submitted"] = True
            st.session_state["clear_form"] = True
            st.rerun()
    else:
        st.info("You have reach the limit of chosen items\nOnly five items, remove so you only have five")
        
if st.session_state.get("order_submitted"):

        st.success('Your Smoothie is order!', icon='✅')
        st.session_state["order_submitted"]=False



