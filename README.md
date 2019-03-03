Use this CLI-tool to import csv in your Google Sheet.

Requirements:
```
click
google-api-python-client
```



Download credential.json via "Enable The Drive Api" button to your working directory.
https://developers.google.com/drive/api/v3/quickstart/python

Run the script

----
https://stackoverflow.com/questions/42362702/how-to-import-a-csv-file-using-google-sheets-api-v4


1. Download `credential.json` via "Enable The Drive Api" button to your working directory.
https://developers.google.com/drive/api/v3/quickstart/python

2. Don't forget to use virtualenv. Activate it

3. Install requirements `pip install requirements.txt`.

4. Change data on config.py. Your can learn SPREADSHEET_ID from url of the Spreadsheet
https://developers.google.com/sheets/api/guides/concepts#sheet_id

5. Run the script
Import all csv rows:
```
python import_csv.py path_to_your_csv
```
Import csv rows except the first line:
```
python import_csv.py path_to_your_csv cut
```
