#-*- coding : utf-8 -*-
import os
from PIL import Image
import shutil
import re
import numpy as np


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
            assert len(regular)!=0, "You should change:  lianjie: to link: , mima: to code: "
            yun_list.append(regular[0])
    f.close()
    return yun_list




if __name__=='__main__':
    pic_info_list=np.load('pic_info_list.npy').tolist()
    sum_pic_list=np.load('sum_pic_list.npy').tolist()
    os.remove('pic_info_list.npy')
    os.remove('sum_pic_list.npy')
    upload_path='http://piaoliangmm.cn/zb_users/upload/2016/11/'
    yun_file='yun.txt'
    yun_list=yun_link(yun_file)
    assert len(yun_list)==len(pic_info_list), "you should check weather two txt len euqal"
    for index in range(len(pic_info_list)):
        create_html(pic_info_list[index], sum_pic_list[index], upload_path,yun_list[index])

