from PyQt5.QtWidgets import (QApplication, QWidget, 
QPushButton, QLabel, QListWidget, QLineEdit, QTextEdit, QHBoxLayout, QVBoxLayout,QInputDialog)


app = QApplication([])

parent_note = list()



notes_win = QWidget()
notes_win.setWindowTitle('Smart Notes')
notes_win.resize(900, 600)



#application window widgets

# list of notes
list_notes = QListWidget()
list_notes_label = QLabel('List of notes')

button_note_create = QPushButton('Create note') 
button_note_save = QPushButton('Save note')
button_note_del = QPushButton('Delete note')


# list of tags
list_tags = QListWidget()
list_tags_label = QLabel('List of tags')

button_add = QPushButton('Add to note')
button_del = QPushButton('Untag from note')
button_search = QPushButton('Search notes by tag')

field_tag = QLineEdit('')
field_tag.setPlaceholderText('Enter tag...')

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
row_1.addWidget(button_note_del)

row_2.addWidget(button_note_save)

col_2.addLayout(row_1)
col_2.addLayout(row_2)

################

col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)

row_3 = QHBoxLayout()
row_3.addWidget(button_add)
row_3.addWidget(button_del)

row_4 = QHBoxLayout()
row_4.addWidget(button_search)

col_2.addLayout(row_3)
col_2.addLayout(row_4)


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
def delete_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        
        for child_note in parent_note:
            if child_note[0] == key:
                index = parent_note.index(child_note)
                parent_note.remove(child_note)
                list_notes.takeItem(list_notes.currentRow())
                filename = str(index) + '.txt'
                with open(filename, 'w') as file:
                    file.write("")  # Clear the contents of the file instead of deleting it
                break
    else:
        print("Note to delete is not selected!")
def add_tag_to_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        
        tag, ok = QInputDialog.getText(notes_win, "Add Tag", "Tag name: ")
        if ok and tag != "":
            for child_note in parent_note:
                if child_note[0] == key:
                    child_note[2].append(tag)
                    filename = str(parent_note.index(child_note)) + '.txt'
                    with open(filename, 'w') as file:
                        file.write(child_note[0] + '\n')
                        file.write(child_note[1] + '\n')
                        for tag in child_note[2]:
                            file.write(tag + ' ')
                        file.write('\n')
                    break
    else:
        print("Note to add tag is not selected!")
        
def show_notee():
    key = list_notes.selectedItems()[0].text()
    
    for child_note in parent_note:
        if child_note[0] == key:
            field_text.setText(child_note[1])
            
            if len(child_note) > 2:
                # Join the tags list into a string separated by spaces
                tags_str = ' '.join(child_note[2])
                print("Tags:", tags_str)
            else:
                print("No tags available for this note.")
            
            break
def remove_tag_from_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        
        tag, ok = QInputDialog.getText(notes_win, "Remove Tag", "Tag name: ")
        if ok and tag != "":
            for child_note in parent_note:
                if child_note[0] == key:
                    if tag in child_note[2]:
                        child_note[2].remove(tag)
                        filename = str(parent_note.index(child_note)) + '.txt'
                        with open(filename, 'w') as file:
                            file.write(child_note[0] + '\n')
                            file.write(child_note[1] + '\n')
                            for tag in child_note[2]:
                                file.write(tag + ' ')
                            file.write('\n')
                    else:
                        print("Tag not found in note.")
                    break
    else:
        print("Note to remove tag is not selected!")
# connecting event handling
list_notes.itemClicked.connect(show_note)
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(delete_note)
list_tags.itemClicked.connect(show_notee)
button_add.clicked.connect(add_tag_to_note)
button_del.clicked.connect(remove_tag_from_note)




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
