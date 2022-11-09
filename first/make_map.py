import csv

class map_for_robot:

    def __init__(self):
        self.mapfile = open('arena.csv','w', newline='')
        self.csvwriter = csv.writer(self.mapfile)

    def make_map(self,h=150,w=300):
        # map with outline
        for i in range(h):
            mapline = []
            if i == 0 or i == h-1:
                for j in range(w):
                    mapline.append(0)
            else:
                for j in range(w):
                    if j == 0 or j == w-1:
                        mapline.append(0)
                    else:
                        mapline.append(1)
            self.csvwriter.writerow(mapline)
        self.mapfile.close()

    def make_clean_map(self,h=150,w=300):
        # map with no outline
        for i in range(h):
            mapline = []
            for j in range(w):
                mapline.append(1)
            self.csvwriter.writerow(mapline)
        self.mapfile.close()