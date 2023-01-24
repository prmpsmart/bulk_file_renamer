QSS = """
Home {
    background: #dfe6f6;
}

Scrollable, Scrollable VFrame {
    background: #edf1fa;
    background: #dfe6f6;
    border: none;
    border-radius: 10px;
}

QScrollBar:vertical {
    width: 3px;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical, QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {
    height: 0px;
    width: 0px;
}

Options Label#title, Option VFrame {
    border-radius: 10px;
    color: white;
}

Options Label#title {
    font-size: 13px;
    font-weight: bold;
    padding: 5px;
}

Option VFrame {
    background: white;
}

Option LineEdit, Option QComboBox {
    border-radius: 10px;
    background: #d9e0ef;
    color: black;
    padding: 5px;
    font-size: 13px;
}

Option LineEdit:disabled {
    color: grey;
}

Button, IntBox {
    border: 1px solid #a0a0a0;
    border-radius: 10px;
    min-height: 25px;
    max-width: 90px;
    background: #89c7ed;
}

Button:hover {
    background: #75abcb;
}

Button:pressed {
    background: #4e7287;
}

IntBox {
    min-height: 25px;
    min-width: 100px;
    border-radius: 10px;
}

IntBox ILabel {
    min-width: 30px;
    max-width: 30px;
    font-size: 25px;
    font-weight: bold;
    color: white;
    padding-bottom: 3px;
}

IntBox ILabel:hover {
    background: #70a5c3;
}

IntBox ILabel:pressed {
    background: #47697c;
}

IntBox ILabel#plus {
    border-top-right-radius: 10px;
    border-bottom-right-radius: 10px;
}

IntBox ILabel#minus {
    border-top-left-radius: 10px;
    border-bottom-left-radius: 10px;
}

IntBox LineEdit {
    border-radius: 0px;
}

HLine {
    background: #d9d9da;
}

Home QPushButton {
    padding: 5px;
    border-radius: 10px;
    border: 2px solid #9e9e9e;
    font-weight: bold;
    font-size: 15px;
}

Home QPushButton#change {
    color: #64a5de;
}

Home QPushButton#change:checked {
    color: #148cdc;
}

Home QPushButton#add {
    color: #91ce91;
}

Home QPushButton#add:checked {
    color: #3e9d3c;
}

Home QPushButton#remove {
    color: #ff5f50;
}

Home QPushButton#remove:checked {
    color: red;
}

Home QPushButton#change:!checked, Home QPushButton#add:!checked, Home QPushButton#remove:!checked {
    background: grey;
}

Options#change Label#title {
    background: #148cdc;
}

Options#add Label#title {
    background: #3e9d3c;
}

Options#remove Label#title {
    background: red;
}

Preview {
    border: 1px solid grey;
}

Item {
    min-height: 40px;
    background: white;
    max-width: 1000px;
}

Item:hover {
    background: #bde3f4;
}

Item:checked {
    background: #e8a2ac;
}

Output {
    min-width: 650px;
}

Output Button#red {
    background:  #d0263f;
}

Output Button#red:hover {
    background:  #8f0000;
}

Output Button#red:pressed {
    background:  #b00000;
}

Item Label#preview {
    color: green;
}


"""
