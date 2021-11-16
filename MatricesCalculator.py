"""
Matrix calculator V2

Created - 16/03/19
By Jonas Ganderton

Current methods:
- Create random data within a matrix
- Create identity matrix
- Conformability
- Similar
- Multiply
- Add
- Subtract
- Dot product
- Magnitude
- Determinant
- Angle between
- Singular
- Transpose
- Inverse of an nxn with 1/det outside
- Inverse of an nxn with 1/det within
- Cofactor
- Rotation between 0 and 180 degrees
"""

from math import sqrt, acos, degrees, cos, sin, radians
from random import randint
from copy import deepcopy


class Matrix:
    """
    a = Matrix(rows, columns, data)

    e.g a = Matrix(2,3,0,1,2,3,4,5)
    a.mat = | 0 1 2 |
            | 3 4 5 |
    """

    def __init__(self, rows, columns, *data):
        self.rows = rows
        self.columns = columns
        self.empty()
        try:
            if data[0] == "r":
                self.randomfill()
            elif data[0] == "i":
                self.identity()
            else:
                self.fillMatrix(data)
        except IndexError:
            self.fillMatrix(data)

    def empty(self):
        self.mat = []
        for r in range(self.rows):
            temp = []
            for c in range(self.columns):
                temp.append(0)
            self.mat.append(temp)

    def identity(self):
        if self.rows == self.columns:
            for r in range(self.rows):
                self.mat[r][r] = 1
        else:
            print("Matrix isn't square, can't be identity")

    def fillMatrix(self, data):
        """
        Matrix is filled up with given data
        If too much data the excess is discarded
        If too little data the remainder is filled with zeros
        If no data then the matrix will be only zeros (shell for result matrix)
        """
        i = 0
        length = len(data)
        for r in range(self.rows):
            for c in range(self.columns):
                if i >= length:
                    num = 0
                else:
                    num = data[i]
                self.mat[r][c] = num
                i += 1

    def randomfill(self):
        """
        Fill matrix with random numbers from -10 to 10
        """
        for r in range(self.rows):
            for c in range(self.columns):
                self.mat[r][c] = randint(-10, 10)

    def copy(self):
        return deepcopy(self)

    def out1(self):
        for r in range(self.rows):
            print("|", end=" ")
            for c in range(self.columns):
                print(self.mat[r][c], end=" ")
            print("|")
        print()

    def out(self):
        length = 0
        for r in range(self.rows):
            for c in range(self.columns):
                if len(str(self.mat[r][c])) > length:
                    length = len(str(self.mat[r][c]))

        string = "".join(["{:^", str(length), "}"])  # Work here

        """
        {: d} = lines up +'ve and -'ve numbers
        {:^str(length)} = padding in total length of 8
        """

        for r in range(self.rows):
            print("|", end=" ")
            for c in range(self.columns):
                num = self.mat[r][c]
                if num >= 0:
                    num = " " + str(num)
                print(string.format(num), end=" ")
            print("|")
        print()

    # Other methods
    def conformability(self, other):
        """
        Checks to see if the dimensions would work for certain operations
        """
        if self.columns == other.rows:
            return True
        else:
            return False

    def similar(self, other):
        """
        Checks if they have the same dimensions
        """
        if self.rows == other.rows and self.columns == other.columns:
            return True
        else:
            return False

    def multiply(self, other):
        works = self.conformability(other)
        if works:
            result = Matrix(self.rows, other.columns)
            for r in range(self.rows):
                for c in range(self.columns):
                    for x in range(other.columns):
                        result.mat[r][x] += self.mat[r][c] * other.mat[c][x]
            result.out()
        else:
            print("Matrices don't conform for multiplication")

    def add(self, other):
        works = self.similar(other)
        if works:
            result = Matrix(self.rows, self. columns)
            for r in range(self.rows):
                for c in range(self.columns):
                    result.mat[r][c] = self.mat[r][c] + other.mat[r][c]
            result.out()
        else:
            print("Matrices are different dimensions, can't be added")

    def sub(self, other):
        works = self.similar(other)
        if works:
            result = Matrix(self.rows, self. columns)
            for r in range(self.rows):
                for c in range(self.columns):
                    result.mat[r][c] = self.mat[r][c] - other.mat[r][c]
            result.out()
        else:
            print("Matrices are different dimensions, can't be subtracted")

    def dotProduct(self, other):
        # For vectors only
        if self.columns == other.columns == 1 and self.rows == other.rows:
            product = 0
            for i in range(len(self.mat)):
                product += self.mat[i][0] * other.mat[i][0]
            return product
        else:
            print("One or both matrices aren't vectors")

    def magnitude(self):
        # For vectors only
        if self.columns == 1:
            sum = 0
            for i in range(self.rows):
                sum += self.mat[i][0] ** 2
            mag = sqrt(sum)
            return mag
        else:
            print("Not vector")
            return False

    def angleBetween(self, other):
        try:
            angle = self.dotProduct(other) / (self.magnitude() * other.magnitude())
            angle = acos(angle)
            # Converts from radians into degrees
            angle = degrees(angle)
            # If loop changes to find the acute angle
            if angle > 90:
                angle = 180 - angle
            return angle
        except TypeError:
            print("Can't find angle")

    def determinant(self):
        # For 2x2 Matrix
        if self.rows == self.columns == 2:
            det = self.mat[0][0] * self.mat[1][1] - self.mat[0][1] * self.mat[1][0]
            return det
        # Making an nxn smaller (using recursion until it is 2x2)
        elif self.rows == self.columns:
            det = 0
            for i in range(self.columns):  # Defines the pivot column
                # Creates a new matrix by value, if done as temp = self it is passed by reference
                temp = self.copy()
                del temp.mat[0]  # Deletes the top row
                temp.rows -= 1
                for u in range(temp.rows):
                    del temp.mat[u][i]  # Deletes all items in the pivot column
                temp.columns -= 1
                # Alternate bewtween add and subtract, add first
                if i % 2 == 0:
                    det += self.mat[0][i] * temp.determinant()
                elif i % 2 == 1:
                    det -= self.mat[0][i] * temp.determinant()
            return det
        else:
            print("Unequal columns and rows, can't find determinant")

    def singular(self):
        if self.determinant() == 0:
            return True
        else:
            return False

    def inverse(self):  # Introduce 1/determinant infront of the inverse
        if self.singular():
            print("Matrix is singular and has no inverse")
        elif self.rows == 2:
            return self.inverse2d()
        else:
            return self.inverseN()

    def inverse2d(self):
        det = self.determinant()
        result = Matrix(self.rows, self.columns)
        # Swap top left and bottom right, other two become the opposite sign
        result.mat[0][0] = self.mat[1][1]
        result.mat[1][1] = self.mat[0][0]
        result.mat[0][1] = -1 * self.mat[0][1]
        result.mat[1][0] = -1 * self.mat[1][0]
        print("1/(" + str(det) + ")")  # 1/determinant
        result.out()
        return result

    def inverseN(self):
        """
        Work out the cofactor of each item
        Replace each item with it's cofactor
        Transpose
        Put 1/determinant at the front
        """
        result = Matrix(self.rows, self.columns)
        for r in range(self.rows):
            for c in range(self.columns):
                result.mat[r][c] = self.cofactor(r, c)
        result.out()
        result = result.transpose()
        det = self.determinant()
        print("1/(" + str(det) + ")")
        result.out()
        return result

    def inverseDetIn(self):
        "Has the determinant within the matrix rather than as a fraction"
        if self.singular():
            print("Matrix is singular and has no inverse")
        elif self.rows == 2:
            self.inverse2dIn()
        else:
            self.inverseNIn()

    def inverse2dIn(self):
        det = 1 / self.determinant()
        result = Matrix(self.rows, self.columns)
        # Swap top left and bottom right, other two become the opposite sign
        result.mat[0][0] = det * self.mat[1][1]
        result.mat[1][1] = det * self.mat[0][0]
        result.mat[0][1] = det * -1 * self.mat[0][1]
        result.mat[1][0] = det * -1 * self.mat[1][0]
        result.out()

    def inverseNIn(self):
        result = Matrix(self.rows, self.columns)
        det = 1 / self.determinant()
        for r in range(self.rows):
            for c in range(self.columns):
                result.mat[r][c] = round(self.cofactor(r, c) * det, 5)
        result.transpose()
        result.out()
        return result

    def cofactor(self, row, column):
        temp = self.copy()
        del temp.mat[row]
        temp.rows -= 1
        for r in range(temp.rows):
            del temp.mat[r][column]
        temp.columns -= 1
        det = temp.determinant()
        if column % 2 == 1 and row % 2 == 0 or column % 2 == 0 and row % 2 == 1:
            det = det * (-1)
        return det

    def transpose(self):
        # Swap rows and columns
        result = Matrix(self.columns, self.rows)
        for r in range(self.rows):
            for c in range(self.columns):
                result.mat[c][r] = self.mat[r][c]
        return result

    def rotation(self):
        # Only works for angles between 0 and 180 (graph repeats and is symetrical)
        num = self.mat[0][0]
        if num <= 1 and num >= -1:
            num = degrees(acos(num))
            return num
        else:
            print("Not a rotation between 0 and 180 degrees")

    def rotation2dDeg(self, angle, unit):
        "Creates Matrix given a rotation"
        if unit == "deg":
            angle = radians(angle)
        elif unit == "rad":
            pass
        else:
            print("unknown unit")
            return self

        self.mat[0][0] = round(cos(angle), 3)
        self.mat[0][1] = round(-sin(angle), 3)
        self.mat[1][0] = round(sin(angle), 3)
        self.mat[1][1] = round(cos(angle), 3)
        return self


a = Matrix(3, 1, 1, 0, -2)
b = Matrix(3, 1, -2, 3, -3)
print(a.angleBetween(b))
