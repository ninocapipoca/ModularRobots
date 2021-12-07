# import stuff here


# Auxiliary functions
def add_zeroes(arr, n):
    # adds a specified amount of zeroes to the beginning and end of an array
    return [0 for x in range(n)] + arr + [0 for x in range(n)]

def extend(mat, n):
    # adds n more rows/cols to the matrix
    res = []
        
    for line in mat:
        line = line + [0 for x in range(n)]
        res.append(line)
        
    for i in range(n):
        res.append([0 for x in range(len(mat) + n)])
            
    return res

# Classes
class Block:
    # properties
    # connectors
    def __init__(self, left, right, top, bottom, front, back):
        self.left = left
        self.right = right
        self.top = top
        self.bottom = bottom
        self.front = front
        self.back = back


# MODIFICATION REQUIRED - how to change center
class FlatShape:
    def  __init__(self, d, mat=[]):
        self.d = d
        self.mat = mat
        
    def transform(self, x, y):
        # shift shape by x and/or y
        pass
    
    def union(self, shape):
        # union of 2 shapes is the space occupied by both of them
        pass
    
    def intersection(self, shape):
        # intersection of 2 shapes is the space occupied where they overlap
        pass
    
    def subtract(self, shape):
        # subtracts shape from self, modifies self matrix and returns it
        n = max(self.d, shape.d)
        res_mat = [[0 for x in range(n)] for y in range(n)]
        
        for i in range(n):
            for j in range(n):
                
                if self.d == shape.d: # if matrices are same size
                    # we always take max because we want our matrices to be binary
                    res_mat[i][j] = max(0, self.mat[i][j] - shape.mat[i][j])
                
                elif n == self.d: # if self is bigger, extend other shape matrix
                    shapemat = extend(shape.mat, self.d-shape.d)
                    res_mat[i][j] = max(0, self.mat[i][j] - shapemat[i][j])
                    
                else: # otherwise, other is bigger, extend self
                    selfmat = extend(self.mat, shape.d - self.d)
                    res_mat[i][j] = max(0, selfmat[i][j] - shape.mat[i][j])
                    
        self.mat = res_mat
        return self.mat
    
    def generate(self):
        # returns the matrix for this shape and sets it as self.mat
        pass
    
    def does_intersect(self, shape):
        # returns a boolean; whether self and the other shape overlap anywhere
        pass
        

class Triangle(FlatShape):
    def __init__(self, d, mat=[]):
        super().__init__(d, mat=[])
        
    def generate(self):
        # generates a triangle of base length self.d
        mat =[]
        cnt = self.d # ones count
        zcnt = 0 # zero count
        for i in range(self.d):
            addme = [1 for x in range(cnt)]
            withzeroes = add_zeroes(addme, zcnt//2)
    
            if len(withzeroes) > self.d:
                mat.append([0 for x in range(self.d)])
            else:
                mat.append(withzeroes)
                
            cnt -= 2
            zcnt += 2
            
        self.mat = mat[::-1]
            
        return self.mat
    

class Square(FlatShape):
    def __init__(self, d, mat=[]):
        super().__init__(d, mat=[])
        
    def generate(self):
        self.mat = [[1 for i in range(self.d)] for j in range(self.d)]
        return self.mat
    
    
class Circle(FlatShape):
    def __init__(self, d, c = None, mat=[]):
        super().__init__(d, mat=[])
        
        if c is None:
            self.center = (self.d//2, self.d//2)
        else:
            self.center = c
        
    def generate(self):
        r = self.d//2
        a, b = self.center
        mat = [[0 for x in range(self.d)] for y in range(self.d)]
    
        # draw the circle
        for y in range(self.d):
            for x in range(self.d):
                dist = abs((x-a)**2 + (y-b)**2)
                if dist <= r**2:
                    mat[y][x] = 1
                    
        self.mat = mat
        return mat
    
    
        
        
    
