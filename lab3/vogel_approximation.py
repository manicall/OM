import numpy as np

def vogel_approximation(pa, pb, pc):
    a = pa
    b = pb
    c = pc
    
    sended = np.array([np.zeros(c.shape[1]) for i in range(c.shape[0])])
    
    ti = []
    tj = []
    def iter():
        res.append([])
        nonlocal c
        di = [el2 - el1 for el1, el2 in mins_row(c)]
        dj = [el2 - el1 for el1, el2 in mins_col(c)]
        
        #print(1, di, dj)
        
        max_di = (max(di), np.argmax(di))
        max_dj = (max(dj), np.argmax(dj))
        
        if max_di[0] > max_dj[0]:
            # индекс строки максимума
            i = max_di[1]
            # индекс минимума в максимальной строке
            j = np.argmin(c, 1)[i]
            
            # выполнение отправки ресурсов
            send(sended, a, b, i, j)
            # удаление строки максимума
            c[i, :] = np.inf
        else:
            # индекс столбца максимума
            j = max_dj[1]
            # индекс минимума в максимальном столбце
            i = np.argmin(c, 0)[j]

            # выполнение отправки ресурсов
            send(sended, a, b, i, j)
            # удаление столбца максимума
            c[:, j] = np.inf
        
        #print(2, di, dj)
        
        res[-1].append(a.copy())
        res[-1].append(di.copy())
        res[-1].append(b.copy())
        res[-1].append(dj.copy())
        res[-1].append(sended.copy())

    res = []
    
    
    while any(i > 0 for i in b):
        iter()
        
    print(*res, sep='\n')
    return res
            
def send(sended, a, b, i, j):
    _min = min(a[i], b[j])
    sended[i][j] = _min
    a[i] -= _min
    b[j] -= _min
    
def mins_row(c):
    result = []
    for i in range(c.shape[0]):
        if all(k == np.inf for k in c[i]):
            result.append((-1, -2))
            continue
        
        min1, min2 = c[i][0], c[i][1]
        if min1 > min2: min1, min2 = min2, min1
        for j in range(2, c.shape[1]):
            if c[i][j] < min2:
                if c[i][j] < min1: 
                    min2, min1 = min1, c[i][j]
                else:
                    min2 = c[i][j]
        result.append((min1, min2))
                
    return result

def mins_col(c):
    result = []
    for i in range(c.shape[1]):
        if all(k == np.inf for k in c[:, i]):  
            result.append((-1, -2))
            continue
        
        min1, min2 = c[0][i], c[1][i]
        if min1 > min2: min1, min2 = min2, min1
        for j in range(2, c.shape[0]):
            if c[j][i] < min2:
                if c[j][i] < min1: 
                    min2, min1 = min1, c[j][i]
                else:
                    min2 = c[j][i]
        result.append((min1, min2))
                
    return result
    
if __name__ == '__main__':
    # a = np.array([160, 140, 170])
    # b = np.array([120, 50, 190, 110])
    # c = np.array(
    #     [[7,8,1,2],
    #     [4,5,9,8],
    #     [9,2,3,6]], np.float64)

    a = np.array([10, 20, 30])
    b = np.array([15, 20, 25])
    c = np.array(
        [[5,3,1],
        [3,2,4],
        [4,1,2]], np.float64)

    vogel_approximation(a, b, c)