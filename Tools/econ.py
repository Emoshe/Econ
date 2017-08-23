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
               POP=False, linear=False):
    plt.rc('legend', handlelength=2) # short legend lines
    
    if top_axis: t_axis = t_from_yr(future, r_u)
    if POP:
        Title  = nation+' Population'
        y_left = 'Population/Population(%i)'%Year[0]
        dollar = ''        
    else:
        Title  = nation+' GDP'
        y_left = 'GDP/GDP(%i)'%Year[0]
        dollar = '\$'        
    model_color = 'Red'
    data_color  = 'grey'
    #time range of plots:
    x0 = Year[0]
    x1 = Year[-1] if future is None else future[-1]
    x_range = (x0, x1)
    #for baseline plots:
    x_base = x_range
    lw_b = 0.7
    base_clr = 'lightgrey'

    Fig = plt.figure(figsize=(8, 10))
    Fig.suptitle(Title,fontsize=fontsize+8)     
    #Employ add_axes method for control of panel sizes
    #to have enough room to display both 
    #title and top axis, when needed
    width  = 0.7
    height = 0.27 if top_axis else 0.28
    x_left = 0.15
    y_bot  = 0.05
    dy = height+0.01
    bot = Fig.add_axes([x_left, y_bot,     width, height])
    mid = Fig.add_axes([x_left, y_bot+dy,  width, height])
    top = Fig.add_axes([x_left, y_bot+2*dy,width, height])
    figs = [top, mid, bot]
    for fig in figs:
        fig.set_xlim(x_range)
        fig.xaxis.set_minor_locator(AutoMinorLocator())
        if fig == figs[-1]:
            fig.set_xlabel('Year')
        else:
            fig.xaxis.set_major_formatter(NullFormatter())

    #top: plot GDP/POP, data and model when supplied
    top.set_ylabel(y_left)
    if linear: 
       top.set_yscale('linear')
       top.yaxis.set_minor_locator(AutoMinorLocator())
       txt = 'Linear Growth Model'     
       top.text(loc_title[0],loc_title[1],txt,transform=top.transAxes)
    else:
       top.set_yscale('log')
    lns1 = top.plot(Year, Q/Q[0], color=data_color, label='data')
    
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
    s = 'million' if i==2 else ('billion' if i==3 else 'trillion')
    y_right = 'Population (%s)'%s if POP else 'GDP (%s 2010 USD)'%s
    ax1.set_ylabel(y_right)
    if model_Q is None:
        x_ = Year
        y_ = Q/10.**(3*i)
    else:
        x_ = future
        y_ = model_Q/10.**(3*i)
    ax1.plot(x_, y_, lw=0) #phantom plot; generates only right axis marking 
    
    #plot the model:
    lns2 = None
    if linear:
        model = 'model: r$_0$ = %3.2f'%r_u + '%/yr,  '
        #list Q_0 using scientific notation with 1 decimal digit
        model+= 'Q$_0$ = %s'%pwr10(Qh,1) + dollar
        lns2 = top.plot(future, model_Q/Q[0], color=model_color, label=model)   
    if top_axis:
        ax2 = top.twiny()                    #generate top x-axis, label tau = r_u*t      
        ax2.set_xlabel(r'$r_u$' + '(Year - %i)'%Year[0])
        ax2.set_xlim(t_axis[0], t_axis[-1])
        ax2.xaxis.set_minor_locator(AutoMinorLocator())        
        model = 'model: r$_u$ = %3.2f'%r_u + '%/yr,  '
        if Q0: model += 'Q$_0$/Q(0) = %.1g, ' %(Q0/Q[0])
        #list Qh only if there's meaningful hindering
        if Q[-1]/Qh > 1.E-3:  #smaller Qf/Qh means pure exponential growth; no hindering
            model += ',  Q$_h$ = %s'%(pwr10(Qh,1) + dollar)
        lns2 = ax2.plot(t_axis, model_Q/Q[0], color=model_color, label=model)
    lns = lns1 if lns2 is None else lns1+lns2
    #and now the legend:
    labls = [l.get_label() for l in lns]
    top.legend(lns, labls, loc=loc_top)

    #mid: ratio, data/model:
    if model_Q is not None:
        ratio = Q/(model_Q[:len(Year)])
        mid.set_ylim(0, 2) 
        mid.yaxis.set_minor_locator(AutoMinorLocator())
        s = 'population' if POP else 'GDP'         
        mid.plot(Year, ratio, label='ratio: %s data/model'%s) 
        mid.legend()
        #baseline at ratio = 1:
        mid.plot(x_base, (1,1), color=base_clr, lw=lw_b)

    #bot: Growth rate plot:
    bot.set_ylabel('growth rate (%/yr)')
    bot.set_ylim(np.amin(gr)-1., np.amax(gr)+1)
    bot.yaxis.set_minor_locator(AutoMinorLocator())    
    bot.plot(Year[1:], gr, color=data_color, lw=1.5, label='data') #plot the data
    if future is None:  #plot running average when not modeling
        bot.plot(Year[2:], avg, label='running average')
    else:
        #plot the model
        bot.plot(future, model_r, color=model_color, label='model')
        if r_model_mixed is not None: #and the mixed model, if supplied
            bot.plot(Year, r_model_mixed, color='goldenrod', label='hybrid model')
    if dn > 0:    #plot moving averages
        yr_avg, gr_avg = calc_mov_avg(Year, gr, dn)      
        bot.plot(yr_avg[1:], gr_avg, label='%i-yr rolling avg'%dn)
    bot.legend(loc=loc_bot)
    #baseline at 0 growth rate:
    bot.plot(x_base, (0,0), color=base_clr, lw=lw_b)

    return Fig


def excel(fname, sheet_name, names_row, years_top_row, years_bot_row,
          data_col1, data_col2=None, years_col=1, minimum=45, the_nation=''):
    """Load data from excel spreadsheet for the 
       nations that have a minimum number of entries
       The time span is returned in dictionary Year[nation]
       Returned data is stored in dictionary Q_data[nation] 
    """
    def entry(row, col): return sheet.cell(row=row, column=col).value
    
    def bounds(col, first_row, last_row):
        """ Find the range of numerical entries
        between first_row and last_row
        """
        top = first_row
        #first get past all empty cells
        if entry(top, col) is None:
            while entry(top, col) is None: top = top + 1
        #and now find first number    
        while not is_number(entry(top, col)):                                                 
            top = top + 1                                                                
            if top > last_row: return -1, -1                                                      
        #now find the last entry:
        bot = last_row
        if entry(bot,col) is None:
            while entry(bot, col) is None: bot = bot - 1
        if is_number(entry(bot,col)): return top, bot                                                                        
        while not is_number(entry(bot,col)):                                                 
            bot = bot - 1                                                                
        return top, bot + 1
                                                                                        
    wb = openpyxl.load_workbook(fname)                                   
    sheet = wb.get_sheet_by_name(sheet_name)                                   
    span = np.array([entry(r, years_col) for r in range(years_top_row, years_bot_row+1)])
    cols = sheet.max_column if data_col2 is None else data_col2
    if cols == data_col1:
        """process a single nation
        meaningful data for the full range of span 
        """
        nation = entry(names_row, cols)
        Q = np.array([entry(r, cols) for r in range(years_top_row, years_bot_row+1)])
        wb.close()
        return nation, span, Q   

    Year = {}                                                                                 
    Q_data = {}                                                                        
    for col in range(data_col1, cols+1):                                                     
        nation = entry(names_row, col)
        top, bot = bounds(col, years_top_row, years_bot_row)
        if top == -1 or bot - top < minimum: continue
        yr_ = span[top - years_top_row: bot - years_top_row+1]
        Q_  = np.array([entry(r, col) for r in range(top, bot+1)])
        if nation in the_nation:
            wb.close()
            return nation, yr_, Q_           
        Year[nation]   = yr_
        Q_data[nation] = Q_
    Nations = sorted(Q_data.keys())
    wb.close()         
    return Nations, Year, Q_data



def gr_data(Q, Year):
    """Annual growth rate in %
    and its running average
    """
    gr   = np.zeros(len(Q) - 1)
    avg  = np.zeros(len(Q) - 2)
    for i in range(len(Q) - 1): 
        gr[i] = (100./Q[i])*(Q[i+1] - Q[i])/(Year[i+1] - Year[i])    
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

def fitting(nation, Q, Year, p0='', gdp='True', mode='sat'):
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

    R = Q[-1]/Q[0]
    print '%s: %i data points'%(nation, len(Year))
    s = 'GDP has grown from %6.2E($10) in %i to %6.2E($10) in %i' if gdp else\
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
            print '   r0 = %3.2f'%r_u +  ' %/year    ' + \
                  'Q0 = %5.2E 2010USD'%Q_h
            s = '   GDP increasses by %.2E USD10 per year' if gdp else\
                '   Population increasses by %.2E per year'
            print s%gr    
            print '  Relative errors of fitting parameters:\n'+\
                  '   err(r0) = %5.2E   err(G0)= %5.2E'%(perr[0], perr[1])
        else:
            print '   ru = %3.2f'%r_u+'%      unhindered (unsaturated) growth rate'
            s = '   Qh = %5.2E   Hindering (saturation) GDP in 2010USD \n' if gdp else\
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
        s = '   GDP of %4.2E $10 and annual growth rate %3.2f' if gdp else\
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


def load_POP(region, unit=1.E3):
    """ Default unit is thousands
    """
    fname = region+'_POP.dat'
    POP_data = np.genfromtxt(fname, skip_header=1, usecols=(0,1), unpack=True,
              dtype=[('Year','i'),('POP','f')])
    Year, POP = POP_data['Year'], unit*POP_data['POP']
    # POP normalized to its initial entry
    P = POP/POP[0]
    # Annual growth rate in %
    gr = np.zeros(len(POP) - 1)
    for i in range(len(gr)): 
        gr[i] = 100.*(POP[i+1]/POP[i] - 1)    

    return Year, POP, P, gr
