from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter import ttk,Entry,messagebox
import tkinter as tk
from tkinter import filedialog
import os 
import re
GRID_SPACING =20
root = Tk()
root.title("White Board")
root.geometry("1050x570+150+50")
is_pressed = False
is_grid_on = False


# root.geometry("1050x570+150+50") sets the main application window to have a width of 1050 pixels, a height of 570 pixels, and its top-left corner positioned 150 pixels from the left edge of the screen and 50 pixels from the top edge of the screen
root.config(bg="white")
root.resizable(False,False)

color='black'

def locate_xy(event):
    """
	Updates the global variables `current_x` and `current_y` with the coordinates of the given `event`.

	Parameters:
	- event: The event object containing the x and y coordinates.

	Return:
	- None
	"""
    
    global current_x,current_y
    
    current_x = event.x
    current_y = event.y
    
    

def addline(event):
    
    """
    Add a line to the canvas based on the given event.

    Parameters:
    - event: The event object that contains information about the mouse click or movement.

    Returns:
    - None
    """
    global current_x,current_y,item_id
    item_id =canvas.create_line((current_x,current_y,event.x,event.y),
                       width=get_current_value(),
                       fill=color,capstyle=ROUND,
                       smooth=True,
                    #    splinesteps=50,
            
                       )
    current_x,current_y = event.x,event.y
      # Draw the grid lines

    
    
    
def show_color(new_color):
    """
    Set the global variable `color` to the specified `new_color`.

    Parameters:
    - `new_color` (any): The new color to be set.

    Returns:
    - None
    """
    global color 
    color = new_color


def is_valid_hex_code(hex_code):
    # Regular expression pattern for a valid hex color code
    pattern = r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$'
    
    # Check if the input matches the pattern
    return re.match(pattern, hex_code) is not None

cross_icon = PhotoImage(file="data/cross_icon1.png")

def toggle_grid():
    global is_grid_on
    is_grid_on = not is_grid_on
    if is_grid_on:
        grid_button_id.config(image=cross_icon)
        for x in range(0, canvas.winfo_reqwidth(), GRID_SPACING):
                canvas.create_line(x, 0, x, canvas.winfo_reqheight(), fill="lightgray",tags="grid_lines")

        for y in range(0, canvas.winfo_reqheight(), GRID_SPACING):
                canvas.create_line(0, y, canvas.winfo_reqwidth(), y, fill="lightgray",tags="grid_lines")
    else:
        canvas.delete("grid_lines")
        grid_button_id.config(image=grid_icon)









def  new_canvas():
    canvas.delete('all')
    display_pallate()

def insertimage():
    global filename
    global f_img
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),title="Select image file ",filetypes=(("PNG file","*.png"),("All file","text.txt")))
    f_img = tk.PhotoImage(file=filename)
    canvas.create_image(180,50,image=f_img)
    root.bind("<B3-Motion>",my_callback)

def my_callback(event):
    global f_img 
    f_img = tk.PhotoImage(file=filename)
    canvas.create_image(event.x,event.y,image=f_img)



def display_and_select(hex):
    global color
    color = hex
    custom_color = Button(root,width=2,height=1,
                          state=DISABLED,
                          bg=hex)
    custom_color.place(x=200,y=525)
    











def color_input():
    global  color_picked
    color_picked = tk.StringVar()
    global entry,text
    entry=Entry(root,textvariable=tk.StringVar(),
                bg="white",fg="black",font="arial 10 bold",
                width=6)

    entry.place(x=200,y=535)
    text=Label(root,text="Enter hex code:",
               bg="white",fg="black",
               font="arial 10 bold",)
    text.place(x=200,y=513)
    
color_picker_icon = PhotoImage(file="data/color_picker.png")
select_icon = PhotoImage(file="data/selected.png")




def toggle_button_icon():
    global is_pressed
    is_pressed = not is_pressed  # Toggle the state
    
    if is_pressed:
        cl_pic_id.config(image=select_icon)
        color_input()
    else:
        cl_pic_id.config(image=color_picker_icon)
        if  is_valid_hex_code(entry.get()):
            display_and_select(entry.get())
        else:
            messagebox.showwarning("Error","Invalid hex code")
        entry.destroy()
        text.destroy()





#colorpicker 

cl_pic_id = Button(root,image=color_picker_icon,bg="white",width=28,height=28,command=toggle_button_icon)
cl_pic_id.place(x=150,y=525)


grid_icon = PhotoImage(file="data/grid.png")
#grid 
grid_button_id = Button(root,image=grid_icon,bg="white",width=28,height=28,command=toggle_grid)
grid_button_id.place(x=800,y=525)


#icon 
image_icon = PhotoImage(file="data/logo.png")
root.iconphoto(False,image_icon)

#sidebar 
color_box = PhotoImage(file="data/color.png")
Label(root,image=color_box,bg="white").place(x=10,y=20)


eraser = PhotoImage(file = 'data/eraser.png')
Button(root,image=eraser,bg="white",command=new_canvas).place(x=30,y=400)

importimage = PhotoImage(file = 'data/addimage.png')
Button(root,image=importimage,bg="white",command=insertimage).place(x=30,y=450)


############colors ###############

colors = Canvas(root,width=37,height=300,
                bd=0,
                highlightthickness=0)
colors.place(x=30,y=60)

def display_pallate():
    id = colors.create_rectangle((10,10,30,30),fill ="black")
    colors.tag_bind(id,"<Button-1>",lambda x :show_color('black'))
    
    id = colors.create_rectangle((10,40,30,60),
                                 fill ="gray",                activefill="#5A5A5A")
    colors.tag_bind(id,"<Button-1>",lambda x :show_color('gray'))

    id = colors.create_rectangle((10,70,30,90),
                                 fill ="brown",
                                 activefill="#7C4700")
    colors.tag_bind(id,"<Button-1>",lambda x :show_color('brown'))

    id = colors.create_rectangle((10,100,30,120),
                                 fill ="red",
                                 activefill="#dc143c")
    colors.tag_bind(id,"<Button-1>",lambda x :show_color('red'))

    id = colors.create_rectangle((10,130,30,150),
                                 fill ="orange",
                                 activefill="#f28500")
    colors.tag_bind(id,"<Button-1>",lambda x :show_color('orange'))

    id = colors.create_rectangle((10,160,30,180),
                                 fill ="yellow",
                                 activefill="#FFD700")
    colors.tag_bind(id,"<Button-1>",lambda x :show_color('yellow'))

    id = colors.create_rectangle((10,220,30,240),
                                 fill ="blue",
                                 activefill="#005A9C")
    colors.tag_bind(id,"<Button-1>",lambda x :show_color('blue'))

    id = colors.create_rectangle((10,190,30,210),
                                 fill ="green",
                                 activefill="#006400")
    colors.tag_bind(id,"<Button-1>",lambda x :show_color('green'))

    id = colors.create_rectangle((10,250,30,270),
                                 fill ="purple",
                                 activefill="#4b0082"
                                 )
    colors.tag_bind(id,"<Button-1>",lambda x :show_color('purple'))
    
    
    id = colors.create_rectangle((10,275,30,295),
                                 fill ="white",
                                 activefill="#C0C0C0"
                                 )
    colors.tag_bind(id,"<Button-1>",lambda x :show_color('white'))

display_pallate()


#main screen 
canvas = Canvas(root,width=930,height=500,
                background="white",
                cursor="hand2",
                insertborderwidth=1,
                relief="raised",#flat,ridge,groove,,solid
                )
canvas.place(x=100,y=10)


canvas.bind('<B1-Motion>',addline)
canvas.bind('<Button-1>',locate_xy)


####################################slider ######################
current_value = tk.DoubleVar()
def get_current_value():
    return '{: .2f}'.format(current_value.get())

def slider_changed(event):
    value_label.configure(text =get_current_value())




slider =ttk.Scale(root,from_=0,to=100,
                  orient=HORIZONTAL,
                  command=slider_changed,
                  variable=current_value,
                  )
slider.place(x=30,y=530)

value_label=ttk.Label(root,text=get_current_value())
value_label.place(x=27,y=550)




root.mainloop()