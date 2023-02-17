import datetime
import os
import mysql.connector
from PIL import Image,ImageDraw,ImageFont
from app import settings
import qrcode
import qrcode.image.svg

# hostdb = '139.162.28.194'
hostdb = 'localhost'

passworddb = 'Chino002'

databasedb = 'pedigree_chicken'

userdb = 'root'


# define a DB class
class DB:
    # define a mydb variable that will store a connection object
    mydb = None

    # define a connect function that will establish a connection with the database
    def connect(self, dbname=databasedb):
        # establish a connection using mysql.connector
        self.mydb = mysql.connector.connect(
            host=hostdb,
            user=userdb,
            password=passworddb,
            database=dbname,
            port='3306'
        )

    # define a function to execute a query with an image as an argument
    def query_with_image(self, query, args):
        # establish a connection
        self.connect()
        # create a cursor object
        cursor = self.mydb.cursor(buffered=True)
        # execute the query with the image argument
        result = cursor.execute(query, args)
        # commit the changes to the database
        self.mydb.commit()

    # define a function to execute a query
    def query(self, task):
        try:
            # try to execute the query with an existing connection
            self.connect()
            mycursor = self.mydb.cursor(buffered=True)
            mycursor.execute(task)
        except Exception as E:
            # if there's an error, establish a new connection and execute the query
            self.connect()
            mycursor = self.mydb.cursor(buffered=True)
            mycursor.execute(task)
        # return the cursor object
        return mycursor

    # define a function to execute a query and return the results
    def check(self, task, db='muslin'):
        try:
            # try to execute the query with an existing connection
            self.connect(dbname=db)
            mycursor = self.mydb.cursor(buffered=True)
            mycursor.execute(task)
        except Exception as E:
            # if there's an error, establish a new connection and execute the query
            self.connect(dbname=db)
            mycursor = self.mydb.cursor(buffered=True)
            mycursor.execute(task)
        # return the results of the query
        return mycursor.fetchall()

    # define a function to execute a custom query on a specific database
    def query_custom(self, task, db):
        try:
            # try to execute the query with an existing connection
            self.connect(dbname=db)
            mycursor = self.mydb.cursor(buffered=True)
            mycursor.execute(task)
        except Exception as E:
            # if there's an error, establish a new connection and execute the query
            self.connect(dbname=db)
            mycursor = self.mydb.cursor(buffered=True)
            mycursor.execute(task)
        # return the cursor object
        return mycursor

    # define a function to execute a query and commit the changes to the database
    def query_commit(self, task):
        try:
            # try to execute the query with an existing connection
            self.connect()
            mycursor = self.mydb.cursor(buffered=True)
            mycursor.execute(task)
            # commit the changes to the database
            self.mydb.commit()
        except Exception as E:
            # if there's an error, establish a new connection and execute the query
            self.connect()
            mycursor = self.mydb.cursor(buffered=True)
            mycursor.execute(task)
            # commit the changes to the database
            self.mydb.commit()
        # return the cursor object
        return mycursor


db = DB()


def write_pdf(id):
    qr_path = generate_qr(f'http://127.0.0.1:8000/share/{id}',id)
    template_path = f'{settings.MEDIA_ROOT}\pedigree_templates.png'
    task = f"""
    select 
    chicken.path_img, 
    c1.path_img as M_name,
    c2.path_img as MM_name,
    c3.path_img as MMF_name,
    c4.path_img as MMM_name,
    c5.path_img as MFF_name,
    c6.path_img as MFM_name,
    c7.path_img as MF_name,
    c8.path_img as F_name,
    c9.path_img as FF_name,
    c10.path_img as FM_name,
    c11.path_img as FFF_name,
    c12.path_img as FFM_name,
    c13.path_img as FMM_name,
    c14.path_img as FMF_name
    from chicken
    inner join chicken_map on chicken_map.chicken_id = chicken.id
    left join chicken as c1 on chicken_map.chicken_M = c1.id
    left join chicken as c2 on chicken_map.chicken_MM = c2.id
    left join chicken as c3 on chicken_map.chicken_MMF = c3.id
    left join chicken as c4 on chicken_map.chicken_MMM = c4.id
    left join chicken as c5 on chicken_map.chicken_MFF = c5.id
    left join chicken as c6 on chicken_map.chicken_MFM = c6.id
    left join chicken as c7 on chicken_map.chicken_MF = c7.id
    left join chicken as c8 on chicken_map.chicken_F = c8.id
    left join chicken as c9 on chicken_map.chicken_FF = c9.id
    left join chicken as c10 on chicken_map.chicken_FM = c10.id
    left join chicken as c11 on chicken_map.chicken_FFF = c11.id
    left join chicken as c12 on chicken_map.chicken_FFM = c12.id
    left join chicken as c13 on chicken_map.chicken_FMM = c13.id
    left join chicken as c14 on chicken_map.chicken_FMF = c14.id
    where chicken.id = '{id}';
    """
    result = db.query_custom(task,'pedigree_chicken')
    result = list(result.fetchall())[0]
    result = list(result)
    for i in range(len(result)):
        if result[i]:
            result[i] = result[i][1:]
    mainpath, Mpath, MMpath, MMFpath, MMMpath, MFFpath, MFMpath, MFpath, Fpath, FFpath, FMpath, FFFpath, FFMpath, FMMpath, FMFpath = result
    task = f"""
    select 
    chicken.name, 
    chicken.chicken_code, 
    c15.value, 
    chicken.reg_no, 
    chicken.birthday, 
    chicken.breeder, 
    chicken.certificste_issued, 
    chicken.farm_name, 
    c1.name as M_name,
    c1.chicken_code as M_code,
    c2.name as MM_name,
    c2.chicken_code as MM_code,
    c3.name as MMF_name,
    c3.chicken_code as MMF_code,
    c4.name as MMM_name,
    c4.chicken_code as MMM_code,
    c5.name as MFF_name,
    c5.chicken_code as MFF_code,
    c6.name as MFM_name,
    c6.chicken_code as MFM_code,
    c7.name as MF_name,
    c7.chicken_code as MF_code,
    c8.name as F_name,
    c8.chicken_code as F_code,
    c9.name as FF_name,
    c9.chicken_code as FF_code,
    c10.name as FM_name,
    c10.chicken_code as FM_code,
    c11.name as FFF_name,
    c11.chicken_code as FFF_code,
    c12.name as FFM_name,
    c12.chicken_code as FFM_code,
    c13.name as FMM_name,
    c13.chicken_code as FMM_code,
    c14.name as FMF_name,
    c14.chicken_code as FMF_code
    from chicken
    inner join chicken_map on chicken_map.chicken_id = chicken.id
    left join chicken as c1 on chicken_map.chicken_M = c1.id
    left join chicken as c2 on chicken_map.chicken_MM = c2.id
    left join chicken as c3 on chicken_map.chicken_MMF = c3.id
    left join chicken as c4 on chicken_map.chicken_MMM = c4.id
    left join chicken as c5 on chicken_map.chicken_MFF = c5.id
    left join chicken as c6 on chicken_map.chicken_MFM = c6.id
    left join chicken as c7 on chicken_map.chicken_MF = c7.id
    left join chicken as c8 on chicken_map.chicken_F = c8.id
    left join chicken as c9 on chicken_map.chicken_FF = c9.id
    left join chicken as c10 on chicken_map.chicken_FM = c10.id
    left join chicken as c11 on chicken_map.chicken_FFF = c11.id
    left join chicken as c12 on chicken_map.chicken_FFM = c12.id
    left join chicken as c13 on chicken_map.chicken_FMM = c13.id
    left join chicken as c14 on chicken_map.chicken_FMF = c14.id
    left join sex_chicken as c15 on chicken.sex_id = c15.id
    where chicken.id = '{id}';
    """
    result = db.query_custom(task,'pedigree_chicken')
    result = list(result.fetchall())[0]
    result = list(result)
    for i in range(len(result)):
        if not result[i]:
            result[i] = '-'
    name, chicken_code, value, reg_no, birthday, breeder, certificste_issued, farm_name,M_name, M_code, MM_name, MM_code, MMF_name, MMF_code, MMM_name, MMM_code, MFF_name, MFF_code, MFM_name, MFM_code, MF_name, MF_code, F_name, F_code, FF_name, FF_code, FM_name, FM_code, FFF_name, FFF_code, FFM_name, FFM_code, FMM_name, FMM_code, FMF_name, FMF_code = result
    if mainpath:
        main_chicken = Image.open(mainpath)
        main_chicken = main_chicken.resize((1500,2130), Image.LANCZOS)

    # M - F
    if Mpath:
        M_chicken = Image.open(Mpath)
        M_chicken = M_chicken.resize((714,888), Image.LANCZOS)
    if Fpath:
        F_chicken = Image.open(Fpath)
        F_chicken = F_chicken.resize((714,888), Image.LANCZOS)

    # MM - FF
    if MMpath:
        MM_chicken = Image.open(MMpath)
        MM_chicken = MM_chicken.resize((594,755), Image.LANCZOS)
    if FFpath:
        FF_chicken = Image.open(FFpath)
        FF_chicken = FF_chicken.resize((594,755), Image.LANCZOS)
    if MFpath:
        MF_chicken = Image.open(MFpath)
        MF_chicken = MF_chicken.resize((594,755), Image.LANCZOS)
    if FMpath:
        FM_chicken = Image.open(FMpath)
        FM_chicken = FM_chicken.resize((594,755), Image.LANCZOS)
    # MMM
    if MMMpath:
        MMM_chicken = Image.open(MMMpath)
        MMM_chicken = MMM_chicken.resize((314,400), Image.LANCZOS)
    if MFMpath:
        MFM_chicken = Image.open(MFMpath)
        MFM_chicken = MFM_chicken.resize((314,400), Image.LANCZOS)
    if MMFpath:
        MMF_chicken = Image.open(MMFpath)
        MMF_chicken = MMF_chicken.resize((314,400), Image.LANCZOS)
    if MFFpath:
        MFF_chicken = Image.open(MFFpath)
        MFF_chicken = MFF_chicken.resize((314,400), Image.LANCZOS)
    # FFF
    if FFFpath:
        FFF_chicken = Image.open(FFFpath)
        FFF_chicken = FFF_chicken.resize((314,400), Image.LANCZOS)
    if FFMpath:
        FFM_chicken = Image.open(FFMpath)
        FFM_chicken = FFM_chicken.resize((314,400), Image.LANCZOS)
    if FMFpath:
        FMF_chicken = Image.open(FMFpath)
        FMF_chicken = FMF_chicken.resize((314,400), Image.LANCZOS)
    if FMMpath:
        FMM_chicken = Image.open(FMMpath)
        FMM_chicken = FMM_chicken.resize((314,400), Image.LANCZOS)
    
    qr_code = Image.open(qr_path)
    qr_code = qr_code.resize((500,500), Image.LANCZOS)

    my_image = Image.open(template_path)
    if my_image.mode != 'RGB':
        my_image = my_image.convert("RGB")
    bias = 30
    bias_sm = 50
    title_font = ImageFont.truetype('static/font/ChakraPetch-Light.ttf', 100)
    small_font = ImageFont.truetype('static/font/ChakraPetch-Light.ttf', 70)
    image_editable = ImageDraw.Draw(my_image)
    # image_editable.text((x, y), title_text, font=title_font, fill=fillcolor)

    # ชื่อไก่
    image_editable.text((620,850 + bias), name,font=title_font,fill='black')
    # รหัสไก่
    image_editable.text((985,1050 + bias), chicken_code,font=title_font,fill='black')
    # เพศไก่
    image_editable.text((1995,850 + bias), value,font=title_font,fill='black')
    # กิ๊บปีก
    image_editable.text((2090,1050 + bias), reg_no,font=title_font,fill='black')
    # วันเกิด
    image_editable.text((3500,850 + bias), str(birthday),font=title_font,fill='black')
    # วันออกพันธ์
    image_editable.text((4000,1050 + bias), str(certificste_issued),font=title_font,fill='black')
    # ผู้ปรับปรุงพันธ์
    image_editable.text((5425,850 + bias), breeder,font=title_font,fill='black')
    # เจ้าของปัจจุบัน
    image_editable.text((5425,1050 + bias), farm_name,font=title_font,fill='black')
    # F-name,code
    image_editable.text((2758,1937 + bias_sm), F_name,font=small_font,fill='black')
    image_editable.text((2758,2090 + bias_sm), F_code,font=small_font,fill='black')
    # M-name,code
    image_editable.text((2758,3559 + bias_sm), M_name,font=small_font,fill='black')
    image_editable.text((2758,3723 + bias_sm), M_code,font=small_font,fill='black')

    # FF-name,code
    image_editable.text((4474,1484 + bias_sm), FF_name,font=small_font,fill='black')
    image_editable.text((4474,1648 + bias_sm), FF_code,font=small_font,fill='black')
    # FM-name,code
    image_editable.text((4474,2314 + bias_sm), FM_name,font=small_font,fill='black')
    image_editable.text((4474,2480 + bias_sm), FM_code,font=small_font,fill='black')
    # MF-name,code
    image_editable.text((4474,3096 + bias_sm), MF_name,font=small_font,fill='black')
    image_editable.text((4474,3256 + bias_sm), MF_code,font=small_font,fill='black')
    # MM-name,code
    image_editable.text((4474,3926 + bias_sm), MM_name,font=small_font,fill='black')
    image_editable.text((4474,4090 + bias_sm), MM_code,font=small_font,fill='black')
    
    # FFF-name,code
    image_editable.text((5936,1318), FFF_name,font=small_font,fill='black')
    image_editable.text((5936,1486), FFF_code,font=small_font,fill='black')
    # FFM-name,code
    image_editable.text((5936,1726), FFM_name,font=small_font,fill='black')
    image_editable.text((5936,1876), FFM_code,font=small_font,fill='black')
    # FMF-name,code
    image_editable.text((5936,2146 + bias_sm), FMF_name,font=small_font,fill='black')
    image_editable.text((5936,2296 + bias_sm), FMF_code,font=small_font,fill='black')
    # FMM-name,code
    image_editable.text((5936,2542 + bias_sm), FMM_name,font=small_font,fill='black')
    image_editable.text((5936,2668 + bias_sm), FMM_code,font=small_font,fill='black')

    # MFF-name,code
    image_editable.text((5936,2938 + bias_sm), MFF_name,font=small_font,fill='black')
    image_editable.text((5936,3082 + bias_sm), MFF_code,font=small_font,fill='black')
    # MFM-name,code
    image_editable.text((5936,3316 + bias_sm), MFM_name,font=small_font,fill='black')
    image_editable.text((5936,3465 + bias_sm), MFM_code,font=small_font,fill='black')
    # MMF-name,code
    image_editable.text((5936,3753 + bias_sm),MMF_name,font=small_font,fill='black')
    image_editable.text((5936,3903 + bias_sm), MMF_code,font=small_font,fill='black')
    # MMM-name,code
    image_editable.text((5936,4155 + bias_sm), MMM_name,font=small_font,fill='black')
    image_editable.text((5936,4300 + bias_sm), MMM_code,font=small_font,fill='black')

    # MAIN
    if mainpath:
        my_image.paste(main_chicken,(265,1810))
    # M - F
    if Fpath:
        my_image.paste(F_chicken,(1810,1672))
    if Mpath:
        my_image.paste(M_chicken,(1810,3175))
    # MM - MF
    if FFpath:
        my_image.paste(FF_chicken,(3668,1239))
    if FMpath:
        my_image.paste(FM_chicken,(3668,2060))
    if MFpath:
        my_image.paste(MF_chicken,(3668,2890))
    if MMpath:
        my_image.paste(MM_chicken,(3668,3720))
    # MMM - FFF
    if FFFpath:
        my_image.paste(FFF_chicken,(5410,1230))
    if FFMpath:
        my_image.paste(FFM_chicken,(5410,1647))
    if FMFpath:
        my_image.paste(FMF_chicken,(5410,2059))
    if FMMpath:
        my_image.paste(FMM_chicken,(5410,2471))
    if MFFpath:
        my_image.paste(MFF_chicken,(5410,2883))
    if MFMpath:
        my_image.paste(MFM_chicken,(5410,3295))
    if MMFpath:
        my_image.paste(MMF_chicken,(5410,3717))
    if MMMpath:
        my_image.paste(MMM_chicken,(5410,4127))

    #QR CODE
    my_image.paste(qr_code,(5200,328))

    my_image.save(f"{settings.MEDIA_ROOT}/{id}.pdf")
    return f"{settings.MEDIA_ROOT}/{id}.pdf"

class DictAsObject:
    def __init__(self, dictionary):
        self.__dict__ = dictionary

def get_image_folder(id):
    task = db.query(f'select path_img from chicken where id = {id}')
    orig_path = (list(task.fetchone())[0])
    os.remove(os.path.join(settings.BASE_DIR,orig_path[1:]))

    # Extract the date parts from the original path
    new_path = orig_path.split('/media/')[1]
    # Construct the new path using the date parts and the desired directory structure
    return new_path

def get_date():
    today = datetime.date.today()
    return [today.year, today.month, today.day]

def prepare_folder_image():
    year,month,day = get_date()
    os.makedirs(os.path.join(settings.MEDIA_ROOT,str(year),f"{month:02d}",f"{day:02d}"),exist_ok=True)
    return f"{str(year)}/{month:02d}/{day:02d}/"

def get_last_id():
    mycursor = db.query("SELECT max(id) from chicken")
    result = mycursor.fetchone()
    first_table_id = result[0]
    return first_table_id

def generate_qr(url,id):
    img = qrcode.make(url)
    img.save(f'{id}.png')
    return f'{id}.png'