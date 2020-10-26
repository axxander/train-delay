# Train Delay
Train Delay interacts with the National Rail Darwin Data Feeds Historical Service Performance APIs to get the actual time of arrival of trains within the UK.

## Motivation
Having spent a lot of time on trains during my student and post-student days, I inevitably got delayed frequently. At least, with the introduction of compensation for dawdling services, I could get some money back! However, this was never as easy as advertised. 

The obfuscation of critical information, such as the actual arrival time, was infuriating. This was amplified when trying to calculate the total delay of a multi-leg journey consisting of many operators. So, I wrote a quick application to get the *actual* arrival time of trains using the National Rail APIs. 

## Roadmap
There are many features that I intend to add in the future. A select few are:
- Output the scheduled journey times (departure and arrival) so users can clarify it is the correct service.
- Multi-leg ticket system where the total delay can be calculated, as well as the operator responsible for delays.
- Making the station name system more user friendly.

## Installation
Use the package manager [pip](https://pip.pypa.io/en/stable/) to install Python project dependencies.

```bash
pip install -r requirements.txt
```

Create the alias command "traindelay" to launch the Train Delay App from anywhere. On Linux OS, change from `.bash_profile` to `.bashrc`.
```bash
source traindelay/alias.sh
```

## Usage
The general syntax is

```bash
traindelay origin-station-CRS destination-station-CRS HHMM YYYY-MM-DD
```

where `origin-station-CRS` and `destination-station-CRS` are the CRS codes of the origin and destination station respectively. The CRS code is a unique station identifier. A list of stations and their corresponding CRS code can be found [here](https://www.nationalrail.co.uk/stations_destinations/48541.aspx). `HHMM` is the time (hour, minute) and `YYYY-MM-DD` is the date (year, month, day).

### Example: York -> Sheffield
Train departing from `York` (CRS: YRK) to `Sheffield` (CRS: SHF) at `0954` on `2020-10-09`
```bash
traindelay yrk shf 0954 2020-10-09
```
Train Delay response
```bash
Journey: YRK --> SHF
Scheduled Arrival: 0954
Actual Arrival: 1004
```

### Example: Leicester -> Narborough
Train departing from `Leicester` (CRS: LEI) to `Narborough` (CRS: NBR) at `1550` on `2020-10-26`
```bash
traindelay lei nbr 1550 2020-10-26
```
Train Delay response
```bash
Journey: LEI --> NBR
Scheduled Arrival: 1559
Actual Arrival: 1558
```

## Tests
The unit tests currently only cover the regular expression for handling the command line interface.

## License
[MIT](https://choosealicense.com/licenses/mit/)

