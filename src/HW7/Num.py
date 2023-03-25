##
# Import the math class
#
# Defines a class "Num" which represents a stream of numbers. The class has
# methods to track mean, standard deviation, lowest, and
# highest numbers in the stream, and the number of items seen.
#
# The "add" method implements the reservoir sampling algorithm which is
# used to update the mean, standard deviation, etc...
# based on a new value "n".
#
# The "mid" method returns the mean of the numbers seen so
# far.
#
# The "div" method returns the standard deviation.
##
class Num():

    def __init__(self, t=[]) -> None:
        self.n = 0
        self.mu = 0
        self.m2 = 0
        self.sd = 0
        for x in t:
            self.add(x)


    ##
    # Adds x and updates mean and standard deviation.
    ##
    def add(self, x):
        self.n += 1
        d = x - self.mu
        self.mu = self.mu + d/self.n
        self.m2 = self.m2 + d*(x-self.mu)
        self.sd = 0 if self.n<2 else (self.m2/(self.n - 1))**0.5

