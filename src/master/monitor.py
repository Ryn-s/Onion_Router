import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, QLabel, QHeaderView
from PyQt5.QtCore import QTimer
from db_manager import DBManager

class MasterMonitor(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("OnionRouter - Interface Admin Master")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        layout.addWidget(QLabel("Routeurs connectés (Topologie)"))
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["IP", "Port", "Status", "Clé Publique (extrait)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.db = DBManager()

        self.timer = QTimer()
        self.timer.timeout.connect(self.refresh)
        self.timer.start(2000) # Actualise toutes les 2 sec
        self.refresh()

    def refresh(self):
        routers = self.db.get_all_active_routers()
        self.table.setRowCount(0)
        for r in routers:
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(r['ip_address']))
            self.table.setItem(row, 1, QTableWidgetItem(str(r['port'])))
            self.table.setItem(row, 2, QTableWidgetItem("En ligne"))
            self.table.setItem(row, 3, QTableWidgetItem(r['pub_key_e'][:10] + "..."))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MasterMonitor()
    window.show()
    sys.exit(app.exec_())