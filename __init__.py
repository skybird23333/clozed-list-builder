# import the main window object (mw) from aqt
from typing import List

import aqt.editor
from aqt import mw, gui_hooks
# import the "show info" tool from utils.py
from aqt.utils import showInfo, qconnect
# import all of the Qt GUI library
from aqt.qt import *
from anki.notes import Note


# {{c1::Alphabet}} {{c2::A}} {{c3::B}} {{c4::C}} {{c5::D}} {{c6::E}}
# {{c1::水果}} {{c2::苹果}} {{c3::香蕉}} {{c4::橙子}} {{c5::梨子}}

def addNotes(editor: aqt.editor.Editor, linked=False):
    numbers = list(editor.note.cloze_numbers_in_fields())
    numbers.sort()
    clozes: list[str] = []
    for i in numbers:
        clozes.append(mw.col.extract_cloze_for_typing(editor.note.fields[0], i))

    notes = []
    title = clozes.pop(0)
    for i, val in enumerate(clozes):
        if linked:
            notes.append(f"<b>{title}</b><br>" +
                         (clozes[i - 1] if i > 0 else '') +  # Only if there is a previous item
                         " -> {{c1::" + val + "}}"
                         )
        else:
            notes.append(
                f"<b>{title}</b><br>" +
                (f'{i}. {clozes[i - 1]}<br>' if i > 0 else '') +
                str(i + 1) + ". {{c1::" + val + "}}" +
                (f'<br>{i + 2}. {clozes[i + 1]}' if i < len(clozes) - 1 else '')   # Only if there is a next item
            )

    list_id = 'list_' + title + ('(linked)' if linked else '')

    print(notes)

    editor.note.fields[1] +=\
        f'<code style="display:none">ID:{list_id}\nORIGINAL:' + editor.note.fields[0].replace("{", "\\{") + '</code>'
    for note_text in notes:
        note: Note = editor.note
        note.fields[0] = note_text
        note.id = 0
        mw.col.add_note(note, deck_id=mw.col.decks.get_current_id())

    browser = aqt.dialogs.open("Browser", mw)
    browser.form.searchEdit.lineEdit().setText(list_id)
    browser.onSearchActivated()
    pass


def addMyButton(buttons, editor: aqt.editor.Editor):
    b = editor.addButton(
        icon="",
        cmd="addLinkedList",
        func=lambda editor: addNotes(editor, linked=True),
        tip="Add linked cloze list",
        label="A->B"
    )

    b2 = editor.addButton(
        icon="",
        cmd="addList",
        func=lambda editor: addNotes(editor),
        tip="Add cloze list",
        label="A,B"
    )

    buttons.append(b)
    buttons.append(b2)
    return buttons


gui_hooks.editor_did_init_buttons.append(addMyButton)