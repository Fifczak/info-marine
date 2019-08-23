import json
from pandas.io.json import json_normalize
from tqdm import tqdm
from tkinter import Tk
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
import csv

import numpy as np
import wavio
import tkinter as tk
from tkinter import Tk
from tkinter import filedialog
from tkinter import ttk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt

import filetype
from matplotlib.widgets import Cursor






class filteringgui:
	def __init__(self):
		self.root = tk.Tk()
		self.root.title("Filtering")
		tk.Label(self.root, text="File type").grid(row=0, column=0)
		self.filetypeswitch = ttk.Combobox(self.root, text="", values=["txt", "wav"], width=45, state="readonly")
		self.filetypeswitch.grid(row=0, column=1)



		self.root.mainloop()




filteringgui()