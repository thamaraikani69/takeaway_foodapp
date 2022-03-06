import secrets
from datetime import date,datetime
from . models import *
from login.models import *
from login.serializers import *
from . serializers import *
import os

today=date.today()
timedate =datetime.now()

from PIL import Image

allowed_format = ["PNG","JPG","JPEG","JFIF"]
allowed_size = 2050000*5

def image_(image_upload,id,server_path,key):
    try:

        image_check=image_securty(image_upload)
        image_save=False 
        
        added_on=today
        lastchange=timedate
        if image_check == True:

            if key=="banner":
                banner_List=banner.objects.all()
                serializer=bannerSerializer(banner_List,many=True)
            elif key=="item":
                item_List=item.objects.all()
                serializer=itemSerializer(item_List,many=True)
            elif key=="dish_cat":
                dish_List=food_catagory.objects.all()
                serializer=foodcatSerializer(dish_List,many=True)
            elif key=="account_admin":
                admin_login_List=admin_login.objects.all()
                serializer=admin_loginSerializer(admin_login_List,many=True)
            elif key=="account_user":
                user_login_List=user_login.objects.all()
                serializer=user_loginSerializer(user_login_List,many=True)
            elif key=="company":
                company_List=company.objects.all()
                serializer=companySerializer(company_List,many=True)
            else:
                return {'message':'key Error'}
            hexa_check=serializer.data
            random_hex = secrets.token_hex(16)
            count=0
            while count<len(hexa_check):

                for i in hexa_check:
                    if key=="banner":
                        images=i['banner_image']
                    elif key=="item":
                        images=i['itemimage']
                    elif key=="dish_cat":
                        images=i['dish_image']
                    elif key=="company":
                        images=i['file']
                    elif key=="account_user":
                        images=i['picture']
                    elif key=="account_admin":
                        images=i['picture']
                    # else:
                    #      images=i['attachement']
                    f_ext = os.path.splitext(str(images))[0]

                    if f_ext==random_hex:
                        random_hex = secrets.token_hex(16)
                        count=0
                    else:
                        count+=1
            _, f_ext = os.path.splitext(str(image_upload))
            picture_fn = random_hex +f_ext

            
            image_save= save_image(picture_fn,image_upload,server_path)
            
            if image_save==True:
                try:
                    if key=="banner":
                        banner_update=banner.objects.filter(id=id).update(banner_image=picture_fn)
                        # banner_update.save()

                    elif key=="item":
                        item_update=item.objects.filter(id=id).update(itemimage=picture_fn)
                        # item_update.save()
                    elif key=="dish_cat":
                        dish_update=food_catagory.objects.filter(id=id).update(dish_image=picture_fn)
                    elif key=="company":
                        company_update=company.objects.filter(id=id).update(file=picture_fn)
                    elif key=="account_admin":
                        company_update=admin_login.objects.filter(id=id).update(picture=picture_fn)
                    elif key=="account_user":
                        company_update=user_login.objects.filter(id=id).update(picture=picture_fn)
            
                    return {"message":True}
                except Exception as e:
                    print('here',e)
                    return {"message":str(e)}
            else:
                return{"message":"something wrong"}
        else:
            return{"message":image_check}
    except Exception as e:
        return{"message":str(e)},400
    

def image_securty(img_upload):

    if img_upload==None:
        return ("empty file")
    else:
        filesize=len(img_upload.read())
        if not image_size(filesize):
            return ("File less than 10mb")

        if img_upload=="":
            return("image must have filename")

        if not allowed_image(img_upload):
            return('image has extention not allowed')
        else:
            return True

def allowed_image(filename):

    if not "." in str(filename):
        return False

    ext=str(filename).rsplit(".",1)[1]
    
    # if ext.upper() == "MP4":
    #     return True
    # else:
    #     if ext.upper() in allowed_format:
    #         return True
    #     else:
    #         return False
    if ext.upper() in allowed_format:
            return True
    else:
        return False

def image_size(filesize):
    
    if int(filesize) < int(allowed_size):
        return True
    else:
        return False

def save_image(picture_fn,image_upload,server_path):
    try:
        
        picture_path = os.path.join(server_path, picture_fn)
        output_size = (250, 250)
        
        i = Image.open(image_upload)
        
        if i.mode in ("RGBA", "P"):
            i = i.convert("RGB")
            # i.thumbnail(output_size, Image.ANTIALIAS)

        i.save(picture_path,quality=100)

        return True
    except:
       return False
    # finally:
    #     print("kani")
