import datetime
import calendar
import requests
import json
import sys
import re
import os

# Service metric to get trains
class ServiceMetric:

	def __init__(self, from_loc, to_loc, from_date, from_time):

		# set attributes
		self.url = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
		self.auth = (os.environ["DAWIN_EMAIL"], os.environ["DAWIN_PASS"])
		self.headers = {"Content-Type": "application/json"}

		self.from_loc = from_loc
		self.to_loc = to_loc
		self.from_date = from_date
		self.to_date = self.from_date
		self.from_time = from_time
		self.to_time = self.__class__.to_time(self.from_time)
		self.day = self.__class__.weekday(self.from_date)

		# body of service metrics POST request
		self.params = {
			"from_loc": self.from_loc,
			"to_loc": self.to_loc,
			"from_time": self.from_time,
			"to_time": self.to_time,
			"from_date": self.from_date,
			"to_date": self.to_date,
			"days": self.day
		}


	@staticmethod
	def to_time(time: str, delta: int = 60) -> str:
		
		# get hour and minute from string
		p = re.compile(r"([0-9]{2})([0-9]{2})")
		hour, minute = re.search(p, time).groups()
		hour, minute = int(hour), int(minute)

		minute += delta
		if minute // 60:  # increment hour and recalculate minute
			hour += 1
			minute = minute%60
			if hour > 23:  # assume midnight
				to_time = "2359"

		return f"{hour*100+minute:04}"


	@staticmethod
	def weekday(date: str) -> str:

		date = datetime.date(*map(int, date.split('-')))
		day = calendar.day_name[date.weekday()] 

		if day != 'Saturday' and day != 'Sunday':
			return 'WEEKDAY'
		else:
			return day.upper()


	def post_service_metrics(self):

		# send POST request and validate OK response
		self.response = requests.post(url=self.url, json=self.params, headers=self.headers, auth=self.auth)
		if self.response.status_code != 200:
			sys.exit(f"Service Metrics POST request failed with status code {self.response.status_code}.")


class ServiceDetail:

	def __init__(self, rid: str) -> None:
		self.url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
		self.auth = (os.environ["DAWIN_EMAIL"], os.environ["DAWIN_PASS"])
		self.headers = {"Content-Type": "application/json"}

		self.params = {"rid": rid}

	def post_service_detail(self) -> None:

		# send POST request and validate OK response
		self.response = requests.post(url=self.url, json=self.params, headers=self.headers, auth=self.auth)
		if self.response.status_code != 200:
			sys.exit(f"Service Detail POST request failed with status code {self.response.status_code}.")



if __name__ == "__main__":

	# user enters origin and scheduled departure time
	sm = ServiceMetric("YRK", "SHF", "2020-10-09", "1731")
	# look for services matching user input
	sm.post_service_metrics()

	rids = []
	for service in sm.response.json()["Services"]:
		rids.append(*service["serviceAttributesMetrics"]["rids"])

	if rids:
		sd = ServiceDetail(rids[0])
		sd.post_service_detail()

		train = sd.response.json()["serviceAttributesDetails"]["locations"]
		for station in train:
			if station["location"] == sm.to_loc:
				print(f"Scheduled Arrival: {station['gbtt_pta']}")
				print(f"Actual Arrival: {station['actual_ta']}")
				break
	else:
		print("No service match")


	# for service in sd.response.json()["serviceAttributesDetails"]:








