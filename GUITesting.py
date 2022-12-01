import tkinter as tk
from tkinter import filedialog, Text
import os, sys
import GUImain
#Secondary GUI for testing

class TextRedirector(object):   #File-Like Struct for Redirecting STD-Out into the textbox
    def __init__(self, widget, tag="stdout"):
        self.widget = widget
        self.tag = tag

    def write(self, str):
        self.widget.configure(state="normal")
        self.widget.insert("end", str, (self.tag,))
        self.widget.configure(state="disabled")

    def flush(self):
        pass

root = tk.Tk()
loxApplication = []
root.geometry("600x600")
root.title("The fLox Interpreter GUI")
root.resizable(False, False)


def selectFile():
    loxApplication.clear()    #To only allow 1 file to be attached
    filename = filedialog.askopenfilename(initialdir= os.getcwd() + "/tests/", title="Select Lox File", filetypes=[("LOX files", "*.lox")])
    fileName.config(text = filename)
    loxApplication.append(fileName)
    
def runInterpreter():
    print("\nOutput From Application:\n" + loxApplication[0]['text'] + "\n")
    GUImain.runningFile(loxApplication[0])

wrapper = tk.LabelFrame(root, text="Select Lox File")
wrapper.pack(fill="both", expand="yes", padx=10, pady=10)

wrapper2 = tk.LabelFrame(root, text="Output")
wrapper2.pack(fill="both", expand="yes", padx=10, pady=10)

fileName = tk.Label(wrapper, text="")
fileName.pack(pady = 2)

attachFile = tk.Button(wrapper, text="Run", command=runInterpreter)
attachFile.pack(side=tk.RIGHT, padx=10, pady=10)

btn = tk.Button(wrapper, text="Browse", command=selectFile)
btn.pack(side=tk.RIGHT, padx=10, pady=10)


FileOutput = tk.Text(wrapper2, borderwidth=5)
sys.stdout = TextRedirector(FileOutput)

#Trying to add a scrollbar to see output
v = tk.Scrollbar(wrapper2, orient="vertical")
v.pack(side=tk.RIGHT, fill="y")
v.config(command=FileOutput.yview)

FileOutput.pack(pady = 2, padx=2)

#clearOutput = tk.Button(wrapper2, text="Clear Terminal", command=ClearTerm)

root.mainloop()