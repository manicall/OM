import numpy as np
from vogel_result import Result

def vogel_approximation(pa, pb, pc):
    a = pa
    b = pb
    c = pc
    
    allowed_rows = [*range(a.shape[0])]
    allowed_cols = [*range(a.shape[1])]
    
    if sum(b) == sum(c): 
        print("Задача является закрытой")
    else:
        print("Задача является открытой")
        return
    
    sended = np.zeros(a.shape)
    
    def iter():
        nonlocal a
        di = [el2-el1 for el1, el2 in mins_row(a, allowed_rows, allowed_cols)]
        dj = [el2-el1 for el1, el2 in mins_col(a, allowed_rows, allowed_cols)]
        
        max_di = (max(di), np.argmax(di))
        max_dj = (max(dj), np.argmax(dj))
        
        colored = ()
        diff = 0
    
        def IndexOfPositive(_list):
            for i, el in enumerate(_list):
                if el > 0: return i
            
        if (max_di[0] < 0 and max_dj[0] < 0):
            # индекс строки максимума
            i = IndexOfPositive(b)
            # индекс минимума в максимальной строке
            j = IndexOfPositive(c)
            
            # выполнение отправки ресурсов
            diff = send(sended, c, b, i, j)
            
            colored = ('', (i, j))        
        else:
            if max_di[0] >= max_dj[0]:
                # индекс строки максимума
                i = max_di[1]
                # индекс минимума в максимальной строке
                j = None
                for col in allowed_cols:
                    if j is None or a[i][j] > a[i][col]: 
                        j = col
                    
                if j is None:
                    # удаление строки максимума
                    allowed_rows.remove(i)
                    return
                
                # выполнение отправки ресурсов
                diff = send(sended, c, b, i, j)
                allowed_rows.remove(i)
                colored = ('di', (i, j))           
            else:
                # индекс столбца максимума
                j = max_dj[1]
                # индекс минимума в максимальном столбце
                i = None
                for row in allowed_rows:
                    if i is None or a[i][j] > a[row][j]: i = row
                    
                if i is  None: 
                    # удаление столбца максимума
                    allowed_cols.remove(j)
                    return
                
                diff = send(sended, c, b, i, j)
                allowed_cols.remove(j)
                colored = ('dj', (i, j))
                

        res.append(Result(b.copy(), di.copy(), c.copy(), dj.copy(), sended.copy(), diff, colored))

    res = []
    n = 1000
    while any(i > 0 for i in b) and n > 0:
        iter()
        
    print(*res, sep='\n')
    return res
            
def send(sended, c, b, i, j):
    _min = min(c[j], b[i])
    sended[i][j] = _min
    c[j] -= _min
    b[i] -= _min
    
    return _min
    
def mins(a, allowed_rows, allowed_cols, axis):
    def getA(i, j):
        if axis == 0: return a[i][j]
        elif axis == 1: return a[j][i] 
    
    def getSize():
        if axis == 0: return a.shape[0], a.shape[1]
        elif axis == 1: return a.shape[1], a.shape[0]
        
    def check_stop():
        if axis == 0 and all(k != i for k in allowed_rows): return True
        elif axis == 1 and all(k != i for k in allowed_cols): return True
        return False
    
    def get_allowed():
        if axis == 0: return allowed_cols
        elif axis == 1: return allowed_rows
    
    result = []
    for i in range(getSize()[0]):
        if check_stop():
            result.append((-1, -2))
            continue
        
        if len(get_allowed()) > 1:
            min1, min2 = getA(i, get_allowed()[0]), getA(i, get_allowed()[1])
            if min1 > min2: min1, min2 = min2, min1
            for j in get_allowed()[2:]:
                if getA(i, j) < min2:
                    if getA(i, j) < min1: 
                        min2, min1 = min1, getA(i, j)
                    else:
                        min2 = getA(i, j)

            result.append((min1, min2))
        else:
            result.append((-1, -2))
                
    return result

def mins_row(a, allowed_rows, allowed_cols):
    return mins(a, allowed_rows, allowed_cols, 0)

def mins_col(a, allowed_rows, allowed_cols):
    return mins(a, allowed_rows, allowed_cols, 1)
    
if __name__ == '__main__':
    c = np.array([10, 20, 30])
    b = np.array([15, 20, 25])
    a = np.array(
        [[5,3,1],
        [3,2,4],
        [4,1,2]], np.float64)
    
    vogel_approximation(a, b, c)