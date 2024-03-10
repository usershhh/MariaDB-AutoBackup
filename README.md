# MariaDB-AutoBackup
This script makes a backup of a mariadb database every day at 6 a.m. (works only on windows)

1) Install the mysql-connector lib with the following command: ```pip install mysql-connector-python```
2) Make sure you've configured the script before launching it by filling in the "db_config" variable and the path to your backup storage folder "backup_directory".
