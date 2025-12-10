from PyQt6.QtCore import QTimer
from PyQt6.QtWidgets import (
    QGridLayout,
    QLabel,
    QPushButton,
    QSizePolicy,
    QTabWidget,
    QWidget,
)


#Class for the various statistics to be displayed on a stats page
class Stat(QWidget):
    def __init__(self, stat_name : str, stat_value : float | int):
        super().__init__()

        #Creates two labels with the name of the statistic to be shown and 
        self.stat_label = QLabel(stat_name, self)
        self.stat_value_label = QLabel(stat_value, self)

    def update_stat(self):
        self.stat_label.repaint()
        self.stat_value_label.repaint()


#Class for all tabs that automatically adds them to the tab container
class Tab(QWidget):
    def __init__(self, tab_name : str, tabs_holder : QTabWidget):
        super().__init__()
        self.tab_name = tab_name

        tabs_holder.addTab(self, tab_name)

#Stats Page that is a tab in the Tabs container
class StatsTab(Tab):
    def __init__(self, tab_name, tabs_holder):
        super().__init__(tab_name, tabs_holder)

        self.stats = {} #Create a dictionary of stats to allow easy access of individual ones later

        #Timer for updating the stats every 10000ms
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_stats)
        self.timer.start(10000)

    #Adds stats by creating an instance of the stat Class
    def add_stat(self, name:str, value:int|float):
        self.stats[name] = Stat(name, value)

    def update_stats(self):
        for stat in self.stats.values():
            stat.update_stat()




#Runs some test code if this file is run directly
if __name__ == "__main__":
    import sys

    from PyQt6.QtWidgets import QApplication, QMainWindow

    app = QApplication(sys.argv)

    tabs = QTabWidget()

    window = QMainWindow()
    window.setFixedSize(576,324) #7-inch touch display 2 size
    window.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
    window.setCentralWidget(tabs)
    window.show()

    sys.exit(app.exec())

