from PIL import Image, ImageDraw, ImageFilter, ImageFont
import os

frame ={
    "width": 150,
    "height": 150,
    "crops": True, 
}
icon = {
    "jpg":{ "isImage": True},
    "gif":{ "isImage": True},
    "png":{ "isImage": True},
    "zip":{
        "isImage": False,
        "b_r" : 0x87,
        "b_g" : 0xCE,
        "b_b" : 0xEB,
        "f_sz": 48,
        "f_x": 15,
        "f_y": 50,
        "title": "ZIP",
    },
    "doc":{
        "isImage": False,
        "b_r" : 0x7F,
        "b_g" : 0xFF,
        "b_b" : 0xD4,
        "f_sz": 24,
        "f_x": 15,
        "f_y": 50,
        "title": "Word\nDocument",
    },
    "pdf":{
        "isImage": False,
        "b_r" : 0xFF,
        "b_g" : 0xC0,
        "b_b" : 0xCB,
        "f_sz": 48,
        "f_x": 15,
        "f_y": 50,
        "title": "PDF",
    },
    "unknown":{
        "isImage": False,
        "b_r" : 0xC0,
        "b_g" : 0xC0,
        "b_b" : 0xC0,
        "f_sz": 24,
        "f_x": 15,
        "f_y": 50,
        "title": "Unknown",
    },
}
def crop_center(pil_img, crop_width, crop_height):
    img_width, img_height = pil_img.size
    return pil_img.crop(((img_width - crop_width) // 2,
                         (img_height - crop_height) // 2,
                         (img_width + crop_width) // 2,
                         (img_height + crop_height) // 2))
def crop_max_square(pil_img):
    return crop_center(pil_img, min(pil_img.size), min(pil_img.size))

def chext(filename):
    print("chext",filename,os.path.isfile(filename))
    #if os.path.isfile(filename) == False: return
    basename = os.path.basename(filename)
    dirname =  os.path.dirname(filename)
    fname = basename.split('.')[0].lower()
    ext = basename.split('.')[1].lower()
    if icon.get(ext):
        if icon[ext]['isImage']:
            return filename
        else:
            return f"{dirname}/{fname}.png"
    else:
        return f"{dirname}/{fname}.png"


def make_thumb(filename,save_dir="./thumbs"):
    if os.path.isfile(filename) == False: return
    basename = os.path.basename(filename)
    dirname =  os.path.dirname(filename)
    fname = basename.split('.')[0].lower()
    ext = basename.split('.')[1].lower()

    print(ext)
    
    if ext in icon.keys():
        pass
    else:
        ext = "unknown"

    if icon[ext]['isImage']:
        print("FILE:",filename)
        print("SAVE_DIR:",save_dir)
        print("BASE NAME:",basename)
        im = Image.open(filename)
        thumb_width = frame['width']

        im_crop_maxsq = crop_max_square(im)  
        im_thumb  = im_crop_maxsq.resize((thumb_width,thumb_width))
        os.makedirs(save_dir, exist_ok=True)
        im_thumb.save(f'{save_dir}/{basename}', quality=95) 

    else:
        im = Image.new("RGB", (frame['width'], frame['height']), (icon[ext]['b_r'], icon[ext]['b_g'], icon[ext]['b_b']))
        draw = ImageDraw.Draw(im)
        font = ImageFont.truetype('ipaexg.ttf', icon[ext]['f_sz'])
        draw.multiline_text((icon[ext]['f_x'], icon[ext]['f_y']), icon[ext]['title'], fill=(0, 0, 0), font=font)
        os.makedirs(save_dir, exist_ok=True)
        im.save(f'{save_dir}/{fname}.png', quality=95)
 

    return



if __name__ == "__main__":
    files = ["./test1.Doc","./test2.Zip","./test3.pdf","./test4.xyz","./test5.jpg"]
    for f in files:
        #make_thumb(f,'./thumbs')
        make_thumb(f)
