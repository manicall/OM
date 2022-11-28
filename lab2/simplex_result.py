import numpy as np

class Result:
    def __init__(self, b, cb, p):
        self.b = b
        self.cb = cb
        self.p = p
        
    def getRow(self, i):
        if i >= 0:
            if i < len(self.cb):
                return [self.b[i], self.cb[i], *self.p[i]]
            elif i < len(self.p):
                return [None, None, *self.p[i]]
            
    def getRowLen(self):
        return len(self.p)
    
    def getColLen(self):
        return len(self.getRow(0))
        
    def getResult(self):                    
        F = float(self.p[-1][0])
        
        maxLen = len(self.p[0]) - 1
        X = np.zeros(maxLen)
        for i in range(len(self.b)):
            X[int(self.b[i][1:]) - 1] = float(self.p[i][0])
            
        return FX(F, X)

class FX:
    def __init__(self, F, X):
        self.F = F
        self.X = X
        