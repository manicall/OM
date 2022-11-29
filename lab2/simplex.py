import numpy as np
from scipy.optimize import linprog
from signs import Signs
from simplex_result import Result 

def simplex(pa, pb, pc, signs = None, task = "max"):
    if signs is not None:
        if (all(i == Signs.equal for i in signs)):
            print("данную задачу невозможно решить симплексным методом")
            return
    
        for i, el in enumerate(signs):
            if el == Signs.more:
                pb[i] = -pb[i]
                for j in range(pa.shape[1]):
                    pa[i][j] = -pa[i][j]             
      
    if (any(i < 0 for i in pb)):
        print("данную задачу невозможно решить симплексным методом")
        return 
    
    if task == 'min':
        pc = list(map(lambda x: -x, pc))

    a = pa.copy()
    b = pb.copy()
    c = pc.copy() + [0] * a.shape[0]   
    
    cb = np.zeros(a.shape[0])

    p = init_p(a, b, c, cb)    

    # инициализация базиса
    bazis = init_bazis(a, p)

    def iter():
        nonlocal bazis
        # получение позиции максимального по модулю (выбор только среди отризательных)
        k, _ = getMaxPos(p[-1])
        
        # получение минимального (выбор только среди положитительных)
        divs = getDivs(p, k)
        r = np.argmin(divs)
        
        pCopy = np.array(p)
        
        # r - разрешающая строка
        # k - разрешающий стобец
        for i in range(len(p)):
            for j in range(len(p[i])):
                if (i == r):
                    p[i][j] /= pCopy[r][k]
                else:
                    p[i][j] -= (pCopy[r][j]/pCopy[r][k])*pCopy[i][k]
        
        cb[r] = c[k-1]
        
        pmax = f'P{k}'
        pmin = get_pmin(bazis, r)
        # обмен в векторе базиса
        bazis = swap_bazis(bazis, pmin, pmax)
       
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
        if (len(full_res) > 1):
            if (full_res[-1].getResult().F == full_res[-2].getResult().F):
                print("Точка максимума лежит на прямой")
                return False
        
        if not list(filter(lambda x: x < 0, p[-1, :])):
            #print("Успешно найдено единственное решение")
            return False # выход из цикла
        
        return True
    
    n = 1000
      
    def get_res():
        b = [key for key, v in filter(lambda x: x[1] > 0,  bazis.items())]
        return Result(b.copy(), cb.copy(), p.copy())
    
    full_res = [get_res()]
    while iter(): 
        full_res.append(get_res())
        if (n := n - 1) == 0: break
    else:
        full_res.append(get_res())
    
    return full_res

def zj(pCol, cb):
    return sum(map(lambda a, b: a*b, pCol, cb))

def init_bazis(a, p):
    j = 0
    bazis = {}
    for i in range(p.shape[1] - 1):
        if i < a.shape[1]:
            bazis[f"P{i+1}"] = 0
        else:
            bazis[f"P{i+1}"] = (j := j + 1)
            
    return bazis
    
def key_to_id(pkey):
    return int(pkey[1:]) - 1

def init_p(a, b, c, cb): 
    p = []
    for i in range(a.shape[0]):
        p.append([b[i]])
        # значения из массива a
        for j in range(a.shape[1]):
            p[-1].append(a[i][j])
        # единичная матрица
        for k in range(a.shape[0]):
            p[-1].append(1 if k == i else 0)
    
    copyP = np.array(p)
    p.append([zj(copyP[:, 0], cb)])
    for i in range(1, len(p[0])):
        p[-1].append(zj(copyP[:, i], cb) - c[i - 1])

    return np.array(p)

def getMaxPos(pSlice):
    maxPos = None
    max = None
    for i, el in enumerate(pSlice):
        if el < 0: # среди отрицательных
            if max is None:
                maxPos, max = i, abs(el) 
            elif abs(el) > max: # максмаальное по модулю
                maxPos, max = i, abs(el) 
    return maxPos, max

def getDivs(p, maxPos):
    p0 = p[:-1, 0]
    pj = p[:-1, maxPos]
    
    def only_positive(a, b):
        if b > 0:
            return a/b
        else: 
            return np.inf
    
    return list(map(only_positive, p0, pj)) 

# ломается потому что p0 начал входить в общую p
def swap_bazis(bazis, pmin, pmax):
    bazis[pmin], bazis[pmax] = bazis[pmax], bazis[pmin]
    return dict(sorted(bazis.items(), key=lambda x: x[1]))
  
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
