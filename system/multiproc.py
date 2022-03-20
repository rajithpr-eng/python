#Proprietary content. ©Great Learning. All Rights Reserved. Unauthorized use or distribution prohibited

# Python program to  create a simple GUI
# calculator using Tkinter

# import everything from tkinter module
from tkinter import *
from ast import literal_eval
import multiprocessing
import time
from tkinter import messagebox


# globally declare the array expression variable
array_expression = ""
totals = []

# Process that generates a window and displays the array of squares
# of individual elements in the array and their sum
def startProcess1(my_list, result, square_sum):
    clientsWin1 = Tk()
    local_list=[]
    clientsWin1.geometry("500x100+250+100")
    clientsWin1.title('client 1')

    for idx, num in enumerate(my_list):
        result[idx] = num * num
        local_list.append(result[idx])
    square_sum.value = sum(result)

    label = Label(clientsWin1, text=str(local_list))
    label.pack()

    square_sum.value = sum(result)
    clientsWin1.mainloop()

# Process that generates a window and displays the array of cube
# of individual elements in the array and their sum
def startProcess2(my_list, result, cube_sum):
    clientsWin2 = Tk()
    local_list = []
    clientsWin2.geometry("500x100+850+100")
    clientsWin2.title('client 2')

    for idx, num in enumerate(my_list):
        result[idx] = num * num * num
        local_list.append(result[idx])
    cube_sum.value = sum(result)

    label = Label(clientsWin2, text=str(local_list))
    label.pack()
    clientsWin2.mainloop()

# Function to update array_expression
# in the text entry box
def press(num):
    # point out the global array_expression variable
    global array_expression

    # concatenation of string
    array_expression = array_expression + str(num)
    # update the array_expression by using set method
    equation.set(array_expression)


# Function to evaluate the square in the array and their sum
def calculate_square_cube():

    global array_expression

    # create the array
    # if array_expression.isspace():
    #     array_expression = equation.get()
    try:
        if array_expression[0] != '[':
            array_expression = ("[" + array_expression + "]")
    except:
        messagebox.showinfo("showinfo", "Input not proper")
        array_expression = ""
        equation.set("")
        return

    try:
        # coverts array string into an actual array
        input_array = literal_eval(array_expression)
    except:
        messagebox.showinfo("showinfo", "Input not proper")
        array_expression = ""
        equation.set("")
        return

    # code to check if all items are integers in the array
    if(all(isinstance(item, int) for item in input_array) == False):
        messagebox.showinfo("showinfo", "Input not proper")
        array_expression = ""
        equation.set("")
        return

    # Let's restrict the nos. to 99 max
    for x in input_array:
        if x > 99:
            messagebox.showinfo("showinfo", "Please enter a no. less than 100")
            array_expression = ""
            equation.set("")
            return

    # initialze the array_expression variable
    # by empty string
    square_array = multiprocessing.Array('i', len(input_array))
    square_sum = multiprocessing.Value('i')

    # Spawning a process to calculate the square of each. no in the array
    p1 = multiprocessing.Process(target=startProcess1, args=(input_array, square_array, square_sum))
    p1.start()

    cube_array = multiprocessing.Array('i', len(input_array))
    cube_sum = multiprocessing.Value('i')

    # Spawning a process to calculate the cube of each. no in the array
    p2 = multiprocessing.Process(target=startProcess2, args=(input_array, cube_array, cube_sum))
    p2.start()
    time.sleep(2)

    s1 = ("{}".format(square_array[:]))
    c1 = ("{}".format(cube_array[:]))

    # display the resultant array in the text
    display_square.set("")
    display_square.set("Square sum: " + str(square_sum.value))

    display_cube.set("")
    display_cube.set("Cube sum: " + str(cube_sum.value))


# Function to clear text box
def clearText():
    global array_expression
    array_expression = ""
    equation.set("")


# Client code
if __name__ == "__main__":
    # create a main GUI window
    main_ui = Tk()

    # set the background colour of main GUI window
    main_ui.configure(background="light blue")

    # set the title of main GUI window
    main_ui.title("Server")

    # set the configuration of main GUI window
    main_ui.geometry("270x180+600+450")

    # StringVar() is the variable class
    # we create an instance of this class
    equation = StringVar()

    # create the text entry box for
    # showing the array_expression .
    expression_field = Entry(main_ui, textvariable=equation, state=DISABLED)
    # grid method is used for placing
    # the widgets at respective positions
    # in table like structure .
    expression_field.grid(columnspan=4, ipadx=70)

    equation.set('Create your array with "," in between the nos')

    # create a Buttons and place at a particular
    # location inside the root window .
    # when user press the button, the command or
    # function affiliated to that button is executed .
    button1 = Button(main_ui, text=' 1 ', fg='black', bg='light gray',
                     command=lambda: press(1), height=1, width=7)
    button1.grid(row=2, column=0)

    button2 = Button(main_ui, text=' 2 ', fg='black', bg='light gray',
                     command=lambda: press(2), height=1, width=7)
    button2.grid(row=2, column=1)

    button3 = Button(main_ui, text=' 3 ', fg='black', bg='light gray',
                     command=lambda: press(3), height=1, width=7)
    button3.grid(row=2, column=2)

    button4 = Button(main_ui, text=' 4 ', fg='black', bg='light gray',
                     command=lambda: press(4), height=1, width=7)
    button4.grid(row=2, column=3)

    button5 = Button(main_ui, text=' 5 ', fg='black', bg='light gray',
                     command=lambda: press(5), height=1, width=7)
    button5.grid(row=3, column=0)

    button6 = Button(main_ui, text=' 6 ', fg='black', bg='light gray',
                     command=lambda: press(6), height=1, width=7)
    button6.grid(row=3, column=1)

    button7 = Button(main_ui, text=' 7 ', fg='black', bg='light gray',
                     command=lambda: press(7), height=1, width=7)
    button7.grid(row=3, column=2)

    button8 = Button(main_ui, text=' 8 ', fg='black', bg='light gray',
                     command=lambda: press(8), height=1, width=7)
    button8.grid(row=3, column=3)

    button9 = Button(main_ui, text=' 9 ', fg='black', bg='light gray',
                     command=lambda: press(9), height=1, width=7)
    button9.grid(row=4, column=0)

    button0 = Button(main_ui, text=' 0 ', fg='black', bg='light gray',
                     command=lambda: press(0), height=1, width=7)
    button0.grid(row=4, column=1)

    Decimal = Button(main_ui, text=',', fg='black', bg='light gray',
                     command=lambda: press(','), height=1, width=7)
    Decimal.grid(row=4, column=2)

    clearButton = Button(main_ui, text='Clear', fg='black', bg='light gray',
                   command=clearText, height=1, width=7)
    clearButton.grid(row=4, column='3')

    display_square = StringVar()
    display_square.set("Square sum: ")
    # this wil create a label widget
    l1 = Label(main_ui, textvariable=display_square, justify=LEFT, anchor="w")
    l1.grid(row=6, column=0, columnspan=5, ipadx=90, pady=2)

    display_cube = StringVar()
    display_cube.set("Cube sum: ")
    # this will create a label widget
    l2 = Label(main_ui, textvariable=display_cube, justify=LEFT, anchor="w")
    l2.grid(row=7, column=0, columnspan=5, ipadx=90, pady=2)

    squareAndCube = Button(main_ui, text='Calculate square & cube', fg='black', bg='light gray',
                   command=calculate_square_cube, height=1, width=7)
    squareAndCube.grid(row=5, column=0, columnspan=4, ipadx=90, pady=2)

    # start the GUI
    main_ui.mainloop()

