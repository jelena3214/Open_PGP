from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QTableWidgetItem, QHeaderView

import context


def initTable(table, column_count, row_count, headers):
    table.setColumnCount(column_count)
    table.setRowCount(row_count)
    table.setHorizontalHeaderLabels(headers)

    header = table.horizontalHeader()
    for i in range(len(headers)):
        header.setSectionResizeMode(i, QHeaderView.ResizeMode.Stretch)
        item = table.horizontalHeaderItem(i)
        item.setTextAlignment(Qt.AlignmentFlag.AlignCenter)

    header.setDefaultAlignment(Qt.AlignmentFlag.AlignCenter)


def updateRingTable(table, data, columns):
    table.clearContents()
    table.setRowCount(len(data))

    for row_idx, key in enumerate(data):
        for col_idx, col_name in enumerate(columns):
            if callable(getattr(key, col_name)):
                value = getattr(key, col_name)()
            else:
                value = getattr(key, col_name)
            table.setItem(row_idx, col_idx, QTableWidgetItem(str(value)))


def updatePrivateRingTable(table):
    all_data = context.private_key_ring.get_all_data()
    columns = ['timestamp', 'key_id', 'public_key_as_string', 'private_key_as_string', 'name', 'email']
    updateRingTable(table, all_data, columns)


def updatePublicRingTable(table):
    all_data = context.public_key_ring.get_all_data()
    columns = ['timestamp', 'key_id', 'public_key_as_string', 'name', 'email']
    updateRingTable(table, all_data, columns)

