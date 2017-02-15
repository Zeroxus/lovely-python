import sys
import os
import datetime
import matplotlib
# 使用Qt5的引擎来渲染matplotlib图像
matplotlib.use('Qt5Agg')
from PyQt5 import QtCore, QtWidgets

import tushare as ts
import matplotlib.finance as mpf
import matplotlib.dates as mdates

from numpy import arange, sin, pi
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.pylab import date2num

progname = os.path.basename(sys.argv[0])
progversion = "0.1"


class MyMplCanvas(FigureCanvas):
    """Ultimately, this is a QWidget (as well as a FigureCanvasAgg, etc.)."""

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)

        self.compute_initial_figure()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                                   QtWidgets.QSizePolicy.Expanding,
                                   QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

    def compute_initial_figure(self):
        pass


class MyDynamicMplCanvas(MyMplCanvas):
    """A canvas that updates itself every second with a new plot."""

    def __init__(self, *args, **kwargs):
        MyMplCanvas.__init__(self, *args, **kwargs)
        timer = QtCore.QTimer(self)
        timer.timeout.connect(self.update_figure)
        timer.start(5000)

    def compute_initial_figure(self):
        data_list = []
        hist_data = ts.get_hist_data('000001')
        for dates, row in hist_data.iterrows():
            # 将时间转换为数字
            date_time = datetime.datetime.strptime(dates, '%Y-%m-%d')
            t = date2num(date_time)
            open, high, low, close = row[:4]
            datas = (t, open, high, low, close)
            data_list.append(datas)
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        # self.axes.plot(date_time, data_list, 'r')
        exam = mpf.candlestick_ohlc(self.axes, data_list, width=0.15, colorup='g', colordown='r')

    def update_figure(self):

        data_list = []
        hist_data = ts.get_hist_data('000001')
        for dates, row in hist_data.iterrows():
            # 将时间转换为数字
            date_time = datetime.datetime.strptime(dates, '%Y-%m-%d')
            t = date2num(date_time)
            open, high, low, close = row[:4]
            datas = (t, open, high, low, close)
            data_list.append(datas)
        self.axes.cla()
        self.axes.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
        exam = mpf.candlestick_ohlc(self.axes, data_list, width=0.15, colorup='r', colordown='g')
        self.draw()


class ApplicationWindow(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowTitle("主窗口")

        self.file_menu = QtWidgets.QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.fileQuit,
                                 QtCore.Qt.CTRL + QtCore.Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.help_menu = QtWidgets.QMenu('&Help', self)
        self.menuBar().addSeparator()
        self.menuBar().addMenu(self.help_menu)

        self.help_menu.addAction('&About', self.about)

        self.main_widget = QtWidgets.QWidget(self)

        l = QtWidgets.QVBoxLayout(self.main_widget)
        dc = MyDynamicMplCanvas(self.main_widget, width=10, height=6, dpi=100)
        l.addWidget(dc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)

        self.statusBar().showMessage("All hail matplotlib!", 2000)

    def fileQuit(self):
        self.close()

    def closeEvent(self, ce):
        self.fileQuit()

    def about(self):
        QtWidgets.QMessageBox.about(self, "About",
                                    """test"""
                                )


qApp = QtWidgets.QApplication(sys.argv)

aw = ApplicationWindow()
aw.setWindowTitle("%s" % progname)
aw.show()
sys.exit(qApp.exec_())
