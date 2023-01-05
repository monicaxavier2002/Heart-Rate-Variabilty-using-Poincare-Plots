import tkinter as tk 
from tkinter import filedialog
from tkinter import Canvas
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
# Implement the default Matplotlib key bindings.
#from matplotlib.backend_bases import key_press_handler
import numpy as np
import heartpy as hp
import heartpy.config
from matplotlib.patches import Ellipse
import matplotlib.pyplot as plt


windows=tk.Tk()
windows.title("Poincare analysis")
windows.geometry("2500x1000")
windows.config(bg="light pink")
plt.ion()
img=tk.PhotoImage(file="logo.png")
tk.Label(windows,image=img).place(x=590,y=0)
tk.Label(windows, text="Biomedical Engineering Department", font=("Times new roman",24), bg="light pink").place(x=650,y=109)
tk.Label(windows, text='Mini Project on "Poincare Presentation of Arrhythmias"', font=("Times new roman",20), bg="light pink").place(x=580,y=156)
def select():
    select.tf = filedialog.askopenfilename(
        initialdir="C:/Files/Backup/Monica/Sem VI Mini project/", 
        title="Open Text file", 
        filetypes=(("Text Files", "*.txt"),)
        )
    select.file = open(select.tf)  # or tf = open(tf, 'r')
    select.data = np.loadtxt(select.file)
    spchar="/_"
    for i in spchar:    
        select.tf=select.tf.replace(i,".")    
    select.b=select.tf.split('.')
    select.name=select.b[-4]    
    select.age=select.b[-3] 
    select.gender=select.b[-2] 
    select.file.close()


def rotate_vec(x, y, angle):
    theta = np.radians(angle)

    cs = np.cos(theta)
    sn = np.sin(theta)

    x_rot = (x * cs) - (y * sn)
    y_rot = (x * sn) + (y * cs)

    return x_rot, y_rot
def plot():
    canvas = Canvas(windows, height=200,width=350)
    canvas.create_rectangle(5,5, 346, 196, outline="pink")
    canvas.place(x=50,y=600)  
    tk.Label(windows, text="Name", font=("Times new roman",12)).place(x=70,y=630)  
    tk.Label(windows, text="Age", font=("Times new roman",12)).place(x=70,y=680)
    tk.Label(windows, text="Gender", font=("Times new roman",12)).place(x=70,y=730)
    Name=tk.Text(windows,font=("Times new roman",12),height=1, width=20)
    Name.place(x=150,y=630)
    Name.insert(tk.INSERT,select.name)
    Name.configure(state='disabled')
    Age=tk.Text(windows,font=("Times new roman",12),height=1, width=20)
    Age.place(x=150,y=680)
    Age.insert(tk.INSERT,select.age)
    Age.configure(state='disabled')
    Gender=tk.Text(windows,font=("Times new roman",12),height=1, width=20)
    Gender.place(x=150,y=730)
    Gender.insert(tk.INSERT,select.gender)
    Gender.configure(state='disabled')

    filtered = hp.filter_signal(select.data, cutoff =0.75, order=2, sample_rate = 500, filtertype='highpass')
    wd, m = hp.process(hp.scale_data(filtered), sample_rate=500)
    fig = Figure(figsize = (5, 4),
                                dpi = 100)
#    plot2 = fig.add_subplot(111) 
    
    heartpy.config.colorblind = False
    heartpy.config.color_style = 'default'
    colorpalette = heartpy.config.get_colorpalette_poincare()

    #get values from dict
    x_plus = wd['poincare']['x_plus']
    x_minus = wd['poincare']['x_minus']
    sd1 = m['sd1']
    sd2 = m['sd2']
    
    ax= fig.add_subplot(111)
    #plot scatter
    ax.scatter(x_plus, x_minus, color = colorpalette[0],
                alpha = 0.75, label = 'peak-peak intervals')

    #plot identity line
    mins = np.min([x_plus, x_minus])
    maxs = np.max([x_plus, x_minus])
    identity_line = np.linspace(np.min(mins), np.max(maxs))
    ax.plot(identity_line, identity_line, color='black', alpha=0.5,
            label = 'identity line')

    #rotate SD1, SD2 vectors 45 degrees counterclockwise
    sd1_xrot, sd1_yrot = rotate_vec(0, sd1, 45)
    sd2_xrot, sd2_yrot = rotate_vec(0, sd2, 45)

    #plot rotated SD1, SD2 lines
    ax.plot([np.mean(x_plus), np.mean(x_plus) + sd1_xrot],
              [np.mean(x_minus), np.mean(x_minus) + sd1_yrot],
              color = colorpalette[1], label = 'SD1')
    ax.plot([np.mean(x_plus), np.mean(x_plus) - sd2_xrot],
              [np.mean(x_minus), np.mean(x_minus) + sd2_yrot],
              color = colorpalette[2], label = 'SD2')

    #plot ellipse
    xmn = np.mean(x_plus)
    ymn = np.mean(x_minus)
    el = Ellipse((xmn, ymn), width = sd2 * 2, height = sd1 * 2, angle = 45.0)
    ax.add_artist(el)
    el.set_edgecolor((0,0,0))
    el.fill = False

    ax.set_xlabel('RRi_n (ms)')
    ax.set_ylabel('RRi_n+1 (ms)')
    if select.name=="Thomas":
        ax.set_xlim([0,600])
        ax.set_ylim([0,600])
    fig.subplots_adjust(right=0.7)
    my_label=['Identity line','SD1','SD2','Peak-Peak \n intervals']
    ax.legend(labels=my_label, bbox_to_anchor=(1.04,0.5,0.2,0.1), loc="center left", borderaxespad=0, framealpha=0.6)
    #fig.tight_layout()
    ax.set_title("Poincare plot")
    
    canvas = FigureCanvasTkAgg(fig, master=windows)  # A tk.DrawingArea.   
    canvas.get_tk_widget().place(x=600,y=530)
    canvas.draw()  
   
    fig = Figure(figsize = (5, 4),
                               dpi = 100)
    plot2 = fig.add_subplot(111)
    
    plot2.set_title("Line plot")
    plot2.plot(x_plus, x_minus)
    plot2.set_xlabel('RRi_n (ms)')
    plot2.set_ylabel('RRi_n+1 (ms)')
    canvas = FigureCanvasTkAgg(fig, master=windows)  # A tk.DrawingArea.   
    canvas.get_tk_widget().place(x=1200,y=530)
    canvas.draw() 

    n=len(select.data)
    i=1
    while i:
        fig = Figure(figsize = (18, 3),
                               dpi = 100)
        plot1 = fig.add_subplot(111)
        plot1.plot(select.data[i:6000+i])
        plot1.set_title("ECG signal")
        canvas = FigureCanvasTkAgg(fig, master=windows)  # A tk.DrawingArea.   
        canvas.get_tk_widget().place(x=50,y=200)
        canvas.draw()
        canvas.flush_events()
        i=i+20
        if i>=n:
            i=1

# def _quit():
#     windows.quit()     # stops mainloop
#     windows.destroy()  # this is necessary on Windows to prevent
#                     Fatal Python Error: PyEval_RestoreThread: NULL tstate

button=tk.Button(windows, text="Input Data", command=select)            
button.place(x=850,y=950)
plot_button=tk.Button(windows, text="Process", command=plot) 
plot_button.place(x=950,y=950)                  
windows.mainloop() 
