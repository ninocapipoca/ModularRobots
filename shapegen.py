# import stuff here


# TO DO
# Fix reduce function
# (Optionally) fix prettyprint
# Add scalar
# 

# DONE


# Auxiliary functions

# Note that some of these may be integrated into the classes directly later
# This is just to simplify things for now
def add_zeroes(arr, n):
    """adds a specified amount of zeroes to the beginning and end of an array"""
    return [0 for x in range(n)] + arr + [0 for x in range(n)]

def prettyprint_mat(mat):
    # This function is not good, it kind of works but it's spaghetti code
    # It modifies the matrix entries to strings, which we don't want
    # Needs to be fixed or replaced
    for y in range(len(mat)):
        for x in range(len(mat)):
            mat[y][x] = str(mat[y][x])

    for line in mat:
        print(' '.join(line))

def extend(mat, n):
    """extends the matrix by n  rows/cols"""
    # adds n more rows/cols to the matrix
    res = []
        
    for line in mat:
        line = line + [0 for x in range(n)]
        res.append(line)
        
    for i in range(n):
        res.append([0 for x in range(len(mat) + n)])
            
    return res

def validconfig(mat):
    """checks if a flat shape / matrix is a valid configuration"""
    # it is valid if a block is connected to at least one other block
    # i.e. all the ones have at least 1 neighbor that is a one

    for x in range(len(mat)):
        for y in range(len(mat)):
            if mat[x][y] == 1:
                neighbors = [mat[x+a[0]][y+a[1]] for a in 
                             [(-1,0), (1,0), (0,-1), (0,1)] 
                             if ( (0 <= x + a[0] < len(mat)) and (0 <= y + a[1] < len(mat)))]
                
                if 1 not in neighbors:
                    return False
    return True

def reduce(mat):
    # THIS FUNCTION NEEDS TO BE FIXED! IT DOESN'T WORK PROPERLY
    # Test it on a couple of different examples to understand why
    # It removes stuff where it shouldn't, and we end up with non square matrices sometimes
    # Or just weird matrices, really.. 
    """makes mat as small as possible while maintaining it square and not
    losing any ones"""
    empty = 0
    d = len(mat)
    
    newmat = []

    for i in range(d-1, -1, -1):
        if 1 in mat[i]:
            break
        empty += 1
    
    newmat.append(mat[0][:-empty])
    for i in range(1,d):
        if 1 in mat[i] and i != 0:
            oneslist = [1 for i in range(len(mat))]
            if mat[i] == oneslist:
                newmat.append(mat[i])
            else:
                newmat.append(mat[i][:-empty])
        
    return newmat

def transform_y(mat, y):
    """moves the shape inside mat by y"""
    # this function treats the matrix as a stationary viewport
    # it means that it is possible to end up with a matrix made up
    # entirely of zeroes if you move the shape too far up
    cnt = 0
    for line in mat:
        if 1 in line:
            break
        cnt += 1
    
    if y > 0: # move up
        return mat[y:] + [[0 for _ in range(len(mat))] for _ in range(y)]
    
    elif y < 0: # move down
        amt = abs(y)
        return [[0 for _ in range(len(mat))] for _ in range(amt)] + mat[:y]
    
    else: # do nothing - i surely hope we never use this condition
        return mat

    
def transform_x(mat, x):
    """ moves the shape inside the mat by x"""
    # this function works similarly to transform_y
    if x > 0:
        # then we are going to move the shape left
        return [mat[i][x:] + [0 for _ in range(x)] for i in range(len(mat))]
    
    elif x < 0:
        # then we move the shape right
        amt = abs(x)
        return [[0 for _ in range(amt)] + mat[i][:x] for i in range(len(mat))]
    
    else:
        return mat


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

class Shape2D:
    def  __init__(self, d, mat=[]): 
        self.d = d # dimension
        self.mat = mat # matrix
        
    def reduceself(self):
        # FIX AUX FUNCTION! THIS DOES NOT WORK
        self.mat = reduce(self.mat)
        self.d = len(self.mat)
        return self.mat
        
    def extendself(self, n):
        self.mat = extend(self.mat, n)
        self.d = len(self.mat)
        return self.mat
        
    def transform(self, x, y):
        # translate s
        xtransf = transform_x(self.mat, x)
        ytransf = transform_y(xtransf, y)
        self.mat = ytransf
        return self.mat
    
    def union(self, shape):
        # union of 2 shapes is the space occupied by both of them
        n = max(self.d, shape.d)
        res_mat = [[0 for x in range(n)] for y in range(n)]
        
        shapemat = shape.mat
        if n == self.d:
            #shapemat = extend(shape.mat, self.d - shape.d)
            shapemat = shape.extendself(self.d - shape.d)
        elif n == shape.d:
            #shapemat = extend(self.mat, shape.d - self.d)
            shapemat = self.extendself(shape.d, self.d)
        
        for i in range(n):
            for j in range(n):
                res_mat[i][j] = self.mat[i][j] or shapemat[i][j]
                
        self.mat = res_mat
        self.d = len(res_mat)
        return self.mat
    
    def valid(self):
        return validconfig(self.mat)
    
    def intersection(self, shape):
        # intersection of 2 shapes is the space occupied where they overlap
        n = max(self.d, shape.d)
        res_mat = [[0 for x in range(n)] for y in range(n)]
        
        shapemat = shape.mat
        if n == self.d:
            #shapemat = extend(shape.mat, self.d - shape.d)
            shapemat = shape.extendself(self.d - shape.d)
        elif n == shape.d:
            #shapemat = extend(self.mat, shape.d - self.d)
            shapemat = self.extendself(shape.d, self.d)
        
        for i in range(n):
            for j in range(n):
                res_mat[i][j] = self.mat[i][j] and shapemat[i][j]
                
        self.mat = res_mat
        self.d = len(res_mat)
        return self.mat
    
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
                    #shapemat = extend(shape.mat, self.d-shape.d)
                    shapemat = shape.extendself(self.d - shape.d)
                    res_mat[i][j] = max(0, self.mat[i][j] - shapemat[i][j])
                    
                else: # otherwise, other is bigger, extend self
                    #selfmat = extend(self.mat, shape.d - self.d)
                    selfmat = self.extendself(shape.d - self.d)
                    res_mat[i][j] = max(0, selfmat[i][j] - shape.mat[i][j])
                    
        self.mat = res_mat
        self.d = len(res_mat)
        return self.mat
    
    def generate(self):
        # returns the matrix for this shape and sets it as self.mat
        pass
    
    def does_intersect(self, shape):
        # returns a boolean; whether self and the other shape overlap anywhere
        ext = shape.mat
        if self.d > shape.d:
            ext = extend(shape.mat, self.d - shape.d)
            
        elif shape.d > self.d:
            ext = extend(self.mat, shape.d - self.d)
        
        for i in range(self.d):
            for j in range(self.d):
                if ext[i][j] == 1 and self.mat[i][j] == 1:
                    return True
        
        return False
    
    def scale(self, x):
        # make shape bigger by x blocks
        new = self.d + x
        self.d = new
        self.mat = self.generate()
        return self.mat
            

class Triangle(Shape2D):
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
        self.d = len(self.mat)
            
        return self.mat
    

class Square(Shape2D):
    def __init__(self, d, mat=[]):
        super().__init__(d, mat=[])
        
    def generate(self):
        self.mat = [[1 for i in range(self.d)] for j in range(self.d)]
        return self.mat
    
    
class Circle(Shape2D):
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
        self.d = len(self.mat)
        return mat
    
    

    
    
        
        
    
