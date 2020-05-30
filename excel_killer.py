import os
import argparse
import re

def draw_histogram(serie, title):
    from math import floor, ceil
    from statistics import mean, stdev
    import matplotlib.pyplot as plt #Did you forget to pip3 install me?

    min_value = floor(min(serie))
    max_value = ceil(max(serie))
    num_data_pt = len(serie) + 1
    avg_value = mean(serie)
    std_dev = stdev(serie)
    pos_y = (max_value + avg_value) / 2

    left = [x for x in range(len(serie))]
    bottom = [min_value for x in range(len(serie))]
    modified_serie = [x-min_value for x in serie]
    plt.bar(left, modified_serie, bottom=bottom)
    plt.axhline(avg_value, color='red')
    plt.text(num_data_pt/2, pos_y, f'Avg: {avg_value:.2f}\n\N{GREEK SMALL LETTER SIGMA}: {std_dev:.2f}', color='red')
    plt.title(title)
    plt.show()


parser = argparse.ArgumentParser(description="""Calculate average/median/deviation from speedtest_cli output.
By default generates a graph, with -x option will output csv file""")

parser.add_argument("-x", "--keep_excel", help="Output will be a csv file", action="store_true")
parser.add_argument("-p", "--path", help="Path to speedtest-cli output. Defaults to .")
parser.add_argument("-n", "--name", help="Radical of the name of the speedtest-cli output files. Defaults to speedtest")

args = parser.parse_args()

if args.path:
    PATH = args.path
else:
    PATH = os.curdir

if args.name:
    RADICAL = args.name
else:
    RADICAL = "speedtest"

prog = re.compile(RADICAL)

download_speed = []
upload_speed = []

for file in os.listdir(PATH):
    if re.match(prog, file):
        with open(f"{PATH}/{file}", "r") as f:
            content = f.readlines()
            for line in content:
                line_split = line.split()
                if "Download:" == line_split[0]:
                    download_speed.append(float(line_split[1]))
                if "Upload:" == line_split[0]:
                    upload_speed.append(float(line_split[1]))


if args.keep_excel:
    output = ["datapoint;Download Speed;Upload Speed"]
    for index in range(len(download_speed)):
        assert len(download_speed) == len(upload_speed), 'data error: Not the same number of Download vs Upload speeds'
        output.append(";".join((str(index), str(download_speed[index]), str(upload_speed[index]))))
    print("\n".join(output))
else:
    draw_histogram(download_speed, "Download Speed Diagram")
    draw_histogram(upload_speed, "Upload Speed Diagram")



