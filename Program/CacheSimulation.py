from PyQt5.QtWidgets import QApplication,QWidget,QHBoxLayout,QAbstractItemView,QTableWidgetItem,QPushButton,QLabel,QVBoxLayout,QComboBox,QTextEdit,QTableWidget,QSizePolicy,QSpinBox,QHeaderView,QGroupBox,QGridLayout
import sys
cache_blocks = 32
cache_line = 16
sets = 8

class CacheSimulator(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
    
    def initUI(self):
        self.setWindowTitle('8 Way BSA-MRU Cache Simulation System')
        self.setGeometry(100, 100, 600, 400)

        main_layout = QVBoxLayout()

        cache_layout = QVBoxLayout()
        main_layout.addLayout(cache_layout)

        self.cache_snapshot_qlabel = QLabel('Final Cache Memory Snapshot:')
        self.cache_qtable = QTableWidget(sets,(cache_blocks//sets)+1)
        intilialize_cache_table(self)
        
        self.cache_qtable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.cache_qtable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.cache_qtable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cache_qtable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.cache_qtable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.cache_qtable.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)

        self.cache_qtable.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.cache_qtable.verticalHeader().setVisible(False)

        cache_layout.addWidget(self.cache_snapshot_qlabel)
        cache_layout.addWidget(self.cache_qtable)

        self.outputs_groupbox = QGroupBox("Cache Outputs")
        self.outputs_layout = QGridLayout()

        self.outputs_groupbox.setStyleSheet("""
            QGroupBox {
                background-color: black;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                color: cyan;
            }
            QLabel {
                font-size: 12px;
                color:cyan;
            }
        """)

        self.memory_access_qstat = QLabel('0')
        self.cache_hit_qstat = QLabel('0')
        self.cache_miss_qstat = QLabel('0')
        self.cache_hit_rate_qstat = QLabel('0.00%')
        self.cache_miss_rate_qstat = QLabel('0.00%')
        self.avg_memory_time_qstat = QLabel('0ns')
        self.total_memory_time_qstat = QLabel('0ns')

        self.outputs_layout.addWidget(QLabel("Memory Access Count:"), 0, 0)
        self.outputs_layout.addWidget(self.memory_access_qstat, 0, 1)
        self.outputs_layout.addWidget(QLabel("Cache Hit Count:"), 1, 0)
        self.outputs_layout.addWidget(self.cache_hit_qstat, 1, 1)
        self.outputs_layout.addWidget(QLabel("Cache Miss Count:"), 2, 0)
        self.outputs_layout.addWidget(self.cache_miss_qstat, 2, 1)
        self.outputs_layout.addWidget(QLabel("Cache Hit Rate:"), 3, 0)
        self.outputs_layout.addWidget(self.cache_hit_rate_qstat, 3, 1)
        self.outputs_layout.addWidget(QLabel("Cache Miss Rate:"), 4, 0)
        self.outputs_layout.addWidget(self.cache_miss_rate_qstat, 4, 1)
        self.outputs_layout.addWidget(QLabel("Avg Memory Access Time:"), 5, 0)
        self.outputs_layout.addWidget(self.avg_memory_time_qstat, 5, 1)
        self.outputs_layout.addWidget(QLabel("Total Memory Access Time:"), 6, 0)
        self.outputs_layout.addWidget(self.total_memory_time_qstat, 6, 1)

        self.outputs_groupbox.setLayout(self.outputs_layout)
        cache_layout.addWidget(self.outputs_groupbox)

        menu_layout = QVBoxLayout()

        self.memory_size_qlabel = QLabel('Enter Number of Memory Blocks:')
        self.memory_size_qinput = QSpinBox()
        self.memory_size_qinput.setButtonSymbols(2)
        self.memory_size_qinput.setMinimum(1024)
        self.memory_size_qinput.setMaximum(32768)
        self.memory_size_qinput.setSuffix(' Blocks')
        menu_layout.addWidget(self.memory_size_qlabel)
        menu_layout.addWidget(self.memory_size_qinput)
        
        self.test_case_qlabel = QLabel('Select Test Case:')
        self.test_case_qselect = QComboBox()
        self.test_case_qselect.addItems(["Sequential", "Random", "Mid-Repeat"])
        
        menu_layout.addWidget(self.test_case_qlabel)
        menu_layout.addWidget(self.test_case_qselect)

        buttonslist = QHBoxLayout()
        self.startsim_qbutton = QPushButton('Start Simulation')
        self.startsim_qbutton.clicked.connect(self.start_simulation)
        
        buttonslist.addWidget(self.startsim_qbutton)

        self.clearsim_qbutton = QPushButton('Clear Simulation')
        self.clearsim_qbutton.clicked.connect(self.clear_simulation)
        buttonslist.addWidget(self.clearsim_qbutton)
        menu_layout.addLayout(buttonslist)

        self.log_output = QTextEdit()
        self.log_output.setStyleSheet("background-color: black; color: lime;border-radius: 5px;padding: 10px;padding-top:0px")
        self.log_output.setReadOnly(True)
        self.log_output.setHtml("<b>Simulation Log</b>")
        menu_layout.addWidget(self.log_output)
        
        main_layout.addSpacing(20) 
        main_layout.addLayout(menu_layout)
        main_layout.setStretchFactor(cache_layout, 3)  
        main_layout.setStretchFactor(menu_layout, 2) 
        self.setLayout(main_layout)
    
    def start_simulation(self):
        memory_blocks = self.memory_size_qinput.value()
        test_case = self.test_case_qselect.currentText()
        total_access,cache_hit,cache_miss,hit_rate,miss_rate,avg_mem_access_time,total_mem_access_time = (0,0,0,0,0,0,0)
        self.log_output.append(f"Simulation Started with {memory_blocks} memory blocks and {test_case} test case")
        self.log_output.append(f"Simulation Completed")
        self.memory_access_qstat.setText(f"{total_access}")
        self.cache_hit_qstat.setText(str(cache_hit))
        self.cache_miss_qstat.setText(str(cache_miss))
        self.cache_hit_rate_qstat.setText(f"{hit_rate:.2f}%")
        self.cache_miss_rate_qstat.setText(f"{miss_rate:.2f}%")
        self.avg_memory_time_qstat.setText(f"{avg_mem_access_time}ns")
        self.total_memory_time_qstat.setText(f"{total_mem_access_time}ns")



    def clear_simulation(self):
        self.log_output.clear()
        self.log_output.setHtml("<b>Simulation Log</b>")
        
        self.memory_access_qstat.setText('0')
        self.cache_hit_qstat.setText('0')
        self.cache_miss_qstat.setText('0')
        self.cache_hit_rate_qstat.setText('0.00%')
        self.cache_miss_rate_qstat.setText('0.00%')
        self.avg_memory_time_qstat.setText('0ns')
        self.total_memory_time_qstat.setText('0ns')
        intilialize_cache_table(self)

def intilialize_cache_table(self):
    self.cache_qtable.clear()
    self.cache_qtable.setHorizontalHeaderLabels(["Set", "Block 0","Block 1","Block 2","Block 3"])
    for i in range(sets):
            item = QTableWidgetItem(str(i))
            self.cache_qtable.setItem(i, 0, item)

def sequential_test(self):
    
    pass

def random_test(self):
    pass

def midrepeat_test(self):  
    pass


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CacheSimulator()
    window.show()
    sys.exit(app.exec_())
