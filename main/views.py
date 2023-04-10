from django.core.paginator import Paginator
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.shortcuts import render,redirect
from django.http import HttpResponse, Http404
from app import settings
from function import db, get_image_folder, get_last_id, prepare_folder_image,write_pdf,DictAsObject
import os,json
# Create your views here.

def dashboard(req):
    task = 'SELECT COUNT(*), COUNT(CASE WHEN sex_id = 1 THEN 1 END), COUNT(CASE WHEN sex_id = 2 THEN 1 END) FROM chicken'
    result = db.query(task)
    result= list(result.fetchone())
    context = {
        "object":result
    }
    return render(req,'dashboard.html',context=context)

def insert(req):
    if req.method == 'GET':
        context = {}

        task = 'select chicken.id,name,reg_no from chicken inner join chicken_map on chicken_map.chicken_id = chicken.id where sex_id = 1'
        result = db.query(task)
        result = list(result.fetchall())
        f_name_list = result
        context['f_list']=f_name_list

        task = 'select chicken.id,name,reg_no from chicken inner join chicken_map on chicken_map.chicken_id = chicken.id where sex_id = 2'
        result = db.query(task)
        result = list(result.fetchall())
        m_name_list = result
        context['m_list']= m_name_list
        task = 'select chicken.id,COALESCE(path_img,"/media/default.png"),reg_no,name from chicken'
        result = db.query(task)
        result = list(result.fetchall())
        image_dict,reg_no_dict,name_dict = {},{},{}
        for i in result:
            image_dict[i[0]] = i[1]
            reg_no_dict[i[0]] = i[2]
            name_dict[i[0]] = i[3]
        context['image_dict'] = json.dumps(image_dict)
        context['reg_no_dict'] = json.dumps(reg_no_dict)
        context['name_dict'] = json.dumps(name_dict)
        f_id,m_id = {},{}
        task = 'select chicken_id,chicken_M,chicken_F from chicken_map'
        result = db.query(task)
        result = list(result.fetchall())
        for i in result:
            f_id[i[0]] = i[2]
            m_id[i[0]] = i[1]

        context['f_id'] = json.dumps(f_id)
        context['m_id'] = json.dumps(m_id)
        return render(req,'insert.html',context=context)
    else:
        image_task = "NULL"
        try:
            myfile = req.FILES.getlist('main_image')
            for i in myfile:
                folder_image = prepare_folder_image()
                print(folder_image,i.name)
                fs = FileSystemStorage(base_url=settings.BASE_DIR)
                filename = fs.save(os.path.join(folder_image,i.name), i)
                image_task = f' "/media/{filename}"'
        except Exception as E:
            print(E)
        if req.POST.get("breeder"):
            breeder = f"'{req.POST.get('breeder')}'"
        else:
            breeder = "NULL"
        # chicken task insert
        task = f'''insert into chicken values (0, "{req.POST.get("name")}", "{req.POST.get("farm_name")}", "{req.POST.get("reg_no")}", 
        "{req.POST.get("sex_id")}", "{req.POST.get("birthday")}", "{req.POST.get("reg_no")}", {breeder}, 
        "{req.POST.get("certificste_issued")}", {image_task}, null, null)'''
        db.query_commit(task)

        # chicken map insert
        keys = req.POST.keys()
        map_dict = {}
        for i in keys:
            if str(i).endswith('_id'):
                if not req.POST.get(i):
                    map_dict[i] = 'NULL'
                else:
                    map_dict[i] = f'"{req.POST.get(i)}"'

        map = DictAsObject(map_dict)
        task = f"""
        insert into chicken_map values 
        (0, {get_last_id()}, {map.m_id}, {map.mm_id}, {map.mf_id}, {map.mmm_id}, {map.mmf_id},
          {map.mff_id}, {map.mfm_id}, {map.f_id}, {map.ff_id}, {map.fm_id}, {map.fff_id},
        {map.ffm_id}, {map.fmm_id}, {map.fmf_id})
        """
        db.query_commit(task)
        # db.query_commit(ta.sk)
        messages.success(req,'เพิ่มสำเร็จ')
        return redirect('main:list')


def edit(req,id):
    if req.method == 'GET':
        task = f"""
        select 
        COALESCE(chicken.path_img,'/media/default.png'), 
        chicken.name, 
        chicken.reg_no, 
        c15.value, 
        chicken.reg_no, 
        chicken.birthday, 
        chicken.breeder, 
        chicken.certificste_issued, 
        chicken.farm_name, 
        c1.name as M_name,
        c1.reg_no as M_code,
        c2.name as MM_name,
        c2.reg_no as MM_code,
        c3.name as MMF_name,
        c3.reg_no as MMF_code,
        c4.name as MMM_name,
        c4.reg_no as MMM_code,
        c5.name as MFF_name,
        c5.reg_no as MFF_code,
        c6.name as MFM_name,
        c6.reg_no as MFM_code,
        c7.name as MF_name,
        c7.reg_no as MF_code,
        c8.name as F_name,
        c8.reg_no as F_code,
        c9.name as FF_name,
        c9.reg_no as FF_code,
        c10.name as FM_name,
        c10.reg_no as FM_code,
        c11.name as FFF_name,
        c11.reg_no as FFF_code,
        c12.name as FFM_name,
        c12.reg_no as FFM_code,
        c13.name as FMM_name,
        c13.reg_no as FMM_code,
        c14.name as FMF_name,
        c14.reg_no as FMF_code,
        COALESCE(c1.path_img,'/media/default.png') as c1_img,
        COALESCE(c2.path_img,'/media/default.png') as c2_img,
        COALESCE(c3.path_img,'/media/default.png') as c3_img,
        COALESCE(c4.path_img,'/media/default.png') as c4_img,
        COALESCE(c5.path_img,'/media/default.png') as c5_img,
        COALESCE(c6.path_img,'/media/default.png') as c6_img,
        COALESCE(c7.path_img,'/media/default.png') as c7_img,
        COALESCE(c8.path_img,'/media/default.png') as c8_img,
        COALESCE(c9.path_img,'/media/default.png') as c9_img,
        COALESCE(c10.path_img,'/media/default.png') as c10_img,
        COALESCE(c11.path_img,'/media/default.png') as c11_img,
        COALESCE(c12.path_img,'/media/default.png') as c12_img,
        COALESCE(c13.path_img,'/media/default.png') as c13_img,
        COALESCE(c14.path_img,'/media/default.png') as c14_img
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
                result[i] = ''
        path_img,name, reg_no, value, reg_no, birthday, breeder, certificste_issued, farm_name, M_name, M_code, MM_name, MM_code, MMF_name, MMF_code, MMM_name, MMM_code, MFF_name, MFF_code, MFM_name, MFM_code, MF_name, MF_code, F_name, F_code, FF_name, FF_code, FM_name, FM_code, FFF_name, FFF_code, FFM_name, FFM_code, FMM_name, FMM_code, FMF_name, FMF_code, c1_img, c2_img, c3_img, c4_img, c5_img, c6_img, c7_img, c8_img, c9_img, c10_img, c11_img, c12_img, c13_img, c14_img = result    
        context = {
        "path_img":path_img,
        "name":name,
        "reg_no":reg_no,
        "value":value,
        "reg_no":reg_no,
        "birthday":str(birthday),
        "breeder":breeder,
        "certificste_issued":str(certificste_issued),
        "farm_name":farm_name,
        "M_name":M_name,
        "M_code":M_code,
        "MM_name":MM_name,
        "MM_code":MM_code,
        "MMF_name":MMF_name,
        "MMF_code":MMF_code,
        "MMM_name":MMM_name,
        "MMM_code":MMM_code,
        "MFF_name":MFF_name,
        "MFF_code":MFF_code,
        "MFM_name":MFM_name,
        "MFM_code":MFM_code,
        "MF_name":MF_name,
        "MF_code":MF_code,
        "F_name":F_name,
        "F_code":F_code,
        "FF_name":FF_name,
        "FF_code":FF_code,
        "FM_name":FM_name,
        "FM_code":FM_code,
        "FFF_name":FFF_name,
        "FFF_code":FFF_code,
        "FFM_name":FFM_name,
        "FFM_code":FFM_code,
        "FMM_name":FMM_name,
        "FMM_code":FMM_code,
        "FMF_name":FMF_name,
        "FMF_code":FMF_code,
        "chicken_M":c1_img,
        "chicken_MM":c2_img,    
        "chicken_MMF":c3_img,    
        "chicken_MMM":c4_img,    
        "chicken_MFF":c5_img,    
        "chicken_MFM":c6_img,    
        "chicken_MF":c7_img,    
        "chicken_F":c8_img,    
        "chicken_FF":c9_img,    
        "chicken_FM": c10_img,    
        "chicken_FFF": c11_img,    
        "chicken_FFM": c12_img,    
        "chicken_FMM": c13_img,    
        "chicken_FMF": c14_img
        }
        task = 'select chicken.id,name,reg_no from chicken inner join chicken_map on chicken_map.chicken_id = chicken.id where sex_id = 1'
        result = db.query(task)
        result = list(result.fetchall())
        f_name_list = result
        context['f_list']=f_name_list

        task = 'select chicken.id,name,reg_no from chicken inner join chicken_map on chicken_map.chicken_id = chicken.id where sex_id = 2'
        result = db.query(task)
        result = list(result.fetchall())
        m_name_list = result
        context['m_list']= m_name_list

        task = 'select chicken.id,COALESCE(path_img,"/media/default.png"),reg_no,name from chicken'
        result = db.query(task)
        result = list(result.fetchall())
        image_dict,reg_no_dict,name_dict = {},{},{}
        for i in result:
            image_dict[i[0]] = i[1]
            reg_no_dict[i[0]] = i[2]
            name_dict[i[0]] = i[3]
        context['image_dict'] = json.dumps(image_dict)
        context['reg_no_dict'] = json.dumps(reg_no_dict)
        context['name_dict'] = json.dumps(name_dict)
        f_id,m_id = {},{}
        task = 'select chicken_id,chicken_M,chicken_F from chicken_map'
        result = db.query(task)
        result = list(result.fetchall())
        for i in result:
            f_id[i[0]] = i[2]
            m_id[i[0]] = i[1]

        context['f_id'] = json.dumps(f_id)
        context['m_id'] = json.dumps(m_id)

        return render(req,'edit.html',context=context)
    else:
        # file_keys = req.FILES.keys()
        try:
            if req.FILES['main_image']:
                image_path = get_image_folder(id)
                myfile = req.FILES.getlist('main_image')
                for i in myfile:
                    fs = FileSystemStorage(base_url=settings.BASE_DIR)
                    filename = fs.save(image_path, i)
        except Exception as e:
            print(e)
        sex_task = ''
        if req.POST.get('sex_id'):
            sex_task = f",sex_id = '{req.POST.get('sex_id')}'"
        task = f"""
        update chicken set name = '{req.POST.get('name')}',reg_no = '{req.POST.get('reg_no')}',
        breeder = '{req.POST.get('breeder')}',birthday = '{req.POST.get('birthday')}',
        certificste_issued = '{req.POST.get('certificste_issued')}',farm_name = '{req.POST.get('farm_name')}',
        chicken_code = '{req.POST.get('reg_no')}' {sex_task}
        where id = {id}
        """
        db.query_commit(task)
        messages.success(req,'แก้ไขสำเร็จ ... ')
        return redirect('main:list')

def sharePage(req,id):
    if req.method == 'GET':
        task = f"""
        select 
        COALESCE(chicken.path_img,'/media/default.png'), 
        chicken.name, 
        chicken.reg_no, 
        c15.value, 
        chicken.reg_no, 
        chicken.birthday, 
        chicken.breeder, 
        chicken.certificste_issued, 
        chicken.farm_name, 
        c1.name as M_name,
        c1.reg_no as M_code,
        c2.name as MM_name,
        c2.reg_no as MM_code,
        c3.name as MMF_name,
        c3.reg_no as MMF_code,
        c4.name as MMM_name,
        c4.reg_no as MMM_code,
        c5.name as MFF_name,
        c5.reg_no as MFF_code,
        c6.name as MFM_name,
        c6.reg_no as MFM_code,
        c7.name as MF_name,
        c7.reg_no as MF_code,
        c8.name as F_name,
        c8.reg_no as F_code,
        c9.name as FF_name,
        c9.reg_no as FF_code,
        c10.name as FM_name,
        c10.reg_no as FM_code,
        c11.name as FFF_name,
        c11.reg_no as FFF_code,
        c12.name as FFM_name,
        c12.reg_no as FFM_code,
        c13.name as FMM_name,
        c13.reg_no as FMM_code,
        c14.name as FMF_name,
        c14.reg_no as FMF_code,
        COALESCE(c1.path_img,'/media/default.png') as c1_img,
        COALESCE(c2.path_img,'/media/default.png') as c2_img,
        COALESCE(c3.path_img,'/media/default.png') as c3_img,
        COALESCE(c4.path_img,'/media/default.png') as c4_img,
        COALESCE(c5.path_img,'/media/default.png') as c5_img,
        COALESCE(c6.path_img,'/media/default.png') as c6_img,
        COALESCE(c7.path_img,'/media/default.png') as c7_img,
        COALESCE(c8.path_img,'/media/default.png') as c8_img,
        COALESCE(c9.path_img,'/media/default.png') as c9_img,
        COALESCE(c10.path_img,'/media/default.png') as c10_img,
        COALESCE(c11.path_img,'/media/default.png') as c11_img,
        COALESCE(c12.path_img,'/media/default.png') as c12_img,
        COALESCE(c13.path_img,'/media/default.png') as c13_img,
        COALESCE(c14.path_img,'/media/default.png') as c14_img
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
                result[i] = ''
        path_img,name, reg_no, value, reg_no, birthday, breeder, certificste_issued, farm_name, M_name, M_code, MM_name, MM_code, MMF_name, MMF_code, MMM_name, MMM_code, MFF_name, MFF_code, MFM_name, MFM_code, MF_name, MF_code, F_name, F_code, FF_name, FF_code, FM_name, FM_code, FFF_name, FFF_code, FFM_name, FFM_code, FMM_name, FMM_code, FMF_name, FMF_code, c1_img, c2_img, c3_img, c4_img, c5_img, c6_img, c7_img, c8_img, c9_img, c10_img, c11_img, c12_img, c13_img, c14_img = result    
        context = {
        "path_img":path_img,
        "name":name,
        "reg_no":reg_no,
        "value":value,
        "reg_no":reg_no,
        "birthday":str(birthday),
        "breeder":breeder,
        "certificste_issued":str(certificste_issued),
        "farm_name":farm_name,
        "M_name":M_name,
        "M_code":M_code,
        "MM_name":MM_name,
        "MM_code":MM_code,
        "MMF_name":MMF_name,
        "MMF_code":MMF_code,
        "MMM_name":MMM_name,
        "MMM_code":MMM_code,
        "MFF_name":MFF_name,
        "MFF_code":MFF_code,
        "MFM_name":MFM_name,
        "MFM_code":MFM_code,
        "MF_name":MF_name,
        "MF_code":MF_code,
        "F_name":F_name,
        "F_code":F_code,
        "FF_name":FF_name,
        "FF_code":FF_code,
        "FM_name":FM_name,
        "FM_code":FM_code,
        "FFF_name":FFF_name,
        "FFF_code":FFF_code,
        "FFM_name":FFM_name,
        "FFM_code":FFM_code,
        "FMM_name":FMM_name,
        "FMM_code":FMM_code,
        "FMF_name":FMF_name,
        "FMF_code":FMF_code,
        "chicken_M":c1_img,
        "chicken_MM":c2_img,    
        "chicken_MMF":c3_img,    
        "chicken_MMM":c4_img,    
        "chicken_MFF":c5_img,    
        "chicken_MFM":c6_img,    
        "chicken_MF":c7_img,    
        "chicken_F":c8_img,    
        "chicken_FF":c9_img,    
        "chicken_FM": c10_img,    
        "chicken_FFF": c11_img,    
        "chicken_FFM": c12_img,    
        "chicken_FMM": c13_img,    
        "chicken_FMF": c14_img
        }

        return render(req,'share.html',context=context)

def deleteId(req,id):
    task = f'delete from chicken where id = {id}'
    db.query_commit(task)
    task = f'delete from chicken_map where chicken_id = {id}'
    db.query_commit(task)
    messages.success(req,'ลบสำเร็จ ... ')
    return redirect('main:list')

def listPage(req):
    id = req.GET.get('id')
    if not id:
        id = ''
    task = f'''select chicken.id,name,reg_no,c1.value as sex from chicken
    left join sex_chicken as c1 on chicken.sex_id = c1.id where reg_no like "%{id}%" or name like "%{id}%" or chicken_code like "%{id}%"
    limit 1000;'''
    print(task)
    result = db.query_custom(task,'pedigree_chicken').fetchall()
    # result = list(result.fetchall())
    context = {
    }
    # Define the number of items per page
    items_per_page = 10

    # Create a Paginator object
    paginator = Paginator(result, items_per_page)

    # Get the requested page number from the URL parameters
    page_number = req.GET.get('page')

    # Get the requested page of data
    page_obj = paginator.get_page(page_number)
    context['page_obj'] = page_obj
    return render(req,'list.html',context=context)

def view_file(req,id):
    pdf = write_pdf(id)
    return redirect(f'/media/{id}.pdf')

def open_file(request, id):
    path = write_pdf(id)
    if os.path.exists(path):
        with open(path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
            response['Content-Disposition'] = 'inline; filename=' + os.path.basename(path)
            return response
    raise Http404