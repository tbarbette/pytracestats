# pytracestats
A simple python script to plot the bandwidth of some huge traces

# example
![example plot](https://github.com/tbarbette/pytracestats/raw/master/bw_rxtx.svg)

# usage
```
usage: Generate interactive SVG displaying the bandwidth of one or multiple PCAP files
       [-h] [--interval INTERVAL] [--stop-after STOP] [--output OUTPUT]
       [--labels [LABELS [LABELS ...]]]
       filename [filename ...]

positional arguments:
  filename              Name(s) of the PCAP files to parse.

optional arguments:
  -h, --help            show this help message and exit
  --interval INTERVAL   Interval to compute the bandwidth upon. Defaults to
                        0.1 seconds.
  --stop-after STOP     Stop after a certain amount of seconds.
  --output OUTPUT       Output filename. Defaults to the name of the last
                        input PCAP file, changing the extension by SVG.
  --labels [LABELS [LABELS ...]]
                        Labels for the traces. As many as given traces. By
                        default, the labels will be the trace name without the
                        common prefix.
```
