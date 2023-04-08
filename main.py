# Read SVG into a list of path objects and list of dictionaries of attributes 
from svgpathtools import svg2paths, wsvg, Path, Line
from numpy import angle, pi
paths, attributes = svg2paths('einstein hat2.svg')

lines = {}

def add_line(p1, p2):
    if p1 in lines:
        lines[p1].append(p2)
    else:
        lines[p1] = [p2]

def collinear_and_smaller(p1, p2, points):
    for p in points:
        if p != p1 and p != p2 and abs(p2 - p1) < abs(p - p1):
            if (abs(angle(p2 - p1) - angle(p - p1)) < 0.001 or
                abs(angle(p2 - p1) - angle(p - p1)) > pi * 2 - 0.001):
                return True
    return False

for path in paths:
    for line in path:
        add_line(line[0], line[1])
        add_line(line[1], line[0])

unique_lines = {}

for start in lines:
    for end in lines[start]:
        if (not (start, end) in unique_lines and
            not (end, start) in unique_lines and
            not collinear_and_smaller(start, end, lines[start]) and
            not collinear_and_smaller(end, start, lines[end])):
            unique_lines[(start, end)] = True

output_lines = []
for line in unique_lines:
    output_lines.append(Line(line[0], line[1]))

wsvg(output_lines, filename='no_duplicate_lines.svg')


#for line in unique_lines:
#    print(Path(line).d())
