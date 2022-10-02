from re import A
import numpy as np

def simplex():
    a = np.array([[18, 15, 12],
                  [6, 4, 8], 
                  [5, 3, 3]])       
    
    c = [9, 10, 16] + [0 for i in range(a.shape[0])]   
    b = np.array([360, 192, 180])
    cb = np.zeros(a.shape[0])
    p0 = []
    # перевод массива b в список
    p0.extend(b.copy())
    p0.append(0) # заполнитель
    p0[-1] = sum(zj(p0, cb))
    
    print(p0)
         
    p = getP(a, zj(p0, cb), c)    

    # инициализация базиса
    bazis = get_bazis(a, p)

    def iter():
        # получение позиции максимального по модулю
        #! в последней строке, среди p неявляющихся базисом
        not_basiz_id, not_basiz_p = get_not_basiz(bazis, p)
        maxPos = np.argmax(getAbs(not_basiz_p))
        
        # получение минимального
        divs = getDiv(p0, p, maxPos)
        min_el, minPos = min(divs), np.argmin(divs)
        
        pmax = f'P{not_basiz_id[maxPos] + 1}'
        pmin = get_pmin(bazis, minPos)
        print(np.round(p, 3))
        
        pCopy = p.copy()
        # деление строки на разрешающий элемент
        for i in not_basiz_id:
            if i == maxPos:
                # ?
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
        print(np.round(p, 3))
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
        print(sum(zj(p[:, maxPos], cb)))
        
        p[-1][maxPos] = sum(zj(p[:, maxPos], cb))
        print(np.round(p, 3))  
        
        # обмен в векторе базиса
        swap_bazis(bazis, pmin, pmax)
        # обмен стоблцов в массиве
        swap_p(p, key_to_id(pmin), key_to_id(pmax))
        # обмен в векторе с
    
        print(c, '\n\n\n\n\n')
    iter()
    iter()
   
   
    
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
    bazis = dict(sorted(bazis.items(), key=lambda x: x[1]))

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
    simplex()
