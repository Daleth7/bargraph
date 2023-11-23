import pyqtgraph as pg
import random

randcolor = lambda:random.randint(0, 0xFF)

class BarGraph:
    min_barlen = 20
    max_barlen = 100
    bar_width = 1
    len_step = 0.1

    def __init__(self) -> None:
        self.layout = pg.GraphicsLayoutWidget()
        self.plot = self.layout.addPlot(row = 0, col = 0, colspan = 2)
        self.bars = pg.BarGraphItem(x = [0], y = [0], height = self.bar_width, width = [0], pen = None)
        self.line = pg.InfiniteLine(pos = 0, pen = pg.mkPen('red', width = 3))
        self.rand_start = True

        self.plot.addItem(self.bars)
        self.plot.addItem(self.line)

        button = pg.QtWidgets.QPushButton('Reset')
        button.clicked.connect(self.setup)
        proxy = pg.QtWidgets.QGraphicsProxyWidget()
        proxy.setWidget(button)
        self.layout.addItem(proxy, row = 1, col = 0)

        x_start_button = pg.QtWidgets.QPushButton('Toggle Start Position')
        x_start_button.clicked.connect(self.toggle_x_start)
        x_start_proxy = pg.QtWidgets.QGraphicsProxyWidget()
        x_start_proxy.setWidget(x_start_button)
        self.layout.addItem(x_start_proxy, row = 1, col = 1)

    def setup(self) -> None:
        self.bar_count = random.randint(2, 100)
        if self.rand_start:
            self.x_start = [random.randint(0, self.max_barlen-self.min_barlen) for _ in range(self.bar_count)]
        else:
            self.x_start = [0]*self.bar_count

        self.colors = [(randcolor(), randcolor(), randcolor()) for _ in range(self.bar_count)]
        self.bars.setOpts(x = self.x_start, y = range(self.bar_count), width = [0]*self.bar_count, brushes = self.colors)
        self.line.setPos(0)

        self.end_lens = [0]*self.bar_count
        for i in range(self.bar_count):
            while self.end_lens[i] < 1:
                self.end_lens[i] = random.randint(self.min_barlen, self.max_barlen)-self.x_start[i]
        self.cur_len = 0.0
        self.max_len = max([self.end_lens[i]+self.x_start[i] for i in range(self.bar_count)])

    def update_bars(self) -> None:
        self.cur_len += self.len_step

        lens = [max(0, min(self.cur_len-self.x_start[i], self.end_lens[i])) for i in range(self.bar_count)]
        x_centers = [self.x_start[i]+(lens[i]/2.0) for i in range(self.bar_count)]

        self.bars.setOpts(x = x_centers, width = lens)
        self.line.setPos(min(self.cur_len, self.max_len))

    def toggle_x_start(self) -> None:
        self.rand_start = not self.rand_start

graph = BarGraph()
graph.setup()

shortcut = pg.QtGui.QShortcut(pg.QtGui.QKeySequence('Space'), graph.layout)
shortcut.activated.connect(graph.setup)

toggle_shortcut = pg.QtGui.QShortcut(pg.QtGui.QKeySequence('t'), graph.layout)
toggle_shortcut.activated.connect(graph.toggle_x_start)

timer = pg.QtCore.QTimer()
timer.timeout.connect(graph.update_bars)
timer.start(16)

graph.layout.show()

pg.exec()