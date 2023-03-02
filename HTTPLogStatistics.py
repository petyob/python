# Parses Apache HTTP server access.log file to produce some statistics: 1.Top 10 requested urls sorted by hits. 2.Top 10 visitors by ip sorted by hits. 3.Total hits per month sorted by month. 4. Unique visits (by ip) per month. 5. Top 10 ips barchart per month.
# Author: Petyo Byankov

# RUN: python3 HTTPLogAnalyzer.py access.log
import argparse
parser = argparse.ArgumentParser(description='Produce some statistics from a http log file')
parser.add_argument(dest='filename', metavar='filename', nargs='*')
parser.add_argument('-v', dest='verbose', help='Verbose mode')
parser.add_argument('-o', dest='op', help='Options')
args = parser.parse_args()
if args.filename:
        log_file = args.filename[0]
else:
        log_file = 'access.log'



# data structures
requsted_uri = dict()  # number of requests per URL
visitors = dict()  # number of visits per IP
months_hits = dict()  # number of hits per month
months_ip_set = set()  # collect unique combination month+IP
months_hits_unique = dict()  # number of unique visits (by ip) per month
month_summary = dict()  # will held dictionaries with counters

with open(log_file) as logfile:  # Default buffering for text files is line buffering- should be OK for large files.
    for line in logfile:
        try:
            items = line.split(" ")  # split parts of the line into a list
            visitor_ip = items[0]
            month = items[3][4:12]
            uri = items[6]

            if visitor_ip not in visitors:  # create a new entry or increment existing
                visitors[visitor_ip] = 1
            else:
                visitors[visitor_ip] += 1

            if month not in months_hits:
                months_hits[month] = 1
            else:
                months_hits[month] += 1

            month_ip = month + visitor_ip  # represent unique combination month+IP
            if month_ip not in months_ip_set:
                months_ip_set.add(month_ip)
                if month not in months_hits_unique:
                    months_hits_unique[month] = 1
                else:
                    months_hits_unique[month] += 1

            if uri not in requsted_uri:
                requsted_uri[uri] = 1
            else:
                requsted_uri[uri] += 1

            if month not in month_summary:
                month_summary[month] = dict()
            if visitor_ip not in month_summary[month]:
                month_summary[month][visitor_ip] = 1
            else:
                month_summary[month][visitor_ip] += 1

        except Exception:
            print("Error parsing line: ", line)


def pick_top(count, items):    # pick top biggest value from a dictionary
    hosts_sorted = sorted(items, key=lambda x: items[x])
    return reversed(hosts_sorted[-count:])


def print_report():
    print("\n1.Top 10 requested urls sorted by hits:\n\"hits: uri:\"")
    for i in pick_top(10, requsted_uri):
        print('{:<10} {}'.format(requsted_uri[i], i))

    print("\n2.Top 10 visitors by ip sorted by hits:\n\"hits:  ip:\"")
    for i in pick_top(10, visitors):
        print('{:<10} {}'.format(visitors[i], i))

    print("\n3.Total hits per month sorted by month:")
    for i in months_hits:
        print(i.replace("/", " "), "hits count -", months_hits[i])

    print("\n4. Unique visits (by ip) per month")
    for i in months_hits_unique:
        print(i.replace("/", " "), "unique visits - ", months_hits_unique[i])

    print("\n5. Top 10 ips barchart per month")
    max_value = 0  # find maximum value of all
    for mon in month_summary:
        for ip in pick_top(1, month_summary[mon]):
            max_value = max(month_summary[mon][ip], max_value)

    for mon in month_summary:
        print(mon.replace("/", " "))
        for ip in pick_top(10, month_summary[mon]):
            current_value = month_summary[mon][ip]
            length_of_bar = round(current_value/max_value*300) or 1  # Length of the current bar chart
            # Longest bar chart will be 300 and others are proportional(but at least 1 !!)
            print('{:<10} {:<15} {} '.format(current_value, ip, "#" * length_of_bar))


print_report()


