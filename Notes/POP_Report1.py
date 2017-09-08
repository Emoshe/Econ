
# coding: utf-8

# <a id='Top'></a>
# # Population Analysis
# ## Moshe, Sep. 1, 2017
# #### Improved summary figure, including display of the unitarity test
# 
# 

# Population data are available from the <a href="https://esa.un.org/unpd/wpp/Download/Standard/Population/">UN Population Reference Bureau</a>.  Their <a href="https://esa.un.org/unpd/wpp/DVD/Files/1_Indicators%20(Standard)/EXCEL_FILES/1_Population/WPP2017_POP_F01_1_TOTAL_POPULATION_BOTH_SEXES.xlsx">Total Population file</a> tabulates "de facto population in a country, area or region as of 1 July of the year indicated". The current version covers 1950--2015. These data enable analysis of population growth for individual nations and total World population, as well as its breakup according to various classification criteria. For fun, let's start with a few individual nations.
# 
# 
# ## US <a id='sec:US'></a>
# Modeling of the [US population](#US) yields an excellent fit; the average deviation of model from data is 0.99%, the largest deviation (in 1963) is 2.67%. With a hindering parameter $H$ = 9.9, the US population growth is deeply in the hindered mode. Indeed, the hindering population is only $Q_h$ = 23 million while the 1950 population was 159 million, 7 times higher; the hindering threshold ($Q = Q_h$) was crossed long before 1950. The US population grows at the constant rate of 2.7 million per year, and it would actually make more sense to model it with the linear growth model since the hindered exponential model gives $r_u$ = 11.7%/yr. The model predicts a 2050 US population of 408 million.  
# 
# 
# ## China <a id='sec:China'></a>
# Similar to the US, the [population of China](#China) has crossed the hindering threshold long before 1950. While modeling with hindered exponential growth fails, the straight linear growth model fits the data quite well: the average deviation of model from data is only 2.75%, the largest deviation (in 1963) only 5.57%. The model outcome is that the population of China is increasing by 14.3 million per year, having crossed the hindering threshold long before 1950. The model predicts that by 2050 the population of China will grow to 2 billion. 
# 
# 
# ## India <a id='sec:India'></a>
# The [population of India](#India) has grown from 376 million in 1950 to 1.31 billion in 2015. The hindered growth model works pretty well--- the average deviation of model from data is 2.05%, the largest deviation (in 1967) is 4.21%. The model predicts a 2050 population of 2.3 billion, growing at 1.37%/yr.  In contrast with the US and China, the hindering parameter is $H$ = 0.26 and the hindering population is $Q_h$ = 2.85 billion so that the hindering threshold $(Q = Q_h)$ will not be crossed even by 2050. 
# 
# India is a interesting case where the hindering effect is significant even though its population will remain below the hindering threshold for sometime to come. Beginning in 1980 the growth rate shows a pronounced, steady downward trend (the figure bottom panel), therefore long-term model predictions could be an overestimate. The impliction is that in this case it might be prudent to add a quadtratic term to the hindering effect. Some further support for this conjecture comes from the fact that the model predicts a population increase of 71 million per year during the hindered growth phase; this is 5 times the rate for China, which might be hard to sustain for an extended period.
# 
# 
# <a id='sec:World Population'></a>
# ## World Population
# 
# Modeling of the [total world population](#World Population) yields an almost perfect fit: the average deviation of model from data is 1.08%, the largest deviation (in 1963) is 2.64%. The hindering parameter is $H$ = 0.94, the hindering population is $Q_h$ = 4.83 billion and $Q = Q_h$ occurred in 1985. The model predictions for 2050 are a world population of 11 billion, adding 156 million per year for an annual growth rate of 0.98%. It would be interesting to extend the data to earlier years.
# 
# The spreadsheet breaks up the world population in different ways. Here's the analysis of the different components.
# 
# 
# <a id='sec:Development'></a>
# ## Degree of Development
# The criteria for classification by degree of development are
# 
# >More developed regions comprise Europe, Northern America, Australia/New Zealand and Japan. Less developed regions comprise all regions of Africa, Asia (except Japan), Latin America and the Caribbean plus Melanesia, Micronesia and Polynesia. 
# 
# So it's really a geographic classification, rearranging the continents into two groups. This segmentation must be understood as applicable to whole regions not individual countries (except for Japan), otherwise it would lead to the curious (for me at least) result that Singapore and Taiwan are 'less developed' because they're in Asia while Albania and Moldova, being in Europe, are 'more developed'. Be that as it may, this is how they classify and we can analyze the population growth of each development class separately. 
# 
# Here are the [results for the two development classes](#development). The population of the more developed regions has increased from 815 million in 1950, when it comprised 32% of the world population, to 1.25 billion in 2015, when it was down to only 17% of total. In 65 years the population increased by only 435 million (53%), with a large chunk of that coming from the 160-million population increase of the US. The average population growth of the more developed regions was less than 7 million(!) per year. Modeling of the time series with hindered exponential growth fails, but the linear growth model fits the data rather well: the average deviation of model from data is only 1.83%, the largest deviation (in 1950) only 5.35%. The model outcome is that the population of the more developed regions is increasing by only 6.62 million per year, having crossed the hindering threshold long before 1950. The Model predictions for 2050 are for a population of 1.52 billion (that is, an increase of only 232 million from 2015 to 2050) and annual growth rate of only 0.43%.
# 
# In contrast, the population of the less developed regions has almost quadrupled from 1.72 billion in 1950 to 6.13 billion in 2015. The hindered growth model works very well (1.54% average deviation of model from data, 3.93% maximum deviation), yielding $r_u$ = 3.47%/yr and $Q_h$ = 4.63 billion; the hindering threshold ($Q = Q_h$) was crossed in 1996. The model predictions for 2050 are a population of 9.75 billion and annual growth rate of 1.12%.
# 
# Below is a [summary of the results](#summary: development). The summary figure shows the continuous decrease of the fractional population of the more developed regions. Every model of population classes must obey a 'unitarity' constraint: the sum of the populations of all classes must equal the world's population. The results, shown in the summary, indicate that the models pass the test: the deviations of the sum of models for more- and less-developed regions from the model for the entire world population are only 0.75% on average, with a maximum of 2.1%. Because these deviations are within the modeling errors (deviations of individual models from their corresponding data), the models are self-consistent. 
# 
# <a id='sec:Continents'></a>
# ## Continents
# The [classification by Continents](#continents) is based (obviuosly) purely on location. In essence, it splits up each of the two development classes into three sub-classes. The model results fall in three groups. Similar to the case of more developed regions, both Europe and Northern America are fitted successfully by the linear growth model, and only by that model. This is not surprising---together they comprise the bulk of the more developed class, leaving out only Japan and Australia. The average deviations of model for data are 2.5% for Europe and 0.94% for Northern America.  Notably, Europe's population is growing by only 2.85 million per year, predicted to rise from 741 million in 2015 to 872 million in 2050.
# 
# The second group comprises Oceania, Latin America and Asia. Each of these continents is fitted successfuly by the hindered growth model. For each member of this group, the following table columns show the average deviation of model from data, the hindering parameter $H$, the year the hindering threshold was crossed, the model prediction for the 2050 population and the annual population increase: 
# 
# <style type="text/css">
# .tg  {border-collapse:collapse;border-spacing:0;}
# .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
# .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
# .tg .tg-baqh{text-align:center;vertical-align:top}
# .tg .tg-yw4l{vertical-align:top}
# </style>
# <table class="tg">
#   <tr>
#     <th class="tg-yw4l"></th>
#     <th class="tg-baqh">avg err(%)<br></th>
#     <th class="tg-baqh">$H$</th>
#     <th class="tg-baqh">$Q &gt; Q_h$<br></th>
#     <th class="tg-baqh">2050 pop<br></th>
#     <th class="tg-baqh">growth</th>
#   </tr>
#   <tr>
#     <td class="tg-yw4l">Oceania</td>
#     <td class="tg-baqh">0.96</td>
#     <td class="tg-baqh">1.15</td>
#     <td class="tg-baqh">1973</td>
#     <td class="tg-yw4l">57.3 million<br></td>
#     <td class="tg-yw4l">$7.6\times10^5$ per year<br></td>
#   </tr>
#   <tr>
#     <td class="tg-yw4l">Latin America<br></td>
#     <td class="tg-baqh">1.31</td>
#     <td class="tg-baqh">2.29</td>
#     <td class="tg-baqh">before 1950<br></td>
#     <td class="tg-yw4l">950 million<br></td>
#     <td class="tg-yw4l">$1.1\times10^7$ per year</td>
#   </tr>
#   <tr>
#     <td class="tg-yw4l">Asia</td>
#     <td class="tg-baqh">1.84</td>
#     <td class="tg-baqh">1.35</td>
#     <td class="tg-baqh">1967</td>
#     <td class="tg-yw4l">6.67 billion<br></td>
#     <td class="tg-yw4l">$8.3\times10^7$ per year</td>
#   </tr>
# </table>
# 
# In a group all by itself is Africa, whose population growth shows no signs of hindering---the hindering parameter is $H = 4.5\times10^{-9}$. A pure exponential with constant growth rate $r$ = 2.54%/yr gives an excellent fit, with model-from-data deviations of 1.55% on average and 3.66% maximum. If this growth is sustained through 2050, Africa's population will more than double from 1.2 billion in 2015 to 2.9 billion in 2050.
# 
# An indication that Africa's growth may not remain unhindered for that long comes from the unitarity test, preformed in the [results summary](#summary: continents). The sum of model predictions for continent populations in 2050 exceeds the prediction for the world population by 8%, outside the modeling errors (deviations of individual models from their corresponding data). Since Africa's fractional contribution is the only one rising while all others are decreasing, evident from the summary figure, the violation of unitarity comes entirely from Africa's unhindered contribution. The growth rate of Africa's population may slow down with economic development, and in some sense this is what the classification by degree of development is indicating: lumping Africa together with other regions into a 'less developed' category results in hindered population growth because the contribution of Africa is diluted by that of Asia, which all in all has curbed its population growth.  
# 
# 
# <a id='sec:Income'></a>
# ## Income Level
# This is the most interesting and arguably the most meaningful of the classifications given. The classification has nothing to do with geography, instead it is based entirely on an objective, measurable indicator:
# 
# >The country classification by income level is based on 2016 GNI per capita from the World Bank.
# 
# All nations are binned into low-, middle- and high-income groups, which are all modeled successfuly. [The results](#income) show that, as might be expected, income and population growth rate are inversely correlated: the models yield unhindered exponential growth for the low-income countries, hindered growth for the mid-income ones and linear growth, i.e., strongly hindered, for the high-income countries:
# 
# <style type="text/css">
# .tg  {border-collapse:collapse;border-spacing:0;}
# .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
# .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;}
# .tg .tg-baqh{text-align:center;vertical-align:top}
# .tg .tg-yw4l{vertical-align:top}
# </style>
# <table class="tg">
#   <tr>
#     <th class="tg-yw4l">Income Level<br></th>
#     <th class="tg-baqh">avg err(%)<br></th>
#     <th class="tg-baqh">$H$</th>
#     <th class="tg-baqh">$Q &gt; Q_h$<br></th>
#     <th class="tg-baqh">2050 pop<br></th>
#     <th class="tg-baqh">growth</th>
#   </tr>
#   <tr>
#     <td class="tg-yw4l">Low</td>
#     <td class="tg-baqh">3.82</td>
#     <td class="tg-baqh">$1.4\times10^{-8}$</td>
#     <td class="tg-baqh">---</td>
#     <td class="tg-yw4l">1.45 billion<br></td>
#     <td class="tg-yw4l">2.42% per year<br></td>
#   </tr>
#   <tr>
#     <td class="tg-yw4l">Middle<br></td>
#     <td class="tg-baqh">1.69</td>
#     <td class="tg-baqh">1.25</td>
#     <td class="tg-baqh">1970<br></td>
#     <td class="tg-yw4l">8.41 billion<br></td>
#     <td class="tg-yw4l">$1.1\times10^8$ per year</td>
#   </tr>
#   <tr>
#     <td class="tg-yw4l">High</td>
#     <td class="tg-baqh">0.76</td>
#     <td class="tg-baqh">linear model<br></td>
#     <td class="tg-baqh">before 1950<br></td>
#     <td class="tg-yw4l">1.46 billion<br></td>
#     <td class="tg-yw4l">$7.7\times10^6$ per year</td>
#   </tr>
# </table>
# 
# Most of the world population resides in middle-income countries, as is evident from the [results summary](#summary: income). The mid-income model most closely resembles that for the total world population, predicting an identical growth rate of 0.98%/yr in 2050. The summary figure shows an interesting result: beginning around 1990, **the fraction of the world population living in mid-income countries is almost constant at ~75-76% of total**. This is suggestive of the following speculative scenario: the income level rises globally so that some low-income nations move into the mid-income category while some mid-income ones are moving up to the high-income bin. The population growth rate of a nation decreases with the rising of its income level. For the mid-income bin, the competing effects of gaining population from the higher-growth-rate lower bin and losing population to the lower-growth-rate higher bin just balance each other so that its fraction of the total remains unchanged. For the low-income nations, the higher growth rate more than compensates for the loss of nations that move to the higher income bin, leading to a rising fractional population, with the opposite effect for high-income nations.
# 
# While plausible, this scenario cannot be tested with the current 'static' data because all nations are classified for all years according to their income level in one single year (2016). To verify the scenario we need 'dynamic' classification according to the income level in each year. It should be possible to get these data, which would make for an excellent follow-up project. 
# 
# 
# ## To do
# 1. Would be good to extend the data to earlier years wherever possible.
# 
# 2. The success in modeling populations probably stems from the smooth time variation of this quantity. Unlike the noisy variability of GDP growth rates, population growth rates are generally smooth, with 5-year rolling averages coinciding with the function itself, which is why they are not plotted. But the growth rates do show clear fluctuations around the model, which outlines the long-term variation of the data, with typical time scales of ~10 years, in contrast with the 1-year jittering of GDP growth rates. Would be good to devise a method to quantify the properties of the fluctuations, both amplitudes and characteristic time scales. Best would be if this could be done from the data alone without a specific model for the underlying long-term trends.   
# 
# 
# <a id='sec:Links'></a>
# ## Links:
# 
# [US](#US)
# 
# [China](#China)
# 
# [India](#India)
# 
# [World Population](#World Population)
# 
# [Segmenting by Development](#development)
# 
# [Checksum, Development](#summary: development)
# 
# [Segmenting by Continents](#continents)
# 
# [Checksum, Continents](#summary: continents)
# 
# [Segmenting by Income](#income)
# 
# [Checksum, Income](#summary: income)
# 
# 

# In[1]:

import numpy as np
from numpy import exp, sqrt, log as ln, log10 as log
import matplotlib.pyplot as plt
import sys
sys.path.append('../Tools')
from ME_utils import *
from econ import *
from POP import *


# [Back to Top](#Top)
# 
# # World Population <a id='World Population'></a>

# In[2]:

Year   = np.arange(1950, 2016)
future = np.arange(1950, 2051)
plot_it = True

data_row = [18]
_, POP, models = POP_analyze(Year, future, data_row, plot_it)
World_pop = POP['WORLD']
World_model = models['WORLD']


# [Back to Top](#Top)
# # Segmenting by Development <a id='development'></a>

# In[3]:

data_row = [19, 20]                                                                                                                               
Regions, POP, models = POP_analyze(Year, future, data_row, plot_it)


# [Back to Top](#sec:Development)
# # Summary, Development <a id='summary: development'></a>

# In[4]:

check_sum(World_pop, World_model, Regions, POP, models, Year, future)


# [Back to Top](#sec:Income)
# # Segmenting by Income <a id='income'></a>

# In[5]:

data_row = [24, 25, 28]                                                                                                                               
Regions, POP, models = POP_analyze(Year, future, data_row, plot_it)


# [Back to Top](#sec:Income)
# # Summary, Income <a id='summary: income'></a>

# In[6]:

check_sum(World_pop, World_model, Regions, POP, models, Year, future)


# [Back to Top](#sec:Continents)
# # Segmenting by Continents <a id='continents'></a>

# In[7]:

data_row = [30, 94, 152, 205, 257, 263]                                                                                                                               
Regions, POP, models = POP_analyze(Year, future, data_row, plot_it)


# [Back to Top](#sec:Continents)
# # Summary, Continents <a id='summary: continents'></a>

# In[8]:

check_sum(World_pop, World_model, Regions, POP, models, Year, future)


# [Back to Top](#sec:US)
# # US <a id='US'></a>

# In[9]:

data_row = [262]  # US
_, POP, models = POP_analyze(Year, future, data_row, plot_it)


# [Back to Top](#sec:US)
# # China <a id='China'></a>

# In[10]:

data_row = [96]  # China
_, POP, models = POP_analyze(Year, future, data_row, plot_it)


# [Back to Top](#sec:China)
# # India <a id='India'></a>

# In[11]:

data_row = [115] #India
_, POP, models = POP_analyze(Year, future, data_row, plot_it)


# [Back to Top](#sec:India)

# In[ ]:



