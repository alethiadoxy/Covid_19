def DL_from_url_and_save(url, destination):
    #move this to subroutine 1
    #request the file
    import requests
    with requests.get(url, stream=True) as response:
        response.raise_for_status()

        with open(destination, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
            file.flush()
    #sub 1 over

def main():
    # .gov release daily CSVs with corona virus death figures that are 2 days behind the present.
    # https://coronavirus.data.gov.uk/?_ga=2.157835066.1251021075.1589887735-1783596499.1585566366
    #notably each CSV has the same URL
    #from datetime import date
    import datetime as dt
    import math
    todaysdate = dt.date.today().__str__()
    print(todaysdate)
    url        = "https://coronavirus.data.gov.uk/downloads/csv/coronavirus-deaths_latest.csv"
    destination="deaths_latest_"+todaysdate+".csv"
    DL_from_url_and_save(url, destination)
    print(".gov data retrieved")



    #each Tuesday the ONS release much more in depth figures that are several weeks behind
    #https: // www.ons.gov.uk / peoplepopulationandcommunity / birthsdeathsandmarriages / deaths / datasets / weeklyprovisionalfiguresondeathsregisteredinenglandandwales
    #this link is currently at: "https://www.ons.gov.uk/file?uri=%2fpeoplepopulationandcommunity%2fbirthsdeathsandmarriages%2fdeaths%2fdatasets%2fweeklyprovisionalfiguresondeathsregisteredinenglandandwales%2f2020/publishedweek192020.xlsx"
    #notably each new week the week number will increment up
    test=False
    if (dt.datetime.today().weekday() == 1)|(test):
        destination = "ONS_deaths_latest_" + todaysdate + ".xlsx"
        urlstart = "https://www.ons.gov.uk/file?uri=%2fpeoplepopulationandcommunity%2fbirthsdeathsandmarriages%2fdeaths%2fdatasets%2fweeklyprovisionalfiguresondeathsregisteredinenglandandwales%2f2020/publishedweek"
        td       = dt.date.today() - dt.date(2020, 1, 1)
        weekno   = math.floor(td.days / 7)
        if dt.datetime.today().weekday() == 0:
            weekno=weekno-1 #if testing on a monday this weeks reports aren't out yet
        weeknostr=str(weekno)
        urlend   = "2020.xlsx"
        url      = urlstart+weeknostr+urlend
        DL_from_url_and_save(url, destination)

        print("ONS data retrieved")

    return 0

if __name__ == "__main__":
    import sys
    sys.exit(main())
