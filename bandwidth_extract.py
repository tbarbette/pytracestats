#!/usr/bin/env python3
import pygal
import os
from datetime import datetime
from scapy.all import PcapReader
import argparse
from tqdm import tqdm

def main():
    parser = argparse.ArgumentParser("Generate interactive SVG displaying the bandwidth of one or multiple PCAP files")
    parser.add_argument("filename",default=["dump.pcap"], nargs='+', help="Name(s) of the PCAP files to parse.")
    parser.add_argument("--interval",type=float,default=0.1,help="Interval to compute the bandwidth upon. Defaults to 0.1 seconds.")
    parser.add_argument("--stop-after",dest='stop',type=float,default=None,help="Stop after a certain amount of seconds.")
    parser.add_argument("--output",type=str,default=None,help="Output filename. Defaults to the name of the last input PCAP file, changing the extension by SVG.")
    parser.add_argument("--labels",type=str,default=[],nargs='*',help="Labels for the traces. As many as given traces. By default, the labels will be the trace name without the common prefix.")
    args = parser.parse_args()

    if args.labels:
        if len(args.labels) != len(args.filename):
            print("ERROR: You must be as many labels as filenames, or no labels")
            sys.exit(1)

    #Manipulate filenames to have meaning full display names
    common = os.path.commonprefix(args.filename)
    if min([len(filename[len(common):]) for filename in args.filename]) == 0:
        common = os.path.commonpath(args.filename)

    chart = pygal.XY(stroke=True, interpolate='hermite', y_title="Bandwidth (Gbits/s)", x_title="Time (s)")
    for ifile,filename in enumerate(args.filename):
        trace = PcapReader(filename)

        if args.labels:
            cname = args.labels[ifile]
        else:
            cname = filename[len(common):].strip(os.path.sep)
        print("Processing %s..." % cname)

        npackets = 0
        last = 0
        tot = 0
        n = 0
        first_time = None
        last_time = None

        bw = []

        with tqdm(total=os.stat(filename).st_size if not args.stop else args.stop, desc="Reading trace...", bar_format="{l_bar}{bar} [ time left: {remaining} ]", dynamic_ncols=True) as pbar:
          for packet in trace:
              try:
                pos = trace.f.tell()
                last = pos
                npackets += 1

                ptime = packet.time
                tot += packet.len
                n += 1

                if first_time is None:
                    first_time = ptime
                    last_time = ptime

                elapsed = ptime - first_time
                pbar.n = pos if not args.stop else elapsed

                if npackets % 1000 == 1:
                    pbar.refresh()

                if args.stop and elapsed > args.stop:
                    break

                if ptime - last_time > args.interval:
                    t = ptime-first_time - (args.interval / 2)
                    b = (tot + 24*n)*8 / (ptime-last_time)
                    bw.append([t,b])
                    #print("T-%.02f-RESULT-THROUGHPUT %f" % (t,b))
                    last_time = ptime
                    tot = 0
                    n = 0
              except Exception as e:
                print("WARNING: Packet ignored")
        chart.add(cname, [(t,b / 1000000000) for t,b in bw])
        #chart.x_labels = [t for t,b in bw]


    chart.render_to_file(args.output if args.output else 'bandwidth-'+os.path.splitext(os.path.basename(filename))[0]+'.svg')

if __name__== "__main__":
      main()


