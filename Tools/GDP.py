import numpy as np
from numpy import exp, sqrt, log as ln, log10 as log
import matplotlib.pyplot as plt
from ME_utils import *
from econ import *
plt.close('all')


##############################################################
data_dir = '../Data/'
## Datasets:

fname = data_dir+'All_from67.xlsx'                                   
sheet_name = 'GDP (2010 USD)'                                   
names_row = 2
years_top_row = 3 
years_bot_row = 51
data_col1 = 2
data_col2 = None
All67 = [fname, sheet_name, names_row, years_top_row, years_bot_row, 
        data_col1, data_col2]

fname = data_dir+'GDP Time Series_Long.xlsx'                                   
sheet_name = 'Sheet2'                                   
names_row = 2
years_top_row = 13 
years_bot_row = 329
data_col1 = 2
data_col2 = 6
Long = [fname, sheet_name, names_row, years_top_row, years_bot_row, 
        data_col1, data_col2]

##################################################################


def summary(print_array, Year, R, ru, qs, H, success, failure, A='', fits=True):
    """print summary sorted on different quantities
    """
    n = 76 if fits else 39
    if A:
        print '\n', n*'*', '\n'
        print 'Sorted by %s:'%A    
    header = 'nation'.ljust(20) + 'entries'.rjust(10) + 'R'.rjust(6)
    if fits: 
        header += 'r_u(%)'.rjust(11) + 'qs'.rjust(7) + 'Qf/Qh'.rjust(10) + 'H'.rjust(8)
    header += '\n' + n*'_' 
    print header
    for nation in print_array: 
        s = nation[:20].ljust(20) + repr(len(Year[nation])).rjust(7)
        s+= str('%.3g'%R[nation]).rjust(11)
        if fits: 
            if nation in success:
                Qf2h = R[nation]/qs[nation] #=(Qf/Qi)/(Qh/Qi) = Qf/Qh
                s+= '%8.2f'%ru[nation] + \
                str('%.3g'%qs[nation]).rjust(10) + \
                str('%.3g'%Qf2h).rjust(10) + \
                str('%.3g'%H[nation]).rjust(10)
                print s
        else:
            if nation in failure: 
                print s      


def summary_print(Nations, Year, GDP, R, ru, qs, Qh, H, success, failure, 
                  future, G_model, r_model, names_too=True):
    #Summary of successful fits:
    print 'Successful fits for %i nations out of %i\n'\
               %(len(success), len(Nations))
    print 'R = Qf/Qi              last-to-first years of data'
    print 'H = (R - 1)/(qs*ln R)  Hindrance parameter\n' 
    args = [Year, R, ru, qs, H, success, failure]
    if names_too: summary(sorted(R.keys()),            *args) 
    summary(sorted(H, key=H.__getitem__), *args, A='H')

    if len(failure) == 0:
        print '\nAll data fitted successfully'
    else:
        print '\nFailed to fit %i out of %i nations:\n'%(len(failure),len(Nations))
        summary(failure, *args, A='', fits= False )
       
    return Nations, success, Year, GDP, ru, Qh, future, G_model, r_model  

def plot_it(Nations, GDP, Year, gr, average, x_range, 
           loc_lbl='lower right', loc_name=(0.1, 0.1), dn=5):

    data_color  = 'grey'
    n = len(Nations)
    Fig = plt.figure(figsize=(7, 10))

    row = 0
    for nation in Nations:
        r = gr[nation]
        avg = average[nation]
        row+=1
        fig = Fig.add_subplot(n, 1, row)
        name = 'UK' if 'UK' in nation else nation
        fig.text(loc_name[0],loc_name[1],name,fontsize=fontsize+6,transform=fig.transAxes)
        
        fig.set_xlim(x_range)
        fig.xaxis.set_minor_locator(AutoMinorLocator())
        if nation == Nations[-1]:
            fig.set_xlabel('Year')
        else:
            fig.xaxis.set_major_formatter(NullFormatter())

        fig.set_ylabel('r (%/yr)')
        fig.set_ylim(np.amin(r)-1., np.amax(r)+1)
        fig.yaxis.set_minor_locator(AutoMinorLocator())
        fig.plot(x_range, (0,0), color='lightgrey', lw=0.7) #plot baseline at r = 0   
        fig.plot(Year[nation][1:], r, color=data_color, lw=1.5, label='data') #plot the data
        fig.plot(Year[nation][2:], avg, label='running average')
        if dn > 0:    #plot moving averages
            yr_avg, gr_avg = calc_mov_avg(Year[nation], r, dn)      
            fig.plot(yr_avg[1:], gr_avg, label='%i-yr rolling avg'%dn)
        if nation == Nations[0]: fig.legend(loc=loc_lbl)

    Fig.subplots_adjust(left=0.12,right=0.98, bottom=0.05, hspace=0.03, top=.98)
    return Fig

def plot_avg(Nations, Year, average, x_range, 
           loc_name=(0.8, 0.75)):

    Fig = plt.figure(figsize=(7, 10))
    Fig.suptitle('Growth Rate Running Average',fontsize=fontsize+8)
    row = 0
    for nation in Nations:
        row +=1
        fig = Fig.add_subplot(len(Nations), 1, row)
        name = 'UK' if 'UK' in nation else nation
        fig.text(loc_name[0],loc_name[1],name,fontsize=fontsize+6,transform=fig.transAxes)
        txt = '1st year in average is %i'%Year[nation][0]
        fig.text(0.1,0.2,txt,transform=fig.transAxes)
        
        fig.set_xlim(x_range)
        fig.xaxis.set_minor_locator(AutoMinorLocator())
        if nation == Nations[-1]:
            fig.set_xlabel('Year')
        else:
            fig.xaxis.set_major_formatter(NullFormatter())

        fig.set_ylabel('r (%/yr)')
        avg = average[nation]       
        yf = avg[-1]
        #y-axis range: 
        i = np.where(Year[nation]==x_range[0])[0][0]
        y_range = [np.amin(avg) - 2, np.amax(avg) + 2] \
                  if (np.amax(avg[i:]) - np.amin(avg[i:]) > 4) else \
                  [yf - 1, yf + 1] 
        fig.set_ylim(y_range)
        fig.yaxis.set_minor_locator(AutoMinorLocator())
        fig.plot(x_range, (yf,yf), color='lightgrey', lw=0.7) #plot baseline at r = 0   
        fig.plot(Year[nation][2:], avg)
    Fig.subplots_adjust(left=0.12,right=0.98, bottom=0.05, hspace=0.03, top=.92)
    return Fig


def load(data_set):   
    Nations, Year, GDP = excel(*data_set) 
    for nation in Nations:
        if data_set[0] == 'GDP Time Series_Long.xlsx':
            if 'US' in nation or 'UK' in nation: GDP[nation] *= 1.E6
    return Nations, Year, GDP
    
def fit_it(n_list, Year, GDP):   
    #split the database to those whose fitting succeeded or failed: 
    failure, success = [], [] 
    #for the successes, dictionaries for all relevant info: 
    qs, ru, Qh, future, G_model, r_model = {}, {}, {}, {}, {}, {}

    H, R = {}, {}
    for nation in n_list:
        R[nation]  = GDP[nation][-1]/GDP[nation][0]
        try:
            ru[nation], Qh[nation], Q0_dummy, future[nation], G_model[nation], r_model[nation]\
               = fitting(nation, GDP[nation], Year[nation])
            success.append(nation)
            qs[nation] = Qh[nation]/GDP[nation][0]
            H[nation]  = (R[nation] - 1)/(ln(R[nation])*qs[nation])
        except:
            failure.append(nation)
    return R, ru, qs, Qh, H, success, failure, future, G_model, r_model

def analyze(data_set, n_list=''):   
    Nations, Year, GDP = load(data_set)
    if not n_list: n_list = Nations
    R, ru, qs, Qh, H, success, failure, future, G_model, r_model\
       = fit_it(n_list, Year, GDP) 
    args = [Nations, Year, GDP, R, ru, qs, Qh, H, success, failure, future, G_model, r_model]
    return args

##############################################################

if __name__ == '__main__':

    n_list = ''
    data_set = All67
    #data_set = Long

    outfile = ''
    #outfile = 'Outfiles/Current_model.dat'

    plot_it = False
    #plot_it = True

    figfile = ''
    figfile = 'Figs/Current_models.pdf'

    dn = 5
    loc_top = 'upper left'
    loc_bot = 'upper right'

    out = print2file(outfile) if outfile else None
    
    #n_list = ['US']
    #n_list = ['US', 'Japan']
    #n_list = ['United States', 'Belgium', 'Netherlands']
    #n_list = ['Netherlands']
    
    #args = analyze(data_set, n_list)
    Nations, Year, GDP, R, ru, qs, Qh, H, success, failure, future, G_model, r_model\
        = analyze(data_set, n_list)
    #summary_print(*args)
    #Nations, success, Year, GDP, ru, Qh, future, G_model, r_model = summary_print(*args)

    #close the output file:
    close_it(out)
    print '\n*** Done with fitting and tabulating'
    

    if not (plot_it or figfile): sys.exit()


    #********* Plotting ********
    print '\nNow plotting\n'
    #'''
    n_list = failure
    if figfile: 
        print '***plotting to file', figfile
        pp = PdfPages(figfile)
    
    for nation in n_list:
        print 'Plotting results for',nation
        gr, avg = gr_data(GDP[nation], Year[nation])   
        Fig = basic_plot(nation, Year[nation], GDP[nation], gr, avg, dn=dn)
        if plot_it: plt.show()
        if figfile: pp.savefig(Fig)
    if figfile: pp.close()
    print '\n*** Done plotting'
    
    sys.exit()
    #'''
    n_list = success
    for nation in n_list:
        print 'Plotting results for',nation
        gr, avg = gr_data(GDP[nation], Year[nation])   
        Fig = basic_plot(nation, Year[nation], GDP[nation], gr, avg, 
              r_u=ru[nation], Qh=Qh[nation], Q0='',
              loc_top=loc_top, loc_bot=loc_bot, 
              future=future[nation], top_axis=True, dn=dn, 
              model_r=r_model[nation], model_Q=G_model[nation]) 
        if plot_it: plt.show()
        if figfile: pp.savefig(Fig)
    if figfile: pp.close()
    print '\n*** Done plotting'
   
    sys.exit()
    
    if figfile: pp = PdfPages(figfile)
    for nation in n_list:
        print 'Plotting results for ',nation
        gr, avg = gr_data(GDP[nation], Year[nation])
        t_axis  = t_from_yr(future[nation], ru[nation])
        Fig = basic_plot(nation, Year[nation], GDP[nation], gr, avg, 
               ru[nation], qs[nation], loc_top, loc_bot, future[nation], t_axis, dn, 
               r_model_mixed=None, model_r=r_model[nation], model_Q=G_model[nation]) 
        if not figfile: Fig.show()
        if figfile: pp.savefig(Fig)
    if figfile: pp.close()
    print '\n*** Done plotting'


