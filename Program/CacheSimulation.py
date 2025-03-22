import random
from PyQt5.QtWidgets import QApplication,QWidget,QHBoxLayout,QAbstractItemView,QTableWidgetItem,QPushButton,QLabel,QVBoxLayout,QComboBox,QTextEdit,QTableWidget,QSizePolicy,QSpinBox,QHeaderView,QGroupBox,QGridLayout,QCheckBox
import sys
import time
cache_blocks = 32 #2^5
cache_line = 16 #2^4
sets = 4 #2^2

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
        initialize_cache_table(self)
        
        self.cache_qtable.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.cache_qtable.horizontalHeader().setSectionResizeMode(0, QHeaderView.Stretch)
        self.cache_qtable.horizontalHeader().setSectionResizeMode(1, QHeaderView.Stretch)
        self.cache_qtable.horizontalHeader().setSectionResizeMode(2, QHeaderView.Stretch)
        self.cache_qtable.horizontalHeader().setSectionResizeMode(3, QHeaderView.Stretch)
        self.cache_qtable.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        self.cache_qtable.horizontalHeader().setSectionResizeMode(5, QHeaderView.Stretch)
        self.cache_qtable.horizontalHeader().setSectionResizeMode(6, QHeaderView.Stretch)
        self.cache_qtable.horizontalHeader().setSectionResizeMode(7, QHeaderView.Stretch)
        self.cache_qtable.horizontalHeader().setSectionResizeMode(8, QHeaderView.Stretch)  
        self.cache_qtable.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
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
        self.step_by_step_qcheckbox = QCheckBox("Step-by-Step Mode")
        menu_layout.addWidget(self.step_by_step_qcheckbox)
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

        cache_blocks = 32
        sets = 4  
        ways = cache_blocks // sets  
        cache_line = 16

        cache = [[{'block': None, 'valid': False, 'mru': 0} for _ in range(ways)] for _ in range(sets)]

        total_access, cache_hit, cache_miss = 0, 0, 0
        total_mem_access_time = 0
        global_counter = 0  # counter for MRU
        step_by_step = self.step_by_step_qcheckbox.isChecked()

        self.log_output.append(f"Simulation Started with {memory_blocks} memory blocks and {test_case} test case")
        self.log_output.append(f"{'Access':<10}{'Set':<5}{'Result':<10}{'Access Time':<10}")
        self.log_output.append("=" * 60)

        if test_case == "Sequential":
            sequence = [(i % (2 * cache_blocks)) for _ in range(4) for i in range(2 * cache_blocks)]
        elif test_case == "Random":
            sequence = [random.randint(0, memory_blocks - 1) for _ in range(4 * cache_blocks)]
        elif test_case == "Mid-Repeat":
            mid = memory_blocks // 2
            sequence = [(mid + i % mid) if i % 2 == 0 else (i % memory_blocks) for i in range(cache_blocks - 1)]
        else:
            sequence = []

        # Cache simulation loop
        for memory_block in sequence:
            total_access += 1
            set_index = memory_block % sets

            hit = False
            # Check if block is in cache
            for way in range(ways):
                if cache[set_index][way]['valid'] and cache[set_index][way]['block'] == memory_block:
                    cache_hit += 1
                    cache[set_index][way]['mru'] = global_counter 
                    global_counter += 1
                    hit = True
                    result = "HIT"
                    break

            if not hit:
                cache_miss += 1

                # Find empty block first (if available) in the correct set
                empty_block = next((way for way in range(ways) if not cache[set_index][way]['valid']), None)

                if empty_block is not None:
                    # Use empty block
                    cache[set_index][empty_block] = {
                        'block': memory_block,
                        'valid': True,
                        'mru': global_counter  # Mark as most recently used
                    }
                    global_counter += 1
                    result = "MISS"
                    
                else:
                    # MRU Replacement
                    mru_index = max(range(ways), key=lambda w: cache[set_index][w]['mru'])  

                    cache[set_index][mru_index] = {
                        'block': memory_block,
                        'valid': True,
                        'mru': global_counter  
                    }
                    global_counter += 1
                    result = "REPLACE"

            # Compute access time
            access_time = (cache_line * 1) if hit else (1 + (cache_line * 10) + (cache_line * 1))
            total_mem_access_time += access_time

            self.log_output.append(f"{memory_block:<10}{set_index:<5}{result:<10}{access_time:<10}ns")

            if step_by_step:
                block = cache[set_index][way if hit else (empty_block if empty_block is not None else mru_index)]
                block_value = str(block['block']) if block['valid'] else "None"
                self.cache_qtable.setItem(set_index, (way if hit else (empty_block if empty_block is not None else mru_index)) + 1, QTableWidgetItem(block_value))

                time.sleep(0.5)  
                QApplication.processEvents()  

        if not step_by_step:
            # Print final cache state
            for set_index in range(sets):
                for way in range(ways):
                    block = cache[set_index][way]
                    block_value = str(block['block']) if block['valid'] else "None"
                    self.cache_qtable.setItem(set_index, way + 1, QTableWidgetItem(block_value))

        # Compute performance metrics
        hit_rate = (cache_hit / total_access) * 100 if total_access > 0 else 0
        miss_rate = (cache_miss / total_access) * 100 if total_access > 0 else 0
        avg_mem_access_time = total_mem_access_time / total_access if total_access > 0 else 0

        # Update GUI stats
        self.memory_access_qstat.setText(f"{total_access}")
        self.cache_hit_qstat.setText(str(cache_hit))
        self.cache_miss_qstat.setText(str(cache_miss))
        self.cache_hit_rate_qstat.setText(f"{hit_rate:.2f}%")
        self.cache_miss_rate_qstat.setText(f"{miss_rate:.2f}%")
        self.avg_memory_time_qstat.setText(f"{avg_mem_access_time:.2f}ns")
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
        initialize_cache_table(self)

def initialize_cache_table(self):
    self.cache_qtable.clear()
    self.cache_qtable.setHorizontalHeaderLabels(["Set", "Block 0","Block 1","Block 2","Block 3","Block 4","Block 5","Block 6","Block 7"])
    for i in range(sets):
            item = QTableWidgetItem(str(i))
            self.cache_qtable.setItem(i, 0, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CacheSimulator()
    window.show()
    sys.exit(app.exec_())
