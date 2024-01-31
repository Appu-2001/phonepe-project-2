![img](./source/images/pulse-logo.png)

# Data Visualization and Exploration : A User-Friendly Tool Using Streamlit and Plotly

## What is PhonePe Pulse?

The [PhonePe Pulse website](https://www.phonepe.com/pulse/) showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With over 45% market share, PhonePe's data is representative of the country's digital payment habits.
The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the [PhonePe Pulse website](https://www.phonepe.com/pulse/) and [GitHub](https://github.com/PhonePe/pulse).

## Libraries / Modules needed for the project!

1.  Streamlit - creates GUI
2.  Plotly - plots and visualizes data
3.  Pandas - creates DataFrame with the scraped data
4.  GitPython - manages Git repositories
5.  mysql-connector-python - accessing MySQL database

## Workflow

### Step 1:

**Importing the Libraries:**

Importing the libraries. As I have already mentioned above the list of libraries/modules needed for the project. First we have to import all those libraries. If the libraries are not installed already use the below piece of code to install.

```python
  pip install ["library name"]
```

If the libraries are already installed then we have to import those into our script by mentioning the below codes.

```python
  import os
  import json
  import pandas as pd
  import streamlit as st
  import plotly.express as px
  import mysql.connector as sql
  from PIL import Image
  from git.repo.base import Repo
  from streamlit_option_menu import option_menu
```

### Step 2:

**Data extraction:**

Clone the Github using scripting to fetch the data from the Phonepe pulse Github repository and store it in a suitable format such as JSON. Use the below syntax to clone the phonepe github repository into your local drive.

```python
  from git.repo.base import Repo
  Repo.clone_from("GitHub repo URL","path to local directory for repo")
```

### Step 3:

**Data transformation:**

In this step the JSON files that are available in the folders are converted into the readable and understandable DataFrame format by using the for loop and iterating file by file and then finally the DataFrame is created. In order to perform this step I've used **os**, **json** and **pandas** packages. And finally converted the dataframe into CSV file and storing in the local drive.

```python
json_path = "path to JSON files"
files_list = os.listdir(json_path)

# column names that you want
columns = {'State': [], 'Year': [], 'Quarter': [], 'Transaction_type': [], 'Transaction_count': [],'Transaction_amount': []}
```

Looping through each and every folder and opening the json files appending only the required key and values and creating the dataframe.

```python
  for state in files_list:
      current_state = os.path.join(json_path, state)
      aggregate_year_list = os.listdir(current_state)

      for year in aggregate_year_list:
          current_year = os.path.join(current_state, year)
          aggregate_file_list = os.listdir(current_year)

          for file in aggregate_file_list:
              current_file = os.path.join(current_year, file)
              data = open(current_file, 'r')
              A = json.load(data)

              for i in A['data']['transactionData']:
                  name = i['name']
                  count = i['paymentInstruments'][0]['count']
                  amount = i['paymentInstruments'][0]['amount']
                  columns['Transaction_type'].append(name)
                  columns['Transaction_count'].append(count)
                  columns['Transaction_amount'].append(amount)
                  columns['State'].append(state)
                  columns['Year'].append(year)
                  columns['Quarter'].append(int(file.strip('.json')))

  df = pd.DataFrame(columns)
```

##### Converting the dataframe into csv file

```python
  df.to_csv('filename.csv',index=False)
```

### Step 4:

**Database insertion:**

To insert the dataframe into SQL first I've created a new database and tables using **"mysql-connector-python"** library in Python to connect to a MySQL database and insert the transformed data using SQL commands.

**Creating the connection between python and mysql**

```python
  db_connection = sql.connect(host="localhost",
              user="username",
              password="password",
              database= "phonepe_pulse"
            )
  db_cursor = db_connection.cursor(buffered=True)
```

**Creating tables**

```python
  db_cursor.execute("CREATE TABLE 'Table name' (col1 VARCHAR(100), col2 INT, col3 INT, col4 VARCHAR(100), col5 INT, col6 DOUBLE)")

  for i,row in df.iterrows():

      # %s means string values
      sql = "INSERT INTO <table> VALUES (%s,%s,%s,%s,%s,%s)"
      db_cursor.execute(sql, tuple(row))

      # the connection is not auto committed by default, so we must commit to save our changes
      db_connection.commit()
```

### Step 5:

**Dashboard creation:**

To create colourful and insightful dashboard I've used Plotly libraries in Python to create an interactive and visually appealing dashboard. Plotly's built-in Pie, Bar, Geo map functions are used to display the data on a charts and map and Streamlit is used to create a user-friendly interface with multiple dropdown options for users to select different facts and figures to display.

### Step 6:

**Data retrieval:**

Finally if needed Using the "mysql-connector-python" library to connect to the MySQL database and fetch the data into a Pandas dataframe.
