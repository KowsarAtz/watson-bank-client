import matplotlib.pyplot as plt
from matplotlib import rc
from kivy.uix.boxlayout import BoxLayout
from constants import *

class LogsScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(LogsScreen, self).__init__(**kwargs)
        self.app = app

    def backToAccountsListScreenCallback(self):
        self.app.screenManager.current = ALL_ACCOUNTS_SCREEN

def createLogsChart(logs, currentCredit):
    all_ = logs[:]
    greenBar = []
    redBar = []
    baseBar = []
    names = []
    sum_ = 0
    for log in all_:
        if log['logType'] == '+':
            t = float(log['amount'])
            greenBar += [t]
            redBar += [0]
            baseBar += [t]
            sum_ += t
        elif log['logType'] == '-':
            t = float(log['amount'])
            redBar += [t]
            greenBar += [0]
            baseBar += [-t]
            sum_ += (-t)
        names += [str(log['id']) + ' , ' + log['date'][11:16] + '\n' + log['date'][:10]]
    
    baseCredit = currentCredit - sum_
    for i in range(len(baseBar)):
        baseBar[i] += baseCredit
        baseCredit = baseBar[i]
    y = baseBar[:]
    for i in range(len(baseBar)):
        baseBar[i] -= greenBar[i]

    createChart(names, baseBar, greenBar, redBar, y)

def createChart(names, baseBar, greenBar, redBar, y):
    rc('font', weight='bold')
    barWidth = 0.8
    r = list(range(len(baseBar)))
    plt.figure(figsize=(18,6))
    ax = plt.axes()
    ax.spines['bottom'].set_color('white')
    ax.spines['top'].set_color('white') 
    ax.spines['right'].set_color('white')
    ax.spines['left'].set_color('white')
    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.bar(r, baseBar, color='#7f6d5f', edgecolor='white', width=barWidth)
    plt.bar(r, greenBar, bottom=baseBar, color='#3ba010', edgecolor='white', width=barWidth)
    plt.bar(r, redBar, bottom=baseBar, color='#f73737', edgecolor='white', width=barWidth)
    x1,x2,y1,y2 = plt.axis()
    plt.axis((x1,x2,y1,y2 + 0.05*y2))
    plt.plot(r, y, 'w--')
    plt.xticks(r, names, rotation='vertical')
    plt.savefig(CHART_PATH, bbox_inches='tight', transparent=True , dpi=100)