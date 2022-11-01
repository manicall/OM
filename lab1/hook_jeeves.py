from equals import Equals, MyEnum

def hook_jeeves():
    f = Equals.get_f(MyEnum.forth)
    
    x = [[1], [1]]
    h = [1]
    a = 0.1
    E = 0.001
    start = 0
    end = 1000
        
    def is_equals(x):
        for i in range(len(x)): 
            if x[i][-2] != x[i][-1]: 
                return False
        return True
    
    while start < end:
        def get_x(): 
            for i in x:
                yield i[-1]
        
        def get_dx(e, i):
            for j in enumerate(x):
                yield j[1][-1] if j[0] != i else j[1][-1] + e*h[-1]

        def search():
            for i in range(len(x)):
                if f(*get_x()) > f(*get_dx(1, i)):
                    x[i].append(x[i][-1] + h[-1])
                elif f(*get_x()) > f(*get_dx(-1, i)):
                    x[i].append(x[i][-1] - h[-1])
                else:
                    x[i].append(x[i][-1])
                
            if is_equals(x): return False              
            
            return True


        if not search():
            if (h[-1] > E): 
                h.append(h[-1] * a)
                continue
            else:
                break
        
        #print(*x, sep='\n')
        
        def xp_v1(i):
            return x[i][-1] + (x[i][-1] - x[i][-2])
        
        # по методичке
        def xp_v2(i):
            return x[i][-2] + 2*(x[i][-1] - x[i][-2])
            
        xp = [xp_v2(i) for i in range(len(x))]
        
        if f(*xp) < f(*get_x()):
            for i in range(len(x)):
                x[i].append(xp[i])
        else:
            if (h[-1] > E): 
                h.append(h[-1] * a)
            else:
                break

        if (h[-1] <= E):
            break 
                 
        start += 1

    print(f"x{tuple(get_x())}")
    
if __name__ == "__main__":
    hook_jeeves()