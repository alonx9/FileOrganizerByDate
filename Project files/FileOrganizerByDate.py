import os
import shutil
from datetime import datetime
import tkinter as tk
from email.policy import default
from tkinter import filedialog, StringVar, IntVar, PhotoImage, ttk
from tkinter.constants import HORIZONTAL
import PIL
import time
import sys


def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS2
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

files = StringVar
file_date = StringVar
target_folder = StringVar
files_list = []

CopyOrMove = ["copy files", "move files"]
CopyTrueFalse = True



def CopyMove():
    global CopyTrueFalse
    if p.get() == 0:
        CopyTrueFalse = True
    elif p.get() == 1:
        CopyTrueFalse = False


date_format_list = ["dd.mm.yyyy", "dd-mm-yyyy"]
date_format_true_false = True

def date_format_select():
    global date_format_true_false
    if q.get() == 0:
        date_format_true_false = True
    elif q.get() == 1:
        date_format_true_false = False



def select_files():
    global files
    files = filedialog.askopenfilenames(title="Select Files")


def select_folder():
    global target_folder
    target_folder = filedialog.askdirectory(title = "Select target directory")


def organize_files():
    global files
    global files_list
    global target_folder
    global CopyTrueFalse
    global date_format_true_false


    new_window = tk.Toplevel()

    new_window_width = 320
    new_window_height = 130
    new_screen_width = root.winfo_screenwidth()
    new_screen_height = root.winfo_screenheight()
    new_x_position = (screen_width - window_width) // 2
    new_y_position = (screen_height - window_height) // 2
    new_window.geometry(f"{new_window_width}x{new_window_height}+{new_x_position}+{new_y_position}")
    new_window.resizable(width=False, height=False)

    new_window.title("Progress")

    #close_button = tk.Button(new_window, text = "close", command = close_window)
    #close_button.pack(anchor = "w")

    percent = StringVar()
    text = StringVar()

    bar = ttk.Progressbar(new_window, orient=HORIZONTAL, length=300)
    bar.pack(pady=10, padx=10)

    percentLabel = tk.Label(new_window, textvariable=percent)
    percentLabel.pack()

    taskLabel = tk.Label(new_window, textvariable=text)
    taskLabel.pack()


    for i in range(len(files)):
        files_list.append(files[i])



    for g in range(len(files_list)):


        file_path = files_list[g]
        timestamp = os.path.getmtime(file_path)

        if date_format_true_false:
            # Get the file's date
            cFile_date = datetime.fromtimestamp(timestamp).strftime("%d.%m.%Y")
        else:
            cFile_date = datetime.fromtimestamp(timestamp).strftime("%d-%m-%Y")

        # Create a folder in the target directory named after the date
        folder_date = os.path.join(target_folder, cFile_date)
        os.makedirs(folder_date, exist_ok=True)

        # Move or copy the file to the date folder
        if CopyTrueFalse:
            shutil.copy2(files_list[g], os.path.join(folder_date, os.path.basename(files_list[g])))
        else:
            shutil.move(files_list[g], os.path.join(folder_date, os.path.basename(files_list[g])))

        bar["value"] += (1 / len(files_list)) * 100

        percent.set(str(int(((g + 1) / len(files_list)) * 100)) + "%")
        text.set(str(g + 1) + "/" + str(len(files_list)) + " files transferred")

        new_frame = tk.Frame(new_window)
        new_frame.pack(anchor = "e")
        new_close_button = tk.Button(new_frame, text="close", command = new_window.destroy)
        new_close_button.pack(padx = 10, pady = 10)

        new_window.update()

    files_list.clear()





root = tk.Tk()
#root.eval("tk::PlaceWindow . center")
root.title("File Organizer By Date")
root.config(bg = "#d7f7ef")
icon_photo = PhotoImage(file = resource_path("assets\\select files button.png"))
root.iconphoto(True, icon_photo)

window_width = 700
window_height = 450
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x_position = (screen_width - window_width) // 2
y_position = (screen_height - window_height) // 2
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")
root.resizable(width = False, height = False)





titleLabel = tk.Label(root,
                      text = "Organize your files by date:",
                      font = ("David", 25, "bold"),
                      bg = "#d7f7ef",
                      pady = 15)
titleLabel.pack()

select_files_frame = tk.Frame(root,
                              bg = "#d7f7ef",
                              pady = 30,
                              padx = 100
                              )
select_files_frame.pack(anchor = "e")
selectFilesImage = PhotoImage(file = resource_path("assets\\select files button.png"))
select_files_label = tk.Label(select_files_frame,
                              text = "Select Files",
                              font = ("Arial", 14, "bold"),
                              bg = "#d7f7ef"
                              )
select_files_label.pack()
Select_Files_bt = tk.Button(select_files_frame,
          text="Select Files",
          command = select_files,
          image = selectFilesImage,
          bg = "#d7f7ef",
          borderwidth = 0,
          highlightthickness = 0
          )
Select_Files_bt.pack()



select_target_frame = tk.Frame(root,
                               bg = "#d7f7ef",
                               pady = 15,
                               padx = 60
                               )
select_target_frame.pack(anchor = "e")
selectTargetImage = PhotoImage(file = resource_path("assets\\select folder button2.png"))
select_target_label = tk.Label(select_target_frame,
                              text = "Select Target Folder",
                              font = ("Arial", 14, "bold"),
                              bg = "#d7f7ef"
                              )
select_target_label.pack()
Choose_Target_Folder_bt = tk.Button(select_target_frame,
          text = "Choose Target Folder",
          command = select_folder,
          image = selectTargetImage,
          bg = "#d7f7ef",
          borderwidth = 0,
          highlightthickness = 0
          )
Choose_Target_Folder_bt.pack()


Organize = tk.Button(root,
          text = "Organize",
          command = organize_files,
          font = ("David", 20, "bold"),
          bg = "#3f8f91",
          fg = "#0d3da3"
          )
Organize.pack()



radio_bt_frame = tk.Frame(root,
                          bg = "#d7f7ef"
                          )
radio_bt_frame.place(x = 80, y = 110)

p = IntVar()
for j in range(len(CopyOrMove)):
    radiobutton = tk.Radiobutton(radio_bt_frame,
                                 text = CopyOrMove[j],
                                 variable = p,
                                 value = j,
                                 padx = 10,
                                 pady = 5,
                                 font = (20),
                                 indicatoron = 0,
                                 command = CopyMove,
                                 width = 8,
                                 borderwidth = 5
                                 )
    radiobutton.pack()


close_button = tk.Button(root,
                         text = "Quit",
                         command = root.destroy,
                         font = ("Arial", 11, "bold"),
                         bg = "#ed1a1a",
                         width = 5
                         )
close_button.place(x = 635, y = 408)



date_format_frame = tk.Frame(root, bg = "#d7f7ef")
date_format_frame.place(x = 35, y = 250)

date_format_label = tk.Label(date_format_frame,
                             text = "Select Folder Name Format:",
                             font = ("Arial", 11, "bold"),
                              bg = "#d7f7ef"

                             )
date_format_label.pack()

q = IntVar()

for k in range(len(date_format_list)):
    date_format = tk.Radiobutton(date_format_frame,
                                 text = date_format_list[k],
                                 variable = q,
                                 value = k,
                                 padx = 9,
                                 pady = 3,
                                 font = ("Arial", 11),
                                 indicatoron = 0,
                                 command = date_format_select,
                                 width = 7,
                                 borderwidth = 5
                                 )
    date_format.pack()


root.mainloop()