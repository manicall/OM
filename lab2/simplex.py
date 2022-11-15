import numpy as np
from scipy.optimize import linprog

def simplex(pa, pb, pc):
    F = []
    
    a = pa.copy()     
    
    cb = np.zeros(a.shape[0])
    p0 = []
    # перевод массива b в список
    p0.extend(pb.copy())
    p0.append(0) # заполнитель
    p0[-1] = sum(zj(p0, cb))

    p = getP(a, zj(p0, cb), pc)    

    # инициализация базиса
    bazis = get_bazis(a, p)

    def iter():
        nonlocal bazis
        # получение позиции максимального по модулю
        #! в последней строке, среди p неявляющихся базисом
        not_basiz_id, not_basiz_p = get_not_basiz(bazis, p)
        maxPos = np.argmax(getAbs(not_basiz_p))
        
        # получение минимального
        divs = getDiv(p0, p, maxPos)
        min_el, minPos = min(divs), np.argmin(divs)
        
        pmax = f'P{not_basiz_id[maxPos] + 1}'
        pmin = get_pmin(bazis, minPos)
        
        pCopy = p.copy()
        # деление строки на разрешающий элемент
        for i in not_basiz_id:
            if i == maxPos:
                p[minPos][i] /= pCopy[minPos][maxPos] ** 2
            else:
                p[minPos][i] /= pCopy[minPos][maxPos]

        # перерасчет p0
        cb[minPos] = c[maxPos]
        p0[minPos] = min_el
        for i in range(len(p0)):
            if i == minPos: continue
            p0[i] -= p0[minPos]*p[i][key_to_id(pmax)] 
        p0[-1] = sum(zj(p0, cb))

        pCopy = p.copy() 
        for i in range(a.shape[0]):
            if i == minPos: continue
            for j in not_basiz_id:
                if j == maxPos: continue
                p[i][j] -= pCopy[i][maxPos]*pCopy[minPos][j]
                
            p[i][maxPos] = pCopy[i][key_to_id(pmin)] \
                - p[i][maxPos]*pCopy[minPos][maxPos]
           
        for i in not_basiz_id:
            if i == maxPos: continue     
            s = sum(zj(p[:, i], cb))
            p[-1][i] = s - c[i]     
        
        p[-1][maxPos] = sum(zj(p[:, maxPos], cb))

        # обмен в векторе базиса
        bazis = swap_bazis(bazis, pmin, pmax)
        # обмен стоблцов в массиве
        swap_p(p, key_to_id(pmin), key_to_id(pmax))
       
        def has_up_border(pColumn):
            for i in pColumn:
                if i > 0: return True
            return False
     
        for i in range(len(p)):
            if not has_up_border(p[:, i]):
                print("Функция не ограничена сверху")
                return False
        
        # если решение содержит множество точек максимума, 
        # необходимо использовать значение списка F для выхода из цикла
        F.append(p0[-1])
        if (len(F) > 1):
            if (F[-1] == F[-2]):
                print("Точка максимума лежит на прямой")
                return False
        
        if len(list(filter(lambda x: x < 0, p[-1, :]))) == 0:
            print("Успешно найдено единственное решение")
            return False # выход из цикла
        
        return True
    
    n = 10
      
    def get_res():
        res = []
        #b = dict(sorted(bazis.items(), key=lambda x: x[1]))
        b = [key for key, v in filter(lambda x: x[1] > 0,  bazis.items())]
        for i in range(a.shape[0]):
            res.append([])
            res[-1].append(i+1)
            res[-1].append(b[i])
            res[-1].append(cb[i])
            res[-1].append(p0[i])
            res[-1].extend(p[i])
            
        res.append([])
        res[-1].append(len(res))
        res[-1].extend((None, None))
        res[-1].append(p0[-1])
        res[-1].extend(p[-1])

        return res
    
    full_res = [get_res()]
    while iter(): 
        full_res.append(get_res())
        if (n := n - 1) == 0: break
    else:
        full_res.append(get_res())
    
    return full_res

def zj(p0, cb):
    return np.array(list(map(lambda a, b: a*b, p0[:-1], cb)))

def get_bazis(a, p):
    j = 0
    bazis = {}
    for i in range(p.shape[1]):
        if i < a.shape[1]:
            bazis[f"P{i+1}"] = 0
        else:
            bazis[f"P{i+1}"] = (j := j + 1)
            
    return bazis
    
def key_to_id(pkey):
    return int(pkey[1:]) - 1

def getP(a, zj, c):
    p = []
    for i in range(a.shape[0]):
        p.append([])
        # значения из массива a
        for j in range(a.shape[1]):
            p[-1].append(a[i][j])
        # единичная матрица
        for k in range(a.shape[0]):
            p[-1].append(1 if k == i else 0)
    
    p.append([])
    for zj_el, c_el in zip(zj, c):
        p[-1].append(zj_el - c_el)
    for k in range(a.shape[0]):
        p[-1].append(0)
    
    return np.array(p)

def getAbs(pSlice):
    copy = list(map(lambda x: 0 if x > 0 else x, pSlice))
    return list(map(abs, copy))

def getDiv(p0, p, maxPos):
    return list(map(lambda a, b: a/b, p0, p[:-1, maxPos])) 

def swap_bazis(bazis, pmin, pmax):
    bazis[pmin], bazis[pmax] = bazis[pmax], bazis[pmin]
    return dict(sorted(bazis.items(), key=lambda x: x[1]))

def swap_p(p, minPos, maxPos):
    p[:,minPos], p[:,maxPos] = p[:,maxPos].copy(), p[:,minPos].copy()

def get_not_basiz(bazis, p): 
    # индексы Pi неявляющихся базисом
    not_bazis_id = []
    for key, value in bazis.items():
        if value == 0: 
            # key[1:] - удаление первого символа 
            # из строки ('P15'[1:] => '15')
            not_bazis_id.append(int(key[1:]) - 1)
            
    # получение и возврат строки (zj - c) в Pi неявляющихся базисом
    not_bazis_p = np.array([p[:, i] for i in not_bazis_id])
    not_bazis_p = np.ndarray.flatten(not_bazis_p[:, [-1]])
    
    return (not_bazis_id, not_bazis_p)
    
def get_pmin(bazis, minPos):
    for key, value in bazis.items():
        if minPos + 1 == value: return key 

if __name__ == '__main__': 
    a = np.array([[18, 15, 12],
                  [6, 4, 8], 
                  [5, 3, 3]])       
    
    b = np.array([360, 192, 180])
    c = [9, 10, 16]

    simplex(a, b, c)
