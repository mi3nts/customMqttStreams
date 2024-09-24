# import pandas as pd
import time 
import site
import sys
sys.path.append("c:\\users\\lakit\\appdata\\local\\programs\\python\\python39\\lib\\site-packages\\")
from watchdog.observers import Observer
from watchdog.events import PatternMatchingEventHandler

from collections import OrderedDict
from mintsXU4 import mintsLatest as mL
from mintsXU4 import mintsDefinitions as mD
from mintsXU4 import mintsSensorReader as mSR
import datetime
# Reading last line of code 

path = "D:\\githubRepos\\palasDataStreamer\\mintsData\\"

def on_mod(event):
    # time.sleep(.1)
    global dateTimePre
    print("-------------------")
    try:
        with open(event.src_path, "r") as f1:
            all = f1.readlines()
            lastLine = all[-1]

        dataOutPre  = lastLine.replace('Inf','-1').split()
        dateTime    = datetime.datetime.strptime((dataOutPre[0] + ' ' + dataOutPre[1]), '%d.%m.%y %H:%M:%S')
        if dateTimePre < dateTime:
            dataOut = dataOutPre[2:len(dataOutPre)]
            mSR.FRG001Write(dataOut,dateTime)
            dateTimePre = dateTime

    except:
        print(sys.exc_info())

if __name__ == "__main__":
    global dateTimePre
    dateTimePre  = datetime.datetime(2016, 1, 1)

    # With patterns="*.csv" you should not have to add ignore_patterns=["*~"
    patterns = [\
            "*.txt"]
 
    ignore_patterns =['2019' ]
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(patterns, ignore_patterns, ignore_directories, case_sensitive)

    my_event_handler.on_modified = on_mod
    
    # path = "D:\\githubRepos\\palasDataStreamer\\mintsData\\"
    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)
    my_observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()