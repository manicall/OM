class Kruskal:
    def __init__(self, graph):
        self.graph = graph
        s = set([g[0] for g in graph] + [g[1] for g in graph])
        self.V = len(s)
 
    def __search(self, parent, i):
        if parent[i] == i: return i
        return self.__search(parent, parent[i])
 
    def __apply_union(self, parent, rank, x, y):
        xroot = self.__search(parent, x)
        yroot = self.__search(parent, y)
        
        if rank[xroot] < rank[yroot]: parent[xroot] = yroot
        elif rank[xroot] > rank[yroot]: parent[yroot] = xroot
        else:
            parent[yroot] = xroot
            rank[xroot] += 1
            
    def kruskal(self):
        result = []
        i, e = 0, 0
        
        g = dict(zip(range(len(self.graph)), self.graph))
        g = sorted(g.items(), key=lambda item: item[1][2])  
        
        parent = []
        rank = []
        for node in range(self.V):
            parent.append(node)
            rank.append(0)
        while e < self.V - 1:
            u, v, w = g[i][1]
            x = self.__search(parent, u)
            y = self.__search(parent, v)
            
            if x != y:
                e = e + 1
                result.append((u, v, w))
                self.__apply_union(parent, rank, x, y)
            
            i = i + 1       
        return result
