from tkinter import *
import random
import keyboard

counter = 0
running = False
keypressed = 0
wpm = 0
accuracy = 0

instruction = (
    "************** WELCOME TO TYPING MASTER **************\n\nKindly go through the instructions below: \n\n"
    "1. This is an app to test your typing speed.\n"
    "2. It is recommended that you should not correct the words after pressing space.\n"
    "3. The timer will start when you enter your first character in the input box.\n"
    "4. To submit press 'Enter'.\n"
    "5. You can see the result on the right side of the window.\n\n"
    "Note : Typing Master will automatically stop after 2 minutes.")

root = Tk()

with open("typing_story.txt", "r") as file:
    allText = file.read()
    para = list(map(str, allText.split('\n')))


def key(event):
    global keypressed
    global running
    keypressed += 1
    if keypressed == 1:
        running = True
        counter_label(lbl)
    if keyboard.is_pressed("enter"):
        running = False
        check_input(input_text, words_text)


def restarting(events):
    """function to restart the typing master"""

    print("Restarting...")
    input_text.delete("1.0", "end")

    global counter
    counter = 0
    if running == False:
        lbl['text'] = '00'
    else:
        lbl['text'] = ''

    # restart time
    global keypressed
    keypressed = 0
    input_text.bind('<Key>', key)

    check_input(input_text, words_text)

    global wpm, accuracy
    wpm = 0
    accuracy = 0



def exiting(events):
    """function to exit the typing master"""
    print("Exiting...")
    quit()



def custom_dialog_box():
    """function to print time"""

    base = Toplevel(root)
    base.geometry("600x400+400+200")
    base.title("Instruction")
    base.focus()

    def exit_instr(event):
        base.destroy()

    dialog_f = Frame(base)
    dialog_m = Message(dialog_f, text=instruction, bg="#9575CD", fg="floralwhite", font="calibri 15 bold", width='580')
    dialog_f.pack()
    dialog_m.pack(side=LEFT)
    btn = Button(base, text="PRESS SPACE TO PROCEED", width=50, font="calibri 15 bold", command=base.destroy)
    btn.pack(side=BOTTOM, padx=20, pady=20)
    base.bind('<space>', exit_instr)

def counter_label(lbl):
    def count():
        global counter
        global running
        if running:
            global counter
            if counter == 0:
                display = "0"
            else:
                display = str(counter)
            if counter < 10:
                lbl['text'] = '0' + display
            else:
                lbl['text'] = display

            lbl.after(1000, count)
            counter += 1

            if counter == 120:
                running = False

    count()


# function to calculate the accuracy
def check(written, words_text):
    count = 0
    for i in range(len(written)):
        if written[i] == words_text[i]:
            count += 1
    acc = (count * 100) // len(written)
    return acc


# function to calculate wpm and print it
def check_input(write, words_text):
    global wpm, accuracy

    written = write.get("1.0", "end-1c")
    written = written.split()
    if counter != 0:
        wpm = len(written) / (counter / 60)
        accuracy = check(written, words_text)
        accuracy = str(accuracy) + "%"
        lbl_wpm = Label(can_widget, text=round(wpm), font="comicsans 15 bold")
        lbl_acc = Label(can_widget, text=accuracy, font="comicsans 15 bold")

    else:
        lbl_wpm = Label(can_widget, text="00", font="comicsans 15 bold")
        lbl_acc = Label(can_widget, text="00 %", font="comicsans 15 bold")

    if wpm != 0:
        lbl_wpm.place(x=100, y=150)
        lbl_acc.place(x=50, y=250)


# setting the tkinter window
root.geometry("1000x600+300+100")
root.title("Typing Speed Test")
root.resizable(0, 0)

# the heading or name of the the application
l1 = Label(root, text="Typing Master", font="comicsans 15 bold")
l1.pack()

# message or paragraph
f1 = Frame(root, bg="red", borderwidth=3)
story = random.choice(para)
m1 = Message(f1, text=story, fg="black", font="calibri 15 bold", width='540')
words_text = story.split()
f1.place(x=50, y=45)
m1.pack()

# text area to type
f2 = Frame(root, bg="red", borderwidth=4, relief=SUNKEN)
f2.place(x=50, y=330)
input_text = Text(f2, width=54, height=10, font="calibri 15 bold", wrap="word")
input_text.pack()

# initializing canvas
can_widget = Canvas(root, width=300, height=500, bg="white")
can_widget.place(x=650, y=55)

# rectangle for words per min
can_widget.create_rectangle(95, 150, 155, 180, outline="black", width=2)
can_widget.create_text(175, 165, text="wpm", font="calibri 12 bold")

# rectangle for accuracy
can_widget.create_rectangle(40, 250, 100, 280, outline="black", width=2)
can_widget.create_text(70, 293, text="Accuracy", font="calibri 12 bold")

# rectangle for time
can_widget.create_rectangle(170, 250, 230, 283, outline="black", width=2)
can_widget.create_text(193, 293, text="Time", font="calibri 12 bold")

# restart icon
restart_img = PhotoImage(file="images/restart-icon.png")
restart = Label(can_widget, image=restart_img)
restart.place(x=30, y=370)
restart.bind('<Button-1>', restarting)
can_widget.create_text(50, 430, text="Restart", font="calibri 12 bold")

# delete icon
delete_img = PhotoImage(file="images/delete-icon.png")
delete = Label(can_widget, image=delete_img)
delete.place(x=170, y=370)
delete.bind('<Button-1>', exiting)
can_widget.create_text(200, 430, text="Exit", font="calibri 12 bold")

lbl = Label(
    can_widget,
    text="00",
    fg="black",
    font="Verdana 15 bold"
)
input_text.bind('<Key>', key)

lbl.place(x=175, y=251)
words_text = story.split()

root.after(10, custom_dialog_box)
root.mainloop()
