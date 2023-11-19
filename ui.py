import os
import platform
import tkinter as tk
import tkinter.ttk as ttk
import tkinter.filedialog
from utils import *
from augmentation import XrayAugmentation
from PIL import Image, ImageTk, ImageDraw

class UI:
    def __init__(self, root):
        self.root = root
        #self.w = self.root.winfo_screenwidth()
        #self.h = self.root.winfo_screenheight()
        if platform.system()=='Linux':
            self.root.attributes("-zoomed", True)
        else:
            self.root.state("zoomed")

        self.root.title("AI X-Ray Viewer")
        self.current_image_path = None
        self.w_state = {}
        self.create_widget_state()
        self.aug = XrayAugmentation()
        self.files = None
        self.folder_path = None
        self.img_path = []
        
#Set all Widgets
        #Frame
        self.mainframe = tk.Frame(root, bg='#605C5B')
        self.Lframe = tk.Frame(self.mainframe, width=200, bg='#3A302E', relief='ridge', bd=2)
        self.Tframe = tk.Frame(self.mainframe, bg='black', relief='ridge', bd=2)
        #Button
        self.browse_txt_btn = tk.Button(self.Lframe, text="Browse Images' Path File (.txt)", command=self.browse_txt, relief='raised', width=50)
        self.browse_dir_btn = tk.Button(self.Lframe, text="Browse Images' Directory (Directory)", command=self.browse_dir, relief='raised', width=50)
        self.start_btn = tk.Button(self.Lframe, text="Start", command=self.start, relief='raised')
        #Check Button
        self.ck_Hflip = tk.Checkbutton(self.Lframe, text='Horizontal Flip',variable= self.w_state['Hflip'], onvalue=1, relief='raised', width=20)
        self.ck_Vflip = tk.Checkbutton(self.Lframe, text='Vertical Flip',variable= self.w_state['Vflip'], onvalue=1, relief='raised', width=20)
        self.ck_Rotate = tk.Checkbutton(self.Lframe, text='Rotation',variable= self.w_state['Rotate'], onvalue=1, relief='raised', width=20)
        #Label
        self.image_label = tk.Label(self.Lframe, text='', width=200)
        self.trans_label = tk.Label(self.Lframe, text='', width=200)
        self.working_dir_label = tk.Label(self.Tframe, text='working', width=60)
        self.saving_dir_label = tk.Label(self.Tframe, text='saving', width=60)

        self.mainframe.pack(expand=True, fill=tk.BOTH)
        self.Lframe.pack(side=tk.LEFT, fill='y')
        self.Tframe.pack(side=tk.TOP, fill='x')
        self.browse_txt_btn.pack()
        self.browse_dir_btn.pack()
        self.ck_Hflip.pack()
        self.ck_Vflip.pack()
        self.ck_Rotate.pack()
        self.working_dir_label.pack(anchor='nw')
        self.saving_dir_label.pack(anchor='nw')

    def start(self):
        pass
        #self.aug.augmentation(self.w_state) 
        

    def create_widget_state(self):
        self.w_state['Hflip'] = tk.IntVar()
        self.w_state['Vflip'] = tk.IntVar()
        self.w_state['Rotate'] = tk.IntVar()

    def browse_txt(self):
        file_path = tk.filedialog.askopenfilename(filetypes=[(".txt files", "*.txt")])
        if file_path:
            print(file_path)
            #self.display_image(file_path)

    def browse_dir(self):
        self.folder_path = tk.filedialog.askdirectory()
        if self.folder_path:
            self.files = [f for f in os.listdir(self.folder_path) if f.lower().endswith(('.jpg', 'jpeg', 'png'))]
            if self.files:
                for f in self.files:
                    self.img_path.append(os.path.join(self.folder_path, f))
                self.display_image(os.path.join(self.folder_path, self.files[0]))
                print(self.files[0])
                print(len(self.img_path))

    def display_image(self, img_path):
        self.current_image_path = img_path
        self.img = Image.open(img_path)
        ratio = 240/ self.img.size[0]
        self.img = self.img.resize((240, int(self.img.size[1]*ratio)))

        bbox_list = get_bbox(self.current_image_path, self.img)
        img_tensor, bbox_tensor = toTensor(self.img, bbox_list)
        bboxes = tv_tensors.BoundingBoxes(bbox_tensor, format="XYXY", canvas_size=(self.img.size[1], self.img.size[0]))
        self.aug.augmentation(img_tensor, bboxes, method='Demo')
        transforms = v2.Compose([
            v2.RandomRotation(degrees=(-90,90)),
            v2.ToDtype(torch.float32, scale=True),
        ])

        trans_img, trans_boxes = transforms(img_tensor, bboxes)
        trans_img, trans_boxes = fromTensor(trans_img, trans_boxes)

        bbox_img = ImageDraw.Draw(self.img)
        self.image_label.pack()
        self.trans_label.pack()
        self.start_btn.pack()


        for bbox in bbox_list:
            bbox_img.rectangle(bbox, outline='red')
        tk_img = ImageTk.PhotoImage(self.img)

        self.image_label.configure(image=tk_img)
        self.image_label.image = tk_img


        bbox_trans_img = ImageDraw.Draw(trans_img)
        for bbox in trans_boxes:
            bbox_trans_img.rectangle(bbox, outline='red')
        tk_trans_img = ImageTk.PhotoImage(trans_img)
        self.trans_label.configure(image=tk_trans_img)
        self.trans_label.image = tk_trans_img


