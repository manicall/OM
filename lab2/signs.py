class Signs:
    bSigns = ['⩽', '⩾']  
    signs = ['<=', ">="]
    eq = '='
    
    def isLess(for_check):
        return for_check == Signs.bSigns[0] or for_check == Signs.signs[0]
    
    def isMore(for_check):
        return for_check == Signs.bSigns[1] or for_check == Signs.signs[1]
    
    def isEqual(for_check):
        return for_check == Signs.eq
    
    def isSign(for_check):
        return any(for_check == i for i in Signs.bSigns) \
            or any(for_check == i for i in Signs.signs) \
            or for_check == Signs.eq