import matplotlib.pyplot as plt
from matplotlib import rc
from matplotlib.ticker import MultipleLocator, AutoMinorLocator
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.utils import get_color_from_hex
from constants import *

class PageButton(Button):
    def __init__(self, app, pageNumber, buttonLabel, **kwargs):
        super(PageButton, self).__init__(**kwargs)
        self.text = buttonLabel
        self.number = pageNumber
        self.app = app

    def pageClickCallback(self, pageNumber=None):
        if pageNumber == None:
            pageNumber = self.pageNumber
        if self.app.logsScreenChild.pressedPageIndex == pageNumber:
            return
        if not self.app.logsScreenChild.pressedPageIndex == -1:
            self.app.logsScreenChild.pageButtons[self.app.logsScreenChild.pressedPageIndex].pressed = False
        self.pressed = True
        self.app.logsScreenChild.pressedPageIndex = pageNumber

        range_=[int(s) for s in self.text.split('-')]
        bars = self.app.logsScreenChild.bars
        createChart(bars['names'][range_[0]-1: range_[1]], \
            bars['baseBar'][range_[0]-1: range_[1]], \
                bars['greenBar'][range_[0]-1: range_[1]], \
                    bars['redBar'][range_[0]-1: range_[1]], \
                        bars['y'][range_[0]-1: range_[1]])

        self.app.logsScreenChild.ids.ChartImageId.reload()


class LogsScreen(BoxLayout):
    def __init__(self, app, **kwargs):
        super(LogsScreen, self).__init__(**kwargs)
        self.app = app
        self.pageButtons = []
        self.logs = None
        self.pressedPageIndex = -1
        self.bars = {
            'names': None, 
            'baseBar': None, 
            'greenBar': None, 
            'redBar': None,
            'y': None
        }

    def backToAccountsListScreenCallback(self):
        self.app.screenManager.current = ALL_ACCOUNTS_SCREEN

    def createLogsChart(self, logs, currentCredit):
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

        self.bars['names'] = names
        self.bars['baseBar'] = baseBar
        self.bars['greenBar'] = greenBar
        self.bars['redBar'] = redBar
        self.bars['y'] = y

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
    ax.set_axisbelow(True)
    ax.yaxis.grid(color='white', linestyle='dashed', alpha=0.5)
    ax.yaxis.set_minor_locator(AutoMinorLocator(5))
    ax.yaxis.grid(True, which='minor', color='white', alpha=0.2)
    plt.bar(r, baseBar, color='#383354', edgecolor='white', width=barWidth)
    plt.bar(r, greenBar, bottom=baseBar, color='#3ba010', edgecolor='white', width=barWidth)
    plt.bar(r, redBar, bottom=baseBar, color='#f73737', edgecolor='white', width=barWidth)
    x1,x2,y1,y2 = plt.axis()
    plt.axis((x1,x2,y1,y2 + 0.05*y2))
    plt.plot(r, y, '--', color='white', linewidth=1.5)
    plt.xticks(r, names, rotation=60, size=8.5)
    plt.savefig(CHART_PATH, bbox_inches='tight', transparent=True , dpi=100)