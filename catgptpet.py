import tkinter as tk
from PIL import Image
from PIL import ImageTk
import time
import random
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from openai import OpenAI
from dotenv import load_dotenv


# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
CORS(app)

# Get OpenAI API key from environment
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
api_request_counter = 0

class pet():
    def __init__(self):
        # create a window
        self.window = tk.Tk()

        # placeholder image
        image = Image.open('chonk.jpg')
        image = image.resize((200, 200))
        image = ImageTk.PhotoImage(image)
        
        self.walking_right = [tk.PhotoImage(image)]
        self.frame_index = 0
        self.img = self.walking_right[self.frame_index]
        self.timer = 0
        self.action_time = random.randint(300, 800)
        
        self.inputtxt = tk.Text(self.window, 
                   height = 5, 
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
        self.x = self.window.winfo_screenwidth() - 250
        self.y = self.window.winfo_screenheight() - 250
        self.window.geometry('128x90+{x}+{y}'.format(x=str(self.x), y = str(self.y)))

        # add the image to our label
        self.label.configure(image=self.img)

        # give window to geometry manager (so it will appear)
        self.label.pack()

        # run self.update() after 0ms when mainloop starts
        self.window.after(0, self.walk_right)
        self.window.mainloop()

    def walk_right(self):
        if self.is_at_edge_of_screen(self):
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_left)
            return 
        # move right by one pixel
        self.x += 1
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
        if self.is_at_edge_of_screen(self):
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_right)
            return 
        # move right by one pixel
        self.x -= 1
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
        if self.is_at_edge_of_screen(self):
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_down)
            return 
        # move right by one pixel
        self.y -= 1
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
        # move right by one pixel
        if self.is_at_edge_of_screen(self):
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_up)
            return 
            
        self.x += 1
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
        if self.is_at_edge_of_screen(self):
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_left)
            return 
            
        self.x += 1
        self.y = self.jump_parabola(self, range(self.action_time)[self.timer])
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
        if self.is_at_edge_of_screen(self):
            self.timer = 0
            self.action_time = random.randint(300, 800)
            self.window.after(10, self.walk_right)
            return 
            
        self.x -= 1
        self.y = self.jump_parabola(self, range(self.action_time).reversed()[self.timer])
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
        if(self.x == 0 or self.x + 200 == self.window.winfo_screenwidth()):
            return True
        if(self.y == 0 or self.y + 200 == self.window.winfo_screenheight()):
            return True
        return False
    
    def jump_parabola(self, x):
        y = -0.003(x - self.x)**2 + 400 + self.y
        return y
    
    def on_click(self):
        x = self.window.winfo_pointerx() - self.window.winfo_rootx()
        y = self.window.winfo_pointery() - self.window.winfo_rooty()
        if self.x == x and self.y == y:
            response = self.chat()
            print(response)
            
    def chat(self):
        global api_request_counter
        api_request_counter += 1
        print(f"API Request Count: {api_request_counter}")
        
        try:
            # Get the user's message from the request body
            user_message = self.inputtxt
            user_message = user_message + "Instruction: make the response sound like a cat replied and not have it be over 200 words NO MATTER WHAT."
            
            # Make a request to the OpenAI API
            response = client.chat.completions.create(model="gpt-4o",  # or gpt-3.5-turbo
            messages=[
                {"role": "user", "content": user_message}
            ])

            # Extract the assistant's response
            assistant_message = response.choices[0].message.content
            
            # Return the assistant's message as a JSON response
            return assistant_message

        except Exception as e:
            print(f"Error: {e}")
            return "Error: Something went wrong"
    
pet()