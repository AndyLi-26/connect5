from tkinter import Label
import controller, sys
import model   # Pass a reference to this module to each update call in update_all
import Board



board=Board.board('B')
player = True
#add the kind of remembered object to the simulation (or remove all objects that contain the
#  clicked (x,y) coordinate
def mouse_click(x,y):
    global player
    i=round((x-board.zeroPoint)/board.rectSize)
    j=round((y-board.zeroPoint)/board.rectSize)
    if player:
        player = False
        valid=board.playerTurn(i,j,controller.the_canvas)
        if not valid:
            player = True
            return
        board.computercheck(controller.the_canvas)
        if board.steps == 255:
            board.new = messagebox.askquestion('Tie','You tied do you want to start a new game?')
        if board.new=='yes':
            reset()
        else:
            board.computerTurn(controller.the_canvas)
        if board.steps == 255:
            board.new = messagebox.askquestion('Tie','You tied do you want to start a new game?')
        player = True

#reset all module variables to represent an empty/stopped simulation
def reset ():
    global board,player
    board=Board.board('B')
    player = True
    
def reg():
    global board
    board.regreat()
##def progress  (parent,**config):
##    #global the_progress
##    the_progress = Label('',**config)
##    if board.run==False:
##        the_progress = Label(board.message,**config)
##    return the_progress

#delete from the canvas every simulton being simulated; next call display on every
#  simulton being simulated to add it back to the canvas, possibly in a new location, to
#  animate it; also, update the progress label defined in the controller
#this function should loop over one set containing all the simultons
#  and should not call type or isinstance: let each simulton do the
#  right thing for itself, without this function knowing what kinds of
#  simultons are in the simulation
def display_all(root):
    for o in controller.the_canvas.find_all():
        controller.the_canvas.delete(o)
    board.update(root)
    board.display(controller.the_canvas)

    #for b in balls:
    #    b.display(controller.the_canvas)
    
    #controller.the_progress.config(text=str(len(balls))+" balls/"+str(cycle_count)+" cycles")
