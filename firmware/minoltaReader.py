import pandas as pd
from collections import OrderedDict
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import os
import time
# Path to the CSV file
csv_file = '../mintsData/MINTS_Minolta_10004098_2024_08_27_22.csv'

def csvToOrderedDict():
    df = pd.read_csv(csv_file).tail(1)

    df.columns = df.columns.str.replace(' ', '')

    df.columns = df.columns.str.replace('/', '')

    df['dateTime'] =pd.to_datetime(df['Date'] + ' ' + df['Time'], format='%Y/%m/%d %H:%M:%S')
        # Drop the original 'Date' and 'Time' columns
    df.drop(['Date', 'Time'], axis=1, inplace=True)

    # Reorder the columns to place 'dateTime' first
    cols = ['dateTime'] + [col for col in df.columns if col != 'dateTime']

    df = df[cols]

    df['dateTime'] = df['dateTime'].dt.strftime('%Y-%m-%d %H:%M:%S.%f')

    # Create a dictionary that maps 'Spectrum[i]' to 'channelXXXnm'
    new_columns = {f'Spectrum[{i}]': f'channel{360 + i}nm' for i in range(421)}

    # Rename the DataFrame columns based on the dictionary
    df.rename(columns=new_columns, inplace=True)
        # Convert the DataFrame to a list of dictionaries
    records = df.to_dict(orient='records')

    # Create an OrderedDict from the list of dictionaries
    ordered_dict = OrderedDict()

    for record in records:
        ordered_dict.update(record)  # Update with each record

    return ordered_dict



class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        # Check if the modified file is the target CSV file
        if event.src_path == os.path.abspath(csv_file):
            print("File changed, processing...")
            ordered_dict = csvToOrderedDict()
            print(ordered_dict)

def monitor_file(file_path):
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path=os.path.dirname(file_path), recursive=False)
    
    print("Monitoring file for changes...")
    observer.start()

    try:
        while True:
            time.sleep(1)  # Keep the script running
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Start monitoring the CSV file for changes
monitor_file(csv_file)