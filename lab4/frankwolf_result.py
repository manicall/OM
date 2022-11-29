class FullResult:
    def __init__(self):
        self.result = []
        
    def appendResult(self, result):
        self.result.append(result)
        
    def getAll(self):
        return self.result
    
    def getLastResult(self):
        return self.result[-1]
    
    def getLen(self):
        return len(self.result)
    
class Result:
    def __init__(self, X, C, Z, L, f):
        self.X = X
        self.C = C
        self.Z = Z
        self.L = L
        self.f = f
        
    def getX(self):
        x1, x2 = self.X.getCoord()
        return f"({x1}, {x2})"
    
    def getC(self):
        c1, c2 = self.C
        return f"({c1}, {c2})"
    
    def getZ(self):
        z1, z2 = self.Z.getCoord()
        return f"({z1}, {z2})"
    
    def getNewX(self):
        x1, x2 = self.newX.getCoord()
        return f"({x1}, {x2})"