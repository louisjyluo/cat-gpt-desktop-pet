import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import time
import random
import CatgptAI
import pyautogui
from tkinter import ttk

class Pet():
    def __init__(self):
        # create a window
        self.window = tk.Tk()
        self.dialog = tk.Toplevel()

        #Reading the gifs for the animation
        idle = Image.open('latte_idle.gif')
        right = Image.open('latte_run_right.gif')     
        left = Image.open('latte_run_left.gif')
        yap_bubble = Image.open('speech_bubble.png')
        #Creating the list of frames
        idle_frames = []
        right_frames = []
        left_frames = []
        
        yap_bubble = yap_bubble.copy().resize((200,200))
        
        #For loops used to make the list of frames per animation
        ind = 0
        for frame in ImageSequence.Iterator(idle):
            idle.seek(ind)
            idle_frames.append(frame.copy())
            ind += 1
        
        ind = 0
        for frame in ImageSequence.Iterator(right):
            right.seek(ind)
            right_frames.append(frame.copy())
            ind += 1
        
        ind = 0
        for frame in ImageSequence.Iterator(left):
            left.seek(ind)
            left_frames.append(frame.copy())
            ind += 1
        
        #Removing the first frame which usually is a bit spotty
        idle_frames.remove(idle_frames[0])
        left_frames.remove(left_frames[0])
        right_frames.remove(right_frames[0])
        
        #Putting each frame in a list 
        self.test_img = [tk.PhotoImage(file='chonk.png').subsample(20)]
        self.ani_idle = [ImageTk.PhotoImage(i.resize((200,200))) for i in idle_frames]
        self.ani_left = [ImageTk.PhotoImage(i.resize((200,200))) for i in left_frames]
        self.ani_right = [ImageTk.PhotoImage(i.resize((200,200))) for i in right_frames]
        
        
        self.frame_index = 0
        self.img = self.ani_idle[1]
        self.bub_img = ImageTk.PhotoImage(yap_bubble)
        self.timer = 0
        
        self.jump_range_param = 40
        
        self.seed_randomizer = random.randint(0, 7)
        self.action_time = 500
        self.x_range_right = [*range(-1 * self.jump_range_param, self.jump_range_param)]
        self.x_range_left = [*range(-1 * self.jump_range_param, self.jump_range_param)]
        self.x_range_left.reverse()    
                
        # self.response_screen = tk.Label(self.window, text="", font= ('Helvetica 12'), height=0)
        # self.response_screen.pack(pady=1)
        
        # self.input_box = tk.Entry(self.window, width=20, bd=0, bg="white", fg="black", highlightthickness = 0,
        #                             borderwidth=0, font=("Ariel", 12))
        # self.input_box.config(highlightthickness = 0, borderwidth=0)
        # self.input_box.pack()
        
        # self.button = tk.Button(self.window, text= "Ask Me", command=self.on_click)
        # self.button.pack()
    
        # timestamp to check whether to advance frame
        self.timestamp = time.time()

        # set focushighlight to black when the window does not have focus
        self.window.config(highlightbackground='black')

        # make window frameless
        self.window.overrideredirect(True)

        # make window draw over all others
        self.window.attributes('-topmost', True)
        
        self.window.wm_attributes('-transparentcolor', 'black')

        # create a label as a container for our image
        self.label = tk.Label(self.window, bd=0, bg='black')

        # create a window of size 128x128 pixels, at coordinates 0,0
        self.x = self.window.winfo_screenwidth() - 800
        self.y = self.window.winfo_screenheight() - 500
        self.window.geometry('200x200+{x}+{y}'.format(x=str(self.x), y = str(self.y)))

        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        ### DIALOG BUBBLE SECTION OF THE CODE. INDEPENDENT FROM THE CAT MOVEMENT CODE ###
        
        # turn black into transparency
        self.dialog.wm_attributes('-transparentcolor', 'black')
        
        self.dialog.config(highlightbackground='black')

        # make window frameless
        self.dialog.overrideredirect(True)

        # make window draw over all others
        self.dialog.attributes('-topmost', True)

        # turn black into transparency
        self.dialog.wm_attributes('-transparentcolor', 'black')
        
        self.bub_label = tk.Label(self.dialog, bd=0, bg='black')
        
        self.bub_x = self.window.winfo_screenwidth() - 780
        self.bub_y = self.window.winfo_screenheight() - 600
        self.dialog.geometry('200x200+{x}+{y}'.format(x=str(self.bub_x), y = str(self.bub_y)))
        
        self.bub_label.configure(image=self.bub_img)

        # give window to geometry manager (so it will appear)
        self.bub_label.pack()
        
        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.idle)
        self.window.mainloop()

    def walk_right(self):
        self.x += 2
        if self.is_at_edge_of_screen():
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_left)
            return 

        # advance frame if 50ms have passed
        if time.time() > self.timestamp + 0.10:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % 4
            self.img = self.ani_right[self.frame_index]

        # create the window
        self.window.geometry('200x200+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()
        
        if self.timer == self.action_time:
            self.next_function()
        else:
            # call update after 10ms
            self.timer += 1
            self.window.after(10, self.walk_right)
        return
        
    def walk_left(self):
        self.x -= 2
        if self.is_at_edge_of_screen():
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_right)
            return 
        # move right by one pixel
      
        # advance frame if 50ms have passed
        if time.time() > self.timestamp + 0.10:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % 4
            self.img = self.ani_left[self.frame_index]

        # create the window
        self.window.geometry('200x200+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()
        
        if self.timer == self.action_time:
            self.next_function()
        else:     
            self.timer += 1
            # call update after 10ms
            self.window.after(10, self.walk_left)
        return
            
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
        self.window.geometry('200x200+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()
        
        if self.timer == self.action_time:
            self.next_function()
        else:     
            self.timer += 1
            # call update after 10ms
            self.window.after(10, self.walk_up)
        return
    
    def walk_down(self):
        self.y += 1
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
        self.window.geometry('200x200+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()
        
        if self.timer == self.action_time:
            self.next_function()
        else:
            self.timer += 1
            # call update after 10ms
            self.window.after(10, self.walk_down)
        return
            
    #calling jump_right:
    # self.timer = 0
    # self.action_time = 730
    # self.window.after(10, self.jump_right)
            
    def jump_right(self):
        # move right by one pixel
        self.x += 7

        self.y = self.y - self.jump_parabola(self.x_range_left[self.timer])
        
        
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
        self.window.geometry('200x200+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()
        
        if self.timer == self.action_time:
            self.next_function()
        else:     
            self.timer += 1
            # call update after 10ms
            self.window.after(10, self.jump_right)
        return
            
    def jump_left(self):
        # move right by one pixel
        self.x -= 7

        self.y = self.y - self.jump_parabola(self.x_range_left[self.timer])
        
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
        self.window.geometry('200x200+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
        # add the image to our label
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()
        
        if self.timer == self.action_time:
            self.next_function()
        else:     
            self.timer += 1
            # call update after 10ms
            self.window.after(10, self.jump_left)
        return
    
    def idle(self):
        
        # advance frame if 50ms have passed
        self.bub_x = self.x + 20
        self.bub_y = self.y - 100
        
        if time.time() > self.timestamp + 0.25:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % 4
            self.img = self.ani_idle[self.frame_index]
        
        
        # create the window
        self.window.geometry('200x200+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
        self.dialog.geometry('200x200+{x}+{y}'.format(x=str(self.bub_x), y = str(self.bub_y)))
        # add the image to our label
        self.label.configure(image=self.img)
        self.bub_label.configure(image=self.bub_img)
        # give window to geometry manager (so it will appear)
        self.label.pack()
        self.bub_label.pack()
        
        #idle 
        if self.timer == self.action_time:
            self.dialog.withdraw()
            self.next_function()
        else:
            self.timer += 1
            self.window.after(10, self.idle)
        return
    
    def is_at_edge_of_screen(self):
        if(self.x <= 0):
            self.x = 5
            return True
        if(self.x + 180 >= self.window.winfo_screenwidth()):
            self.x = self.window.winfo_screenwidth() - 185
            return True
        if(self.y <= 0):
            self.y = 5
            return True
        if(self.y + 150 >= self.window.winfo_screenheight()):
            self.y = self.window.winfo_screenheight() - 155
            return True
        return False
    
    def jump_parabola(self, x):
        y = 0.5 * x
        return int(y)
    
    def next_function(self):
        self.seed_randomizer = random.randint(0,6)
        self.timer = 0
        print(self.seed_randomizer)
        match self.seed_randomizer:
            case 0: 
                self.action_time = random.randint(300, 800)
                self.window.after(10, self.walk_right)
                return
            case 1: 
                self.action_time = random.randint(300, 800)
                self.window.after(10, self.walk_left)
                return
            case 2: 
                self.action_time = random.randint(300, 800)
                self.window.after(10, self.walk_down)
                return
            case 3: 
                self.action_time = random.randint(300, 800)
                self.window.after(10, self.walk_up)
                return
            case 4: 
                self.action_time = self.jump_range_param * 2 -1
                self.window.after(10, self.jump_right)
                return 
            case 5: 
                self.action_time = self.jump_range_param * 2 -1
                self.window.after(10, self.jump_left)
                return
            case 6: 
                self.dialog.deiconify()
                self.action_time = random.randint(300, 800)
                self.window.after(10, self.idle)
                return
    
    def on_click(self):
        #x, y = pyautogui.position()
        #if x >= self.x and y >= self.y and x <= self.x + 125 and y <= self.y + 165:
            # response = catgptAI.catgptAI.chat(self.input_box.get())
            try: 
                self.window.geometry('200x200+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
                # self.response_screen.config(text="response", wraplength= 180, height=6, padx=-1)
            except:
                print("meow")
        #self.window.after(100, self.on_click)
Pet()