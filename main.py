


import cv2
import tkinter as tk
from tkinter import filedialog
import numpy
import os

class ImageProcessing():
    def __init__(self, root_w):
        self.root = root_w
        self.image_path = 'F:/Image_Processing/Code/InputImages/1.jpeg'
        self.root.title('Image Processing')
        self.root.geometry('800x500+200+100')
        self.root.config(background='#fff')
        self.root.resizable(False, False)

        self.all_selected_images = []
        self.item_selected = False

        self.checked_images = []
    

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

    def images_section(self):
        self.images_s = tk.Frame(self.root, bg='lightgray')
        self.images_s.pack(fill=tk.BOTH)

        self.img_list = tk.Listbox(self.images_s, font=('sans-serif' , 12))
        self.img_list.pack(fill=tk.X)
        self.img_list.bind('<<ListboxSelect>>', self.onselect)

        self.operations = tk.Frame(self.images_s, bg='white')
        self.operations.pack(fill=tk.X, ipadx=5, ipady=5)
        self.add_oper_btns()

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
            self.dlt_btn = tk.Button(self.operations, text='Checked' if s_item in self.checked_images else 'Check', command=self.mark_as_checked)
            self.dlt_btn.pack(side=tk.RIGHT)
        pass

    def mark_as_checked(self):
        s_item  = self.img_list.curselection()
        s_item = self.img_list.get(s_item[0])
        self.checked_images.append(s_item)
        self.add_oper_btns()

    def delete_selected_item(self):
        s_item  = self.img_list.curselection()
        self.img_list.delete(s_item[0])
        self.add_oper_btns()


    def add_images_handler(self):
        all_images = filedialog.askopenfilenames(
            title='Select Images Files', 
            filetypes=[
                ("Image File",'.jpg'),
                ("Image File",'.png'),
                ("Image File",'.jpeg'),
                ("Image File",'.webp'),
            ]
        )
        self.all_selected_images = all_images
        self.show_images_list()

    def show_images_list(self):
        for index , img in enumerate(self.all_selected_images):
            # new_text = self.
            self.img_list.insert(index, img)

    def convert_images_handler(self):
        self.process_image()

    def start(self):
        pass

    def white_image(self, current_img=None):
        c_img_width = 500
        if current_img is not None:
            c_img_width = current_img.shape[1]
        
        image_height = 50
        image_width = c_img_width
        number_of_color_channels = 3
        color = (255,255,255)
        pixel_array = numpy.full((image_height, image_width, number_of_color_channels), color, dtype=numpy.uint8)
        return pixel_array

    def process_image(self):
        for r_img in self.all_selected_images:
            image_name = r_img.split('/')[-1].split('.')[0]
            if r_img not in self.checked_images:
                for i in image_name:
                    if i.isdigit():
                        image_name = image_name.replace(i , '')
                image_name = image_name.replace('--' , '')
                image_name = image_name.replace('(' , '')
                image_name = image_name.replace(')' , '')

                if len(image_name) > 0 and image_name[-1] == '-':
                    image_name = image_name.replace('-' , '' , -1)
                if len(image_name) > 0 and image_name[-1] == ' ':
                    image_name = image_name.replace(' ' , '' , -1)
            
                if len(image_name) == 0:
                    image_name = 'random'

            img_ext = r_img.split('/')[-1].split('.')[-1]
            img = cv2.imread(r_img , cv2.IMREAD_UNCHANGED)
            gray_img = cv2.cvtColor(img , cv2.COLOR_BGR2GRAY)
            inverted_img = 255-gray_img
            blur_img = cv2.GaussianBlur(inverted_img , (21,21) , 0)
            inverted_blur = 255-blur_img

            pencil_sketch = cv2.divide(gray_img , inverted_blur, scale=256.0)

            final_image = pencil_sketch

            if img_ext == 'png':
                *_, alpha = cv2.split(img)
                final_image = cv2.merge((final_image, final_image, final_image, alpha))


            print_able_name = image_name
            for i in print_able_name:
                if i.isdigit():
                    print_able_name = print_able_name.replace(i , '')

            print_able_name = print_able_name.replace('--' , ' ')
            print_able_name = print_able_name.replace('(' , ' ')
            print_able_name = print_able_name.replace(')' , ' ')
            print_able_name = print_able_name.replace('_' , ' ')
            print_able_name = print_able_name.replace('.' , ' ')
            print_able_name = print_able_name.replace('  ' , ' ')

            print_able_name = print_able_name.replace('-' , ' ')
            
            if len(print_able_name) == 0:
                print_able_name = 'random'

            get_text_size=  cv2.getTextSize(print_able_name , cv2.FONT_HERSHEY_SIMPLEX, 1, 2)[0]
            
            # text_image = self.white_image(current_img=final_image)
            hd = (final_image.shape[1] - get_text_size[0]) / 2
            cv2.putText(
                final_image, 
                print_able_name,
                (int(hd),30), 
                cv2.FONT_HERSHEY_SIMPLEX, 
                1,
                (0,0,0),
                2,
                2
            )

            is_folder = os.path.isdir('./outputImages')
            if not is_folder:
                os.mkdir('outputImages')
            cv2.imwrite(f'./outputImages/{image_name}.png' , final_image)

        self.all_selected_images = []
        self.img_list.delete(0 , tk.END)
        self.item_selected = False
        self.add_oper_btns()
        pwd_path = os.getcwd()
        os.startfile(f'{pwd_path}/outputImages')
        


if __name__ == '__main__':
    root = tk.Tk()
    img_processing = ImageProcessing(root)
    img_processing.window_header()

    root.mainloop()