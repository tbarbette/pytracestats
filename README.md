# pytracestats
A simple python script to plot the bandwidth of some huge traces

# usage
```
usage: Generate interactive SVG displaying the bandwidth of one or multiple PCAP files
       [-h] [--interval INTERVAL] [--stop-after STOP] [--output OUTPUT]
       filename [filename ...]

positional arguments:
  filename             Name(s) of the PCAP files to parse.

optional arguments:
  -h, --help           show this help message and exit
  --interval INTERVAL  Interval to compute the bandwidth upon. Defaults to 0.1
                       seconds.
  --stop-after STOP    Stop after a certain amount of seconds.
  --output OUTPUT      Output filename. Defaults to the name of the last input
                       PCAP file, changing the extension by SVG.
```
