# Sym's summarize a stream of symbols.
from collections import defaultdict
import math

##
# Import math and collections from defaultdict
#
# Defines a class named Sym that summarizes a stream of symbols. The class
# provides methods to add new symbols to the stream, and to calculate the
# mode (most common symbol) and diversity of the symbols in the stream. The # Sym class has two instance variables.
#
# num_items: Keeps track of the number of symbols processed so far.
#
# has: A defaultdict that keeps track of the frequency of each symbol that
# has been seen.
#
# The add method takes a symbol value as input and increments the frequency
# count of that symbol in the has dictionary. The method also increments
# the num_items variable.
#
# The mid method calculates the mode of the symbols in the stream. It
# iterates over the has dictionary and keeps track of the symbol with the
# highest frequency count. The method returns the mode.
#
# The div method calculates the diversity of the symbols in the stream. It
# uses the entropy formula to calculate the diversity. The method takes an
# optional argument e which is used as an accumulator for the diversity
# calculation. The method returns the diversity, which is -e in the case of
# Sym.
##
class Sym:
    def __init__(self, at=0, txt=""):
        self.at = at
        self.txt = txt
        
        self.n = 0
        self.has = {}
        self.most = 0
        self.mode = None

    ##
    # Add symbol value to Sym object
    #
    # Defines a method add. The method takes a single argument, value
    #
    # The method first checks if the input value is not equal to "?". If
    # the value is not equal to "?"
    # It increments the num_items (number of symbols processed) by 1.
    # Increments the frequency count of the value in the 'has' defaultdict # by 1.
    ##
    def add(self, value):

        ##
        # If value is not equal to "?", the method proceeds to update the
        # counts.
        #
        # The line self.num_items += 1 increments the count by 1.
        #
        # The second if increments the count of the value in a dictionary
        # self.has. Returns the value of self.has[value] if it exists, or 0
        # if it doesn't. Then adds 1 to the value returned. This increments
        # the count of the value in the dictionary self.has.
        ##
        if value != "?":
            if value != '?':
                self.n = self.n + 1
                if value in self.has:
                    self.has[value] = self.has[value] + 1
                else:
                    self.has[value] = 1
                ##
                # Updates the values of self.most and self.mode if the count of value in
                # self.has is greater than the current value of self.most. If this is the
                # case, self.most is set to the count of value, and self.mode is set to value.
                ##
                if self.has[value] > self.most:
                    self.most = self.has[value]
                    self.mode = value


    ##
    # Calculates the mode, most common symbol
    #
    # Defines a method mid. The method does not take any arguments.
    # The method returns the symbol that occurs most frequently among the
    # symbols processed so far by the add method.
    #
    # To do this it iterates over all the keys of the 'has' defaultdict,
    # which stores the frequencies of the symbols, and keep track of the
    # symbol with the highest frequency.
    #
    # mode is initialized to None and most is initialized to -1. For each
    # key in 'has', the count of the symbol is obtained from has[key] and
    # stored in sym_count. If count of symbol (sym_count) is greater than
    # most, the value of most is updated to sym_count and mode is updated
    # to key. After looping through all the keys, the final value of mode
    # is returned as the result.
    ##
    def mid(self):
        return self.mode

    ##
    # Calculate diversity, which is entropy in the case of Sym
    #
    # Defines a function "div". The function takes an
    # optional argument "e" with a default value of 0. The function also
    # defines another function "fun" which takes an argument "p" and
    # returns its logarithmic value to the base 2.
    #
    # Calculates the entropy of the distribution by looping over the values # in the "has" dictionary and updating the "e" value with the result of
    # "fun" divided by the number of items. The final result is the
    # negative of the "e" value.
    ##
    def div(self, e = 0):
        e = 0
        for i in self.has:
            p = self.has[i] / self.n
            e = e + (p * math.log(p, 2))
        return -e

    ##
    # Returns `n` unchanged (SYMs do not get rounded)
    ##
    def rnd(self, value):
        return value

    ##
    # Defined a function dis which take 3 arguments. i, s1 and s2.
    #
    # 1 if "s1" and "s2" are both equal to "?"
    # 0 if "s1" and "s2" are equal to each other
    # 1 if "s1" and "s2" are not equal to each other or not equal to "?"
    ##
    def dist(self, s1, s2):
        if s1 == "?" and s2 == "?":
            return 1
        elif s1 == s2:
            return 0
        else:
            return 1