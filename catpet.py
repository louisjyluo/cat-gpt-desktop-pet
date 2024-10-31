import asyncio
import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import time
import random
import catgpt
import pyautogui
from tkinter import ttk

class Pet():
    def __init__(self):
        # create a window
        self.window = tk.Tk()
        #self.dialog_img = tk.Toplevel()
        self.dialog = tk.Toplevel()
        self.food = tk.Toplevel()

        #Reading the gifs for the animation
        idle = Image.open('data/latte_idle.gif')
        right = Image.open('data/latte_run_right.gif')     
        left = Image.open('data/latte_run_left.gif')
        yap_bubble = Image.open('data/speech_bubble.png')
        tuna = Image.open('data/can-of-tuna.png')
        #Creating the list of frames
        idle_frames = []
        right_frames = []
        left_frames = []
        
        yap_bubble = yap_bubble.copy().resize((200,200))
        tuna = tuna.copy().resize((200,200))
        
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
        self.test_img = [tk.PhotoImage(file='data/chonk.png').subsample(20)]
        self.ani_idle = [ImageTk.PhotoImage(i.resize((200,200))) for i in idle_frames]
        self.ani_left = [ImageTk.PhotoImage(i.resize((200,200))) for i in left_frames]
        self.ani_right = [ImageTk.PhotoImage(i.resize((200,200))) for i in right_frames]
        print("ani_right_size:", len(self.ani_right))
        print("ani_left_size:", len(self.ani_left))
        print("ani_idle_size:", len(self.ani_idle))
        
        
        self.frame_index = 0
        self.img = self.ani_idle[1]
        self.bub_img = ImageTk.PhotoImage(yap_bubble)
        self.food_img = ImageTk.PhotoImage(tuna)
        self.timer = 0
        self.eating = False
        
        self.jump_range_param = 40
        
        self.seed_randomizer = random.randint(0, 7)
        self.action_time = 500
        self.x_range_right = [*range(-1 * self.jump_range_param, self.jump_range_param)]
        self.x_range_left = [*range(-1 * self.jump_range_param, self.jump_range_param)]
        self.x_range_left.reverse()    
                
    
        # timestamp to check whether to advance frame
        self.timestamp = time.time()
        
        ### CAT ANIMATION SECTION OF THE CODE. INDEPENDENT FROM THE CAT MOVEMENT CODE ###

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
        self.x = self.window.winfo_screenwidth() - 500
        self.y = self.window.winfo_screenheight() - 220
        self.window.geometry('200x200+{x}+{y}'.format(x=str(self.x), y = str(self.y)))

        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        ### DIALOG BUBBLE SECTION OF THE CODE. INDEPENDENT FROM THE CAT MOVEMENT CODE ###
        
        self.dialog.config(highlightbackground='black')
        #self.dialog_img.config(highlightbackground='black')

        # make window frameless
        self.dialog.overrideredirect(True)
        #self.dialog_img.overrideredirect(True)
        
        # make window draw over all others
        self.dialog.attributes('-topmost', True)
        #self.dialog_img.attributes('-topmost', True)

        
        # turn black into transparency
        self.dialog.wm_attributes('-transparentcolor', 'black')
        #self.dialog_img.wm_attributes('-transparentcolor', 'black')
        
        self.bub_label = tk.Label(self.dialog, bd=0, text="meow :3", font= ('Helvetica 12'), height=1)
        #self.bub = tk.Label(self.dialog_img, bd=0, bg='black', image=self.bub_img)
        self.bub_label.pack()
        #self.bub.pack()
        
        self.bubble_width = 100
        self.bubble_height = 30
        self.bub_x = self.x + 20
        self.bub_y = self.y - 40
        self.offset_x = 0
        self.offset_y = 0
        
        ### FOOD INPUT SECTION OF THE CODE. INDEPENDENT FROM THE CAT MOVEMENT/DIALOG BUBBLE CODE ###
        
        self.food.wm_attributes('-transparentcolor', 'black')
        
        self.food.config(highlightbackground='black')

        # make window frameless
        self.food.overrideredirect(True)

        # make window draw over all others
        self.food.attributes('-topmost', True)

        # turn black into transparency
        self.food.wm_attributes('-transparentcolor', 'black')
        
        self.food_label = tk.Label(self.food, bd=0, bg='black')
        
        self.food_x = self.food_label.winfo_screenwidth() - 200
        self.food_y = self.food_label.winfo_screenheight() - 245
        self.food.geometry('200x200+{x}+{y}'.format(x=str(self.food_x), y = str(self.food_y)))
        
        self.input_box = tk.Entry(self.food, width=20, bd=0, bg="white", fg="black", highlightthickness = 0,
                                    borderwidth=0, font=("Ariel", 12))
        self.input_box.config(highlightthickness = 0, borderwidth=0)
        self.input_box.pack()
        
        self.button = tk.Button(self.food, text= "Feed", command=self.on_click)
        self.button.pack()
        
        self.food_label.configure(image=self.food_img)
        self.food_label.pack()
        
        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.idle)
        try:
            self.window.mainloop()
        except:
            self.window.quit()

    def idle(self):
        # advance frame if 50ms have passed
        self.bub_x = self.x + 20 - self.offset_x
        self.bub_y = self.y - 40 - self.offset_y
        
        if self.timer == 0:
            self.dialog.deiconify()
            #self.dialog_img.deiconify()
           
        if time.time() > self.timestamp + 0.15:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % 7
            self.img = self.ani_idle[self.frame_index]
        
        #self.dialog_img.geometry('200x200+{x}+{y}'.format(x=str(self.bub_x), y = str(self.bub_y)))
        self.dialog.geometry('{width}x{height}+{x}+{y}'.format(width=str(self.bubble_width), height=str(self.bubble_height), x=str(self.bub_x + 30), y = str(self.bub_y + 30)))
        self.label.configure(image=self.img)
        # give window to geometry manager (so it will appear)
        self.label.pack()
        self.bub_label.pack()
        #self.bub.pack()
        
        #idle 
        if self.timer == self.action_time:
            self.dialog.withdraw()
            #self.dialog_img.withdraw()
            self.next_function()
        else:
            self.timer += 1
            self.window.after(10, self.idle)
        return

    def walk_right(self):
        self.x += 2
        if self.is_at_edge_of_screen():
            self.timer = 0
            self.action_time = random.randint(250, 500)
            self.window.after(10, self.walk_left)
            return 

        # advance frame if 50ms have passed
        if time.time() > self.timestamp + 0.10:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % 6
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
            self.action_time = random.randint(250, 500)
            self.window.after(10, self.walk_right)
            return 
        # move right by one pixel
      
        # advance frame if 50ms have passed
        if time.time() > self.timestamp + 0.10:
            self.timestamp = time.time()
            # advance the frame by one, wrap back to 0 at the end
            self.frame_index = (self.frame_index + 1) % 6
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
            self.window.after(10, self.fall_down)
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
    
    def fall_down(self):
        self.y += 5
        # fall all the way down to the bottom
        if self.is_at_edge_of_screen():
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.idle)
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
        
        # call update after 10ms
        self.window.after(10, self.fall_down)
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
            self.action_time = random.randint(250, 500)
            self.window.after(10, self.fall_down)
            return 
            
        # advance frame if 50ms have passed
        if self.timer > 0 and self.timer <= 20:
            self.img = self.ani_right[4]
        elif self.timer > 20 and self.timer <= 28:
            self.img = self.ani_right[5]
        elif self.timer > 28 and self.timer <= 48:
            self.img = self.ani_right[0]
        elif self.timer > 48 and self.timer <= 60:
            self.img = self.ani_right[1]
        else:
            self.img = self.ani_right[2]

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
            self.action_time = random.randint(250, 500)
            self.window.after(10, self.fall_down)
            return 
            
        if self.timer > 0 and self.timer <= 20:
            self.img = self.ani_left[4]
        elif self.timer > 20 and self.timer <= 28:
            self.img = self.ani_left[5]
        elif self.timer > 28 and self.timer <= 48:
            self.img = self.ani_left[0]
        elif self.timer > 48 and self.timer <= 60:
            self.img = self.ani_left[1]
        else:
            self.img = self.ani_left[2]

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
    
    #Go towards the tuna can and "eat" it for the prompt
    def eat(self):
        self.timer = 0
        if self.x + 200 > self.food_x and self.x < self.food_x + 200:
            response_str = self.response
            if len(response_str) > 50:
                height_size = int(len(response_str) / 50) + 1
                self.bubble_height = height_size * 30
            if len(response_str) * 5 > 50 * 5:
                self.bubble_width = 50 * 5
            else:
                self.bubble_width = len(response_str) * 5
            self.offset_x = int(self.bubble_width / 4)
            self.offset_y = self.bubble_height - 30
            self.dialog.geometry('{width}x{height}+{x}+{y}'.format(width=str(self.bubble_width), height=str(self.bubble_height), x=str(self.bub_x), y = str(self.bub_y)))
            self.window.after(10, self.gen_msg)
        elif self.x < self.food_x:
            self.x += 2

            if time.time() > self.timestamp + 0.10:
                self.timestamp = time.time()
                self.frame_index = (self.frame_index + 1) % 6
                self.img = self.ani_right[self.frame_index]

            # create the window
            self.window.geometry('200x200+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
            # add the image to our label
            self.label.configure(image=self.img)
            # give window to geometry manager (so it will appear)
            self.label.pack()
            
            self.window.after(10, self.eat)
        else:
            self.x -= 2

            if time.time() > self.timestamp + 0.10:
                self.timestamp = time.time()
                self.frame_index = (self.frame_index + 1) % 6
                self.img = self.ani_left[self.frame_index]

            # create the window
            self.window.geometry('200x200+{x}+{y}'.format(x=str(self.x), y = str(self.y)))
            # add the image to our label
            self.label.configure(image=self.img)
            # give window to geometry manager (so it will appear)
            self.label.pack()
            
            self.window.after(10, self.eat)
    
    def gen_msg(self):
        if self.timer != len(self.response):
            self.bub_x = self.x + 20 - self.offset_x
            self.bub_y = self.y - 40 - self.offset_y
            
            if self.timer == 0:
                self.dialog.deiconify()
                #self.dialog_img.deiconify()
            
            if time.time() > self.timestamp + 0.15:
                self.timestamp = time.time()
                # advance the frame by one, wrap back to 0 at the end
                self.frame_index = (self.frame_index + 1) % 7
                self.img = self.ani_idle[self.frame_index]
            
            #self.dialog_img.geometry('200x200+{x}+{y}'.format(x=str(self.bub_x), y = str(self.bub_y)))
            self.dialog.geometry('{width}x{height}+{x}+{y}'.format(width=str(self.bubble_width), height=str(self.bubble_height), x=str(self.bub_x + 30), y = str(self.bub_y + 30)))
            self.label.configure(image=self.img)
            # give window to geometry manager (so it will appear)
            self.bub_label.config(text=self.response[0:self.timer], wraplength=self.bubble_width, font="Arial 12", height=self.bubble_height, width= self.bubble_width)
            self.timer += 1
            self.label.pack()
            self.bub_label.pack()
            self.window.after(30, self.gen_msg)
        else:
            self.eating = False
            self.action_time = random.randint(300, 800)
            self.timer = 0
            self.window.after(10, self.idle)
    
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
        if(self.y + 215 >= self.window.winfo_screenheight()):
            self.y = self.window.winfo_screenheight() - 220
            return True
        return False
    
    def jump_parabola(self, x):
        y = 0.3 * x
        return int(y)
    
    def next_function(self):
        #random.randint(0,4)
        if self.eating:
            self.window.after(10, self.eat)
            return
        
        self.seed_randomizer = random.randint(0,4)
        self.timer = 0
        match self.seed_randomizer:
            case 0: 
                self.action_time = random.randint(250, 500)
                self.window.after(10, self.walk_right)
                return
            case 1: 
                self.action_time = random.randint(250, 500)
                self.window.after(10, self.walk_left)
                return
            case 2: 
                self.action_time = self.jump_range_param * 2 -1
                self.window.after(10, self.jump_right)
                return 
            case 3: 
                self.action_time = self.jump_range_param * 2 -1
                self.window.after(10, self.jump_left)
                return
            case 4:
                self.action_time = random.randint(300, 800)
                self.window.after(10, self.idle)
                return
    
    def on_click(self):
        #x, y = pyautogui.position()
        #if x >= self.x and y >= self.y and x <= self.x + 125 and y <= self.y + 165:
            try: 
                asyncio.run(self.get_response())
                print("Starting the Eating process")
            except:
                print("meow")
    
    async def get_response(self):
        self.response = await catgpt.Catgpt.chat(self.input_box.get())
        print("Response Ready!")
        self.eating = True
Pet()