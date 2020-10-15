## Train Delay

Communicates with the National Rail Darwin Data Feeds Historical Service Performance APIs to get the actual arrival time of trains within the UK.

I spent a lot of time on trains, which were frequently delayed. When it came to applying for compensation, I found it difficult to find out exactly when my train arrived, especially when I had to deviate to a different route. So I decided to write a quick application that requires both the origin and destination station, date of travel and departure time. It returns the scheduled and actual arrival time of the service.

More documentation will be added in the near future. I also have a list of features I wish to add. For example:
- Ability to track multi-leg journies.
- Calculating exact delay times.
- Outputing the service operator responsible for the delay.
- Extending the station name input beyond CRS codes.

### How to Use
- Run the Bash script in /traindelay to create the alias 'traindelay'.
- You can then execute the program in the command line with the following syntax
```bash
traindelay origin-station-CRS destination-station-CRS HHMM YYYY-MM-DD
```
- So, for a train departing from York (YRK) on 09/10/2020 at 0954 to Sheffield (SHF), we do the following:
```bash
traindelay yrk shf 0954 2020-10-09
```
and the response is:
```bash
Journey: YRK --> SHF
Scheduled Arrival: 0954
Actual Arrival: 1004
```
