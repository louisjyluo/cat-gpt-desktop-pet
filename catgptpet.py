import tkinter as tk
from PIL import Image
from PIL import ImageTk
import time
import random
import catgptAI

class pet():
    def __init__(self):
        # create a window
        self.window = tk.Tk()

        # placeholder image
        
        self.walking_right = [tk.PhotoImage(file='chonk.png').subsample(20)]
        self.frame_index = 0
        self.img = self.walking_right[self.frame_index]
        self.timer = 0
        self.action_time = 730
        
        self.inputtxt = tk.Text(self.window, 
                   height = 1, 
                   width = 20) 
  
        self.inputtxt.pack() 

        # timestamp to check whether to advance frame
        self.timestamp = time.time()

        # set focushighlight to black when the window does not have focus
        self.window.config(highlightbackground='black')

        # make window frameless
        self.window.overrideredirect(True)

        # make window draw over all others
        self.window.attributes('-topmost', True)

        # turn black into transparency
        self.window.wm_attributes('-transparentcolor', 'black')

        # create a label as a container for our image
        self.label = tk.Label(self.window, bd=0, bg='black')

        # create a window of size 128x128 pixels, at coordinates 0,0
        self.x = self.window.winfo_screenwidth() - 800
        self.y = self.window.winfo_screenheight() - 200
        self.window.geometry('128x90+{x}+{y}'.format(x=str(self.x), y = str(self.y)))

        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.jump_left)
        self.window.mainloop()

    def walk_right(self):
        self.x += 1
        if self.is_at_edge_of_screen():
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_left)
            return 
        # move right by one pixel
        # advance frame if 50ms have passed
        # if time.time() > self.timestamp + 0.05:
        #     self.timestamp = time.time()
        #     # advance the frame by one, wrap back to 0 at the end
        #     self.frame_index = (self.frame_index + 1) % 4
        #     self.img = self.walking_right[self.frame_index]

        # create the window
        self.window.geometry('128x90+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()
        
        if self.timer == self.action_time:
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_left)
        else:
            # call update after 10ms
            self.timer += 1
            self.window.after(10, self.walk_right)
        
    def walk_left(self):
        self.x -= 1
        if self.is_at_edge_of_screen():
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_right)
            return 
        # move right by one pixel
      
        # advance frame if 50ms have passed
        # if time.time() > self.timestamp + 0.05:
        #     self.timestamp = time.time()
        #     # advance the frame by one, wrap back to 0 at the end
        #     self.frame_index = (self.frame_index + 1) % 4
        #     self.img = self.walking_right[self.frame_index]

        # create the window
        self.window.geometry('128x90+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()
        
        if self.timer == self.action_time:
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_right)
        else:     
            self.timer += 1
            # call update after 10ms
            self.window.after(10, self.walk_left)
            
    def walk_up(self):
        self.y -= 1
        
        if self.is_at_edge_of_screen():
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_down)
            return 
        # move right by one pixel
       
        # advance frame if 50ms have passed
        # if time.time() > self.timestamp + 0.05:
        #     self.timestamp = time.time()
        #     # advance the frame by one, wrap back to 0 at the end
        #     self.frame_index = (self.frame_index + 1) % 4
        #     self.img = self.walking_right[self.frame_index]

        # create the window
        self.window.geometry('128x90+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()
        
        if self.timer == self.action_time:
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_down)
        else:     
            self.timer += 1
            # call update after 10ms
            self.window.after(10, self.walk_up)
    
    def walk_down(self):
        self.x += 1
        # move right by one pixel
        if self.is_at_edge_of_screen():
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_up)
            return 
    
        # advance frame if 50ms have passed
        # if time.time() > self.timestamp + 0.05:
        #     self.timestamp = time.time()
        #     # advance the frame by one, wrap back to 0 at the end
        #     self.frame_index = (self.frame_index + 1) % 4
        #     self.img = self.walking_right[self.frame_index]

        # create the window
        self.window.geometry('128x90+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()
        
        if self.timer == self.action_time:
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_up)
        else:
            self.timer += 1
            # call update after 10ms
            self.window.after(10, self.walk_down)
            
    #calling jump_right:
    # self.timer = 0
    # self.action_time = 730
    # self.window.after(10, self.jump_right)
            
    def jump_right(self):
        # move right by one pixel
        self.x += 1
        x_range = [*range(-1 * self.action_time / 2, self.action_time / 2)]
        self.y = self.jump_parabola(x_range[self.timer])
        
        if self.is_at_edge_of_screen():
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_left)
            return 
            
        # advance frame if 50ms have passed
        # if time.time() > self.timestamp + 0.05:
        #     self.timestamp = time.time()
        #     # advance the frame by one, wrap back to 0 at the end
        #     self.frame_index = (self.frame_index + 1) % 4
        #     self.img = self.walking_right[self.frame_index]

        # create the window
        self.window.geometry('128x90+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()
        
        if self.timer == self.action_time:
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_left)
        else:     
            self.timer += 1
            # call update after 10ms
            self.window.after(10, self.jump_right)
            
    def jump_left(self):
        # move right by one pixel
        self.x -= 1
        x_range = [*range(-1 * self.action_time / 2, self.action_time / 2)]
        x_range.reverse()
        self.y = self.jump_parabola(x_range[self.timer])
        
        if self.is_at_edge_of_screen():
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_right)
            return 
            
        # advance frame if 50ms have passed
        # if time.time() > self.timestamp + 0.05:
        #     self.timestamp = time.time()
        #     # advance the frame by one, wrap back to 0 at the end
        #     self.frame_index = (self.frame_index + 1) % 4
        #     self.img = self.walking_right[self.frame_index]

        # create the window
        self.window.geometry('128x90+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()
        
        if self.timer == self.action_time:
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_right)
        else:     
            self.timer += 1
            # call update after 10ms
            self.window.after(10, self.jump_left)
    
    def idle(self):
        # create the window
        self.window.geometry('128x90+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()
        
        #idle 
        if self.timer == self.action_time:
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_right)
        else:
            self.window.after(10, self.idle)
    
    def is_at_edge_of_screen(self):
        if(self.x <= 0 or self.x + 120 >= self.window.winfo_screenwidth()):
            return True
        if(self.y <= 0 or self.y + 40 >= self.window.winfo_screenheight()):
            return True
        return False
    
    def jump_parabola(self, x):
        y = -0.003 * (x - self.x)**2 + 400 + self.y
        return int(y)
    
    def on_click(self):
        x = self.window.winfo_pointerx() - self.window.winfo_rootx()
        y = self.window.winfo_pointery() - self.window.winfo_rooty()
        if self.x == x and self.y == y:
            #response = catgptAI.chat("say something cool")
            print("hi")
    
pet()