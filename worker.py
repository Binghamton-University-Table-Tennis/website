from work import *
import time

if __name__ == '__main__':

	month = datetime.date.today().month

	while True:
		checkForMatchUpdates()
		checkForPracticeUpdates()

		# Delete log entries once a month
		if month != datetime.date.today().month:
			deleteLogEntries()

		time.sleep(5)


