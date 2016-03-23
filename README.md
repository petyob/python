Python script parses TCP dump file to produce a plain text report containing
the following information:

  * Top 10 servers receiving the most packets
    Showing the amount of packets received by each
  * Percentage of "small packets" (maximum 512 bytes)
  * Percentage of "large packets" (over 512 bytes)
  * Top 10 clients sending the most bytes
    Showing the IP address and the number of bytes sent
  * Option parsing to produce only selected statistics
    (eg. only show top 10 servers)

The input files will only contain IPv4 addresses. The clients are only sending
packets and the servers are only receiving them. The client will always appear
on the left side of the ">". Both the addresses and the ports will appear in
numeric representation.


1. To see usage:
python test.py -h 

2. Default - use the file 'tcpdump.log' in current dir. run:
python test.py

2.1 Select a file using command line:
python test.py <filename>

3.  Produce statistics only for clients:
python test.py -o clients

4.  Other cases are similar:

python test.py -o servers 
python test.py -o small
python test.py -o large

5. To run Unit tests - only uncomment the line:

#unittest.main()



