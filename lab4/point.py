class Point:
    def __init__(self, x1 = 0, x2 = 0):
        self.x1 = x1
        self.x2 = x2
    
    def print(self):
        print(f"({self.x1}, {self.x2})")