import sys

import numpy as np
from numpy import exp, sqrt, log as ln, log10 as log, average
import matplotlib.pyplot as plt
from scipy import stats
from scipy.optimize import curve_fit

plt.close('all')
from ME_utils import *
from econ import *


########################################################################

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


def POP_excel(data_rows):

    def entry(row, col): return sheet.cell(row=row, column=col).value

    fname = '../Data/WPP2017_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.xlsx'                                              
    sheet_name = 'ESTIMATES'                                          
    names_col = 3                                                          
    data_col1 = 6  
    
    wb = openpyxl.load_workbook(fname)                                   
    sheet = wb.get_sheet_by_name(sheet_name)                                   
    cols = sheet.max_column 

    POP = {}
    for r in data_rows:
        nation = entry(r, names_col)
        POP[nation] = 1.E3*np.array([entry(r, col) for col in range(data_col1, cols+1)])
    
    Nations = POP.keys()
    wb.close()         
    return Nations, POP
   
def POP_analyze(Year, future, data_row, plot_it):
    Nations, POP = POP_excel(data_row)
    Q_model = {}
    for nation in Nations:
        print '\n', 70*'*','\n'
        try:
            r0, Q_h, Q0, ftr, Q_model[nation], r_model = \
                fitting(nation, POP[nation], Year, gdp=False)   
            linear = False
            top_axis = True
        except:
            print '*** Attempting linear fit:'
            r0, Q_h, Q0, ftr, Q_model[nation], r_model = \
                   fitting(nation, POP[nation], Year, gdp=False, mode='lin')   
            linear = True
            top_axis = False
        if plot_it:
            r, avg = gr_data(POP[nation], Year)
            basic_plot(nation, Year, POP[nation], r, avg,       
                r_u=r0, Qh=Q_h, future=future, 
                dn=0, loc_top='upper left', 
                model_r=r_model, model_Q=Q_model[nation], 
                POP=True, top_axis=top_axis, linear=linear )   
            plt.show()                                                                              
    return Nations, POP, Q_model 

def check_sum(World_pop, World_model, Nations, POP, models, Year, future):

    def summary_prt(ind, ind2=-1):
        W = [World_pop, World_model]
        R = [POP, models]
        T = [tot_pop, tot_model]
        h1 = '\n1950 ' if ind2==0 else '\n2015 '       
        hd = [h1+'populations in billions:\n',\
              '\n\nPredictions for 2050 populations (billions):\n']

        print hd[ind]
        print '%36s'%'pop', '%12s'%'% of tot'
        print '%25s'%'World'.ljust(25), '%10.2f'%(1.E-9*W[ind][ind2]) 
        tot_pct = 100*T[ind][ind2]/W[ind][ind2]
        for nation in Nations:
            pct = 100*R[ind][nation][ind2]/W[ind][ind2]
            s = 2*'%10.2f'% (1.E-9*R[ind][nation][ind2], pct)
            print '%25s'%nation[:25].ljust(25), s
        print 47*'_'
        print '%22s'%'sum:',
        print '%13.2f %9.1f'%(1.E-9*T[ind][ind2], tot_pct)

    tot_pop   = np.zeros(len(World_pop))
    tot_model = np.zeros(len(World_model))
    for nation in Nations:
        if not nation == 'WORLD':
            tot_pop   += POP[nation]
            tot_model += models[nation]
    summary_prt(0, 0)
    summary_prt(0)
    summary_prt(1)

    err_d = 100*abs(World_pop/tot_pop - 1)   
    err_m = 100*abs(World_model/tot_model - 1)
    s = '\nDeviations of population sums from total:'
    print s
    s = '   Data(%i--%i)   -- average of %.2G percent, maximum %.2G percent'
    print s  %(Year[0], Year[-1], np.average(err_d), np.amax(err_d)) 
    s = '   Models(%i--%i) -- average of %.2G percent, maximum %.2G percent'
    print s  %(future[0], future[-1], np.average(err_m), np.amax(err_m))
    
    #######Plotting   
    Fig, (top, bot) = plt.subplots(2,1, sharex=True, figsize=(8, 10))
    for fig in [top, bot]:
        fig.set_xlim(Year[0], future[-1])
        fig.xaxis.set_minor_locator(AutoMinorLocator())
        fig.set_xlabel('Year')
        if fig is not bot: plt.setp(fig.get_xticklabels(), visible=False)

    #top: data and models
    top.set_ylabel('Population')
    top.set_yscale('log')
    err_max = 0
    for n, nation in enumerate(Nations):
        top.plot(Year, POP[nation], color=color[n])
        top.plot(future, models[nation], '--', color=color[n])
        err = abs(POP[nation]/models[nation][:len(Year)] - 1)  # errors
        err_max = max(np.max(err), err_max)
    s  = 'solid lines: data'+15*' '+'dashed lines: models'
    top.set_title(s, va='bottom')

    #Error strip of the individual models:
    x_range = (Year[0], future[-1])
    bot.fill_between(x_range, 1-err_max, 1+err_max, color='gainsboro') #color='lightgray')
    bot.plot(x_range, (1,1), color='white', lw=0.7)

    line1,  = bot.plot(future, tot_model/World_model, 'k--', label='sum of fractions')
    legend1 = bot.legend(handles=[line1], loc=1)
    plt.gca().add_artist(legend1)
    #ax = plt.gca().add_artist(legend1)

    #bot: Fractional populations
    bot.set_ylim(0, 1.3)
    bot.yaxis.set_minor_locator(AutoMinorLocator())
    bot.set_ylabel('fraction of total')

    for n, nation in enumerate(Nations):
        frac_pop = POP[nation]/tot_pop
        frac_mod = models[nation]/tot_model
        ln_n = bot.plot(Year, frac_pop, color=color[n], label=nation)
        lns = ln_n if n==0 else lns+ln_n
        bot.plot(future, frac_mod, '--', color=color[n])
    '''
    Legend below the figure:
    bbox can be a BboxBase instance, a tuple of 
    [left, bottom, width, height] in the given transform 
    (normalized axes coordinate if None), 
    or a tuple of [left, bottom] where the width and height 
    will be assumed to be zero.
    loc refers to the location of the anchor point
    '''
    labls = [l.get_label() for l in lns]   
    bot.legend(lns, labls, bbox_to_anchor=(0.5, -0.15), loc='upper center', ncol=2) 


    Fig.subplots_adjust(left=0.12,right=0.95, bottom=0.15, top=0.9, hspace=0.02)
    plt.show()

    
########################################################################


if __name__ == '__main__': 

    outfile = ''
    plot_it = False       
    
    #outfile = 'Outfiles/Current_model.dat'
    #plot_it = True

    out = print2file(outfile) if outfile else None

    Year   = np.arange(1950, 2016)
    future = np.arange(1950, 2051)
    
    data_row = [18]
    Nations, POP, models = POP_analyze(Year, future, data_row, plot_it)
    #sys.exit()

    World_pop = POP['WORLD']
    World_model = models['WORLD']   

    data_row = [19, 20]
    #data_row = [30, 94, 152, 205, 257, 263] #continents
    #data_row = [24, 25, 28]                                                                                                                               

    Nations, POP, models = POP_analyze(Year, future, data_row, plot_it)
    #sys.exit()
    
    check_sum(World_pop, World_model, Nations, POP, models, Year, future)
    
    sys.exit()



    #tabulate(POP, Year, future, G_model) 
    close_it(out)
    sys.exit()
