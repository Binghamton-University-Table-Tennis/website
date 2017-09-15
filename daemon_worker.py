from work import *
import time

if __name__ == '__main__':
    while True:
        checkForMatchUpdates()
        checkForPracticeUpdates()
        deleteLogEntries()
        time.sleep(1)
