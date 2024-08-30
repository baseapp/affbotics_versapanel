import lvgl as lv

import usys as sys
sys.path.append('')

script_path = './apps/data/focus.bin'
#script_path = '/wall_1.png'

#with open(script_path, 'rb') as f:
#  bin_data = f.read()
#  print("img open")

#bin_image_dsc = lv.image_dsc_t({
#    "header": {"w": 50, "h": 50, "cf": lv.COLOR_FORMAT.RGB565},
#    'data_size': len(bin_data),
#    'data': bin_data 
#})


def drawScreen():
    scr = lv.screen_active()
    
    i = 0
    while i < 5:
        #image1 = lv.image(scr)
        #image1.set_src(bin_image_dsc)
        #image1.set_pos(j, i * 55)
        j = 0
        while j < 5:
            with open(script_path, 'rb') as f:
                bin_data = f.read()

            bin_image_dsc = lv.image_dsc_t({
                "header": {"w": 50, "h": 50, "cf": lv.COLOR_FORMAT.RGB565},
                'data_size': len(bin_data) - 12,
                'data': bin_data[12:]
            })
            image1 = lv.image(scr)
            image1.set_src(bin_image_dsc)
            image1.set_pos(j * 55, i * 55)
            j = j + 1
        i = i + 1
        
        
    
    print("done")

