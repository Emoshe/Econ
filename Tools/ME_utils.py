import re
import pandas
import numpy as np
from numpy import exp, sqrt, log as ln, log10 as log
import matplotlib.pyplot as plt
from matplotlib.ticker import NullFormatter, MaxNLocator, AutoMinorLocator, MultipleLocator, FixedLocator 

# plotting setup: 
fontsize = 14; l_tick = 6
plt.rcParams['lines.linewidth'] = 2
plt.rcParams['font.size'] =  fontsize
plt.rcParams['axes.labelsize'] = fontsize + 2
plt.rcParams['legend.fontsize'] = fontsize - 2
plt.rcParams['xtick.labelsize'] = fontsize
plt.rcParams['ytick.labelsize'] = fontsize
plt.rcParams['axes.linewidth'] = 1.
plt.rcParams['xtick.direction'] = 'in'
plt.rcParams['ytick.direction'] = 'in'
plt.rcParams['xtick.top'] = True
plt.rcParams['ytick.right'] = True
plt.rcParams['xtick.major.size'] = l_tick   # major tick size in points
plt.rcParams['xtick.minor.size'] = l_tick-2 # minor tick size in points
plt.rcParams['ytick.major.size'] = l_tick   # major tick size in points
plt.rcParams['ytick.minor.size'] = l_tick-2 # minor tick size in points
plt.rcParams['legend.handlelength'] = 4     # line lengths in legends
plt.rcParams['legend.frameon'] = False 
plt.rcParams['mathtext.default'] = 'default' 
# color sequence for multi-plots:
color = ['DarkBlue','Red','DarkGreen','DarkMagenta','DarkGoldenRod','DarkOrange','Green']

def even(x): return x%2 == 0
def  odd(x): return x%2 == 1

def is_number(x):
    try:
        f = float(x)
        return True
    except ValueError:
        return False    

def print2file(outfile):
    """ Direct printing to new file named outfile
    the virtual file is returned in out
    to return to screen printing use close_it(out)
    """
    print '***Printing diverted to file ', outfile
    out = open(outfile,'w');   
    sys.stdout = out
    return out

def close_it(out):
    """Before calling, make sure 'out' is defined
    if not as a file then as out = None
    """
    try:
        out.close()
        sys.stdout = sys.__stdout__      
    except:
        return

# Two versions for calculating moving averages:
def moving_average(data_set, frame):
    """ Moving average and standard deviation of data for given frame size
    Uses convolution with uniform weight 1/frame_size. The 'valid' option
    ensures there are no edge effcts; only elements where data_set and frame 
    fully overlap are returned
    """
    window = np.ones(int(frame))/float(frame)
    sma  = np.convolve(data_set, window, 'valid')
    sma2 = np.convolve(data_set**2, window, 'valid')
    std  = np.sqrt(sma2 - sma**2)
    return sma, std
    
def rolling_avg(data_set, frame):
    """ Moving average and standard deviation of data for given frame size
    Uses the procedure rolling_mean from the Pandas package; only elements 
    where data_set and frame fully overlap are returned
    """
    sma  = pandas.rolling_mean(data_set, frame)[frame-1:]
    sma2 = pandas.rolling_mean(data_set**2, frame)[frame-1:]
    std  = np.sqrt(sma2 - sma**2)
    return sma, std    


def alphanum(s):
    """Split a string s into a list of integers and non-int-able substrings.
    Example: './T200/SLED_nE6_T200.out' --> ['./T', 200, '/SLED_nE', 6, '_T', 200, '.out']
    ****** This is from Robert
    """
    def getint(s):  # tries to convert a substring s into an integer
        try:
            return int(s)
        except:
            return s

    # List comprehension; takes a string s and splits it on digit groups
    return [ getint(c) for c in re.split('([0-9]+)', s) ] 


def get_to_next(st, in_file, after=''):
    """Get next line that starts with string 'st' from already open in_file; 
    optionally after the first occurence of a line starting with 'after' 
    """    
    line = ''
    if after:    #returns False for empty string 
       while not line.startswith(after):
         line = in_file.readline().strip()          
    while not line.startswith(st): 
       line = in_file.readline().strip()# read a line as string, strip all whitespace from head and tail       
    return line


def smaller_of(x, y, p):
    """ Smooth version of min(x,y)
    p (> 0) controlls the transition abruptness; 
    as p increases it aproaches the min function
    """
    return x*y/(x**p + y**p)**(1./p)         


def smallest_in(a, p):
    """ Smooth version of min(a0,a1,a2...)
    p (> 0) controlls the transition abruptness; 
    as p increases it aproaches the min function
    """
    if np.any(a[:]==0): return 0
    s = sum((1./np.array(a))**p)
    return 1./s**(1./p)         


def pwr10(x, d=0):
    """ Return a tex string with scientific notation of the number
        d is the number of decimal digits printed
        when d = 0, the number is printed as entered (default)
    """
    def single(x):#this is where the actual work is done
        pwr = int(log(abs(x)))
        num = x/10.**pwr
        s = '10^{%i}'%pwr
        if num != 1: #then need to add the number in front of 10^pwr
            n = str(num) if d == 0 else '%.*f'%(d,num)
            s = n+'x'+s
        return '$'+s+'$'
    try:
        len(x)
    except:
        return single(x)
    return [single(x_) for x_ in x]

if __name__ == '__main__':

    x = np.pi*1.E43
    print x
    print pwr10(x)
    print pwr10(x, 1)
    print pwr10(x, 2)
    print pwr10(x, 3)
    print pwr10(x, 4)
    print
    a = [1.E15, 3.24E-17, -6.2345E44]
    print a
    print pwr10(a)
    print pwr10(a, 1)
    print pwr10(a, 2)
    print pwr10(a, 3)
    print pwr10(a, 4)

    sys.exit()
    
    a = range(5,50)
    plist = range(1,50)
    fmt = '%3d %12.4f'
    print '\n  p  smallest_in(a)'
    for p in plist:
        print fmt %(p, smallest_in(a, p))
    
    
    