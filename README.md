1. Download `credential.json` via "Enable The Drive Api" button to your working directory.
https://developers.google.com/drive/api/v3/quickstart/python

2. Don't forget to use virtualenv. Activate it.

3. Install requirements `pip install -r requirements.txt`.

4. Change data on config.py. Your can learn SPREADSHEET_ID from url of the Spreadsheet
https://developers.google.com/sheets/api/guides/concepts#sheet_id

5. Run the script.

Import all csv rows:
```
python import_csv.py path_to_your_csv first
```
Import csv rows except the first line:
```
python import_csv.py path_to_your_csv
```
