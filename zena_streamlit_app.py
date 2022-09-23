import snowflake.connector
import streamlit
import pandas

streamlit.title('Zena\'s Amazing Athleisure Catalog')

#connect to snowflake
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()

# run a snowflake query and put it all in a var called my_catalog
my_cur.execute("select color_or_style from catalog_for_website")
my_catalog = my_cur.fetchall()
# streamlit.write(my_catalog)
# put the data into a dataframe
df = pandas.DataFrame(my_catalog)

# put the first column into a list
color_list = df[0].values.tolist()

# pick list for picking color
option = streamlit.selectbox('Pick a sweatsuit color or style:', list(color_list))

# build image caption
product_caption = 'Our warm, comfortable, ' + option + 'sweatsuit!'

# use the option selected to go back to db to get all info
my_cur.execute("select direct_url, price, size_list, upsell_product_desc from catalog_for_website where color_or_style ='" + option + "';")
df2 = pandas.DataFrame(my_cur.fetchall())
streamlit.image(
    df2[0],
    width = 400,
    caption=product_caption
)
streamlit.write('Price: ', df2[1])
streamlit.write('Sizes Available: ', df2[2])
streamlit.write(df2[3])