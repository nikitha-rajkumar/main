import os

output = r"D:
ikitha-portfoliouild_html.py"

# Read original to get the HTML template parts that are tricky to escape
# Instead, we build the whole file from scratch

with open(output, "w", encoding="utf-8") as f:
    f.write(open(r"D:
ikitha-portfolio\_part1.txt", encoding="utf-8").read())
    f.write(open(r"D:
ikitha-portfolio\_part2.txt", encoding="utf-8").read())
    f.write(open(r"D:
ikitha-portfolio\_part3.txt", encoding="utf-8").read())

print("Done")