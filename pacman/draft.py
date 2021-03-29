import random
import matplotlib.pyplot as plt
import time
import timeit


class TimerError(Exception):
    """A custom exception used to report errors in use of Timer class"""
    
class Timer:
    def __init__(self):
        self._start_time = None

    def start(self):
        """Start a new timer"""
        if self._start_time is not None:
            raise TimerError(f"Timer is running. Use .stop() to stop it")

        self._start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and report the elapsed time"""
        if self._start_time is None:
            raise TimerError(f"Timer is not running. Use .start() to start it")

        elapsed_time = time.perf_counter() - self._start_time
        self._start_time = None
        print(f"Elapsed time: {elapsed_time:0.4f} seconds")


def generate_list(size: int, max: int): 
    # this function generates a list of random numbers with given limit, and max size
    return [random.randint(0, max) for _ in range (size)]

def elapsed_sec(function, toofast=0.05):
    # this function is taken from one of the class notes
    n = 1
    while True:
        start_time = time.time()              # start timer
        for i in range(n):
            function()
        seconds = time.time() - start_time    # stop timer
        if seconds > toofast:
            return seconds/n
        else:
            n *= 2


def merge_sort (unsorted_list):
    t = Timer()
    t.start()
    if len(unsorted_list) > 1: # if the list size is bigger than one, we have to divide it 
        middle = len(unsorted_list) // 2
        left = unsorted_list[:middle] # left list starts as it is and ends in the middle
        right = unsorted_list[middle:] # right list starts in the middle and ends as it is
        
        merge_sort(left) # first we need to merge sort right and left lists separately, 
        merge_sort(right) # dividing them by 2 until each list has only one element
        
        i = j = k = 0 # i for left, j for right, k for the general list 
        
        while i < len(left) and j < len(right): # this part will merge the two final lists into one and sort it
            if left[i] <= right[j]:
                unsorted_list[k]=left[i]
                i=i+1
            else:
                unsorted_list[k]=right[j]
                j=j+1
            k=k+1

        while i < len(left): # this part sorts the left parts of the list
            unsorted_list[k]=left[i]
            i=i+1
            k=k+1

        while j < len(right): # and this part sorts the right parts of the list 
            unsorted_list[k]=right[j]
            j=j+1
            k=k+1
        t.stop()


unsorted_list = generate_list(100, 1000) # generate a random list of size 100 with max value 1000
merge_sort(unsorted_list)