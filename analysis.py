import csv
import pandas
from datetime import datetime
from datetime import timedelta
import json
import statistics
import plotly.graph_objects as px


def monthly_analyze(start, end, filename):
    hourly_delay = {'06': [], '07': [], '08': [], '09': [], '10': [], '11': [],
                '12': [], '13': [], '14': [], '15': [], '16':[], '17':[], '18':[], '19':[], '20':[], '21':[], '22':[], '23':[], '24':[]}
    daily_delay = {}
    stop_delay = {}
    peak_delay = {}
    with open(filename, "r") as historicalfile:
    # column name for file:
    # 0:tripId 1:stopSequence 2:arrivalDelay 3:arrivalTime 4:depatureDelay 5:depatureTime 6:stopID 7:timestamp
        has_header = csv.Sniffer().has_header(historicalfile.read())
        historicalfile.seek(0)  # Rewind.
        reader = csv.reader(historicalfile)
        if has_header:
            next(reader)
        for row in reader:
            arrival_time = datetime.strptime(row[3], '%m/%d/%Y %I:%M:%S %p')
            depature_time = datetime.strptime(row[5], '%m/%d/%Y %I:%M:%S %p')
            timestamp = datetime.strptime(row[7], '%m/%d/%Y %I:%M:%S %p')
            sequence = row[1]
            # check this record is valid (not prediction, acutally happened situation)
            # and timestamp > start_date and timestamp < end_date:
            if arrival_time <= timestamp and depature_time <= timestamp and row[7][11:] != '04:00:00 AM' and row[6]!='depen' and timestamp>start and timestamp<end:
                # delay seconds
                if "," in row[2]:
                    delay = int(row[2].replace(",", ""))
                else:
                    delay = int(row[2])
                # if delay <0:
                #     delay = abs(delay)

                tripID = row[0]
                stopID = row[6]

                try:
                    if int(stopID) < 8128 and int(stopID) % 2 == 1:
                        stopID = str(int(stopID)-1)
                except ValueError as e:
                    pass

                if stopID == '8128':
                    stopID = '8129'

                hour_time = datetime.strptime(row[7][11:], '%I:%M:%S %p')

                if stopID not in stop_delay:
                    stop_delay[stopID] = {'06:00-07:00':[], '07:00-08:00':[], '08:00-09:00':[],
                    '09:00-10:00':[], '10:00-11:00':[], '11:00-12:00':[], '12:00-13:00':[], '13:00-14:00':[], '14:00-15:00':[], '15:00-16:00':[], '16:00-17:00':[], '17:00-18:00':[], '18:00-19:00':[],
                    '19:00-20:00':[], '20:00-21:00':[], '21:00-22:00':[], '22:00-23:00':[], '23:00-24:00':[], '24:00-02:00':[]}
                    if hour_time >= datetime.strptime("06:00:00", '%H:%M:%S') and hour_time < datetime.strptime("07:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['06:00-07:00'].append(delay)
                    elif hour_time >= datetime.strptime("07:00:00", '%H:%M:%S') and hour_time < datetime.strptime("08:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['07:00-08:00'].append(delay)
                    elif hour_time >= datetime.strptime("08:00:00", '%H:%M:%S') and hour_time < datetime.strptime("09:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['08:00-09:00'].append(delay)
                    elif hour_time >= datetime.strptime("09:00:00", '%H:%M:%S') and hour_time < datetime.strptime("10:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['09:00-10:00'].append(delay)
                    elif hour_time >= datetime.strptime("10:00:00", '%H:%M:%S') and hour_time < datetime.strptime("11:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['10:00-11:00'].append(delay)
                    elif hour_time >= datetime.strptime("11:00:00", '%H:%M:%S') and hour_time < datetime.strptime("12:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['11:00-12:00'].append(delay)
                    elif hour_time >= datetime.strptime("12:00:00", '%H:%M:%S') and hour_time < datetime.strptime("13:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['12:00-13:00'].append(delay)
                    elif hour_time >= datetime.strptime("13:00:00", '%H:%M:%S') and hour_time < datetime.strptime("14:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['13:00-14:00'].append(delay)
                    elif hour_time >= datetime.strptime("14:00:00", '%H:%M:%S') and hour_time < datetime.strptime("15:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['14:00-15:00'].append(delay)
                    elif hour_time >= datetime.strptime("15:00:00", '%H:%M:%S') and hour_time < datetime.strptime("16:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['15:00-16:00'].append(delay)
                    elif hour_time >= datetime.strptime("16:00:00", '%H:%M:%S') and hour_time < datetime.strptime("17:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['16:00-17:00'].append(delay)
                    elif hour_time >= datetime.strptime("17:00:00", '%H:%M:%S') and hour_time < datetime.strptime("18:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['17:00-18:00'].append(delay)
                    elif hour_time >= datetime.strptime("18:00:00", '%H:%M:%S') and hour_time < datetime.strptime("19:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['18:00-19:00'].append(delay)
                    elif hour_time >= datetime.strptime("19:00:00", '%H:%M:%S') and hour_time < datetime.strptime("20:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['19:00-20:00'].append(delay)
                    elif hour_time >= datetime.strptime("20:00:00", '%H:%M:%S') and hour_time < datetime.strptime("21:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['20:00-21:00'].append(delay)
                    elif hour_time >= datetime.strptime("21:00:00", '%H:%M:%S') and hour_time < datetime.strptime("22:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['21:00-22:00'].append(delay)
                    elif hour_time >= datetime.strptime("22:00:00", '%H:%M:%S') and hour_time < datetime.strptime("23:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['22:00-23:00'].append(delay)
                    elif hour_time >= datetime.strptime("23:00:00", '%H:%M:%S') and hour_time <= datetime.strptime("23:59:59", '%H:%M:%S'):
                        stop_delay[stopID]['23:00-24:00'].append(delay)
                    else:
                        stop_delay[stopID]['24:00-02:00'].append(delay)
                else:
                    if hour_time >= datetime.strptime("06:00:00", '%H:%M:%S') and hour_time < datetime.strptime("07:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['06:00-07:00'].append(delay)
                    elif hour_time >= datetime.strptime("07:00:00", '%H:%M:%S') and hour_time < datetime.strptime("08:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['07:00-08:00'].append(delay)
                    elif hour_time >= datetime.strptime("08:00:00", '%H:%M:%S') and hour_time < datetime.strptime("09:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['08:00-09:00'].append(delay)
                    elif hour_time >= datetime.strptime("09:00:00", '%H:%M:%S') and hour_time < datetime.strptime("10:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['09:00-10:00'].append(delay)
                    elif hour_time >= datetime.strptime("10:00:00", '%H:%M:%S') and hour_time < datetime.strptime("11:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['10:00-11:00'].append(delay)
                    elif hour_time >= datetime.strptime("11:00:00", '%H:%M:%S') and hour_time < datetime.strptime("12:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['11:00-12:00'].append(delay)
                    elif hour_time >= datetime.strptime("12:00:00", '%H:%M:%S') and hour_time < datetime.strptime("13:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['12:00-13:00'].append(delay)
                    elif hour_time >= datetime.strptime("13:00:00", '%H:%M:%S') and hour_time < datetime.strptime("14:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['13:00-14:00'].append(delay)
                    elif hour_time >= datetime.strptime("14:00:00", '%H:%M:%S') and hour_time < datetime.strptime("15:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['14:00-15:00'].append(delay)
                    elif hour_time >= datetime.strptime("15:00:00", '%H:%M:%S') and hour_time < datetime.strptime("16:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['15:00-16:00'].append(delay)
                    elif hour_time >= datetime.strptime("16:00:00", '%H:%M:%S') and hour_time < datetime.strptime("17:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['16:00-17:00'].append(delay)
                    elif hour_time >= datetime.strptime("17:00:00", '%H:%M:%S') and hour_time < datetime.strptime("18:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['17:00-18:00'].append(delay)
                    elif hour_time >= datetime.strptime("18:00:00", '%H:%M:%S') and hour_time < datetime.strptime("19:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['18:00-19:00'].append(delay)
                    elif hour_time >= datetime.strptime("19:00:00", '%H:%M:%S') and hour_time < datetime.strptime("20:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['19:00-20:00'].append(delay)
                    elif hour_time >= datetime.strptime("20:00:00", '%H:%M:%S') and hour_time < datetime.strptime("21:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['20:00-21:00'].append(delay)
                    elif hour_time >= datetime.strptime("21:00:00", '%H:%M:%S') and hour_time < datetime.strptime("22:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['21:00-22:00'].append(delay)
                    elif hour_time >= datetime.strptime("22:00:00", '%H:%M:%S') and hour_time < datetime.strptime("23:00:00", '%H:%M:%S'):
                        stop_delay[stopID]['22:00-23:00'].append(delay)
                    elif hour_time >= datetime.strptime("23:00:00", '%H:%M:%S') and hour_time <= datetime.strptime("23:59:59", '%H:%M:%S'):
                        stop_delay[stopID]['23:00-24:00'].append(delay)
                    else:
                        stop_delay[stopID]['24:00-02:00'].append(delay)

                if hour_time >= datetime.strptime("06:00:00", '%H:%M:%S') and hour_time < datetime.strptime("07:00:00", '%H:%M:%S'):
                    hourly_delay['06'].append(delay)
                elif hour_time >= datetime.strptime("07:00:00", '%H:%M:%S') and hour_time < datetime.strptime("08:00:00", '%H:%M:%S'):
                    hourly_delay['07'].append(delay)
                elif hour_time >= datetime.strptime("08:00:00", '%H:%M:%S') and hour_time < datetime.strptime("09:00:00", '%H:%M:%S'):
                    hourly_delay['08'].append(delay)
                elif hour_time >= datetime.strptime("09:00:00", '%H:%M:%S') and hour_time < datetime.strptime("10:00:00", '%H:%M:%S'):
                    hourly_delay['09'].append(delay)
                elif hour_time >= datetime.strptime("10:00:00", '%H:%M:%S') and hour_time < datetime.strptime("11:00:00", '%H:%M:%S'):
                    hourly_delay['10'].append(delay)
                elif hour_time >= datetime.strptime("11:00:00", '%H:%M:%S') and hour_time < datetime.strptime("12:00:00", '%H:%M:%S'):
                    hourly_delay['11'].append(delay)
                elif hour_time >= datetime.strptime("12:00:00", '%H:%M:%S') and hour_time < datetime.strptime("13:00:00", '%H:%M:%S'):
                    hourly_delay['12'].append(delay)
                elif hour_time >= datetime.strptime("13:00:00", '%H:%M:%S') and hour_time < datetime.strptime("14:00:00", '%H:%M:%S'):
                    hourly_delay['13'].append(delay)
                elif hour_time >= datetime.strptime("14:00:00", '%H:%M:%S') and hour_time < datetime.strptime("15:00:00", '%H:%M:%S'):
                    hourly_delay['14'].append(delay)
                elif hour_time >= datetime.strptime("15:00:00", '%H:%M:%S') and hour_time < datetime.strptime("16:00:00", '%H:%M:%S'):
                    hourly_delay['15'].append(delay)
                elif hour_time >= datetime.strptime("16:00:00", '%H:%M:%S') and hour_time < datetime.strptime("17:00:00", '%H:%M:%S'):
                    hourly_delay['16'].append(delay)
                elif hour_time >= datetime.strptime("17:00:00", '%H:%M:%S') and hour_time < datetime.strptime("18:00:00", '%H:%M:%S'):
                    hourly_delay['17'].append(delay)
                elif hour_time >= datetime.strptime("18:00:00", '%H:%M:%S') and hour_time < datetime.strptime("19:00:00", '%H:%M:%S'):
                    hourly_delay['18'].append(delay)
                elif hour_time >= datetime.strptime("19:00:00", '%H:%M:%S') and hour_time < datetime.strptime("20:00:00", '%H:%M:%S'):
                    hourly_delay['19'].append(delay)
                elif hour_time >= datetime.strptime("20:00:00", '%H:%M:%S') and hour_time < datetime.strptime("21:00:00", '%H:%M:%S'):
                    hourly_delay['20'].append(delay)
                elif hour_time >= datetime.strptime("21:00:00", '%H:%M:%S') and hour_time < datetime.strptime("22:00:00", '%H:%M:%S'):
                    hourly_delay['21'].append(delay)
                elif hour_time >= datetime.strptime("22:00:00", '%H:%M:%S') and hour_time < datetime.strptime("23:00:00", '%H:%M:%S'):
                    hourly_delay['22'].append(delay)
                elif hour_time >= datetime.strptime("23:00:00", '%H:%M:%S') and hour_time <= datetime.strptime("23:59:59", '%H:%M:%S'):
                    hourly_delay['23'].append(delay)
                else:
                    hourly_delay['24'].append(delay)

                if datetime.strptime("05:00:00", '%H:%M:%S') > hour_time and hour_time > datetime.strptime("00:00:00", '%H:%M:%S'):
                    # date - 1 day
                    record_date = datetime.strftime(
                        timestamp + timedelta(days=-1), '%m/%d/%Y')
                else:
                    record_date = row[7][0:10]

                if record_date not in daily_delay:
                    daily_delay[record_date] = {tripID: [delay]}
                else:
                    if tripID not in daily_delay[record_date]:
                        daily_delay[record_date][tripID] = [delay]
                    else:
                        daily_delay[record_date][tripID].append(delay)

                # analysis for weekday peak hours
                if timestamp.weekday() < 5 and ((datetime.strptime("07:30:00", '%H:%M:%S') < hour_time and hour_time < datetime.strptime("09:30:00", '%H:%M:%S')) or (datetime.strptime("17:00:00", '%H:%M:%S') < hour_time and hour_time < datetime.strptime("19:00:00", '%H:%M:%S'))):
                    if record_date not in peak_delay:
                        peak_delay[record_date] = {tripID: [delay]}
                    else:
                        if tripID not in peak_delay[record_date]:
                            peak_delay[record_date][tripID] = [delay]
                        else:
                            peak_delay[record_date][tripID].append(delay)
    historicalfile.close

    with open(f'output/{start.month}_Hourly_delay_average.csv', 'w') as hourly_average:
        heads = ['time', 'delay']
        names = ['06:00-07:00', '07:00-08:00', '08:00-09:00', '09:00-10:00', '10:00-11:00', '11:00-12:00', 
                        '12:00-13:00', '13:00-14:00', '14:00-15:00', '15:00-16:00', '16:00-17:00', '17:00-18:00', 
                            '18:00-19:00', '19:00-20:00', '20:00-21:00', '21:00-22:00', '22:00-23:00', '23:00-24:00', '24:00-02:00']
        writer = csv.DictWriter(hourly_average, fieldnames=heads)
        writer.writeheader()
        for t in names:
            writer.writerow({'time': t, 'delay': format(statistics.mean(hourly_delay[t[:2]]), '.2f')})
    hourly_average.close

    with open(f'output/{start.month}_hourly_box.csv', 'w') as hourly_box:
        heads = ['time', 'delay']
        names = ['06:00-07:00', '07:00-08:00', '08:00-09:00', '09:00-10:00', '10:00-11:00', '11:00-12:00', 
                        '12:00-13:00', '13:00-14:00', '14:00-15:00', '15:00-16:00', '16:00-17:00', '17:00-18:00', 
                            '18:00-19:00', '19:00-20:00', '20:00-21:00', '21:00-22:00', '22:00-23:00', '23:00-24:00', '24:00-02:00']
        writer = csv.DictWriter(hourly_box, fieldnames=heads)
        writer.writeheader()
        for t in names:
            for d in hourly_delay[t[:2]]:
                writer.writerow({'time': t, 'delay': d})
    hourly_box.close

    Stop = {}
    for st in sorted(stop_delay.keys()):
        Stop[st] = {}
        for t in stop_delay[st]:
            try:
                Stop[st][t] = statistics.mean(stop_delay[st][t])
            except statistics.StatisticsError as e:
                Stop[st][t] = 0
    with open(f'output/{start.month}_Stop_delay.json', 'w') as file3:
        json.dump(Stop, file3)
    file3.close
    
    Daily = {}
    for dt in sorted(daily_delay.keys()):
        Daily[dt] = {}
        for tid in daily_delay[dt]:
            try:
                Daily[dt][tid] = format(statistics.mean(daily_delay[dt][tid]), '.2f')
            except statistics.StatisticsError as e:
                Daily[dt][tid] = 0
    with open(f'output/{start.month}_Daily_delay.json', 'w') as outfile:
        json.dump(Daily, outfile)
    outfile.close

    Peak = {}
    for dt in sorted(peak_delay.keys()):
        Peak[dt] = {}
        for tid in peak_delay[dt]:
            try:
                Peak[dt][tid] = format(statistics.mean(peak_delay[dt][tid]), '.2f')
            except statistics.StatisticsError as e:
                Daily[dt][tid] = 0
    with open(f'output/{start.month}_Peak_delay.json', 'w') as peakfile:
        json.dump(Peak, peakfile)
    peakfile.close

months_lsit = json.load(open('output/months_index.json'))['months']
filename = "Canberra_Metro_Light_Rail_Transit_Feed_-_Trip_Updates__Historical_Archive_.csv"
for i in months_lsit:
    monthly_analyze(datetime(i[0],i[1],1), datetime(i[0],i[1]+1,1), filename)