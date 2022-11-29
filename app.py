import tkinter as tk
from tkinter import filedialog, Text
import os, sys
import GUImain
import subprocess

class IORedirector(object):
    def __init__(self,TEXT_INFO):
        self.TEXT_INFO = TEXT_INFO

class StdoutRedirector(IORedirector):
        def write(self,str):
           self.TEXT_INFO.config(text=self.TEXT_INFO.cget('text') + str)

root = tk.Tk()
apps = []

def selectFile():
    apps.clear()
    filename = filedialog.askopenfilename(initialdir= os.getcwd() + "/tests/", title="Select Lox File", filetypes=[("LOX files", "*.lox")])
    fileName.config(text = filename)
    apps.append(fileName)
    
def runInterpreter():
    FileOutput.config(text="")
    sys.stdout = StdoutRedirector(FileOutput)
    GUImain.runningFile(apps[0])

def ClearTerm():
    FileOutput.config(text="")

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


FileOutput = tk.Label(wrapper2, text="", borderwidth=5)
# v = tk.Scrollbar(root, orient="vertical")
# v.pack(side=tk.RIGHT, fill="y")
# v.config(command=root.yview)
FileOutput.pack(pady = 10)

clearOutput = tk.Button(wrapper2, text="Clear Terminal", command=ClearTerm)


# FileOutput = tk.Label(root, text="", borderwidth=5)
# FileOutput.pack(pady = 20)

# runLox = tk.Button(root, text="Run fLox!", padx=18, pady=4, fg="white", bg="#181818", command=runInterpreter)
# runLox.pack(side="bottom")

# attachFile = tk.Button(root, text="Pick Lox File", padx=10, pady=5, fg="white", bg="#181818", command=selectFile)
# attachFile.pack(side="bottom")

root.geometry("600x600")
root.title("The fLox Interpreter GUI")
root.resizable(False, False)
root.mainloop()