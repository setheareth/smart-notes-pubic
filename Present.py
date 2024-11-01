from PyQt5.QtWidgets import (QApplication, QWidget, 
QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout,QInputDialog)


app = QApplication([])

parent_note = list()



notes_win = QWidget()
notes_win.setWindowTitle('Eco_Notes')
notes_win.resize(900, 600)



#application window widgets

# list of notes
list_notes = QListWidget()
list_notes_label = QLabel('List of notes')

button_note_create = QPushButton('Create note') 
button_note_save = QPushButton('Save note')




######################

field_text = QTextEdit()
col_1 = QVBoxLayout()
col_1.addWidget(field_text)

######################

col_2 = QVBoxLayout()
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)

row_1 = QHBoxLayout()
row_2 = QHBoxLayout()

row_1.addWidget(button_note_create)

row_1.addWidget(button_note_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)

################





layout_notes = QHBoxLayout()
layout_notes.addLayout(col_1, stretch = 2)
layout_notes.addLayout(col_2, stretch = 1)
notes_win.setLayout(layout_notes)


def add_note():
    note_name, ok = QInputDialog.getText(notes_win, "Add note", "Note name: ")
    if ok and note_name != "":
        child_note = list()
        child_note = [note_name, '', []]
        parent_note.append(child_note)
        list_notes.addItem(child_note[0])
        filename = str(len(parent_note)-1) + '.txt'
        with open(filename, 'w') as file:
            file.write(child_note[0] + '\n')


def save_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()

        index = 0

        for child_note in parent_note:
            if child_note[0] == key:
                child_note[1] = field_text.toPlainText()

                with open(str(index)+'.txt', 'w') as file:
                    file.write(child_note[0]+'\n')
                    file.write(child_note[1]+'\n')
                    
                    for tag in child_note[2]:
                        file.write(tag+' ')

                    file.write('\n')

            index += 1
        print(parent_note)
    else:
        print("Note to save is not selected!")


def show_note():
    key = list_notes.selectedItems()[0].text()
    
    for child_note in parent_note:
        if child_note[0] == key:
            field_text.setText(child_note[1])

# connecting event handling
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)





notes_win.show()

number_name = 0
child_note = list()

while True:
    ''' '''
    filename = str(number_name)+'.txt'

    try:
        with open(filename, 'r', encoding='utf-8') as file:
            ''' reading and adding '''
            for line in file:
                line = line.replace('\n', '')
                child_note.append(line)
        
        ''' note inside note '''
        if len(child_note) > 2:
            tags = child_note[2].split(' ')
            child_note[2] = tags
        else:
            # Handle the case where child_note does not have enough elements
            print("child_note does not have enough elements")
        parent_note.append(child_note)
        child_note = list()
        number_name += 1

    except IOError:
        break
    
print(parent_note)
for child_note in parent_note:
    list_notes.addItem(child_note[0])

app.exec_()
