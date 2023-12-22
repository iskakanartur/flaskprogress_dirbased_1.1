from flask import render_template
from app import app, db
from app.models import *            
from app.helper_functions import *  ## pay attention to imports  -- from helper_functions import * won't work 
from flask import Flask, render_template, request, redirect, url_for, flash

from sqlalchemy import and_      ### to combine db queries in past Mo to su function 
from calendar import monthrange  ### to combine db queries in past Mo to su function 
from datetime import date, datetime, timedelta


######## For Multi Plot Progress Bar
from math import pi
import numpy as np
from matplotlib.patches import Patch
from matplotlib.lines import Line2D
import numpy as np               ### To create evenly spaced numbers 
import io
import random
from flask import Response
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt







def multi_progress_plot_viz ():

    fig, ax = plt.subplots(figsize=(7, 7))
    ax = plt.subplot(projection='polar')

    ######### Get individual progres circle data
    subjects = subj_total()                         ## Get the ('subj_name', hours_learned) touple
    data =  [i[1] for i in subjects if i[1]!= None] ## Get the hours_total from the tuple

   
    

    weekly_learning_total = get_last_weekly_goal() ## Weekly Total Learning Goal  for all subjects

    if len (data ) < 1:
       full_circle_each_subj =100000
    else : 
        full_circle_each_subj = weekly_learning_total/(len(data))        ## If empty records you have division by 0 error

    progress_full_circle_each_subj = [i/full_circle_each_subj*100 for i in data]   ## % cmplete


    startangle = 90

    ######### COLORS : Depending on Varying number of Distinct Subjects
    ######### Pick up a random color based on data length
    import random
    color_palette = ['#3FFF33', '#4393E5', '#F9FF33', '#7AE6EA', '#4933FF', '#FF336E', '#33FF8A',
                     '#FF33C1', '#FF4633', '#F9FF33', '#3FFF33', '#43BAE5'] 
    # colors = random.choices(color_palette, k = len(data)) Radnom can repeat
    colors = color_palette[:len(data)]

    xs = [(i * pi *2)/ full_circle_each_subj for i in data]

    ###### SPAcing the circles
    ys = np.linspace(3, 9, num=len(data))  ## This controls gap btw circles. Match data len 

    left = (startangle * pi *2)/ 360 #this is to control where the bar starts

    # plot bars and points at the end to make them round
    for i, x in enumerate(xs):
        ax.barh(ys[i], x, left=left, height=0.8, color=colors[i])
        ax.scatter(x+left, ys[i], s=350, color=colors[i], zorder=2) ## The cup at the end of crcle
        ax.scatter(left, ys[i], s=350, color=colors[i], zorder=2)
    
    # plt.ylim(-4, 4)   ### This Mother fucker was limiting y axis - hence number of rings
    

    ############# LEGEND ELEMENTS
    subject_titles = [i[0] for i in subjects if i[1]!= None]  ## Get the Subj names from above tuple
    legend_elements =[]

    for legend, color in list(zip(subject_titles, colors)):
        legend_elem =  [Line2D([0], [0], marker='o', color='w', label=f'{legend}',
                            markerfacecolor=f'{color}', markersize=12)]
        legend_elements.append(legend_elem)
    legend_elements = [i[0] for i in legend_elements] ## Get rid of nested lists
        
    
    ax.legend(handles=legend_elements, loc='upper right', frameon=False)
    ### clear ticks, grids, spines
    ax.set_xticks([]) # values
    ax.set_xticklabels([]) # labels

    ax.set_yticks([]) # values
    ax.set_yticklabels([]) # labels
    
    ax.spines.clear()


    plt.savefig('app/static/images/multi_progress_plot.png') ## Careful with relative and absolute paths
    # print (weekly_learning_total, full_circle_each_subj, subject_titles)
    
    # plt.show()