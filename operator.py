
#How to use:
#   put this script into a path with picture folders
import os
from PIL import Image
import shutil


# step1: from each folder extract 4 picture and resize them
def extract_picture(folder_path=os.getcwd(), picked_pic_folder='picked_pic'):
    """
    arg: 
            floder_path: str default path is current folder path
            picked_pic_folder: str desired folder to store picked pictures
    return:
            pic_info_list: list each element is picked pictures' names
                            this is for html code
            sum_pic_list: list each element includes name,num of pic, size of pic
                            this is for blog title
    """

    # make a folder to store picked pictures
    if not os.path.exists(picked_pic_folder):
        os.mkdir(picked_pic_folder)
    # get all picture folders
    all_file = os.listdir(folder_path)
    # scan the folder to find which one include .jpg files
    pic_info_list=[] #a list to store pic folder name , size and number
    sum_pic_list=[]
    beauty_count=0
    for parent, dirfile, picture_list in os.walk(folder_path):
        if parent.split('/')[-1] != picked_pic_folder:  # not scan picked_pic_folder
            if os.path.splitext(picture_list[0])[1] == '.jpg':
                beauty_count+=1 #count how many file have been scaned
                os.chdir(parent)  # get in the folder which include .jpg               
                pic_num=len(os.listdir(parent))         
                picked_pic_list = []  # create a list to store picked pictures
                # pick 4 length pictures into list
                for picture in picture_list:
                    img = Image.open(picture)
                    if img.size[0] > img.size[1] and len(picked_pic_list) < 4:
                        picked_pic_list.append(picture)
                rename_list=[]
                #while in picked picture list,copy and rename them to another folder
                for picked_pic in picked_pic_list: #for each picture in picked 4 pictures
                    newname = str(beauty_count)+'__' + picked_pic
                    shutil.copy(picked_pic, os.path.join(
                        folder_path, picked_pic_folder, newname))
                    rename_list.append(newname) 

                sum_pic_list.append(rename_list)       
                pic_info_list.append(parent.split('/')[-1]+'['+str(pic_num)+'P'+str(pic_num*4)+'M]')
    os.chdir(folder_path) #return to origin folder
    return pic_info_list,sum_pic_list


# step2: rezise picture
def resize_pic(pic_folder, width_new=1000,cut_height=30):
    """
  arg:
      pic_folder: str where the pic to store
      width_new: int disired width pix of each picture
  return:
      None
  """
    os.chdir(pic_folder)#enter pic folder
    pic_list = os.listdir(pic_folder)
    for picture in pic_list:
        img = Image.open(picture)
        (width, heigh) = img.size
        height_new=heigh*width_new/width
        out=img.resize((width_new,height_new),Image.ANTIALIAS)
        #crop watermark and store
        out.crop((0,0,width_new,height_new-cut_height)).save(picture)
    

#step3: #for each beauty, create html 
def create_html(pic_info,sum_pic,upload_path,yun_link=('1','2')):
    """create a templete html, and each created hmtl just copy and replace
    arg: 
        pic_info: str info of beauty's , pic size pic num 
        sum_pic: list each  name of 4 picture
        upload_path: website path to store pictures
        yun_link: tumple the fisrt element is baiduyun link,
                    the second element is code 
    """
    save_file=pic_info+'.txt'
    content="""
    <p>
    <img src="%s%s" style="" title="%s"/>
    </p>
    <p>
    <img src="%s%s" style="" title="%s"/>
    </p>
    <p>
    <img src="%s%s" style="" title="%s"/>
    </p>
    <p>
    <img src="%s%s" style="" title="%s"/>
    </p>
    <p>
    <span style="color: #FF0000; font-size: 24px;">link: 
    </span>
    <a href="%s" target="_blank" 
    style="font-size: 24px; text-decoration: underline;">
        <span style="font-size: 24px;">%s
        </span>
    </a> 
    <span style="font-size: 24px;">
        <span style="color: #FF0000; font-size: 24px;">code:
        </span>
        %s
    </span>
    </p>\n\n\n\n\n\n\n\n\n
    """%(upload_path,sum_pic[0],sum_pic[0],upload_path,sum_pic[1],sum_pic[1],
         upload_path,sum_pic[2],sum_pic[2],upload_path,sum_pic[3],sum_pic[3],
         yun_link[0],yun_link[0],yun_link[1])
    with open(save_file, 'w') as f:
        f.write(content)
        f.close()


if __name__ == '__main__':
    folder_path = os.getcwd()
    picked_pic_folder = 'picked_pic'
    pic_info_list,sum_pic_list=extract_picture(folder_path, picked_pic_folder)
    resize_pic(os.path.join(folder_path, picked_pic_folder), width_new=1000)
    os.chdir(folder_path) #change to original folder

    upload_path='http://piaoliangmm.cn/zb_users/upload/2016/11/'
    for index in range(len(pic_info_list)):
        create_html(pic_info_list[index], sum_pic_list[index],upload_path)


