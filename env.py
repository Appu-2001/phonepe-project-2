# import os to manage filesystem
import os

# GUI support variables
project_dataset_year = {2018, 2019, 2020, 2021, 2022, 2023}
project_dataset_quarter = {1, 2, 3, 4}

# project support variables
project_dir = os.getcwd()
project_source_dir = os.path.join(project_dir, "source")
pulse_repo_dir = os.path.join(project_source_dir, "pulse-data-raw")

# project setup support variables
project_transaction_aggregate_dir = os.path.join(
    pulse_repo_dir, "data", "aggregated", "transaction", "country", "india", "state"
)

project_transaction_map_dir = os.path.join(
    pulse_repo_dir, "data", "map", "transaction", "hover", "country", "india", "state"
)

project_transaction_top_dir = os.path.join(
    pulse_repo_dir, "data", "top", "transaction", "country", "india", "state"
)

project_user_aggregate_dir = os.path.join(
    pulse_repo_dir, "data", "aggregated", "user", "country", "india", "state"
)

project_user_map_dir = os.path.join(
    pulse_repo_dir, "data", "map", "user", "hover", "country", "india", "state"
)

project_user_top_dir = os.path.join(
    pulse_repo_dir, "data", "top", "user", "country", "india", "state"
)

# json support variable
project_json_dir = os.path.join(project_source_dir, "json")
project_json_india_states = os.path.join(project_json_dir, "india_states.geojson")

# csv support variable
project_csv_dir = os.path.join(project_source_dir, "csv")
project_csv_states = os.path.join(project_csv_dir, "state-names.csv")
project_csv_transaction_aggregate = os.path.join(
    project_csv_dir, "transaction_aggregate.csv"
)
project_csv_transaction_map = os.path.join(project_csv_dir, "transaction_map.csv")
project_csv_transaction_top = os.path.join(project_csv_dir, "transaction_top.csv")
project_csv_user_aggregate = os.path.join(project_csv_dir, "user_aggregate.csv")
project_csv_user_map = os.path.join(project_csv_dir, "user_map.csv")
project_csv_user_top = os.path.join(project_csv_dir, "user_top.csv")

# images support variable
project_images_dir = os.path.join(project_source_dir, "images")
project_favicon = os.path.join(project_images_dir, "favicon.png")
project_image_footer = os.path.join(project_images_dir, "footer.jpg")
project_image_pulse_logo = os.path.join(project_images_dir, "pulse-logo.png")

# database support variables
sql_hostname = "localhost"
sql_username = "root"
sql_password = ""
sql_database = "pybase"
sql_table_transaction_aggregate = "transaction_aggregate"
sql_table_transaction_map = "transaction_map"
sql_table_transaction_top = "transaction_top"
sql_table_user_aggregate = "user_aggregate"
sql_table_user_map = "user_map"
sql_table_user_top = "user_top"
