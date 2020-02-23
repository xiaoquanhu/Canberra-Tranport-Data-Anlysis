import csv
import json
from datetime import datetime
from datetime import timedelta

historicalfilename = 'Canberra_Metro_Light_Rail_Transit_Feed_-_Trip_Updates__Historical_Archive_.csv'
measurings = ['8100', '8129', '8110', '8111', '8114', '8115', '8120', '8121']
# schedual: from trips.txt to parse weekend, weekday information in schedual timetable
WD_trips = []
FR_trips = []
SA_trips = []
SU_trips = []

with open("google_transit_lr/trips.txt", "r") as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:
        if row[1] == "WD":
            if row[2] != ' ':
                WD_trips.append(row[2])
        elif "FR" == row[1]:
            FR_trips.append(row[2])
        elif "SA" == row[1]:
            SA_trips.append(row[2])
        elif "SU" == row[1]:
            SU_trips.append(row[2])
csvfile.close

# To Calculate Completed Service
# sorted list in dict eg: SA_determ_time = {"8100"(StopID):[("trip2", 00:07:35)], "8129":[]}
WD_determ_time = {'8100':[], '8129':[], '8110':[], '8111':[], '8114':[], '8115':[], '8120':[], '8121':[]}
FR_determ_time = {'8100':[], '8129':[], '8110':[], '8111':[], '8114':[], '8115':[], '8120':[], '8121':[]}
SA_determ_time = {'8100':[], '8129':[], '8110':[], '8111':[], '8114':[], '8115':[], '8120':[], '8121':[]}
SU_determ_time = {'8100':[], '8129':[], '8110':[], '8111':[], '8114':[], '8115':[], '8120':[], '8121':[]}
Last_trips = []  # '266', '544', '710', '847'
WD_last = {}
FR_last = {}
SA_last = {}
SU_last = {}

# TO Calculate partially completed trips
# for every trip, the scheduled stopIDs for this trip
# eg: Schedule_stops = {"(trip)2":["8111", "8109", "8107", "8105", "8100"], "135":["8100","8104"....] }
Schedule_stops = {}

# To Calculate the number of scheduled arrivals at Stops for the relevant day
# eg: Schedule_num_arrivals = {'WD': 2915, 'FR': 3076, 'SA': 2022, 'SU': 1647}
Schedule_num_arrivals = {"WD": 0, "FR": 0, "SA": 0, "SU": 0}
with open("google_transit_lr/stop_times_forparse.txt", "r") as cs:
    reader = csv.reader(cs)
    num = 0
    WDlast = datetime.strptime("00:00:00", '%H:%M:%S')
    FRlast = datetime.strptime("00:00:00", '%H:%M:%S')
    SAlast = datetime.strptime("00:00:00", '%H:%M:%S')
    SUlast = datetime.strptime("00:00:00", '%H:%M:%S')
    for row in reader:
        # store sheduled stops for every trip
        TripID = row[0]
        stopID = row[3]
        arr_str = row[1]
        if int(arr_str[:2]) > 23:
            arr_str = str(int(arr_str[:2])-24) + arr_str[2:]
        arrival_time = datetime.strptime(arr_str, '%H:%M:%S')

        if row[4] == "1":
            Schedule_stops[TripID] = [row[3]]
        else:
            Schedule_stops[TripID].append(row[3])
            if stopID in measurings:
                if TripID in WD_trips:
                    WD_determ_time[stopID].append((TripID, arrival_time))
                elif TripID in FR_trips:
                    FR_determ_time[stopID].append((TripID, arrival_time))
                elif TripID in SA_trips:
                    SA_determ_time[stopID].append((TripID, arrival_time))
                else:
                    SU_determ_time[stopID].append((TripID, arrival_time))

        if TripID in WD_trips:
            Schedule_num_arrivals["WD"] += 1
        elif TripID in FR_trips:
            Schedule_num_arrivals["FR"] += 1
        elif TripID in SA_trips:
            Schedule_num_arrivals["SA"] += 1
        else:
            if row[4] != "1":
                Schedule_num_arrivals["SU"] += 1

        new_num = int(row[4])
        if new_num > num:
            num = new_num
            tempTripID = TripID
            detime = arrival_time
        else:
            if tempTripID in WD_trips:
                if detime > datetime.strptime("00:00:00", '%H:%M:%S') and detime < datetime.strptime("03:00:00", '%H:%M:%S') and detime > WDlast:
                    WDlast = detime
                    WDlid = tempTripID
            elif tempTripID in FR_trips:
                if detime > datetime.strptime("00:00:00", '%H:%M:%S') and detime < datetime.strptime("03:00:00", '%H:%M:%S') and detime > FRlast:
                    FRlast = detime
                    FRlid = tempTripID
            elif tempTripID in SA_trips:
                if detime > datetime.strptime("00:00:00", '%H:%M:%S') and detime < datetime.strptime("03:00:00", '%H:%M:%S') and detime > SAlast:
                    SAlast = detime
                    SAlid = tempTripID
            else:
                if detime > datetime.strptime("00:00:00", '%H:%M:%S') and detime < datetime.strptime("03:00:00", '%H:%M:%S') and detime > SUlast:
                    SUlast = detime
                    SUlid = tempTripID
            num = new_num
    Last_trips.append(WDlid)
    Last_trips.append(FRlid)
    Last_trips.append(SAlid)
    Last_trips.append(SUlid)
cs.close

for k in WD_determ_time:
    WD_determ_time[k].sort(key=lambda t: t[1])
    for index, tup in enumerate(WD_determ_time[k]):
        if index == 0:
            if tup[1] > datetime.strptime("05:00:00", '%H:%M:%S'):
                WD_last[k] = WD_determ_time[k][-1][0]
                break
            else:
                WD_last[k] = tup[0]
        else:
            if tup[1] < datetime.strptime("05:00:00", '%H:%M:%S'):
                WD_last[k] = tup[0]
for k in FR_determ_time:
    FR_determ_time[k].sort(key=lambda t: t[1])
    for index, tup in enumerate(FR_determ_time[k]):
        if index == 0:
            if tup[1] > datetime.strptime("05:00:00", '%H:%M:%S'):
                FR_last[k] = FR_determ_time[k][-1][0]
                break
            else:
                FR_last[k] = tup[0]
        else:
            if tup[1] < datetime.strptime("05:00:00", '%H:%M:%S'):
                FR_last[k] = tup[0]
for k in SA_determ_time:
    SA_determ_time[k].sort(key=lambda t: t[1])
    for index, tup in enumerate(SA_determ_time[k]):
        if index == 0:
            if tup[1] > datetime.strptime("05:00:00", '%H:%M:%S'):
                SA_last[k] = SA_determ_time[k][-1][0]
                break
            else:
                SA_last[k] = tup[0]
        else:
            if tup[1] < datetime.strptime("05:00:00", '%H:%M:%S'):
                SA_last[k] = tup[0]
for k in SU_determ_time:
    SU_determ_time[k].sort(key=lambda t: t[1])
    for index, tup in enumerate(SU_determ_time[k]):
        if index == 0:
            if tup[1] > datetime.strptime("05:00:00", '%H:%M:%S'):
                SU_last[k] = SU_determ_time[k][-1][0]
                break
            else:
                SU_last[k] = tup[0]
        else:
            if tup[1] < datetime.strptime("05:00:00", '%H:%M:%S'):
                SU_last[k] = tup[0]

with open('output/WD-determ.csv', 'w') as dadafa:
    heads = ['stop', 'tripID', 'time']
    writer = csv.DictWriter(dadafa, fieldnames=heads)
    writer.writeheader()
    for k in WD_determ_time:
        for de in WD_determ_time[k]:
            writer.writerow({'stop': k, 'tripID': de[0], 'time': de[1]})
dadafa.close


with open('output/last.csv', 'w') as file3:
    heads = ['time', 'last-tripID']
    writer = csv.DictWriter(file3, fieldnames=heads)
    writer.writeheader()
    for row in Last_trips:
        writer.writerow({'time': 'dada', 'last-tripID': row})
file3.close

# calculate daily indexations and write into daily_performance.csv

daily_results = {}
arr_at_stops = {}
year_months = set()

with open(historicalfilename, "r") as historicalfile:
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
        year_months.add((timestamp.year, timestamp.month))
        sequence = row[1]
        # check this record is valid (not prediction, acutally happened situation)
        # and timestamp > start_date and timestamp < end_date:
        if arrival_time <= timestamp and depature_time <= timestamp and row[0] in Schedule_stops:
            # chech timestamp is between 00:00:00 - 03:00:00
            midnight = datetime.strptime(row[7][11:], '%I:%M:%S %p')
            # if midnight > datetime.strptime("03:59:00", '%H:%M:%S') and midnight < datetime.strptime("04:02:00", '%H:%M:%S'):
            #     continue
            if datetime.strptime("05:00:00", '%H:%M:%S') > midnight and midnight > datetime.strptime("00:00:00", '%H:%M:%S'):
                # date - 1 day
                record_date = datetime.strftime(
                    timestamp + timedelta(days=-1), '%m/%d/%Y')
            else:
                # keep original date
                record_date = row[7][0:10]
            if record_date not in daily_results:
                daily_results[record_date] = {
                    "completed": set(), "arrivals": 0, "missed": set(), "partial": set(), "early": [], "late": [], "data_lost": [], "arrival_at_determ": 0, "dep_at_determ": 0, 'no_record': []}
                arr_at_stops[record_date] = {}

            tripID = row[0]
            stopID = row[6]
            delay = row[2]
            if "," in row[2]:
                delay = int(row[2].replace(",", ""))
            else:
                delay = int(row[2])

            if tripID not in arr_at_stops[record_date]:
                arr_at_stops[record_date][tripID] = {stopID}
            else:
                arr_at_stops[record_date][tripID].add(stopID)

            # need to confirm the smallest period of time between closest two services
            arr_dely_compare = datetime.strptime(row[3][11:], '%I:%M:%S %p')
            if tripID in WD_trips and stopID == Schedule_stops[tripID][-1]:
                # if this trip is the last one of the day
                if tripID == WD_last[stopID]:
                    if delay >= 15*60:
                        daily_results[record_date]["missed"].add(tripID)
                else:
                    length = len(WD_determ_time[stopID])
                    for i in range(length):
                        if WD_determ_time[stopID][i][0] == tripID:
                            if i == length-1:
                                if abs(24*60*60 - (arr_dely_compare - WD_determ_time[stopID][0][1]).total_seconds()) <= delay:
                                    daily_results[record_date]["missed"].add(
                                        tripID)
                            else:
                                if arr_dely_compare >= WD_determ_time[stopID][i+1][1]:
                                    daily_results[record_date]["missed"].add(
                                        tripID)
            elif tripID in FR_trips and stopID == Schedule_stops[tripID][-1]:
                if tripID == FR_last[stopID]:
                    if delay >= 15*60:
                        daily_results[record_date]["missed"].add(tripID)
                else:
                    length = len(FR_determ_time[stopID])
                    for i in range(length):
                        if FR_determ_time[stopID][i][0] == tripID:
                            if i == length-1:
                                if abs(24*60*60 - (arr_dely_compare - FR_determ_time[stopID][0][1]).total_seconds()) <= delay:
                                    daily_results[record_date]["missed"].add(
                                        tripID)
                            else:
                                if arr_dely_compare >= FR_determ_time[stopID][i+1][1]:
                                    daily_results[record_date]["missed"].add(
                                        tripID)
            elif tripID in SA_trips and stopID == Schedule_stops[tripID][-1]:
                if tripID == SA_last[stopID]:
                    if delay >= 15*60:
                        daily_results[record_date]["missed"].add(tripID)
                else:
                    length = len(SA_determ_time[stopID])
                    for i in range(length):
                        if SA_determ_time[stopID][i][0] == tripID:
                            if i == length-1:
                                if abs(24*60*60 - (arr_dely_compare - SA_determ_time[stopID][0][1]).total_seconds()) <= delay:
                                    daily_results[record_date]["missed"].add(
                                        tripID)
                            else:
                                if arr_dely_compare >= SA_determ_time[stopID][i+1][1]:
                                    daily_results[record_date]["missed"].add(
                                        tripID)
            elif stopID in SU_determ_time and stopID == Schedule_stops[tripID][-1]:
                if tripID == SU_last[stopID]:
                    if delay >= 15*60:
                        daily_results[record_date]["missed"].add(
                            tripID)
                else:
                    length = len(SU_determ_time[stopID])
                    for i in range(length):
                        if SU_determ_time[stopID][i][0] == tripID:
                            if i == length-1:
                                if abs(24*60*60 - (arr_dely_compare - SU_determ_time[stopID][0][1]).total_seconds()) <= delay:
                                    daily_results[record_date]["missed"].add(
                                        tripID)
                            else:
                                if arr_dely_compare >= SU_determ_time[stopID][i+1][1]:
                                    daily_results[record_date]["missed"].add(
                                        tripID)

            if sequence != '1' and stopID == '8120' or stopID == '8121' or stopID == '8110' or stopID == '8111':
                if tripID in WD_trips:
                # if this trip is the last one of the day
                    if tripID == WD_last[stopID]:
                        if delay >= 15*60:
                            daily_results[record_date]["missed"].add(tripID)
                    else:
                        length = len(WD_determ_time[stopID])
                        for i in range(length):
                            if WD_determ_time[stopID][i][0] == tripID:
                                if i == length-1:
                                    if abs(24*60*60 - (arr_dely_compare - WD_determ_time[stopID][0][1]).total_seconds()) <= delay:
                                        daily_results[record_date]["missed"].add(
                                            tripID)
                                else:
                                    if arr_dely_compare >= WD_determ_time[stopID][i+1][1]:
                                        daily_results[record_date]["missed"].add(
                                            tripID)
                elif tripID in FR_trips:
                    if tripID == FR_last[stopID]:
                        if delay >= 15*60:
                            daily_results[record_date]["missed"].add(tripID)
                    else:
                        length = len(FR_determ_time[stopID])
                        for i in range(length):
                            if FR_determ_time[stopID][i][0] == tripID:
                                if i == length-1:
                                    if abs(24*60*60 - (arr_dely_compare - FR_determ_time[stopID][0][1]).total_seconds()) <= delay:
                                        daily_results[record_date]["missed"].add(
                                            tripID)
                                else:
                                    if arr_dely_compare >= FR_determ_time[stopID][i+1][1]:
                                        daily_results[record_date]["missed"].add(
                                            tripID)
                elif tripID in SA_trips:
                    if tripID == SA_last[stopID]:
                        if delay >= 15*60:
                            daily_results[record_date]["missed"].add(tripID)
                    else:
                        length = len(SA_determ_time[stopID])
                        for i in range(length):
                            if SA_determ_time[stopID][i][0] == tripID:
                                if i == length-1:
                                    if abs(24*60*60 - (arr_dely_compare - SA_determ_time[stopID][0][1]).total_seconds()) <= delay:
                                        daily_results[record_date]["missed"].add(
                                            tripID)
                                else:
                                    if arr_dely_compare >= SA_determ_time[stopID][i+1][1]:
                                        daily_results[record_date]["missed"].add(
                                            tripID)
                else:
                    if tripID == SU_last[stopID]:
                        if delay >= 15*60:
                            daily_results[record_date]["missed"].add(
                                tripID)
                    else:
                        length = len(SU_determ_time[stopID])
                        for i in range(length):
                            if SU_determ_time[stopID][i][0] == tripID:
                                if i == length-1:
                                    if abs(24*60*60 - (arr_dely_compare - SU_determ_time[stopID][0][1]).total_seconds()) <= delay:
                                        daily_results[record_date]["missed"].add(
                                            tripID)
                                else:
                                    if arr_dely_compare >= SU_determ_time[stopID][i+1][1]:
                                        daily_results[record_date]["missed"].add(
                                            tripID)
historicalfile.close

for k in arr_at_stops:
    for tid in arr_at_stops[k]:
        if tid not in daily_results[k]['missed']:
            daily_results[k]['completed'].add(tid)
        daily_results[k]['arrivals'] += len(arr_at_stops[k][tid])-1
        if tid in daily_results[k]['completed']:
            for sp in arr_at_stops[k][tid]:
                if sp == Schedule_stops[tid][0]:
                    daily_results[k]['dep_at_determ'] += 1
                elif sp == Schedule_stops[tid][-1]:
                    daily_results[k]['arrival_at_determ'] += 1
                elif sp in measurings:
                    daily_results[k]['dep_at_determ'] += 1
                    daily_results[k]['arrival_at_determ'] += 1
    # re-add no_record trips into daily_results
    if datetime.strptime(k, '%m/%d/%Y').weekday() < 4:
        for sche_strip in WD_trips:
            if sche_strip not in arr_at_stops[k]:
                daily_results[k]['no_record'].append(sche_strip)
    elif datetime.strptime(k, '%m/%d/%Y').weekday() == 4:
        for sche_strip in FR_trips:
            if sche_strip not in arr_at_stops[k]:
                daily_results[k]['no_record'].append(sche_strip)
    elif datetime.strptime(k, '%m/%d/%Y').weekday() == 5:
        for sche_strip in SA_trips:
            if sche_strip not in arr_at_stops[k]:
                daily_results[k]['no_record'].append(sche_strip)
    else:
        for sche_strip in SU_trips:
            if sche_strip not in arr_at_stops[k]:
                daily_results[k]['no_record'].append(sche_strip)

for dt in arr_at_stops:
    for tid in arr_at_stops[dt]:
        for st in Schedule_stops[tid]:
            if st not in arr_at_stops[dt][tid]:
                if st == Schedule_stops[tid][-1]:
                    daily_results[dt]["partial"].add(tid) 
                elif st == Schedule_stops[tid][0]:
                    daily_results[dt]["data_lost"].append((tid, st))
                else:
                    for s in measurings:
                        if s !='8115' and s!='8114' and s in arr_at_stops[dt][tid]:
                            daily_results[dt]["data_lost"].append((tid, st))
                            break
                    else:
                        daily_results[dt]["partial"].add(tid)

# there are some trips have no records: count them as lost and re-add to daily_results
for k in daily_results:
    daily_results[k]['arrivals'] += len(daily_results[k]['data_lost'])
    # re-add lost-data into 'arrivals' and 'arr_determ' and 'deptature_determ'
    for tup in daily_results[k]['data_lost']:
        if tup[1]!= Schedule_stops[tup[0]][0] and tup[0] in daily_results[k]['completed'] and tup[1] in measurings:
            daily_results[k]['arrival_at_determ'] += 1
            daily_results[k]['dep_at_determ'] += 1

# to calculate late_arrivals and early_departures
with open(historicalfilename, "r") as forearlyandlate:
    # column name for file:
    # 0:tripId 1:stopSequence 2:arrivalDelay 3:arrivalTime 4:depatureDelay 5:depatureTime 6:stopID 7:timestamp
    has_header = csv.Sniffer().has_header(forearlyandlate.read())
    forearlyandlate.seek(0)  # Rewind.
    reader = csv.reader(forearlyandlate)
    if has_header:
        next(reader)
    for entry in reader:
        # try:
        #     arrival_time = datetime.strptime(
        #         entry[3][0:19], '%Y-%m-%dT%H:%M:%S')
        #     depature_time = datetime.strptime(
        #         entry[5][0:19], '%Y-%m-%dT%H:%M:%S')
        #     timestamp = datetime.strptime(entry[7][0:19], '%Y-%m-%dT%H:%M:%S')
        # except ValueError:
        arrival_time = datetime.strptime(entry[3], '%m/%d/%Y %I:%M:%S %p')
        depature_time = datetime.strptime(entry[5], '%m/%d/%Y %I:%M:%S %p')
        timestamp = datetime.strptime(entry[7], '%m/%d/%Y %I:%M:%S %p')
        # check this record is valid (not prediction, acutally happened situation)
        # and timestamp > start_date and timestamp < end_date
        if arrival_time < timestamp and depature_time < timestamp and (datetime.strptime(entry[7][11:], '%I:%M:%S %p') > datetime.strptime("05:00:00", '%H:%M:%S') or datetime.strptime(entry[7][11:], '%I:%M:%S %p') < datetime.strptime("03:30:00", '%H:%M:%S')):
            # chech timestamp is between 00:00:00 - 03:00:00
            midnight = datetime.strptime(entry[7][11:], '%I:%M:%S %p')
            if datetime.strptime("05:00:00", '%H:%M:%S') > midnight and midnight > datetime.strptime("00:00:00", '%H:%M:%S'):
                # date - 1 day
                record_date = datetime.strftime(
                    timestamp + timedelta(days=-1), '%m/%d/%Y')
            else:
                # keep original date
                record_date = entry[7][0:10]
                # try:
                #     record_date = datetime.strptime(
                #         record_date, '%m/%d/%Y').strftime('%Y-%m-%d')
                # except ValueError:
                #     pass

            tripID = entry[0]
            stopID = entry[6]
            sequence = entry[1]

            if "," in entry[2]:
                arr_delay = int(entry[2].replace(",", ""))
            else:
                arr_delay = int(entry[2])
            if "," in entry[4]:
                dep_delay = int(entry[4].replace(",", ""))
            else:
                dep_delay = int(entry[4])

            # early departure: 30 seconds early for measuring stops( start, terminating, EPIC, Well-station)
            if dep_delay < -120 and tripID in daily_results[record_date]["completed"] and stopID in measurings and stopID != Schedule_stops[tripID][-1]:
                daily_results[record_date]["early"].append((tripID, stopID))
            # late arrival: completed servive arrived late over 120s at measuring stops
            if arr_delay > 90 and tripID in daily_results[record_date]["completed"] and stopID in measurings and sequence != '1':
                daily_results[record_date]["late"].append((tripID, stopID))
forearlyandlate.close

fortable = {}
missed_record = {}


def calculate_monthly_index(start, end):
    result = {"AOTRA": 0, "PSA": 0, "ESA": 0, "LSA": 0, "MA": 0, "CS": 0, "MHS": 0,
               "PCSR": 0, "TPS": 0, "SE": 0, "LSR": 0, "SL": 0, "SS": 0, "SC": 0}
    month = start.strftime('%B')
    fortable[month] = result
    missed_record[month] = set()
    d = datetime(start.year, start.month, start.day)
    while d < end:
        k = d.strftime('%m/%d/%Y')
        if k in daily_results:
            missed_record[month] = missed_record[month].union(set([(k, v) for v in daily_results[k]['missed']]))
            result["CS"] += len(daily_results[k]["completed"])
            result["MHS"] += len(daily_results[k]["missed"])
            result["SE"] += len(daily_results[k]["early"])
            result["SL"] += len(daily_results[k]["late"])
            if d.weekday() < 4:
                result["SS"] += (daily_results[k]["dep_at_determ"]-len(WD_trips))
                result["SC"] += (daily_results[k]
                                    ["arrival_at_determ"]-len(WD_trips))
                result["TPS"] += len(WD_trips)
                result["PCSR"] += (daily_results[k]["arrivals"]+0.0) / \
                    (Schedule_num_arrivals["WD"])*0.7*len(daily_results[k]["partial"])
            elif d.weekday() == 4:
                result["SS"] += (daily_results[k]["dep_at_determ"]-len(FR_trips))
                result["SC"] += (daily_results[k]
                                    ["arrival_at_determ"]-len(FR_trips))
                result["TPS"] += len(FR_trips)
                result["PCSR"] += (daily_results[k]["arrivals"]+0.0) / \
                    (Schedule_num_arrivals["FR"])*0.7*len(daily_results[k]["partial"])
            elif d.weekday() == 5:
                result["SS"] += (daily_results[k]["dep_at_determ"]-len(SA_trips))
                result["SC"] += (daily_results[k]
                                    ["arrival_at_determ"]-len(SA_trips))
                result["TPS"] += len(SA_trips)
                result["PCSR"] += (daily_results[k]["arrivals"]+0.0) / \
                    (Schedule_num_arrivals["SA"])*0.7*len(daily_results[k]["partial"])
            else:
                result["SS"] += (daily_results[k]["dep_at_determ"]-len(SU_trips))
                result["SC"] += (daily_results[k]
                                    ["arrival_at_determ"]-len(SU_trips))
                result["TPS"] += len(SU_trips)
                result["PCSR"] += (daily_results[k]["arrivals"]+0.0) / \
                    (Schedule_num_arrivals["SU"])*0.7*len(daily_results[k]["partial"])
        d += timedelta(days=1)

    result['ESA'] = (result['SE']+0.0)/result['SS']
    result['LSR'] = (result['SL']+0.0)/result['SC']
    result['LSA'] = (
        1-min(0.98, (1-result['LSR']))/0.98)*0.35
    result['MA'] = (result['CS']+(result['MHS']
                                            * 0.7)+result['PCSR']) / result['TPS']
    result['PSA'] = min(0.995, result['MA']) / 0.995
    result['AOTRA'] = result['PSA']-result['ESA']-result['LSA']

month_list = sorted(list(year_months), key = lambda x: x[1])
for m in month_list:
    calculate_monthly_index(datetime(m[0], m[1], 1), datetime(m[0], m[1]+1, 1))

def generate_complete(start, end):
    month = start.month
    with open(f'output/{month}_trips_analysis.csv', 'w') as tripsfile:
        heads = ['date', 'complete_trips', 'missed_trips', 'partial_trips', 'no_record_trips']
        writer = csv.DictWriter(tripsfile, fieldnames=heads)
        writer.writeheader()
        d = datetime(start.year, start.month, start.day)
        while d < end:
            k = d.strftime('%m/%d/%Y')
            if k in daily_results:
                writer.writerow({'date': k[:5], 'complete_trips':len(daily_results[k]['completed']), 'missed_trips':len(daily_results[k]['missed']), 'partial_trips':len(daily_results[k]['partial']), 'no_record_trips':len(daily_results[k]['no_record'])})
            else:
                writer.writerow({'date': k[:5], 'complete_trips':0, 'missed_trips':0, 'partial_trips':0, 'no_record_trips':0})
            d += timedelta(days=1)
    tripsfile.close
    with open(f'output/{month}_arrival_analysis.csv', 'w') as arrfile:
        heads = ['date', 'data_lost', 'arrivals', 'schedule_arrival']
        writer = csv.DictWriter(arrfile, fieldnames=heads)
        writer.writeheader()
        d = datetime(start.year, start.month, start.day)
        while d < end:
            k = d.strftime('%m/%d/%Y')
            if d.weekday() < 4:
                if k in daily_results:
                    writer.writerow({'date': k[:5], 'data_lost': Schedule_num_arrivals['WD']-daily_results[k]['arrivals'], 'arrivals':daily_results[k]['arrivals'], 'schedule_arrival':Schedule_num_arrivals['WD']})
                else:
                    writer.writerow({'date': k[:5], 'data_lost':0, 'arrivals':0, 'schedule_arrival':0})
            elif d.weekday() == 4:
                if k in daily_results:
                    writer.writerow({'date': k[:5], 'data_lost': Schedule_num_arrivals['FR']-daily_results[k]['arrivals'], 'arrivals':daily_results[k]['arrivals'], 'schedule_arrival':Schedule_num_arrivals['FR']})
                else:
                    writer.writerow({'date': k[:5], 'data_lost':0, 'arrivals':0, 'schedule_arrival':0})
            elif d.weekday()== 5:
                if k in daily_results:
                    writer.writerow({'date': k[:5], 'data_lost': Schedule_num_arrivals['SA']-daily_results[k]['arrivals'], 'arrivals':daily_results[k]['arrivals'], 'schedule_arrival':Schedule_num_arrivals['SA']})
                else:
                    writer.writerow({'date': k[:5], 'data_lost':0, 'arrivals':0, 'schedule_arrival':0})
            else:
                if k in daily_results:
                    writer.writerow({'date': k[:5], 'data_lost': Schedule_num_arrivals['SU']-daily_results[k]['arrivals'], 'arrivals':daily_results[k]['arrivals'], 'schedule_arrival':Schedule_num_arrivals['SU']})
                else:
                    writer.writerow({'date': k[:5], 'data_lost':0, 'arrivals':0, 'schedule_arrival':0})
            d += timedelta(days=1)
    arrfile.close
    
for m in month_list:
    generate_complete(datetime(m[0], m[1], 1), datetime(m[0], m[1]+1, 1))

for m in missed_record:
    st = ''
    for tri in missed_record[m]:
        st = st + ', ' + tri[0][0:5]+': '+tri[1]
    missed_record[m] = st

formonthindex = {'months':month_list}
with open(f'output/months_index.json', 'w') as monthindex:
    json.dump(formonthindex, monthindex)
monthindex.close

with open(f'output/missed_results.json', 'w') as missedfile:
    json.dump(missed_record, missedfile)
missedfile.close

with open(f'output/payment_results.csv', 'w') as paymentcsv:
        heads = ["Month", "AOTRA", "PSA", "ESA", "LSA", "MA", "CS", "MHS",
                    "PCSR", "TPS", "SE", "LSR", "SL", "SS", "SC"]
        names = [datetime(m[0],m[1],1).strftime('%B') for m in month_list]
        writer = csv.DictWriter(paymentcsv, fieldnames=heads)
        writer.writeheader()
        for t in names:
            writer.writerow({"Month":t, "AOTRA":fortable[t]["AOTRA"], "PSA":fortable[t]["PSA"], "ESA":fortable[t]["ESA"], "LSA":fortable[t]["LSA"], "MA":fortable[t]["MA"], "CS":fortable[t]["CS"], "MHS":fortable[t]["MHS"],
                    "PCSR":fortable[t]["PCSR"], "TPS":fortable[t]["TPS"], "SE":fortable[t]["SE"], "LSR":fortable[t]["LSR"], "SL":fortable[t]["SL"], "SS":fortable[t]["SS"], "SC":fortable[t]["SC"]})
paymentcsv.close