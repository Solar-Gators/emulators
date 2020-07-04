import importlib
from Message import Message
class point():
    def __init__(self, lat, lng):
        self.lat = lat
        self.lng = lng

    def print(self):
        print(self.lat)
        print(self.lng)

class GPS(Message):
    def __init__(self, addr_CAN, addr_telem, pathToData):
        self.file = open(pathToData, "r")
        self.addr_CAN = addr_CAN
        self.addr_telem = addr_telem
        self.data = []
        self.i = 0
        self.__processFile()
    def __processFile(self):
        for line in self.file:
            temp = line.split(',')
            try:
                self.data.append(point(float(temp[0]), float(temp[1])))
            except:
                pass
    def print(self):
        for data in self.data:
            data.print()
    def toCharArray(self):
        r = []
        p = self.data[self.i]
        lat = int(p.lat * 10000)
        lng = int(p.lng * 10000)
        r.append(lat & 0xFF)
        r.append((lat >> 8) & 0xFF)
        r.append(lng & 0xFF)
        r.append((lng >> 8) & 0xFF)
        self.i = self.i + 1
        if(self.i >= len(self.data)):
            self.i = 0
        return r
    def toPitRFDmsg(self):
        temp = self.toCharArray()
        temp.insert(0, self.addr_telem)
        temp.insert(1, len(temp)-1)
        return temp


if __name__ == "__main__":
    dataPath = "Support/GPS_7-4-2020.csv"
    data = GPS(0xff, 0x00, dataPath)
    print(data.toPitRFDmsg())