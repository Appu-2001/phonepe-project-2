# importing libraries
import os
import json
import pandas as pd
import streamlit as st
import plotly.express as px
import mysql.connector as sql
from PIL import Image
from git.repo.base import Repo
from streamlit_option_menu import option_menu

# importing project environment
import env


## creating geojson polygons
geojson_data = open(env.project_json_india_states, "r")
geojson_polygons = json.load(geojson_data)

## accessing mySQL database
# creating connection
db_connection = sql.connect(
    host=env.sql_hostname,
    user=env.sql_username,
    password=env.sql_password,
    database=env.sql_database,
)

# creating cursor to execute queries
db_cursor = db_connection.cursor(buffered=True)


## setting up page configuration
# page favicon
icon = Image.open(env.project_favicon)

# page layout
st.set_page_config(
    page_title="Phonepe Pulse Data Visualization",
    page_icon=icon,
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "About": """ **Data has been cloned from Phonepe Pulse Github Repo** """
    },
)

# creating option menu in the side bar
with st.sidebar:
    selected = option_menu(
        "Dashboard",
        ["Top Charts", "Explore Data"],
        icons=["graph-up-arrow", "bar-chart-line"],
        menu_icon="menu-button-wide",
        default_index=0,
        styles={
            "nav-link": {
                "font-size": "17px",
                "text-align": "left",
                "padding": "8px",
                "--hover-color": "rgba(128, 128, 255, 0.5)",
            },
            "nav-link-selected": {"background-color": "rgba(128, 128, 255, 0.75)"},
        },
    )

# MENU 1 - TOP CHARTS
if selected == "Top Charts":
    # sidebar
    Type = st.sidebar.selectbox(" **TYPE** ", ("Transactions", "Users"))
    Year = st.sidebar.selectbox(" **YEAR** ", env.project_dataset_year)
    Quarter = st.sidebar.selectbox(" **QUARTER** ", env.project_dataset_quarter)

    # Top Charts - TRANSACTIONS
    if Type == "Transactions":
        # Plot for top 5 states
        db_cursor.execute(
            f"SELECT `state`, sum(Transaction_count) AS `Total_Transactions_Count`, sum(Transaction_amount) AS `Total` FROM {env.sql_table_transaction_aggregate} WHERE `year` = {Year} AND `quarter` = {Quarter} GROUP BY `state` ORDER BY `Total` DESC LIMIT 5"
        )

        df = pd.DataFrame(
            db_cursor.fetchall(),
            columns=["State", "Transactions_Count", "Total_Amount"],
        )

        fig = px.pie(
            df,
            title="Top 5 state",
            values="Total_Amount",
            names="State",
            color_discrete_sequence=px.colors.sequential.Agsunset,
        )

        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

        # Plot for top 5 district
        db_cursor.execute(
            f"SELECT `district` , sum(Count) AS `Total_Count`, sum(Amount) AS `Total` FROM {env.sql_table_transaction_map} WHERE `year` = {Year} AND `quarter` = {Quarter} GROUP BY `district` ORDER BY Total DESC LIMIT 5"
        )

        df = pd.DataFrame(
            db_cursor.fetchall(),
            columns=["District", "Transactions_Count", "Total_Amount"],
        )

        fig = px.pie(
            df,
            title="Top 5 district",
            values="Total_Amount",
            names="District",
            color_discrete_sequence=px.colors.sequential.Agsunset,
        )

        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

        # Plot for top 5 pincode
        db_cursor.execute(
            f"SELECT `pincode`, sum(Transaction_count) AS `Total_Transactions_Count`, sum(Transaction_amount) AS `Total` FROM {env.sql_table_transaction_top} WHERE `year` = {Year} AND `quarter` = {Quarter} GROUP BY `pincode` ORDER BY `Total` DESC LIMIT 5"
        )

        df = pd.DataFrame(
            db_cursor.fetchall(),
            columns=["Pincode", "Transactions_Count", "Total_Amount"],
        )

        fig = px.pie(
            df,
            title="Top 5 pincode",
            values="Total_Amount",
            names="Pincode",
            color_discrete_sequence=px.colors.sequential.Agsunset,
        )

        fig.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig, use_container_width=True)

    # Top Charts - USERS
    if Type == "Users":
        # plot for brand
        db_cursor.execute(
            f"SELECT `brands`, sum(count) AS `Total_Count`, avg(percentage)*100 AS `Avg_Percentage` FROM {env.sql_table_user_aggregate} WHERE `year` = {Year} AND `quarter` = {Quarter} GROUP BY `brands` ORDER BY `Total_Count` DESC LIMIT 5"
        )

        df = pd.DataFrame(
            db_cursor.fetchall(),
            columns=["Brand", "Total_Users", "Avg_Percentage"],
        )

        fig = px.bar(
            df,
            title="Top 5 brand",
            x="Total_Users",
            y="Brand",
            orientation="h",
            color="Avg_Percentage",
            color_continuous_scale=px.colors.sequential.Agsunset,
        )

        st.plotly_chart(fig, use_container_width=True)

        # plot for state
        db_cursor.execute(
            f"SELECT `state`, sum(Registered_user) AS `Total_Users`, sum(App_opens) AS `Total_Appopens` FROM {env.sql_table_user_map} WHERE `year` = {Year} AND `quarter` = {Quarter} GROUP BY `state` ORDER BY `Total_Users` DESC LIMIT 5"
        )

        df = pd.DataFrame(
            db_cursor.fetchall(), columns=["State", "Total_Users", "Total_Appopens"]
        )

        fig = px.bar(
            df,
            title="Top 5 state",
            x="Total_Users",
            y="State",
            orientation="h",
            color="Total_Users",
            color_continuous_scale=px.colors.sequential.Agsunset,
        )

        st.plotly_chart(fig, use_container_width=True)

        # plot for district
        db_cursor.execute(
            f"SELECT `district`, sum(Registered_User) AS `Total_Users`, sum(app_opens) AS `Total_Appopens` FROM {env.sql_table_user_map} WHERE `year` = {Year} AND `quarter` = {Quarter} GROUP BY `district` ORDER BY `Total_Users` DESC LIMIT 5"
        )

        df = pd.DataFrame(
            db_cursor.fetchall(),
            columns=["District", "Total_Users", "Total_Appopens"],
        )

        df.Total_Users = df.Total_Users.astype(float)
        fig = px.bar(
            df,
            title="Top 5 district",
            x="Total_Users",
            y="District",
            orientation="h",
            color="Total_Users",
            color_continuous_scale=px.colors.sequential.Agsunset,
        )

        st.plotly_chart(fig, use_container_width=True)

# MENU 2 - EXPLORE DATA
if selected == "Explore Data":
    # sidebar
    Type = st.sidebar.selectbox(" **TYPE** ", ("Transactions", "Users"))
    Year = st.sidebar.selectbox(" **YEAR** ", env.project_dataset_year)
    Quarter = st.sidebar.selectbox(" **QUARTER** ", env.project_dataset_quarter)

    # Overall State Data - TRANSACTIONS AMOUNT - INDIA MAP
    if Type == "Transactions":
        db_cursor.execute(
            f"SELECT `state`, sum(count) AS `Total_Transactions`, sum(amount) AS `Total_amount` FROM {env.sql_table_transaction_map} WHERE `year` = {Year} AND `quarter` = {Quarter} GROUP BY `state` ORDER BY `state`"
        )

        df = pd.DataFrame(
            db_cursor.fetchall(),
            columns=["State", "Total_Transactions", "Total_amount"],
        )

        df.State = pd.read_csv(env.project_csv_states)

        fig = px.choropleth(
            df,
            geojson=geojson_polygons,
            featureidkey="properties.ST_NM",
            locations="State",
            color="Total_amount",
            color_continuous_scale="sunset",
        )

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # Overall State Data - TRANSACTIONS COUNT - INDIA MAP
        db_cursor.execute(
            f"SELECT `state`, sum(count) AS `Total_Transactions`, sum(amount) AS `Total_amount` FROM {env.sql_table_transaction_map} WHERE `year` = {Year} AND `quarter` = {Quarter} GROUP BY `state` ORDER BY `state`"
        )

        df = pd.DataFrame(
            db_cursor.fetchall(),
            columns=["State", "Total_Transactions", "Total_amount"],
        )

        df.Total_Transactions = df.Total_Transactions.astype(int)
        df.State = pd.read_csv(env.project_csv_states)

        fig = px.choropleth(
            df,
            geojson=geojson_polygons,
            featureidkey="properties.ST_NM",
            locations="State",
            color="Total_Transactions",
            color_continuous_scale="sunset",
        )

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # BAR CHART - TOP PAYMENT TYPE
        db_cursor.execute(
            f"SELECT `Transaction_type`, sum(Transaction_count) AS `Total_Transactions`, sum(Transaction_amount) AS `Total_amount` FROM {env.sql_table_transaction_aggregate} WHERE `year` = {Year} AND `quarter` = {Quarter} GROUP BY `transaction_type` ORDER BY `Transaction_type`"
        )

        df = pd.DataFrame(
            db_cursor.fetchall(),
            columns=["Transaction_type", "Total_Transactions", "Total_amount"],
        )

        fig = px.bar(
            df,
            title="Transaction Types vs Total Transactions",
            x="Total_Transactions",
            y="Transaction_type",
            orientation="h",
            color="Total_amount",
            color_continuous_scale=px.colors.sequential.Agsunset,
        )

        st.plotly_chart(fig, use_container_width=False)

        # BAR CHART TRANSACTIONS - DISTRICT WISE DATA
        transaction_states_list = os.listdir(env.project_transaction_aggregate_dir)

        selected_state = st.selectbox(
            "",
            (transaction_states_list),
        )

        db_cursor.execute(
            f"SELECT `State`, `District`, `year`, `quarter`, sum(count) AS `Total_Transactions`, sum(amount) AS `Total_amount` FROM {env.sql_table_transaction_map} WHERE `year` = {Year} AND `quarter` = {Quarter} AND State = '{selected_state}' GROUP BY `State`, `District`, `year`, `quarter` ORDER BY `state`, `district`"
        )

        df = pd.DataFrame(
            db_cursor.fetchall(),
            columns=[
                "State",
                "District",
                "Year",
                "Quarter",
                "Total_Transactions",
                "Total_amount",
            ],
        )

        fig = px.bar(
            df,
            title=selected_state,
            x="Total_Transactions",
            y="District",
            orientation="h",
            color="Total_amount",
            color_continuous_scale=px.colors.sequential.Agsunset,
        )

        st.plotly_chart(fig, use_container_width=True)

    # EXPLORE DATA - USERS
    if Type == "Users":
        db_cursor.execute(
            f"SELECT `state`, sum(Registered_user) AS `Total_Users`, sum(App_opens) AS `Total_Appopens` FROM {env.sql_table_user_map} WHERE `year` = {Year} AND `quarter` = {Quarter} GROUP BY `state` ORDER BY `state`"
        )

        df = pd.DataFrame(
            db_cursor.fetchall(), columns=["State", "Total_Users", "Total_Appopens"]
        )

        df.Total_Appopens = df.Total_Appopens.astype(int)
        df.State = pd.read_csv(env.project_csv_states)

        fig = px.choropleth(
            df,
            geojson=geojson_polygons,
            featureidkey="properties.ST_NM",
            locations="State",
            color="Total_Appopens",
            color_continuous_scale="sunset",
        )

        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)

        # BAR CHART TOTAL UERS - DISTRICT WISE DATA
        user_states_list = os.listdir(env.project_user_aggregate_dir)

        selected_state = st.selectbox(
            "",
            (user_states_list),
        )

        db_cursor.execute(
            f"SELECT `State`, `year`, `quarter`, `District`, sum(Registered_user) AS `Total_Users`, sum(App_opens) AS `Total_Appopens` FROM {env.sql_table_user_map} WHERE `year` = {Year} AND `quarter` = {Quarter} AND `state` = '{selected_state}' GROUP BY `State`, `District`, `year`, `quarter` ORDER BY `state`, `district`"
        )

        df = pd.DataFrame(
            db_cursor.fetchall(),
            columns=[
                "State",
                "year",
                "quarter",
                "District",
                "Total_Users",
                "Total_Appopens",
            ],
        )

        df.Total_Users = df.Total_Users.astype(int)

        fig = px.bar(
            df,
            title=selected_state,
            x="Total_Users",
            y="District",
            orientation="h",
            color="Total_Users",
            color_continuous_scale=px.colors.sequential.Agsunset,
        )

        st.plotly_chart(fig, use_container_width=True)
