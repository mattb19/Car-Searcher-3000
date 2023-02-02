class Car:
    def __init__(self, price, name, mileage, distance, website) -> None:
        self._id = price+name+mileage
        self._price = price
        self._name = name
        self._mileage = mileage
        self._distance = distance
        self._website = website

    def getId(self):
        return self._id
    
    def setId(self, id):
        self._id = id
    
    def setPrice(self, value):
        self._price = value
        
    def getPrice(self):
        return self._price
    
    def setPrice(self, value):
        self._price = value
        
    def getName(self):
        return self._name
    
    def setName(self, value):
        self._name = value
        
    def getMileage(self):
        return self._mileage
    
    def setMileage(self, value):
        self._mileage = value
        
    def getDistance(self):
        return float(self._distance)
    
    def setDistance(self, value):
        self._distance = value
        
    def getWebsite(self):
        return self._website
    
    def setWebsite(self, value):
        self._website = value
    
    def __str__(self):
        return "Name:      "+self._name+"\nPrice:     "+self._price+"\nMileage:   "+self._mileage+"\n"

    def __repr__(self):
        return "Name:      "+self._name+"\nPrice:     "+self._price+"\nMileage:   "+self._mileage+"\n"
