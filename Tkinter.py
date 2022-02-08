import sys 
from tkinter import *

root = Tk()
my_string_var = StringVar() 

def runcode(code):
        codeareadata = code

        try:

            original_stdout = sys.stdout
            sys.stdout = open('output.txt', 'w') 


            exec(codeareadata)

            sys.stdout.close()

            sys.stdout = original_stdout  



            output = open('output.txt', 'r').read()

        except Exception as e:
        
            sys.stdout = original_stdout
            output = e
        return output

def callback():
    text = textEditor.get(0.1,END)
    print(runcode(text))

textEditor = Text(root, width=43, height=10, font=(("Times"), 10,"bold"), wrap=WORD, fg="grey", bg="light yellow")
textEditor.pack()
def otjp(): 
    text = textEditor.get(0.1,END)
    my_string_var.set(runcode(text)) 
button1 = Button(root, text="execute", command = otjp)
button1.pack(pady=12)
texta = textEditor.get(0.1,END)

def java(): 
    my_string_var.set(runcode(texta))

my_string_var = StringVar() 
  
my_string_var.set("Output") 
  
my_label = Label(root,  
                 textvariable = my_string_var) 
root.geometry('370x230')
root.title("Excthiscode")
my_label.pack() 
root.mainloop()
