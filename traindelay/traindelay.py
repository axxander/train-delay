import datetime
import calendar
import requests
import json
import sys
import re
import os
from typing import List, Tuple, Dict
from constants import Constants


class ServiceMetric:
    """Communication with the National Rail Darwin Data Feeds Historical Service Performance
       (HSP) API. Specifically, the Service Metrics component.
       More information @https://wiki.openraildata.com/index.php?title=HSP.

    Args:
        url: HSP API URL.
        auth: Darwin Data Feeds email and password.
        headers: HTTP header for API call.
        from_loc: CRS code of origin station (https://www.nationalrail.co.uk/stations_destinations/48541.aspx).
        to_loc: CRS code of destination station (https://www.nationalrail.co.uk/stations_destinations/48541.aspx).
        from_date: Date of travel "YYYY-MM-DD".
        to_date: Must equal or later than from_date. Not relevant for this application.
        from_time: Time of departure "HHMM".
        to_time: Must be later than from_time. Handled by static method.
        day; Either WEEKDAY, SATURDAY or SUNDAY. Handled by static method.
        params: POST request parameters.

    """
    def __init__(self, from_loc: str, to_loc: str, from_date: str, from_time: str) -> None:

        # set parameters
        self.url: str = "https://hsp-prod.rockshore.net/api/v1/serviceMetrics"
        self.auth: Tuple[str] = (os.environ["DAWIN_EMAIL"], os.environ["DAWIN_PASS"])
        self.headers: Dict[str, str] = {"Content-Type": "application/json"}
        self.from_loc = from_loc.upper()
        self.to_loc = to_loc.upper()
        self.from_date = from_date
        self.to_date = self.from_date
        self.from_time = from_time
        self.to_time = self.__class__.to_time(self.from_time)
        self.day = self.__class__.weekday(self.from_date)

        # POST request parameters
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
        """Adds delta minutes to a time and maintains 24-hour format.
           If time + delta is beyond midnight, 2359 is returned.

        Args:
            time: 24-hour time.
            delta: Amount, in minutes, to add to the time variable.

        Returns:
            : 24-hour formatted time of input time + delta minutes. Returns 2359 if
            beyond midnight.
            
        """
        hour, minute = int(time[:2]), int(time[2:])

        minute += delta
        if minute // 60:  # increment hour and recalculate minute
            hour += 1
            minute = minute%60
            if hour > 23:  # assume midnight
                to_time = "2359"

        return f"{hour*100+minute:04}"


    @staticmethod
    def weekday(date: str) -> str:
        """For a given date, returns either SATURDAY is returned for 
           Saturday, SUNDAY for Sunday or WEEKDAY for all other days.

        Args:
            date: Calendar date, formatted YYYY-MM-DD.

        Returns:
            : WEEKDAY for Monday-Friday, SATURDAY for Saturday and 
            SUNDAY for Sunday.

        """
        date = datetime.date(*map(int, date.split("-")))
        day = calendar.day_name[date.weekday()]  # get day of the week

        if day != "Saturday" and day != "Sunday":
            return "WEEKDAY"
        else:
            return day.upper()


    def post_service_metrics(self) -> None:
        """Sends POST request to Darwin Data Feeds HSP Service Metrics API.
        
        Args:
            None

        Returns:
            None

        """
        # send POST request
        self.response = requests.post(url=self.url, json=self.params, headers=self.headers, auth=self.auth)
        if self.response.status_code != 200:  # validate response code
            sys.exit(f"Service Metrics POST request failed with status code {self.response.status_code}.")


class ServiceDetail:
    """Communication with the National Rail Darwin Data Feeds Historical Service Performance
       (HSP) API. Specifically, the Service Details component.
       More information @https://wiki.openraildata.com/index.php?title=HSP.

    Args:
        url: HSP API URL.
        auth: Darwin Data Feeds email and password.
        headers: HTTP header for API call.
        rid: Unique identifier used by a train on a particular day.

    """
    def __init__(self, rid: str) -> None:

        # set parameters
        self.url = "https://hsp-prod.rockshore.net/api/v1/serviceDetails"
        self.auth = (os.environ["DAWIN_EMAIL"], os.environ["DAWIN_PASS"])
        self.headers = {"Content-Type": "application/json"}

        # POST request parameters
        self.params = {"rid": rid}


    def post_service_detail(self) -> None:
        """Sends POST request to Darwin Data Feeds HSP Service Details API.
        
        Args:
            None

        Returns:
            None

        """
        # send POST request
        self.response = requests.post(url=self.url, json=self.params, headers=self.headers, auth=self.auth)
        if self.response.status_code != 200:  # validate response code
            sys.exit(f"Service Detail POST request failed with status code {self.response.status_code}.")



def arg_parse(user_input: List[str]) -> Tuple[str]:
    """Command-line interface. Extracts from_loc, to_loc, date and time.

    Args:
        user_inputs: User input in console.

    Returns:
        args: from_loc, to_loc, time and date.

    """
    input_str = "".join(arg.strip() + " " for arg in user_input).strip()

    if len(input_str) != 23:  # all valid inputs will be the same length
        sys.exit("Arguments are invalid. Please try again.")

    match = re.search(Constants.interface_pattern, input_str)
    if not match:
        sys.exit("Arguments are invalid. Please try again.")

    args = match.groups()  # example: yrk shf 1731 2020-10-09

    return args


if __name__ == "__main__":

    from_loc, to_loc, time, date = arg_parse(sys.argv[1:])  # get user arguments

    sm = ServiceMetric(from_loc, to_loc, date, time)
    sm.post_service_metrics()  # send POST request to Service Metrics

    # get RIDs for service
    rids = []
    for service in sm.response.json()["Services"]:
        rids.append(*service["serviceAttributesMetrics"]["rids"])

    if rids:  # service found
        sd = ServiceDetail(rids[0])
        sd.post_service_detail()  # send POST request to Service Details

        train = sd.response.json()["serviceAttributesDetails"]["locations"]
        for station in train:
            if station["location"] == sm.to_loc:
                print(f"Journey: {from_loc.upper()} --> {to_loc.upper()}")
                print(f"Scheduled Arrival: {station['gbtt_pta']}")
                print(f"Actual Arrival: {station['actual_ta']}")
                break
    else:
        print("No service match.")








