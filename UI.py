from tkinter import Tk,Frame,TOP,LEFT,BOTTOM,RAISED,BOTH 
import controller
import model

# Construct a simple root window
root = Tk()
root.title("Simulation")
root.protocol("WM_DELETE_WINDOW",quit)
frame = Frame(root)

# Place buttons simply at the top
frame.pack(side=TOP)
controller.reset_button (frame,text="Reset")     .pack(side=LEFT)
controller.reg_button (frame,text="regret")     .pack(side=LEFT)
#controller.start_button (frame,text="Start")     .pack(side=LEFT)
#model.progress     (frame,text="",width=25,relief=RAISED).pack(side=TOP)
 
    
# Place canvas in the space below
controller.simulation_canvas(root,width=1000,height=1000,bg="#707070").pack(side=BOTTOM,expand=True,fill=BOTH)
