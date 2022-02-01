import math
import warnings
import matplotlib
import numpy as np 
import pandas as pd 
from plotnine import *
import seaborn as sns
import plotly.io as pio
import plotly.express as px
from pylab import rcParams
from lmfit import minimize
from lmfit import Parameters
from lmfit import Parameter
from lmfit import report_fit
from datetime import datetime
from datetime import timedelta
import matplotlib.pyplot as plt 
import plotly.graph_objects as go
import plotly.figure_factory as ff
from scipy.integrate import odeint
from matplotlib.axis import Axis
import matplotlib.dates as mdates
pd.options.display.max_rows = None
pd.options.display.max_columns = None
from matplotlib.pyplot import figure
from plotly.subplots import make_subplots
from matplotlib.dates import DateFormatter
style = {'description_width': '100px'}
rcParams['figure.figsize'] = 12,7
warnings.filterwarnings('ignore')
matplotlib.rcParams['axes.labelsize'] = 14
matplotlib.rcParams['xtick.labelsize'] = 12
matplotlib.rcParams['ytick.labelsize'] = 12
matplotlib.rcParams['text.color'] = 'k'
plt.style.use('ggplot')


# def visualize_rha(dfeha, dfcha, dfwha, dflgha):
#     fig, ax = plt.subplots(2,2,figsize=(25, 18));

#     ax[0,0].plot(dfeha.index, dfeha['currently_hospitalized'],ls = '-.', marker = 'o', color = 'teal', label = 'EHA') 
#     ax[0,0].plot(dfcha.index,dfcha['currently_hospitalized'],ls = '-.', marker = 'o', color = 'orange',label = 'CHA') 
#     ax[0,0].plot(dfwha.index,dfwha['currently_hospitalized'],ls = '-.', marker = 'o', color = 'blue',label = 'WHA') 
#     ax[0,0].plot(dflgha.index,dflgha['currently_hospitalized'],ls = '-.', marker = 'o', color = 'brown',label = 'lG-HA') 
#     ax[0,0].set(title="NL Trend in COVID-19 Reported Cases of Hospitalization")
#     ax[0,0].xaxis.set_major_locator(mdates.DayLocator())
#     ax[0,0].xaxis.set_major_formatter(DateFormatter("%d-%b-%y"))
#     ax[0,0].tick_params(axis="x", labelrotation= 75)

#     ax[1,0].plot(dfeha.index,dfeha['total_number_of_deaths'],ls = '-.', marker = 'o', color = 'teal',label = 'EHA') 
#     ax[1,0].plot(dfcha.index,dfcha['total_number_of_deaths'],ls = '-.', marker = 'o', color = 'orange',label = 'CHA') 
#     ax[1,0].plot(dfwha.index,dfwha['total_number_of_deaths'],ls = '-.', marker = 'o', color = 'blue',label = 'WHA') 
#     ax[1,0].plot(dflgha.index,dflgha['total_number_of_deaths'],ls = '-.', marker = 'o', color = 'brown',label = 'lG-HA') 
#     ax[1,0].set(title="NL Trend in COVID-19 Reported Cases of Mortality")
#     ax[1,0].xaxis.set_major_locator(mdates.DayLocator())
#     ax[1,0].xaxis.set_major_formatter(DateFormatter("%d-%b-%y"))
#     ax[1,0].tick_params(axis="x", labelrotation= 75)

#     ax[0,1].plot(dfeha.index,dfeha['cum_cases'],ls = '-.', marker = 'o', color = 'teal',label = 'EHA') 
#     ax[0,1].plot(dfcha.index,dfcha['cum_cases'],ls = '-.', marker = 'o', color = 'orange',label = 'CHA') 
#     ax[0,1].plot(dfwha.index,dfwha['cum_cases'],ls = '-.', marker = 'o', color = 'blue',label = 'WHA') 
#     ax[0,1].plot(dflgha.index,dflgha['cum_cases'],ls = '-.', marker = 'o', color = 'brown',label = 'lG-HA') 
#     ax[0,1].set(title="NL rend in COVID-09 Total Reported Cases")
#     ax[0,1].xaxis.set_major_locator(mdates.DayLocator())
#     ax[0,1].xaxis.set_major_formatter(DateFormatter("%d-%b-%y"))
#     ax[0,1].tick_params(axis="x", labelrotation= 75)

#     ax[1,1].plot(dfeha.index,dfeha['cum_tests'],ls = '-.', marker = 'o', color = 'teal',label = 'EHA') 
#     ax[1,1].plot(dfcha.index,dfcha['cum_tests'],ls = '-.', marker = 'o', color = 'orange',label = 'CHA') 
#     ax[1,1].plot(dfwha.index,dfwha['cum_tests'],ls = '-.', marker = 'o', color = 'blue',label = 'WHA') 
#     ax[1,1].plot(dflgha.index,dflgha['cum_tests'],ls = '-.', marker = 'o', color = 'brown',label = 'lGHA') 
#     ax[1,1].set(title="NL Trend in COVID-19 Reported Number of Tests")
#     ax[1,1].xaxis.set_major_locator(mdates.DayLocator())
#     ax[1,1].xaxis.set_major_formatter(DateFormatter("%d-%b-%y"))
#     ax[1,1].tick_params(axis="x", labelrotation= 75)

#     sns.despine()
#     fig.subplots_adjust(top=0.9, left=0.1, right=1, bottom=0.12) 
#     ax.flatten()[-2].legend(loc='upper center', bbox_to_anchor=(1.08, 1.06), ncol=4) #1, -0.12
#     # it wou
#     plt.show();

#     return ax


def daily_analysis_eha(dfeha):
    fig = make_subplots(rows=2, cols=2, specs=[[{}, {}],[{}, {}]], vertical_spacing=0.15,
                    horizontal_spacing=0.055,
                    x_title='Date',
                    y_title="Daily Count",
                    subplot_titles=("EHA Daily Test Vrs Cases Count","EHA Daily Hospitalization Vrs Death Count", 
                    "EHA Daily Cases Vrs Recovery Count", "EHA Current Hospitalization Vrs ICU Count"))

    fig.add_trace(go.Bar(x = dfeha.index, y = dfeha['daily_tests'],
                        hoverinfo = 'y+x+name',name="daily-test",marker_color = 'blue'),row=1, col=1)
    fig.add_trace(go.Bar(x = dfeha.index, y = dfeha['daily_cases'],
                        hoverinfo = 'y+x+name',name="daily-cases",marker_color = 'darkorange'), row=1, col=1),

    fig.add_trace(go.Bar(x = dfeha.index, y = dfeha['daily_hospitalized'],
                        hoverinfo = 'y+x+name',name="daily-hosp",marker_color = 'green'),row=1, col=2)
    fig.add_trace(go.Bar(x = dfeha.index, y = dfeha['daily_deaths'],
                        hoverinfo = 'y+x+name',name="daily-death",marker_color = 'red'), row=1, col=2)

    fig.add_trace(go.Bar(x = dfeha.index, y = dfeha['daily_cases'],
                        hoverinfo = 'y+x+name',name="daily-cases",marker_color = 'darkorange'),row=2, col=1)
    fig.add_trace(go.Bar(x = dfeha.index, y = dfeha['daily_recovery'],
                        hoverinfo = 'y+x+name',name="daily-recovery",marker_color = 'olive'), row=2, col=1)

    fig.add_trace(go.Bar(x = dfeha.index, y = dfeha['current_in_icu'],
                        hoverinfo = 'y+x+name',name="current-icu",marker_color = 'purple'),row=2, col=2)
    fig.add_trace(go.Bar(x = dfeha.index, y = dfeha['currently_hospitalized'],
                        hoverinfo = 'y+x+name',name="current-hosp",marker_color = 'pink'), row=2, col=2)

    fig.update_layout(height=700,width = 1200, showlegend=True,template='ggplot2',barmode = 'group') 
    return fig

def daily_analysis_cha(cha_dataframe):
    fig = make_subplots(rows=2, cols=2, specs=[[{}, {}],[{}, {}]], vertical_spacing=0.15,
                    horizontal_spacing=0.055,
                    x_title='Date',
                    y_title="Daily Count",
                    subplot_titles=("CHA Daily Test Vrs Cases Count","CHA Daily Hospitalization Vrs Death Count", 
                                    "CHA Daily Cases Vrs Recovery Count", "CHA Current Hospitalization Vrs ICU Count"))

    fig.add_trace(go.Bar(x = cha_dataframe.index, y = cha_dataframe['daily_tests'],
                        hoverinfo = 'y+x+name',name="daily-test",marker_color = 'blue'),row=1, col=1)
    fig.add_trace(go.Bar(x = cha_dataframe.index, y = cha_dataframe['daily_cases'],
                        hoverinfo = 'y+x+name',name="daily-cases",marker_color = 'darkorange'), row=1, col=1),

    fig.add_trace(go.Bar(x = cha_dataframe.index, y = cha_dataframe['daily_hospitalized'],
                        hoverinfo = 'y+x+name',name="daily-hosp",marker_color = 'green'),row=1, col=2)
    fig.add_trace(go.Bar(x = cha_dataframe.index, y = cha_dataframe['daily_deaths'],
                        hoverinfo = 'y+x+name',name="daily-death",marker_color = 'red'), row=1, col=2)

    fig.add_trace(go.Bar(x = cha_dataframe.index, y = cha_dataframe['daily_cases'],
                        hoverinfo = 'y+x+name',name="daily-cases",marker_color = 'darkorange'),row=2, col=1)
    fig.add_trace(go.Bar(x = cha_dataframe.index, y = cha_dataframe['daily_recovery'],
                        hoverinfo = 'y+x+name',name="daily-recovery",marker_color = 'olive'), row=2, col=1)

    fig.add_trace(go.Bar(x = cha_dataframe.index, y = cha_dataframe['current_in_icu'],
                        hoverinfo = 'y+x+name',name="current-icu",marker_color = 'purple'),row=2, col=2)
    fig.add_trace(go.Bar(x = cha_dataframe.index, y = cha_dataframe['currently_hospitalized'],
                        hoverinfo = 'y+x+name',name="current-hosp",marker_color = 'teal'), row=2, col=2)

    fig.update_layout(height=700,width = 1200, showlegend=True,template='ggplot2',barmode = 'group') 
    return fig

def daily_analysis_wha(wha_dataframe):
    fig = make_subplots(rows=2, cols=2, specs=[[{}, {}],[{}, {}]], vertical_spacing=0.15,
                    horizontal_spacing=0.055,
                    x_title='Date',
                    y_title="Daily Count",
    subplot_titles=("WHA Daily Test Vrs Cases Count","WHA Daily Hospitalization Vrs Death Count", 
                    "WHA Daily Cases Vrs Recovery Count", "WHA Current Hospitalization Vrs ICU Count"))

    fig.add_trace(go.Bar(x = wha_dataframe.index, y = wha_dataframe['daily_tests'],
                        hoverinfo = 'y+x+name',name="daily-test",marker_color = 'blue'),row=1, col=1)
    fig.add_trace(go.Bar(x = wha_dataframe.index, y = wha_dataframe['daily_cases'],
                        hoverinfo = 'y+x+name',name="daily-cases",marker_color = 'darkorange'), row=1, col=1),

    fig.add_trace(go.Bar(x = wha_dataframe.index, y = wha_dataframe['daily_hospitalized'],
                        hoverinfo = 'y+x+name',name="daily-hosp",marker_color = 'green'),row=1, col=2)
    fig.add_trace(go.Bar(x = wha_dataframe.index, y = wha_dataframe['daily_deaths'],
                        hoverinfo = 'y+x+name',name="daily-death",marker_color = 'red'), row=1, col=2)

    fig.add_trace(go.Bar(x = wha_dataframe.index, y = wha_dataframe['daily_cases'],
                        hoverinfo = 'y+x+name',name="daily-cases",marker_color = 'darkorange',showlegend = False),row=2, col=1)
    fig.add_trace(go.Bar(x = wha_dataframe.index, y = wha_dataframe['daily_recovery'],
                        hoverinfo = 'y+x+name',name="daily-recovery",marker_color = 'olive'), row=2, col=1)

    fig.add_trace(go.Bar(x = wha_dataframe.index, y = wha_dataframe['current_in_icu'],
                        hoverinfo = 'y+x+name',name="current-icu",marker_color = 'purple'),row=2, col=2)
    fig.add_trace(go.Bar(x = wha_dataframe.index, y = wha_dataframe['currently_hospitalized'],
                        hoverinfo = 'y+x+name',name="current-hosp",marker_color = 'teal'), row=2, col=2)

    fig.update_layout(height=700,width = 1200, showlegend=True,template='ggplot2',barmode = 'stack') 
    return fig 

def daily_analysis_wha(dflgha):

    fig = make_subplots(rows=2, cols=2, specs=[[{}, {}],[{}, {}]], vertical_spacing=0.15,
                    horizontal_spacing=0.055,
                    x_title='Date',
                    y_title="Daily Count",
                    subplot_titles=("LG-HA Daily Test Vrs Cases Count","LG-HA Daily Hospitalization Vrs Death Count", 
                    "LG-HA Daily Cases Vrs Recovery Count", "LG-HA Current Hospitalization Vrs ICU Count"))

    fig.add_trace(go.Bar(x = dflgha.index, y = dflgha['daily_tests'],
                        hoverinfo = 'y+x+name',name="daily-test",marker_color = 'blue'),row=1, col=1)
    fig.add_trace(go.Bar(x = dflgha.index, y = dflgha['daily_cases'],
                        hoverinfo = 'y+x+name',name="daily-cases",marker_color = 'darkorange'), row=1, col=1),

    fig.add_trace(go.Bar(x = dflgha.index, y = dflgha['daily_hospitalized'],
                        hoverinfo = 'y+x+name',name="daily-hosp",marker_color = 'green'),row=1, col=2)
    fig.add_trace(go.Bar(x = dflgha.index, y = dflgha['daily_deaths'],
                        hoverinfo = 'y+x+name',name="daily-death",marker_color = 'red'), row=1, col=2)

    fig.add_trace(go.Bar(x = dflgha.index, y = dflgha['daily_cases'],
                        hoverinfo = 'y+x+name',name="daily-cases",marker_color = 'darkorange',showlegend = False),row=2, col=1)
    fig.add_trace(go.Bar(x = dflgha.index, y = dflgha['daily_recovery'],
                        hoverinfo = 'y+x+name',name="daily-recovery",marker_color = 'olive'), row=2, col=1)

    fig.add_trace(go.Bar(x = dflgha.index, y = dflgha['current_in_icu'],
                        hoverinfo = 'y+x+name',name="current-icu",marker_color = 'purple'),row=2, col=2)
    fig.add_trace(go.Bar(x = dflgha.index, y = dflgha['currently_hospitalized'],
                        hoverinfo = 'y+x+name',name="current-hosp",marker_color = 'teal'), row=2, col=2)

    fig.update_layout(height=700,width = 1200, showlegend=True,template='ggplot2',barmode = 'stack') 
    
    return fig

def plot_totals_rha(dfeha, dfcha, dfwha, dflgha):

    fig = make_subplots(rows=2, cols=2, specs=[[{}, {}],[{}, {}]], vertical_spacing=0.15,
                    horizontal_spacing=0.055,
                    x_title='Date',
                    y_title="Total Count",
                    subplot_titles=("Total Test Count/1k People ","Total Cases Count/100 People", 
                                    "Total Hospitalization Count", "Total Death Count")) 
    fig.add_trace(go.Scatter(x = dfeha.index, y = dfeha['cum_tests']/1000 , 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="EHA",line=dict(color='blue', width=0.5),
                                showlegend=True),row=1, col=1)
    fig.add_trace(go.Scatter(x = dfcha.index, y = dfcha['cum_tests']/1000, 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="CHA",line=dict(color='green', width=0.5),
                                showlegend=True), row=1, col=1)
    fig.add_trace(go.Scatter(x = dfwha.index, y = dfwha['cum_tests']/1000, 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="WHA",line=dict(color='red', width=0.5),
                                showlegend=True), row=1, col=1)
    fig.add_trace(go.Scatter(x = dflgha.index, y = dflgha['cum_tests']/1000, 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="LG-HA",line=dict(color='orange', width=0.5),
                                showlegend=True), row=1, col=1)

    fig.add_trace(go.Scatter(x = dfeha.index, y = dfeha['cum_cases'], 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="EHA",line=dict(color='blue', width=0.5),
                                showlegend=False),row=1, col=2)
    fig.add_trace(go.Scatter(x = dfcha.index, y = dfcha['cum_cases']/100, 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="CHA",line=dict(color='green', width=0.5),
                                showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x = dfwha.index, y = dfwha['cum_cases']/100, 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="WHA",line=dict(color='red', width=0.5),
                                showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x = dflgha.index, y = dflgha['cum_cases']/100, 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="LG-HA",line=dict(color='orange', width=0.5),
                                showlegend=False), row=1, col=2)

    fig.add_trace(go.Scatter(x = dfeha.index, y = dfeha['currently_hospitalized'], 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="EHA",line=dict(color='blue', width=0.5),
                                showlegend=False),row=2, col=1)
    fig.add_trace(go.Scatter(x = dfcha.index, y = dfcha['currently_hospitalized'], 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="CHA",line=dict(color='green', width=0.5),
                                showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x = dfwha.index, y = dfwha['currently_hospitalized'], 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="WHA",line=dict(color='red', width=0.5),
                                showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x = dflgha.index, y = dflgha['currently_hospitalized'], 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="LG-HA",line=dict(color='orange', width=0.5),
                                showlegend=False), row=2, col=1)

    fig.add_trace(go.Scatter(x = dfeha.index, y = dfeha['total_number_of_deaths'], 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="EHA",line=dict(color='blue', width=0.5),
                                showlegend=False),row=2, col=2)
    fig.add_trace(go.Scatter(x = dfcha.index, y = dfcha['total_number_of_deaths'], 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="CHA",line=dict(color='green', width=0.5),
                                showlegend=False), row=2, col=2)
    fig.add_trace(go.Scatter(x = dfwha.index, y = dfwha['total_number_of_deaths'], 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="WHA",line=dict(color='red', width=0.5),
                                showlegend=False), row=2, col=2)
    fig.add_trace(go.Scatter(x = dflgha.index, y = dflgha['total_number_of_deaths'], 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="LG-HA",line=dict(color='orange', width=0.5),
                                showlegend=False), row=2, col=2)

    fig.update_layout(height=700,width = 1200, showlegend=True,template='ggplot2',barmode='overlay')
    
    return fig  #['ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', ...]

def plot_dailys_rha(dfeha, dfcha, dfwha, dflgha): 

    fig = make_subplots(rows=2, cols=2, specs=[[{}, {}],[{}, {}]], vertical_spacing=0.15,horizontal_spacing=0.055,
                    x_title='Date',
                    y_title="Count",
                    subplot_titles=("Daily Test Count / 100 People","Daily Cases Count", 
                    "Daily Hospitalization Count", "Daily Death Count"))
    fig.add_trace(go.Scatter(x = dfeha.index, y = dfeha['daily_tests']/100 , 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="EHA",line=dict(color='blue', width=0.5),
                                showlegend=True),row=1, col=1)
    fig.add_trace(go.Scatter(x = dfcha.index, y = dfcha['daily_tests']/100, 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="CHA",line=dict(color='green', width=0.5),
                                showlegend=True), row=1, col=1)
    fig.add_trace(go.Scatter(x = dfwha.index, y = dfwha['daily_tests']/100, 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="WHA",line=dict(color='red', width=0.5),
                                showlegend=True), row=1, col=1)
    fig.add_trace(go.Scatter(x = dflgha.index, y = dflgha['daily_tests']/100, 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="LG-HA",line=dict(color='orange', width=0.5),
                                showlegend=True), row=1, col=1)

    fig.add_trace(go.Scatter(x = dfeha.index, y = dfeha['daily_cases'], 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="EHA",line=dict(color='blue', width=0.5),
                                showlegend=False),row=1, col=2)
    fig.add_trace(go.Scatter(x = dfcha.index, y = dfcha['daily_cases'], 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="CHA",line=dict(color='green', width=0.5),
                                showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x = dfwha.index, y = dfwha['daily_cases'], 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="WHA",line=dict(color='red', width=0.5),
                                showlegend=False), row=1, col=2)
    fig.add_trace(go.Scatter(x = dflgha.index, y = dflgha['daily_cases'], 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="LG-HA",line=dict(color='orange', width=0.5),
                                showlegend=False), row=1, col=2)

    fig.add_trace(go.Scatter(x = dfeha.index, y = dfeha['daily_hospitalized'], 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="EHA",line=dict(color='blue', width=0.5),
                                showlegend=False),row=2, col=1)
    fig.add_trace(go.Scatter(x = dfcha.index, y = dfcha['daily_hospitalized'], 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="CHA",line=dict(color='green', width=0.5),
                                showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x = dfwha.index, y = dfwha['daily_hospitalized'], 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="WHA",line=dict(color='red', width=0.5),
                                showlegend=False), row=2, col=1)
    fig.add_trace(go.Scatter(x = dflgha.index, y = dflgha['daily_hospitalized'], 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="LG-HA",line=dict(color='orange', width=0.5),
                                showlegend=False), row=2, col=1)

    fig.add_trace(go.Scatter(x = dfeha.index, y = dfeha['daily_deaths'], 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="EHA",line=dict(color='blue', width=0.5),
                                showlegend=False),row=2, col=2)
    fig.add_trace(go.Scatter(x = dfcha.index, y = dfcha['daily_deaths'], 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="CHA",line=dict(color='green', width=0.5),
                                showlegend=False), row=2, col=2)
    fig.add_trace(go.Scatter(x = dfwha.index, y = dfwha['daily_deaths'], 
                                hoverinfo = 'x+y+name', mode='lines+markers', name="WHA",line=dict(color='red', width=0.5),
                                showlegend=False), row=2, col=2)
    fig.add_trace(go.Scatter(x = dflgha.index, y = dflgha['daily_deaths'], 
                                hoverinfo = 'x+y+name', mode='lines+markers',name="LG-HA",line=dict(color='orange', width=0.5),
                                showlegend=False), row=2, col=2)

    fig.update_layout(height=700,width = 1200, showlegend=True,template='ggplot2',barmode='overlay') #['ggplot2', 'seaborn', 'simple_white', 'plotly', 'plotly_white', ...]

    return fig


def daily_test_positivity(dfeha, dfcha, dfwha, dflgha):
    # fig = make_subplots(rows=2, cols=2, specs=[[{}, {}],[{}, {}]], 
    # subplot_titles=("EHA: Daily Test Positivity ","CHA: Daily Test Positivity", "WHA: Daily Test Positivity", "LG-HA: Daily Test Positivity"),
    # ) #[{"colspan": 2}, None]

    fig = make_subplots(rows=2,cols=2,specs=[[{}, {}],[{}, {}]],
                    #print_grid=True,
                    vertical_spacing=0.15,
                    horizontal_spacing=0.055,
                    x_title='Date',
                    y_title="Daily Count",
                    subplot_titles=("EHA: Daily Test Positivity ", "CHA: Daily Test Positivity", 
                                    "WHA: Daily Test Positivity", "LG-HA: Daily Test Positivity"))

    fig.add_trace(go.Scatter(x = dfeha.index, y = dfeha['daily_test_pos_rate'], hoverinfo = 'x+y+name',
                            mode='lines+markers', name="EHA",line=dict(color='blue', width=1),showlegend=True),row=1, col=1)

    fig.add_trace(go.Scatter(x = dfcha.index, y = dfcha['daily_test_pos_rate'], hoverinfo = 'x+y+name',
                            mode='lines+markers',  name="CHA",line=dict(color='green', width=1),showlegend=True), row=1, col=2)

    fig.add_trace(go.Scatter(x = dfwha.index, y = dfwha['daily_test_pos_rate'], hoverinfo = 'x+y+name', 
                            mode='lines+markers', name="WHA",line=dict(color='red', width=1),showlegend=True), row=2, col=1)

    fig.add_trace(go.Scatter(x = dflgha.index, y = dflgha['daily_test_pos_rate'], hoverinfo = 'x+y+name',
                            mode='lines+markers', name="LG-HA",line=dict(color='orange', width=1),showlegend=True), row=2, col=2)

    fig.update_layout(height=700,width = 1200, showlegend=True,template='ggplot2',barmode='overlay')

    return fig

def compare_daily_test_positivity(dfeha, dfcha, dfwha, dflgha):
    fig = make_subplots(rows=1, cols=1, specs=[[{}]],)

    fig.add_trace(go.Scatter(x = dfeha.index, y = dfeha['daily_test_pos_rate'], hoverinfo = 'x+y+name',
                            mode='lines+markers', name="EHA",line=dict(color='blue', width=1),showlegend=True),row=1, col=1)

    fig.add_trace(go.Scatter(x = dfcha.index, y = dfcha['daily_test_pos_rate'], hoverinfo = 'x+y+name',
                            mode='lines+markers',  name="CHA",line=dict(color='green', width=1),showlegend=True), row=1, col=1)

    fig.add_trace(go.Scatter(x = dfwha.index, y = dfwha['daily_test_pos_rate'], hoverinfo = 'x+y+name', 
                            mode='lines+markers', name="WHA",line=dict(color='red', width=1),showlegend=True), row=1, col=1)

    fig.add_trace(go.Scatter(x = dflgha.index, y = dflgha['daily_test_pos_rate'], hoverinfo = 'x+y+name',
                            mode='lines+markers', name="LG-HA",line=dict(color='orange', width=1),showlegend=True), row=1, col=1)

    fig.update_layout(title="Daily Test Positivity For ALL RHA",xaxis_title="Date",yaxis_title="Test Positivity (%)",height=700,width = 1200, showlegend=True,template='ggplot2',barmode='overlay')
    # fig.for_each_xaxis(lambda axis: axis.title.update(font=dict(color = 'blue', size=20)))

    return fig











