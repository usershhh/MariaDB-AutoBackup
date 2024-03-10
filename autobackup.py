import os
import datetime
import mysql.connector
from mysql.connector import Error
import time
import shutil

#Configuration
db_config = {
    'host': '127.0.0.1', #database adress
    'user': '', #database username
    'password': '', #database password
    'database': '' #database name
}
backup_directory = 'path to your backup storage folder'
####

#don't change the "cleared_this_month" variable it's not a configuration
cleared_this_month = False

def create_backup(db_config, backup_directory):
    try:
        connection = mysql.connector.connect(**db_config)
        current_datetime = datetime.datetime.now()
        
        backup_filename = current_datetime.strftime('%Y-%m-%d_%H-%M-%S') + '.sql'
        backup_path = os.path.join(backup_directory, backup_filename)

        mysqldump_path = shutil.which("mysqldump")
        if mysqldump_path is None:
            print("mysqldump not found. Make sure it is installed and added to the PATH.")
            return

        backup_command = f'"{mysqldump_path}" -u {db_config["user"]} ' \
                 f'--host={db_config["host"]} {db_config["database"]} > "{backup_path}"'

        os.system(backup_command)
        
        print('Successfully created backup :', backup_path)
    except mysql.connector.Error as e:
        print('Backup error:', e)
        
    finally:
        if connection.is_connected():
            connection.close()

def clear_folder(folder_path):
    for item in os.listdir(folder_path):
        item_path = os.path.join(folder_path, item)
        if os.path.isfile(item_path):
            os.remove(item_path)
        elif os.path.isdir(item_path):
            shutil.rmtree(item_path)

if __name__ == "__main__":
    while True:
        try:
            current_time = datetime.datetime.now().time()
            if current_time.hour == 6 and current_time.minute == 0:
                create_backup()
            current_date = datetime.datetime.now().date()

            if current_date.day == 1 and not cleared_this_month:
                clear_folder(backup_directory)
                cleared_this_month = True
                print("Contents of folder deleted on 1st day of month.")

            if current_date.day == 2:
                cleared_this_month = False

            time.sleep(60)
        except Exception as e:
            print(e)