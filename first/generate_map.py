import csv

def making_map():
    mapfile = open('arena.csv','w', newline='')
    writemap = csv.writer(mapfile)
    for i in range(150):
        mapline = []
        if i == 0 or i == 149:
            for j in range(300):
                mapline.append(0)
        else:
            for j in range(300):
                if j == 0 or j == 299:
                    mapline.append(0)
                else:
                    mapline.append(1)
        writemap.writerow(mapline)
    mapfile.close()