from tkinter import *
import PIL
from PIL import ImageTk, Image, ImageDraw
import tensorflow
import keras
import numpy as np



# Normalize input of neural network
def normalize(picture):
	width, height = picture.size
	normalized_array = []

	for j in range(0, height):
		for i in range(0, width):
            # Divide each pixle by 255 to create a range from 0 to 1
			pixel = picture.getpixel((i,j))
			normalized_array.append( pixel[0] / 255.0 )
	return np.array(normalized_array)


# Track mouse movements, and draw.
def paint( event ):
    global prev_x, prev_y
    color = "#ffffff"
    # Grab mouse location
    x = event.x
    y = event.y
    # If it's first click, add padding.
    if prev_x == 0:
        prev_x = x-1
        prev_y = y-1
    # Draw on canvas
    w.create_line (prev_x, prev_y, x, y, fill = color, width = 10)
    # Draw on image on memory.
    draw.ellipse((x-5, y-5, x+5, y+5), fill=(0,0,0))
    # Save values
    prev_x = x;
    prev_y = y;


# clear previous variables
def release (event):
    global prev_x, prev_y
    prev_x = 0
    prev_y = 0
    
    
# Clear canvas
def clear (event):
    global prev_x, prev_y
    prev_x = 0
    prev_y = 0
    # Clear image on memory
    draw.rectangle((0, 0, 250, 250), fill=(0,0,0))
    w.delete("all")

# Perform prediction with drawn image.
def predict ():
    global model, image
    # Save image to file
    image.save("input.jpeg", quality=95)
    # Load image
    img = Image.open("input.jpeg")
    # Resize image to fit the standard size
    img = img.resize((28, 28), Image.ANTIALIAS)
    # Show image
    img.show()
    # Normalize input image
    input =  normalize(img)
    # Reshape input to reduce color channel.
    input = input.reshape(1, 28, 28, 1)
    # Perform prediction with Keras
    answer = model.predict(input)
    # Get highest
    max = answer[0].max()
    print(max)
    c = 0
    # Print predicted value (e.g. recognize digit)
    for x in answer[0]:
        if x == max:
            answerRes.set("Result: {}".format(c))
        c = c+1
    
    
    
# Create window
master = Tk()
# Set winodw title
master.title( "MNIST Prediction Model" )
# Create canvas with black background
w = Canvas(master,  background="#000000", width=canvas_width, height=canvas_height)
w.pack(side = BOTTOM)
# Define events for mouse clicks
# Mouse down to paint
w.bind( "<B1-Motion>", paint )
# Mouse up to release
w.bind( "<ButtonRelease-1>", release )
# Double click to clear canvas
w.bind( "<Double-Button-1>", clear )

prev_x = 0
prev_y = 0

# Place a label
answerRes = StringVar()
answerLabel = Label(master, textvariable=answerRes)
answerLabel.pack(side = TOP)
answerRes.set("Result: null")

# Create an empty image to draw on.
image = PIL.Image.new("RGB", (canvas_width, canvas_height), (255,255,255))
draw = ImageDraw.Draw(image)

# Define prediction button
button = Button (text="Predict", command=predict)
button.pack(side = BOTTOM)

# Load CNN model
model = keras.models.load_model("model.h5")

mainloop()
