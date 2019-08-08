import os,re
import shutil



dir_src ='./images/'
dir_dst = './image_classifier/'

list_dir = os.listdir(dir_src)

for file in list_dir:
    # print(type(dir_src))
    dir_name = re.match(r'(.*)_.*$', file).group(1)
    # print(f'%s : {dir_name}' % file)
    dir_path = dir_dst + dir_name
    # print(dir_path)
    try:
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            print(dir_path)
        if os.path.exists(dir_path):
            file_path = dir_src + file
            # print(file_path)
            #move
            shutil.copy(file_path, dir_path)
    except Exception:
        print("None")
print ("Done")