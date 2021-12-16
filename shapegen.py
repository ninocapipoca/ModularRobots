# import stuff here

# TO DO
# Fix reduce function for 2D shapes
# (Optionally) fix prettyprint
# Add scale for 3D shapes
# Union for 3D
# Intersection for 3D
# Subtract for 3D
# Fix scale function (centering shapes issue)

# DONE
# Add scalar function for 2D shapes



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

class DSU:
    """ disjoint set union / union find """
    def __init__(self):
        self.dsu = {}  # maps to parent or -size comp, if is root
    
    def find(self, x):
        """ returns par(component x) """
        px = self.dsu.get(x, -1)
        if isinstance(px, int) and px < 0:
            return x
        else:
            self.dsu[x] = self.find(self.dsu[x])
            return self.dsu[x]

    def merge(self, x, y):
        """ merges the sets containing x and y """
        x = self.find(x)
        y = self.find(y)
        if x != y:
            vx, vy = self.dsu.get(x, -1), self.dsu.get(y, -1)
            if vx > vy:
                x,y = y,x
            self.dsu[x] = vx + vy
            self.dsu[y] = x


def check_connected(X):
    """ are all filled voxels are in the same connected component
        of the graph of direct neighbors """
    if isinstance(X[0][0], list): # 3D
        dx,dy,dz = len(X), len(X[0]), len(X[0][0])
        pos = [(x,y,z) 
            for x in range(dx)
            for y in range(dy)
            for z in range(dz)
            if X[x][y][z]
        ]
        def valid(x,y,z):
            return (0 <= x < dx
                    and 0 <= y < dy
                    and 0 <= z < dz)
        dsu = DSU()
        for (x,y,z) in pos:
            for xx,yy,zz in [
                (x+1,y,z),
                (x-1,y,z),
                (x,y+1,z),
                (x,y-1,z),
                (x,y,z+1),
                (x,y,z-1),
            ]:
                if valid(xx,yy,zz) and X[xx][yy][zz]:
                    dsu.merge((x,y,z), (xx,yy,zz))
        components = set(dsu.find(p) for p in pos)
        return len(components) == 1
    else:
        # 2D
        dx,dy = len(X), len(X[0])
        pos = [(x,y) 
            for x in range(dx)
            for y in range(dy)
            if X[x][y]
        ]
        def valid(x,y):
            return (0 <= x < dx
                    and 0 <= y < dy)
        dsu = DSU()
        for (x,y) in pos:
            for xx,yy in [
                (x+1,y),
                (x-1,y),
                (x,y+1),
                (x,y-1),
            ]:
                if valid(xx,yy) and X[xx][yy]:
                    dsu.merge((x,y), (xx,yy))
        components = set(dsu.find(p) for p in pos)
        return len(components) == 1
    
from itertools import product

def get_shape(M):
    if isinstance(M, list):
        return (len(M),) + get_shape(M[0])
    else: return tuple()


def iterate(shape):
    return product(*map(range, shape))


def mdaccess(coords, M):
    if len(coords) == 3:
        i,j,k = coords
        return M[i][j][k]
    if len(coords) == 2:
        i,j = coords
        return M[i][j]
    if len(coords) == 1:
        i, = coords
        return M[i]


def reduce(M): # 
    shape = get_shape(M)
    resize = []
    
    def all_zeros(ax,i):
        for coor in iterate(shape[:ax] + shape[ax+1:]):
            coor = (*coor[:ax], i, *coor[ax:])
            if mdaccess(coor, M): return False
        return True
    
    for ax, sz in enumerate(shape):
        for i in range(sz):
            if not all_zeros(ax,i):
                break
        for j in range(sz-1, i-1, -1):
            if not all_zeros(ax, j):
                break
        resize.append((i,j+1))
    # print(resize)
    def rsz(M, shape):
        if len(shape) == 1:
            (x,y), = shape
            return M[x:y]
        (x,y),*rest = shape
        return [rsz(m,rest) for m in M[x:y]]
    return rsz(M, resize)
        

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
    
def extend_center(mat, n):
    if n%2 != 0:
        print("Error, you can only extend by an even number")
        return mat
    res = []
        
    for line in mat:
        line = [0 for x in range(n//2)] + line + [0 for x in range(n//2)]
        res.append(line)
        
    amt = len(mat) + n
    res = [[0 for x in range(amt)] for y in range(n//2)] + res + [[0 for x in range(amt)] for y in range(n//2)]
        
    return res


# Classes

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
            shapemat = self.extendself(shape.d - self.d)
            
        # print(shapemat) # DEBUGGING
        
        for i in range(n):
            for j in range(n):
                res_mat[i][j] = self.mat[i][j] or shapemat[i][j]
                
        self.mat = res_mat
        self.d = len(res_mat)
        return self.mat
    
    def valid(self):
        return check_connected(self.mat)
    
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
    

class Shape3D():
    # in the event that we have a weird irregular shape, 
    # self.d is the largest number of continuous ones in a row
    def __init__(self, d, layers=[]):
        self.d = d
        self.layers = layers
        
    def generate(self):
        pass
    
    def valid(self):
        if self.layers == []:
            return True
        
        res = self.layers[0].valid()
        for shape in self.layers:
            res = res and shape.mat.valid()
            
        return res
       

    # Actually I'm not so sure we want to include this 
    
    # This function doesn't work anyway
    # def subtract(self, shape):
    #     # subtracts shape from self
    #     res = []
    #     if len(self.layers) >= shape.layers:
    #         for i in range(len(shape.layers)):
    #             try:
    #                 res.append(self.layers[i].subtract(shape.layers[i]))
    #             except IndexError:
    #                 self.layers = res
    #                 return self.layers
            
    
    # def union(self, shape):
    #     pass
    
    # def intersection(self, shape):
    #     pass
    
    
class Sphere(Shape3D):
    def __init__(self, d, layers=[]):
        super().__init__(d, layers=[])
        
    def generate(self):
        cnt = 1
        res = []

        while cnt != self.d + 2:
            circle = Circle(cnt)
            mat = circle.generate()
            
            if len(mat) < self.d:
                diff = len(mat) - self.d
                circle.mat = extend_center(mat, diff)
            
            res.append(circle)
            
            cnt += 2
        
        
        self.layers = res
        addme = self.layers[:len(self.layers)-1]
        self.layers = self.layers + addme[::-1]
        
        return self.matlist

class Cube(Shape3D):
    def __init__(self, d, layers=[]):
        super().__init__(d, layers=[])

    def generate(self):
        cnt = 0
        res = []
        
        while cnt != self.d:
            square = Square(self.d)
            mat = square.generate()
            res.append(square)
            
            cnt += 1
        
        self.layers = res
        
        return self.layers
    
class Cylinder(Shape3D):
    def __init__(self, d, layers=[]):
        super().__init__(d, layers=[])

    def generate(self):
        res = []
        cnt = 0
        
        while cnt != self.d:
            circle = Circle(self.d)
            mat = circle.generate()
            res.append(circle)
            
            cnt += 1
        
        self.layers = res
        return self.layers

class Cone(Shape3D):
    def __init__(self, d, layers=[]):
        super().__init__(d, layers=[])

    def generate(self):
        cnt = 1
        res = []
            
        while cnt != self.d + 2:
            circle = Circle(cnt)
            mat = circle.generate()
            
            if len(mat) < self.d:
                diff = len(mat) - self.d
                circle.mat = extend_center(mat, diff)
            
            res.append(circle)
            cnt += 2
        
        self.layers = res
        return self.layers

class Pyramid(Shape3D):
    def __init__(self, d, layers=[]):
        super().__init__(d, layers=[])
        
    def generate(self):
        cnt = 1
        res = []
            
        while cnt != self.d + 2:
            square = Square(cnt)
            mat = square.generate()
                
            if len(mat) < self.d:
                diff = len(mat) - self.d
                square.mat = extend_center(mat, diff)
            
            res.append(square)
            cnt += 2
            
        self.layers = res
            
        return self.layers

    
    
    
                   
            
            
            
            
    
    
    

    
    
        
        
    
