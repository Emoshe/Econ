#   Solve the equation ln(q/q0) + (q - q0)/q_s = t

import numpy as np
from numpy import exp, sqrt, log as ln, log10 as log
from ME_utils import *

def q_from_t(t, qs, q0=1, eps=1.E-4):
    """Enter with t-array; t[0] = 0 or close to it 
       Get the solution q for
        ln(q/q0) + (q - q0)/q_s = t
    """
                    
    def Solve(t, apr, qs, q0, eps):
        """Here's where we solve using
           Newton's method
        """
        q = apr #initial guess
        check = 1.
        while check > eps:
            f = ln(q/q0) + (q - q0)/qs - t
            dq = f/(1./q + 1./qs)   # = f/f'
            q = q - dq
            check = abs(f) + abs(dq/q)
        return q    
    
    apr = q0    
    q = np.ones(len(t))
    for i, t_ in enumerate(t):
        q[i] = Solve(t_, apr, qs, q0, eps)
        apr = q[i]
    
    return q
   
def r_from_q(ro, qs, q):
    """ Modeling GDP hindered (saturate) growth:
    r0 is the unhidered (unsaturated) growth rate
    qs is the hindering (saturation) GDP
    q is the input quantity, same unit as qs 
    """
    return ro/(1. + q/qs)


if __name__ == '__main__':
    outfile = ''
    #outfile = 'Saturation_Solution.dat'
    out = print2file(outfile) if outfile else None
    eps = 1.e-4
    print "    ******* General Saturation Model ******\n"
    print 'Solution of \n'
    print '   ln(q/q0) + (q - q0)/qs = t \n'
    print 'for q as function of t with q0 and qs as parameters\n'
    

    
    for n in range(1, 11):
        qs = 10**n   
        T  = range(int(5*ln(qs)))
        print 48*'*'
        #for q0 in [1]:
        for q0 in np.concatenate((np.arange(.1,1,.1), np.arange(1,11))):
            #print q0
            #sys.exit()    
            
            Q  = q_from_t(T, qs, q0) 
            #print "\n  qs = %5.2E  ln(qs) = %4.2f"%(qs, ln(qs))
            print "\n  qs = %5.2E  ln(qs) = %4.2f    q0 = %.2g"%(qs, ln(qs), q0)
            print 
            print "   t       q       t(q)     t/t(q)"
            print 
            
            for i, t in enumerate(T):
                q  = Q[i]
                t_ = ln(q/q0) + (q - q0)/qs
                str = '%4i   %5.2E   %5.2f'%(t, q, t_)
                if t > 0: str = str + '   %6.4f'%(t_/t) 
                print str
            
    close_it(out)
    print '*** Done!'
    
    
    