#!/usr/bin/env python3

from tkinter import Tk
from tkinter.ttk import Frame, Label
from tkinter.ttk import Notebook
from os import walk, path
from re import search

# Button(frame, text='Quit!', command=root.destroy).grid(column=0, row=1)
FONT = ('monospace', 12)
FONT_SUBJECT = ('monospace', 14)


class CustomNotebook:
    def __init__(self, master) -> None:
        self.master = master
        self.notebook = Notebook(self.master)
        self.notebook.grid()
        self.notebook.grid_rowconfigure(0, weight=1)
        self.notebook.grid_columnconfigure(0, weight=1)
        self.__pages()

    def __pages(self) -> None:
        files = self.__get_config_files()
        for file in files:
            self.__add_pages_from_file(file)

    def __get_config_files(self) -> list:
        files_to_return = []
        for root, _, files in walk(path.expanduser('~/.config/i3/config.d')):
            for file in files:
                with open(path.join(root, file), 'r') as fp:
                    data = fp.read()
                    if search(r'# i3menu - create', data):
                        files_to_return.append(path.join(root, file))
        return files_to_return

    def __add_pages_from_file(self, file) -> None:
        # Collect Data from Config file
        with open(file, 'r') as fp:
            data = fp.readlines()

        # Get Section Name
        section_name = None
        found_section = False
        for line in data:
            if search(r'# i3menu - create.*?', line):
                found_section = True
                continue
            if found_section:
                section_name = search(r'#.*? - (.*?)\n', line).group(1)
                found_section = False
                break
        print(section_name)

        if 'Mode' in section_name:
            # Configure Mode Notebook as Sub-Notebook
            mode_notebook = Notebook(self.notebook)
            mode_notebook.grid()
            mode_notebook.grid_rowconfigure(0, weight=1)
            mode_notebook.grid_columnconfigure(0, weight=1)
            frame = None
            tab_title = None
            frame_text = ''
            for line in data:
                if search(r'# i3menu - usage.*?', line):
                    # Set the title for later use
                    tab_title = search(r'# i3menu - usage - (.*?\n)', line).group(1)
                    # Create a Frame to add stuff to
                    frame = Frame(mode_notebook)
                    frame.grid()
                    frame.grid_rowconfigure(0, weight=1)
                    frame.grid_columnconfigure(0, weight=1)
                    # Add Label to the Frame with the Section Name
                    label = Label(
                        frame,
                        text=search(r'# i3menu - usage - (.*?\n)', line).group(1),
                        font=FONT_SUBJECT
                    )
                    # Configure Label
                    label.grid(
                        column=0,
                        row=len(frame.grid_slaves()),
                        sticky='w',
                        padx=10
                    )
                    continue
                elif not search(r'#.*?', line) and frame:
                    # Create Label with text collected and attach it to the frame
                    label = Label(
                        frame,
                        text=frame_text,
                        font=FONT
                    )
                    label.grid(
                        column=0,
                        row=len(frame.grid_slaves()),
                        sticky='w',
                        padx=10
                    )
                    # Add Frame as Page to the Notebook
                    mode_notebook.add(frame, text=tab_title)
                    # Clear vars
                    frame_text = ''
                    frame = None
                    tab_title = None
                    continue
                if frame:
                    # If Frame is set add all the stuff to the text
                    frame_text += search(r'#(.*?\n)', line).group(1)
            self.notebook.add(mode_notebook, text=section_name)
        else:
            # Selfbuild Sections are here
            selfbuild_notebook = Notebook(self.notebook)
            selfbuild_notebook.grid()
            selfbuild_notebook.grid_rowconfigure(0, weight=1)
            selfbuild_notebook.grid_columnconfigure(0, weight=1)
            frame = None
            tab_title = None
            frame_text = ''
            for line in data:
                if search(r'# i3menu - selfbuild - Start', line):
                    # Create Frame if section is found
                    frame = Frame(selfbuild_notebook)
                    frame.grid()
                    frame.grid_rowconfigure(0, weight=1)
                    frame.grid_columnconfigure(0, weight=1)
                    continue
                elif search(r'# i3menu - selfbuild - End', line):
                    label = Label(
                        frame,
                        text=frame_text,
                        font=FONT
                    )
                    label.grid(
                        column=0,
                        row=len(frame.grid_slaves()),
                        sticky='w',
                        padx=10
                    )
                    selfbuild_notebook.add(frame, text=tab_title)
                    # Clear
                    frame_text = ''
                    frame = None
                    tab_title = None
                    continue
                if frame and not tab_title:
                    # Add Label to the Frame with the Section Name
                    tab_title = search(r'# (.*?\n)', line).group(1)
                    label = Label(
                        frame,
                        text=search(r'# (.*?\n)', line).group(1),
                        font=FONT_SUBJECT
                    )
                    # Configure Label
                    label.grid(
                        column=0,
                        row=len(frame.grid_slaves()),
                        sticky='w',
                        padx=10
                    )
                elif frame:
                    if search(r'#.*?disabled.*?', line):
                        frame_text += 'Disabled\n'
                    elif search(r'set $.*?', line):
                        match_set = search(r'set ($.*?) (.*?\n)', line)
                        frame_text += 'Var ' + match_set.group(1) + ': ' + match_set.group(2)
                    elif search(r'bindsym.*?', line):
                        frame_text += search(r'bindsym (.*?\n)', line).group(1)
                    elif search(r'# .*?', line):
                        frame_text += search(r'# (.*?\n)', line).group(1)
                    else:
                        frame_text += '\n'
            self.notebook.add(selfbuild_notebook, text=section_name)


if __name__ == '__main__':
    root = Tk(className='i3menu')
    root.title('I3 Keybindings')
    CustomNotebook(root)
    root.mainloop()
