from .Message import Message

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
        super().__init__(addr_CAN, addr_telem)
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
    def __DDtoDDM(self, lat, lng):
        deg_lat = int(lat)
        deg_lng = int(lng)
        min_lat = (lat - deg_lat)*60
        min_lng = (lng - deg_lng)*60
        str_lat = str(deg_lat)+str(min_lat)
        str_lng = str(deg_lng)+str(min_lng)
        return str_lat, str_lng
    # return array of ascii
    def __toAsciiArr(self, lat, lng):
        r = []
        str_lat, str_lng = self.__DDtoDDM(abs(lat), abs(lng))
        for ele in str_lat: 
            r.append(ord(ele))
        if(lat < 0):
            r.append(ord("S"))
        else:
            r.append(ord("N"))
        r.append(ord(","))
        
        for ele in str_lng:
            r.append(ord(ele))
        if(lng < 0):
            r.append(ord("W"))
        else:
            r.append(ord("E"))
        r.append(ord(","))
        # send speed
        speed = "10.00"
        for ele in speed:
            r.append(ord(ele))
        r.append(ord(","))
        # send Heading
        heading = "90.00"
        for ele in heading:
            r.append(ord(ele))
        return r
        
    def toCharArray(self):
        r = []
        p = self.data[self.i]
        # convert from decimal degress to DMS
        r = self.__toAsciiArr(p.lat, p.lng)
        self.i = self.i + 1
        if(self.i >= len(self.data)):
            self.i = 0
        return r


if __name__ == "__main__":
    dataPath = "Support/GPS_7-4-2020.csv"
    data = GPS(0xff, 0x00, dataPath)
    print(data.toPitRFDmsg())