import numpy as np
from numpy import exp, sqrt, log as ln, log10 as log
import matplotlib.pyplot as plt
from matplotlib.ticker import AutoMinorLocator, ScalarFormatter
from scipy import stats
from scipy.optimize import curve_fit
import openpyxl
from matplotlib.backends.backend_pdf import PdfPages

from ME_utils import *
from saturation import *

def basic_plot(nation, Year, Q, gr, avg, r_u='', Qh='', Q0='',
               loc_top='best', loc_bot='best', loc_title=[0.6,0.2],
               future=None, top_axis=False, dn=None, 
               r_model_mixed=None, model_r=None, model_Q=None, 
               POP=False, linear=False, gdppc=False):
    def baseline(fig, y):
        '''Plot a thin x-axis at y
        '''
        fig.plot(x_range, (y,y), color='lightgrey', lw=0.7)
    
    if top_axis: t_axis = t_from_yr(future, r_u)
    
    if POP:
        Title  = nation+' Population'
        y_left = 'Population/Population(%i)'%Year[0]
        dollar = ''        
    elif gdppc:
        Title  = nation+' GDP per Capita'
        y_left = 'GDPPC/GDPPC(%i)'%Year[0]
        dollar = '\$'
        GDP_   = 'GDPPC'               
    else:
        Title  = nation+' GDP'
        y_left = 'GDP/GDP(%i)'%Year[0]
        dollar = '\$'        
        GDP_   = 'GDP'               
    model_color = 'Red'
    data_color  = 'grey'
    #time range of plots:
    x0 = Year[0]
    x1 = Year[-1] if future is None else future[-1]
    x_range = (x0, x1)

    if model_Q is None:        
        Fig, (top, bot) = plt.subplots(2,1, sharex=True, figsize=(8, 7))
        figs = [top, bot]
    else:
        Fig, (top, mid, bot) = plt.subplots(3,1, sharex=True, figsize=(8, 10))
        figs = [top, mid, bot]
        
    Fig.suptitle(Title,fontsize=fontsize+8)     
    bot.set_xlabel('Year')
    for fig in figs:
        fig.set_xlim(x_range)
        fig.xaxis.set_minor_locator(AutoMinorLocator())
        if fig is not bot: plt.setp(fig.get_xticklabels(), visible=False)
    #plt.setp([fig.get_xticklabels() for fig in figs[:-1]], visible=False)

    #top: plot GDP/POP, data and model when supplied
    top.set_ylabel(y_left)
    if linear: 
       top.set_yscale('linear')
       top.yaxis.set_minor_locator(AutoMinorLocator())
       txt = 'Linear Growth Model'     
       top.text(loc_title[0],loc_title[1],txt,transform=top.transAxes)
    else:
       top.set_yscale('log')   
    # mark the right y-axis with actual, not normalized, Q
    # do that through phantom plot of Q:
    ax1 = top.twinx()
    ax1.set_xlim(x_range)
    if linear:
       ax1.set_yscale('linear')
       ax1.yaxis.set_minor_locator(AutoMinorLocator())
    else:
       ax1.set_yscale('log')
    #Scale out powers of 10 to get nicer unit for the axis
    i = int(log(np.amax(Q)))//3 if model_Q is None else int(log(np.amax(model_Q)))//3 
    s = 'thousand' if i==1 else('million' if i==2 else ('billion' if i==3 else 'trillion'))   
    y_right = 'Population (%s)'%s if POP else GDP_ +' (%s 2010 USD)'%s
    ax1.set_ylabel(y_right)
    if model_Q is None:
        x_ = Year
        y_ = Q/10.**(3*i)
    else:
        x_ = future
        y_ = model_Q/10.**(3*i)
    ax1.plot(x_, y_, lw=0) #phantom plot; generates only right axis marking 
    
    #plot the data:
    lns1 = top.plot(Year, Q/Q[0], color=data_color, label='data')
    #plot the model; first get labels:
    model = 'model'   
    if linear:
        model += ': r$_0$ = %3.2f'%r_u + '%/yr'
        #list Q_0 using scientific notation with 1 decimal digit
        model+= ', Q$_0$ = %s'%pwr10(Qh,1) + dollar
    if top_axis:
        ax2 = top.twiny()                    #generate top x-axis, label tau = r_u*t      
        ax2.set_xlabel(r'$r_u$' + '(Year - %i)'%Year[0])
        ax2.set_xlim(t_axis[0], t_axis[-1])
        ax2.xaxis.set_minor_locator(AutoMinorLocator())        
        model += ': r$_u$ = %3.2f'%r_u + '%/yr'
        if Q0: model += ', Q$_0$/Q(0) = %.1g' %(Q0/Q[0])
        #list Qh only if there's meaningful hindering
        if Q[-1]/Qh > 1.E-3:  #smaller Qf/Qh means pure exponential growth; no hindering
            model += ', Q$_h$ = %s'%(pwr10(Qh,1) + dollar)
    #and now plot:
    if model_Q is None:
        lns2 = None
    else:
        lns2 = top.plot(future, model_Q/Q[0], color=model_color, label=model)
    lns = lns1 if lns2 is None else lns1+lns2
    #and now the legend:
    labls = [l.get_label() for l in lns]
    top.legend(lns, labls, loc=loc_top, handlelength=2, labelspacing=0.15)

    #mid: ratio, data/model:
    if model_Q is not None:
        ratio = Q/(model_Q[:len(Year)])
        mid.set_ylim(0, 2) 
        mid.yaxis.set_minor_locator(AutoMinorLocator())
        s = 'population' if POP else GDP_         
        mid.plot(Year, ratio, label='ratio: %s data/model'%s) 
        mid.legend()
        #baseline at ratio = 1:
        baseline(mid, 1)

    #bot: Growth rate plot:
    bot.set_ylabel('growth rate (%/yr)')
    bot.set_ylim(np.amin(gr)-1., np.amax(gr)+1)
    bot.yaxis.set_minor_locator(AutoMinorLocator())    
    bot.plot(Year, gr, color=data_color, lw=1.5, label='data') #plot the data
    if future is None:  #plot running average when not modeling
        bot.plot(Year[1:], avg, label='running average')
    else:
        #plot the model
        bot.plot(future, model_r, color=model_color, label='model')
        if r_model_mixed is not None: #and the mixed model, if supplied
            bot.plot(Year, r_model_mixed, color='goldenrod', label='hybrid model')
    if dn > 0:    #plot moving averages
        yr_avg, gr_avg = calc_mov_avg(Year, gr, dn)      
        bot.plot(yr_avg, gr_avg, label='%i-yr rolling avg'%dn)
    bot.legend(loc=loc_bot)
    #baseline at 0 growth rate:
    baseline(bot, 0)
    
    top = 0.88 if top_axis else 0.93
    Fig.subplots_adjust(left=0.12,right=0.88, 
                        bottom=0.08, hspace=0.02, 
                        wspace=0.02, top=top)
    return Fig


def gr_data(Q, Year):
    """Annual growth rate in %
    and its running average
    """   
    gr = (100./Q)*np.gradient(Q, Year)
    avg  = np.zeros(len(gr) - 1)
    for i in range(len(gr) - 1): 
        avg[i] = np.average(gr[:i+1])
    return gr, avg


def calc_mov_avg(Year, gr, dn):
    yr_avg, _ = moving_average(Year, dn)
    gr_avg, _ = moving_average(gr, dn)
    return yr_avg, gr_avg    


def t_from_yr(Year, r0): 
    """ Transform a range of calendar years to
    time equivalent of unsaturated tau from rate
    r0 in percents
    """
    return r0*1.E-2*(Year - Year[0])

def fitting(nation, Q, Year, p0='', gdp=True, mode='sat', gdppc=False):
    '''Fit the data to one of the following models:
    '''
    #2-parameter saturation model:
    def func(yr, r0, qs):                       
        t = t_from_yr(yr, r0)                   
        q = q_from_t(t, qs)                     
        return q                                
                                               
    #3-parameter saturation model:
    def func3param(yr, r0, qs, q0):             
        t = t_from_yr(yr, r0)                   
        q = q_from_t(t, qs, q0)                 
        return q                                
                                                
    #linear model:
    def linear(y, a, b): return a + b*(y - y[0])

    modes = ['sat', 'sat3par', 'lin']
    #The modes fitting functions:
    F = {'sat':func, 'sat3par':func3param, 'lin':linear }
    header = {'sat': '2-parameter fit [ru, qh]:',\
          'sat3par': '3-parameter fit [ru, qh, q0]:',\
              'lin': 'Fitting with linear model:   Q = Q0*(1 + r0*t)'}

    if not mode in modes:
        print '***Unrecognized fitting mode:', mode
        print '   recognized modes for fitting are', modes
        return

    G_ = 'GDP per capita ' if gdppc else 'GDP '
    R = Q[-1]/Q[0]
    print '%s: %i data points'%(nation, len(Year))
    s = G_ +'has grown from %6.2E($10) in %i to %6.2E($10) in %i' if gdp else\
        'Population has grown from %6.2E in %i to %6.2E in %i'
    print s %(Q[0], Year[0], Q[-1], Year[-1])
    print 'an increase by factor of %.2g' % R
    print '\n***', header[mode]
    s = ' Initial guess --- '
    #Controll printing of p0 with .join()
    #remove the final coma with the mask [:-1]
    s += 'None' if not p0 else\
      '['+' '.join(['%.3E,' %p for p in p0])[:-1]+']'
    print s 
    try:       
        q = Q/Q[0]
        #do the fitting:
        if p0:
            popt, pcov = curve_fit(F[mode], Year, q, p0=p0, bounds=(0, np.inf))
        else:
            popt, pcov = curve_fit(F[mode], Year, q, bounds=(0, np.inf))
        perr = np.sqrt(np.diag(pcov))/popt       #the relative errors of fitting params
        future  = np.arange(Year[0], 2051)       #the best-fitting model
        Q_model = Q[0]*F[mode](future,*popt)     
        err = 100*abs(q/F[mode](Year,*popt) - 1) #and its errors
        #assign the fitting parameters and finish the solution:
        Q0 = ''
        if mode == 'lin':
            '''The function is a + b*t = G0(1 + r0*t)
               Becuse we solve in q, the returned parameters are:
                 a  = popt[0] = G0/Q[0]       
                 r0 = b/a = popt[1]/popt[0]
            '''
            Q_h = popt[0]*Q[0]        #this is G0
            r0  = popt[1]/popt[0]     #this is r0
            r_u = 100*r0              #r0 in percent
            r_model = r_u*Q_h/Q_model
            gr  = r0*Q_h        #=r0*G0, the annual increase 
        else:
            r_u = popt[0]
            qs  = popt[1]
            Q_h = qs*Q[0]
            if mode == 'sat3par':
                q0  = popt[2]
                Q0  = q0*Q[0]        
            r_model = r_from_q(r_u, Q_h, Q_model)
            tau = t_from_yr(Year, r_u)[-1]
            H = (R - 1)/(qs*ln(R))

        print ' Final result  --- ['+' '.join(['%.3E,' %p for p in popt])[:-1]+']'
        print '*** Best-fit parameters:'
        if mode=='lin':
            s = 'Q0 = %5.2E 2010USD'%Q_h if gdp else 'Q0 = %5.2E'%Q_h           
            print '   r0 = %3.2f'%r_u +  ' %/year    ' +  s
            s = '   '+G_ +'increasses by %.2E USD10 per year' if gdp else\
                '   Population increasses by %.2E per year'
            print s%gr    
            print '  Relative errors of fitting parameters:\n'+\
                  '   err(r0) = %5.2E   err(G0)= %5.2E'%(perr[0], perr[1])
        else:
            print '   ru = %3.2f'%r_u+'%      unhindered (unsaturated) growth rate'
            s = '   Qh = %5.2E   Hindering (saturation) '+G_ +'in 2010USD \n' if gdp else\
                '   Qh = %5.2E   Hindering (saturation) population \n'
            print s%Q_h,
            if mode == 'sat3par':
                print '   Q0 = %5.2E = %5.2E Q[0]'%(Q0, Q0/Q[0])
            print '   qh = Qh/Q0 = %5.2E' % qs
            print '  Relative errors of fitting parameters:'
            print   '   err(ru) = %5.2E'%perr[0]
            print   '   err(Qh) = %5.2E'%perr[1]       
            if mode == 'sat3par': print '   err(Q0) = %5.2E'%perr[2]
            print '***Data covers a range of %.2f growth times'%tau
            print '***Hindering paramater H = %.3E' %H
            print '   Hindering degree Qf/Qh = %.3G' %(Q[-1]/Q_h)
            X = 3*' '
            if Q_h < Q[0]:
                print X+'Hindering threshold (Q > Qh) was crossed before', Year[0]
            elif Q[0] < Q_h and Q_h < Q[-1]:
                y1 = np.where(Q > Q_h)[0][0]
                print X+'Hindering threshold (Q > Qh) crossed in', Year[y1]
            elif Q_h > Q[-1] and Q_h < Q_model[-1]:
                y1 = np.where(Q_model > Q_h)[0][0]
                print X+'Hindering threshold (Q > Qh) will be crossed in', future[y1]
            if (Q[-1]/Q_h) > 1.E-3:
                s = 'USD10 per year' if gdp else 'per year'
                print X+'Hindered growth mode has a rate of %.3G '%(1.e-2*r_u*Q_h)+s
                           
            

        print '***Average deviation of model from data is %4.2f'\
                %(np.average(err))+'%'
        print '   largest deviation of model from data is %4.2f'\
                %(np.amax(err))+'%' + ' in %i'%Year[np.argmax(err)]
        
        s = '\n***Model predictions for %i for %s economy:' if gdp else\
            '\n***Model predictions for %i for %s population:'
        print s%(future[-1],nation)
        s = '   '+G_ +'of %4.2E $10 and annual growth rate %3.2f' if gdp else\
            '   Population of %4.2E and annual growth rate %3.2f'
        print s %(Q_model[-1],r_model[-1])+'%'   
        print '\n', 70*'_','\n'
        return r_u, Q_h, Q0, future, Q_model, r_model
    except Exception as ex:
        print(ex)
        print 'Failed to fit the data for', nation
        print '\n', 70*'_','\n'
        return


def tabulate(Q, Year, future, Q_model):  
    print '\nYear     Model   population    ratio'
    for n in range(len(future)):       
        str = '%4i   %5.2E'%(future[n], Q_model[n])
        if n < len(Year): 
            str += 2*'   %5.2E' %(Q[n], Q[n]/Q_model[n])
        print str

