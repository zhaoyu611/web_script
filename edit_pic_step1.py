#-*- coding : utf-8 -*-
import os
from PIL import Image
import shutil
import re
import numpy as np

def extract_picture(folder_path=os.getcwd(),picked_pic_folder='picked_pic'):
    if not os.path.exists(picked_pic_folder):
        os.mkdir(picked_pic_folder)
    all_file=os.listdir(folder_path)
    pic_info_list=[]
    sum_pic_list=[]
    beauty_count=0
    for parent,dirfile,picture_list in os.walk(folder_path):
        if parent.split('\\')[-1]==picked_pic_folder or \
            len(picture_list)==0 or picture_list[0].split('.')[-1]!='jpg':
            continue
        beauty_count+=1
        os.chdir(parent)
        parent_path=os.path.dirname(os.getcwd())
        beauty_name=parent_path.split('\\')[-1]
        beauty_name= beauty_name.replace(' ','_')
        pic_num=len(os.listdir(parent))
        picked_pic_list=[]
        for picture in picture_list:
            #confirm picture is .jpg, if not ,then del it
            if picture.split('.')[-1]!='jpg':
                os.remove(picture)
                continue
            img=Image.open(picture)
            if img.size[0]<img.size[1] and len(picked_pic_list)<4:
                picked_pic_list.append(picture)
            
            rename_list=[]
            for picked_pic in picked_pic_list:
                
                newname=str(beauty_name)+'__'+picked_pic
                shutil.copy(picked_pic, os.path.join(folder_path,picked_pic_folder,newname))
                rename_list.append(newname)  
        sum_pic_list.append(rename_list)
        pic_info_list.append(parent.split('\\')[-1]+'['+str(pic_num)+'P'+str(pic_num*4)+'M]')
        print "while extracting: done %s pictures" %(beauty_count)
    os.chdir(folder_path)
    return pic_info_list,sum_pic_list


def resize_pic(pic_folder,width_new=1000,cut_height=50):
    os.chdir(pic_folder)
    pic_list=os.listdir(pic_folder)
    for picture in pic_list:
        img=Image.open(picture)
        (width,heigh)=img.size
        height_new=heigh*width_new/width
        out=img.resize((width_new,height_new),Image.ANTIALIAS)
        out.crop((0,0,width_new,height_new-cut_height)).save(picture)


def create_html(pic_info,sum_pic,upload_path,yun_link):
    """create a templete html, and each created hmtl just copy and replace
    arg: 
        pic_info: str info of beauty's , pic size pic num 
        sum_pic: list each  name of 4 picture
        upload_path: website path to store pictures
        yun_link: tumple the fisrt element is baiduyun link,
                    the second element is code 
    """
    content=""" %s
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
    """%(pic_info,
         upload_path,sum_pic[0],sum_pic[0],upload_path,sum_pic[1],sum_pic[1],
         upload_path,sum_pic[2],sum_pic[2],upload_path,sum_pic[3],sum_pic[3],
         yun_link[0],yun_link[0],yun_link[1])


    with open('content.txt', 'a') as f:
        f.write(content)
        f.close()


def yun_link(file_name='yun.txt'):
    yun_list=[]
    with open(file_name,'r') as f:
        lines=f.readlines()
        for line in lines:
            regular=re.findall(':(.*?) code: (.*)',line)
            yun_list.append(regular[0])
    f.close()
    return yun_list




if __name__=='__main__':
    folder_path=os.getcwd()
    picked_pic_folder='picked_pic'
    pic_info_list,sum_pic_list=extract_picture(folder_path,picked_pic_folder)
    #save pic info
    np.save('pic_info_list.npy',pic_info_list)
    np.save('sum_pic_list.npy',sum_pic_list)
    print "finished picking and summarizing info"
    resize_pic(os.path.join(folder_path,picked_pic_folder),width_new=1000)
    print "finished resizing pictures"

