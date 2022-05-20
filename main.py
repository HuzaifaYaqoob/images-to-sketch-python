


from tkinter import ttk
import cv2
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
from tkinter import ttk
import numpy
import os
import time
import asyncio
import threading
import datetime

class ImageProcessing():
    def __init__(self, root_w):
        self.root = root_w
        self.root.title('Image Processing')
        self.root.geometry('800x500+200+100')
        self.root.config(background='#fff')
        self.root.resizable(False, False)
        self.all_threads = {}

        self.progress_value = 1

        self.all_selected_images = []
        self.item_selected = False

        self.check_box_value = tk.BooleanVar()

    def change_title(self):
        self.h_heading['text'] = 'Please wait, Loading...'

    def update_prog_value(self):
        self.progress_bar['value'] += self.progress_value


    def window_header(self):
        self.header = tk.Frame(self.root, bg='white')
        self.header.pack(fill=tk.X)

        self.h_left = tk.Frame(self.header)
        self.h_left.pack(side=tk.LEFT)

        self.h_heading = tk.Label(self.h_left, font=('sans-serif',12) , text='Convert Images to Sketches' , foreground='black', background='white')
        self.h_heading.pack(fill=tk.X, ipady=10)

        self.h_right = tk.Frame(self.header, bg='white')
        self.h_right.pack(side=tk.RIGHT, ipadx=5, ipady=5)

        self.add_btn = tk.Button(self.h_right, text='Add Images', command=self.add_images_handler)
        self.add_btn.pack(side=tk.LEFT, padx=10, ipadx=10)

        self.convert_btn = tk.Button(self.h_right, text='Convert Images', command=self.convert_images_handler)
        self.convert_btn.pack(side=tk.RIGHT , ipadx=10)

        self.images_section()
        self.show_progress_bar()

    def images_section(self):
        self.images_s = tk.Frame(self.root, bg='lightgray')
        self.images_s.pack(fill=tk.BOTH,  expand=True)

        self.lbl_frame = tk.Frame(self.images_s, background='white')
        self.lbl_frame.pack(fill=tk.X)


        self.check_btn_imname = tk.Checkbutton(
            self.lbl_frame, 
            text='Print Name on top of Image', 
            background='white', 
            font=('sans-serif', 12),
            onvalue=True,
            offvalue=False,
            variable=self.check_box_value
        )
        self.check_btn_imname.pack(fill=tk.X, side=tk.LEFT)




        scrollbar = tk.Scrollbar(self.images_s)
        scrollbar.pack(side = tk.RIGHT, fill = tk.Y)

        self.img_list = tk.Listbox(self.images_s, font=('sans-serif' , 12))
        self.img_list.pack(fill=tk.BOTH, expand=True)
        self.img_list.bind('<<ListboxSelect>>', self.onselect)
        
        self.img_list.config(yscrollcommand = scrollbar.set)
        scrollbar.config(command = self.img_list.yview)
        
        self.operations = tk.Frame(self.images_s, bg='white')
        self.operations.pack(fill=tk.X, ipadx=5, ipady=5)

        self.add_oper_btns()
    
    def show_progress_bar(self):
        self.progress_bar = ttk.Progressbar(self.root, orient='horizontal', mode='determinate')
        self.progress_bar['value'] = 0
        self.progress_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def onselect(self, evnt):
        self.item_selected = True
        self.add_oper_btns()


    def add_oper_btns(self):
        for btn in self.operations.winfo_children():
            btn.destroy()
        if self.item_selected:
            s_item  = self.img_list.curselection()
            s_item = self.img_list.get(s_item[0])
            self.dlt_btn = tk.Button(self.operations, text='Delete selected item', command=self.delete_selected_item)
            self.dlt_btn.pack(side=tk.RIGHT , padx=5)
        pass


    def delete_selected_item(self):
        if self.item_selected:
            try:
                s_item  = self.img_list.curselection()
                self.img_list.delete(s_item[0])
                self.add_oper_btns()
                self.item_selected = None
            except:
                pass


    def add_images_handler(self):
        all_images = filedialog.askopenfilenames(
            title='Select Images Files', 
            filetypes=[
                ("Image File",'.png'),
            ]
        )

        self.all_selected_images += all_images
        self.show_images_list()

    def show_images_list(self):
        self.progress_bar['value'] = 0
        for index , img in enumerate(self.all_selected_images):
            self.img_list.insert(index, img)

    def convert_images_handler(self):
        time_now = str(datetime.datetime.now().strftime('%m%H%S'))
        self.all_threads[time_now] =  threading.Thread(name=time_now, target=self.process_image)
        all_keys = self.all_threads.keys()
        all_keys = list(all_keys)
        self.all_threads[all_keys[-1]].setDaemon(True)
        self.all_threads[all_keys[-1]].start()


    def start(self):
        pass

    def get_A4_Paper(self, noc=3):
        image_width = 910
        image_height = 1200
        color = (255,255,255, 255)
        pixel_array = numpy.full((image_height, image_width, noc), color, dtype=numpy.uint8)
        return pixel_array

    def get_white_bg(self, width=None, height=None ):
        image_width = width
        image_height = height
        number_of_color_channels = 4
        color = (255,255,255, 255)
        pixel_array = numpy.full((image_height, image_width, number_of_color_channels), color, dtype=numpy.uint8)
        return pixel_array

    def process_image(self):
        self.progress_bar['value'] = 0
        progress_inc = 100 / len(self.all_selected_images)
        self.progress_value = progress_inc
        self.h_heading['text'] = 'Please wait, Loading...'
        for r_img in self.all_selected_images:
            if ' ' in r_img:
                messagebox.showerror('Error' , 'Spaces are not allowed in Image path \ne.g /path/path with space/ not allowed \n Removing all images, Please select new one') 
                self.all_selected_images = []
                self.img_list.delete(0 , tk.END)
                self.item_selected = False
                
                break
            self.progress_bar['value'] += progress_inc

            img_name_splt = r_img.split('/')[-1].split('.')
            image_name = img_name_splt[0]
            img_ext = img_name_splt[-1]

            replace_w = {
                '--' : '',
                '(' : '',
                ')' : '',
                '_' : '',
                '  ' : '',
                '0' : '',
                '1' : '',
                '2' : '',
                '3' : '',
                '4' : '',
                '5' : '',
                '6' : '',
                '7' : '',
                '8' : '',
                '9' : '',
            }
            for key, value in replace_w.items():
                image_name = image_name.replace(key , value)

            if len(image_name) > 0 and image_name[-1] == '-':
                image_name = image_name.replace('-' , '' , -1)
        
            if len(image_name) == 0:
                image_name = 'random'

            try:
                img = cv2.imread(r_img , cv2.IMREAD_UNCHANGED)
                gray_img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
                inverted_img = 255-gray_img
                blur_img = cv2.GaussianBlur(inverted_img , (21,21) , 0)
                inverted_blur = 255-blur_img

                final_image = cv2.divide(gray_img , inverted_blur, scale=256.0)
                # if img_ext == 'png':
                *_, alpha = cv2.split(img)
                final_image = cv2.merge((final_image, final_image, final_image, alpha))
                
                fm_height = final_image.shape[0]
                fm_width = final_image.shape[1]


                a4_paper = self.get_A4_Paper(
                    noc=img.shape[2]
                )
                a4_height = a4_paper.shape[0]
                a4_width  = a4_paper.shape[1]

                if fm_width > a4_width or fm_height > a4_height - 150:
                    scale_percent = 60
                    new_width = int(fm_width * scale_percent / 100)
                    new_height = int(fm_height * scale_percent / 100)
                    dim = (new_width, new_height)
                    final_image = cv2.resize(final_image, dim, interpolation=cv2.INTER_AREA)
                    fm_width = new_width
                    fm_height = new_height

                if fm_width > a4_width or fm_height > a4_height - 150:
                    scale_percent = 70
                    new_width = int(fm_width * scale_percent / 100)
                    new_height = int(fm_height * scale_percent / 100)
                    dim = (new_width, new_height)
                    final_image = cv2.resize(final_image, dim, interpolation=cv2.INTER_AREA)
                    fm_width = new_width
                    fm_height = new_height

                y1 = (a4_height - fm_height ) // 2
                y2 = fm_height + y1
                x1 = (a4_width - fm_width) // 2
                x2 = fm_width + x1
                a4_paper[y1:y2, x1:x2] = final_image

                trans_mask = a4_paper[:,:,3] == 0
                a4_paper[trans_mask] = [255, 255, 255, 255]


                if self.check_box_value.get():
                    print_able_name = image_name.replace('-' , ' ')
                    font_size = 4
                    font_weight = 9
                    get_text_size=  cv2.getTextSize(print_able_name , cv2.FONT_HERSHEY_SIMPLEX, font_size, 2)[0]

                    if get_text_size[0] > a4_paper.shape[1]:
                        font_size = 2
                        font_weight = 5
                        get_text_size=  cv2.getTextSize(print_able_name , cv2.FONT_HERSHEY_SIMPLEX, font_size, 2)[0]
                    
                    if get_text_size[0] > a4_paper.shape[1]:
                        font_size = 1
                        font_weight = 2
                        get_text_size=  cv2.getTextSize(print_able_name , cv2.FONT_HERSHEY_SIMPLEX, font_size, 2)[0]
                    
                    hd = (a4_paper.shape[1] - get_text_size[0]) / 2
                    print_able_name = print_able_name.capitalize()
                    cv2.putText(
                        a4_paper, 
                        print_able_name,
                        (int(hd),120), 
                        cv2.FONT_HERSHEY_SIMPLEX, 
                        font_size,
                        (0,0,0, 255),
                        font_weight,
                        2
                    )

                is_img_exist = os.path.exists(f'./outputImages/{image_name}.png')
                if is_img_exist:
                    image_name += str(int(progress_inc))

                if not os.path.isdir('./outputImages'):
                    os.mkdir('outputImages')
                cv2.imwrite(f'./outputImages/{image_name}.png' , a4_paper)

            except Exception as err:
                print(err)
            
            try:
                idx = self.img_list.get(0, tk.END).index(r_img)
                self.img_list.delete(idx)
            except:
                pass


        self.h_heading['text'] = 'Convert Images to Sketch'
        self.progress_bar['value'] = 100
        self.all_selected_images = []
        self.img_list.delete(0 , tk.END)
        self.item_selected = False
        self.add_oper_btns()
        try:
            self.open_folder()
        except:
            pass

    def open_folder(self):
        pwd_path = os.getcwd()
        os.startfile(f'{pwd_path}/outputImages')


        


if __name__ == '__main__':
    root = tk.Tk()
    img_processing = ImageProcessing(root)
    img_processing.window_header()

    root.mainloop()