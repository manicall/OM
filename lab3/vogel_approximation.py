import numpy as np

def vogel_approximation(pa, pb, pc):
    a = pa
    b = pb
    c = pc
    
    if sum(b) == sum(c): 
        print("Задача является закрытой")
    else:
        print("Задача является открытой")
        return
    
    sended = np.zeros(a.shape)
    
    def iter():
        res.append([])
        nonlocal a
        di = [el2 - el1 for el1, el2 in mins_row(a)]
        dj = [el2 - el1 for el1, el2 in mins_col(a)]
        
        max_di = (max(di), np.argmax(di))
        max_dj = (max(dj), np.argmax(dj))
        
        diff = ()
        
        def IndexOfPositive(_list):
            for i, el in enumerate(_list):
                if el > 0: return i
        
        if (max_di[0] < 0 and max_dj[0] < 0):
            # индекс строки максимума
            i = IndexOfPositive(b)
            # индекс минимума в максимальной строке
            j = IndexOfPositive(c)
            
            # выполнение отправки ресурсов
            send(sended, c, b, i, j)
            # удаление строки максимума
            a[i, :] = np.inf  
            
            diff = ('', (i, j))        
        else:
            if max_di[0] >= max_dj[0]:
                # индекс строки максимума
                i = max_di[1]
                # индекс минимума в максимальной строке
                j = np.argmin(a, 1)[i]
                
                # выполнение отправки ресурсов
                send(sended, c, b, i, j)
                # удаление строки максимума
                a[i, :] = np.inf
                
                diff = ('di', (i, j))   
            elif max_di[0] < max_dj[0]:
                # индекс столбца максимума
                j = max_dj[1]
                # индекс минимума в максимальном столбце
                i = np.argmin(a, 0)[j]

                # выполнение отправки ресурсов
                send(sended, c, b, i, j)
                # удаление столбца максимума
                a[:, j] = np.inf
                
                diff = ('dj', (i, j))
            
            
        res[-1].append(b.copy())
        res[-1].append(di.copy())
        res[-1].append(c.copy())
        res[-1].append(dj.copy())
        res[-1].append(sended.copy())
        res[-1].append(diff)

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
    
def mins_row(a):
    result = []
    for i in range(a.shape[0]):
        min1, min2 = np.inf, np.inf
        if all(k == np.inf for k in a[i]):
            result.append((-1, -2))
            continue
        
        for j in range(a.shape[1]):
            if a[i][j] < min2:
                if a[i][j] < min1: 
                    min2, min1 = min1, a[i][j]
                else:
                    min2 = a[i][j]
        
        if any(i < 0 or i == np.inf for i in (min1, min2)): return (-1, -2)
        result.append((min1, min2))
                
    return result

def mins_col(a):
    result = []
    for i in range(a.shape[1]):
        min1, min2 = np.inf, np.inf
        if all(k == np.inf for k in a[:, i]):  
            result.append((-1, -2))
            continue
        
        for j in range(a.shape[0]):
            if a[j][i] < min2:
                if a[j][i] < min1: 
                    min2, min1 = min1, a[j][i]
                else:
                    min2 = a[j][i]
                    
        if any(i < 0 or i == np.inf for i in (min1, min2)): 
            result.append((-1, -2))
        else:
            result.append((min1, min2))
                
    return result
    
if __name__ == '__main__':
    c = np.array([10, 20, 30])
    b = np.array([15, 20, 25])
    a = np.array(
        [[5,3,1],
        [3,2,4],
        [4,1,2]], np.float64)
    
    vogel_approximation(a, b, c)