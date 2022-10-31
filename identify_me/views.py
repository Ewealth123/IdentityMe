from django.shortcuts import redirect, render,  get_object_or_404
from django.conf import settings
from django.http.request import  HttpRequest
from django.http.response import HttpResponse
from django.contrib import messages
from account.models import agent
from .models import Payment
import requests
import json
import PIL.Image as Image
from io import BytesIO
import io
import base64
from . import forms
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa



# Create your views here.
def index_nin(request):
    return render(request, 'index_nin.html')

def v_by_ninw(request):
    user = request.user
    mm = agent.objects.filter(email= user.username).values("wallet_bal")
    nn=mm[0]['wallet_bal']
    
    

    
    
    if nn < '150':
        messages.info(request,"Insufficient balance", extra_tags='ans')
        
    else:
        
        if request.method == 'POST':
            me=request.POST["nin_number"]
            url = "https://api.verified.africa/sfx-verify/v3/id-service/"

            payload = {
                "searchParameter": me,
                "verificationType": "NIN-SEARCH"
            }
            headers = {
                "accept": "application/json",
                "userid": "1647784769854",
                "apiKey": "OiJ8EYBw98vaDWClMZLO",
                "content-type": "application/json"
            }

            res = requests.post(url, json=payload, headers=headers).json()
            ress = res['response']
            vs = res['verificationStatus']
            print(vs)
            
            if vs == "PENDING":
                messages.info(request,"Something unexpected happened", extra_tags='ans')
            else:
                if vs == "NOT VERIFIED":
                    messages.info(request,"No Record Found", extra_tags='ans')
                else:
                    if vs == "FAILED":
                        messages.info(request,"Third Party System is Unavailable", extra_tags='ans')
                    else:
                        math = int(nn) 
                        i = int(150)
                        done  =  math - i
                        print(done)
                        agent.objects.filter(email = user.username).update(wallet_bal = done)
                        rr = agent.objects.filter(email= user.username).values("wallet_bal")
                        ss=rr[0]['wallet_bal']
                        
                        nin_Surname =ress[0]['surname']
                        nin_firstname =ress[0]['firstname']
                        nin_middlename =ress[0]['middlename']
                        nin_gender =ress[0]['gender']
                        nin_dateofbirth =ress[0]['birthdate']
                        nin_nin =ress[0]['nin']
                        nin_phonenumber =ress[0]['telephoneno']
                        nin_email =ress[0]['heigth']
                        nin_trackingid =ress[0]['trackingId']
                        nin_town =ress[0]['residence_Town']
                        nin_address =ress[0]['residence_AdressLine1']
                        nin_residencelga =ress[0]['residence_lga']
                        nin_residencestate =ress[0]['residence_state']
                        nin_stateoforigin =ress[0]['self_origin_state']
                        nin_noksurname =ress[0]['nok_surname']
                        nin_nokfirstname =ress[0]['nok_firstname']
                        nin_nokmiddlename =ress[0]['nok_middlename']
                        nin_noktown =ress[0]['nok_town']
                        nin_nokstate =ress[0]['nok_state']
                        nin_country =ress[0]['birthcountry']
                        nin_title =ress[0]['title']
                        
                        request.session['nin_Surname'] = nin_Surname
                        request.session['nin_firstname'] = nin_firstname
                        request.session['nin_middlename'] = nin_middlename
                        request.session['nin_gender'] = nin_gender
                        request.session['nin_nin'] = nin_nin
                        request.session['nin_trackingid'] = nin_trackingid
                        request.session['nin_address'] = nin_address
                        request.session['nin_town'] = nin_town
                        request.session['nin_residencelga'] = nin_residencelga
                        
                        messages.info(request,nin_Surname,extra_tags='m1')
                        messages.info(request,nin_firstname,extra_tags='m2')
                        messages.info(request,nin_middlename,extra_tags='m3')
                        messages.info(request,nin_gender,extra_tags='m4')
                        messages.info(request,nin_dateofbirth,extra_tags='m5')
                        messages.info(request,nin_nin,extra_tags='m6')
                        messages.info(request,nin_phonenumber,extra_tags='m7')
                        messages.info(request,nin_email,extra_tags='m8')
                        messages.info(request,nin_trackingid,extra_tags='m9')
                        messages.info(request,nin_town,extra_tags='m10')
                        messages.info(request,nin_address,extra_tags='m11')
                        messages.info(request,nin_residencelga,extra_tags='m12')
                        messages.info(request,nin_residencestate,extra_tags='m13')
                        messages.info(request,nin_stateoforigin,extra_tags='m14')
                        messages.info(request,nin_noksurname,extra_tags='m15')
                        messages.info(request,nin_nokfirstname,extra_tags='m16')
                        messages.info(request,nin_nokmiddlename,extra_tags='m17')
                        messages.info(request,nin_noktown,extra_tags='m18')
                        messages.info(request,nin_nokstate,extra_tags='m19')
                        messages.info(request,nin_country,extra_tags='m20')
                        messages.info(request,nin_title,extra_tags='m21')
                        
                        #image 
                        photo = ress[0]['photo']
                        byte_data =f"'{photo}'"
                        b= base64.b64decode(byte_data)
                        data = io.BytesIO(b)
                        data.seek(0)
                        pp = Image.open(data)
                        pp.save(data, "PNG")
                        end = base64.b64encode(data.getvalue())
                        img  = end.decode('utf-8')
                        request.session['img'] = img
                        #sig  
                        photo1 = ress[0]['signature']
                        byte_data1 =f"'{photo1}'"
                        b1= base64.b64decode(byte_data1)
                        data1 = io.BytesIO(b1)
                        data1.seek(0)
                        pp1 = Image.open(data1)
                        pp1.save(data1, "PNG")
                        end1 = base64.b64encode(data1.getvalue())
                        img1  = end1.decode('utf-8')
                        
                        
                        
                        return render(request,'v_by_ninw.html',{"img_data":img,"img_data1":img1,"wallet":ss})
        
        
    return render(request, 'v_by_ninw.html',{"wallet":nn})

def v_by_phone(request):
    user = request.user
    mm = agent.objects.filter(email= user.username).values("wallet_bal")
    nn=mm[0]['wallet_bal']
    if nn < '150':
        messages.info(request,"Insufficient balance", extra_tags='ans')
        
    else:
        if request.method == 'POST':
            me=request.POST["nin_phone"]
            url = "https://api.verified.africa/sfx-verify/v3/id-service/"

            payload = {
                "searchParameter": me,
                "verificationType": "NIN-PHONE-SEARCH"
            }
            headers = {
                "accept": "application/json",
                "userid": "1647784769854",
                "apiKey": "fv6LUVnQGNcp4eEPdK5A",
                "content-type": "application/json"
            }

            res = requests.post(url, json=payload, headers=headers).json()
            ress = res['response']
            vs = res['verificationStatus']
            print(vs)
            
            if vs == "PENDING":
                messages.info(request,"Something unexpected happened", extra_tags='ans')
            else:
                if vs == "NOT VERIFIED":
                    messages.info(request,"No Record Found", extra_tags='ans')
                else:
                    if vs == "FAILED":
                        messages.info(request,"Third Party System is Unavailable", extra_tags='ans')
                    else:
                        math = int(nn) 
                        i = int(150)
                        done  =  math - i
                        print(done)
                        agent.objects.filter(email = user.username).update(wallet_bal = done)
                        rr = agent.objects.filter(email= user.username).values("wallet_bal")
                        ss=rr[0]['wallet_bal']
                        
                        nin_Surname =ress[0]['surname']
                        nin_firstname =ress[0]['firstname']
                        nin_middlename =ress[0]['middlename']
                        nin_gender =ress[0]['gender']
                        nin_dateofbirth =ress[0]['birthdate']
                        nin_nin =ress[0]['nin']
                        nin_phonenumber =ress[0]['telephoneno']
                        nin_email =ress[0]['heigth']
                        nin_trackingid =ress[0]['trackingId']
                        nin_town =ress[0]['residence_Town']
                        nin_address =ress[0]['residence_AdressLine1']
                        nin_residencelga =ress[0]['residence_lga']
                        nin_residencestate =ress[0]['residence_state']
                        nin_stateoforigin =ress[0]['self_origin_state']
                        nin_noksurname =ress[0]['nok_surname']
                        nin_nokfirstname =ress[0]['nok_firstname']
                        nin_nokmiddlename =ress[0]['nok_middlename']
                        nin_noktown =ress[0]['nok_town']
                        nin_nokstate =ress[0]['nok_state']
                        nin_country =ress[0]['birthcountry']
                        nin_title =ress[0]['title']
                        
                        messages.info(request,nin_Surname,extra_tags='m1')
                        messages.info(request,nin_firstname,extra_tags='m2')
                        messages.info(request,nin_middlename,extra_tags='m3')
                        messages.info(request,nin_gender,extra_tags='m4')
                        messages.info(request,nin_dateofbirth,extra_tags='m5')
                        messages.info(request,nin_nin,extra_tags='m6')
                        messages.info(request,nin_phonenumber,extra_tags='m7')
                        messages.info(request,nin_email,extra_tags='m8')
                        messages.info(request,nin_trackingid,extra_tags='m9')
                        messages.info(request,nin_town,extra_tags='m10')
                        messages.info(request,nin_address,extra_tags='m11')
                        messages.info(request,nin_residencelga,extra_tags='m12')
                        messages.info(request,nin_residencestate,extra_tags='m13')
                        messages.info(request,nin_stateoforigin,extra_tags='m14')
                        messages.info(request,nin_noksurname,extra_tags='m15')
                        messages.info(request,nin_nokfirstname,extra_tags='m16')
                        messages.info(request,nin_nokmiddlename,extra_tags='m17')
                        messages.info(request,nin_noktown,extra_tags='m18')
                        messages.info(request,nin_nokstate,extra_tags='m19')
                        messages.info(request,nin_country,extra_tags='m20')
                        messages.info(request,nin_title,extra_tags='m21')
                        
                        #image 
                        photo = ress[0]['photo']
                        byte_data =f"'{photo}'"
                        b= base64.b64decode(byte_data)
                        data = io.BytesIO(b)
                        data.seek(0)
                        pp = Image.open(data)
                        pp.save(data, "PNG")
                        end = base64.b64encode(data.getvalue())
                        img  = end.decode('utf-8')
                        
                        #sig  
                        photo1 = ress[0]['signature']
                        byte_data1 =f"'{photo1}'"
                        b1= base64.b64decode(byte_data1)
                        data1 = io.BytesIO(b1)
                        data1.seek(0)
                        pp1 = Image.open(data1)
                        pp1.save(data1, "PNG")
                        end1 = base64.b64encode(data1.getvalue())
                        img1  = end1.decode('utf-8')
                        return render(request,'v_by_phone.html',{"img_data":img,"img_data1":img1,"wallet":ss})
            
    return render(request, 'v_by_phone.html',{"wallet":nn})

def v_by_vnin(request):
    user = request.user
    mm = agent.objects.filter(email= user.username).values("wallet_bal")
    nn=mm[0]['wallet_bal']
    if nn < '150':
        messages.info(request,"Insufficient balance", extra_tags='ans')
        
    else:
        
        if request.method == 'POST':
            me=request.POST["nin_number"]
            url = "https://api.verified.africa/sfx-verify/v3/id-service/"

            payload = {
                "searchParameter": me,
                "verificationType": "NIN-SEARCH"
            }
            headers = {
                "accept": "application/json",
                "userid": "1647784769854",
                "apiKey": "OiJ8EYBw98vaDWClMZLO",
                "content-type": "application/json"
            }

            res = requests.post(url, json=payload, headers=headers).json()
            ress = res['response']
            vs = res['verificationStatus']
            print(vs)
            
            if vs == "PENDING":
                messages.info(request,"Something unexpected happened", extra_tags='ans')
            else:
                if vs == "NOT VERIFIED":
                    messages.info(request,"No Record Found", extra_tags='ans')
                else:
                    if vs == "FAILED":
                        messages.info(request,"Third Party System is Unavailable", extra_tags='ans')
                    else:
                        math = int(nn) 
                        i = int(150)
                        done  =  math - i
                        print(done)
                        agent.objects.filter(email = user.username).update(wallet_bal = done)
                        rr = agent.objects.filter(email= user.username).values("wallet_bal")
                        ss=rr[0]['wallet_bal']
                        
                        nin_Surname =ress[0]['surname']
                        nin_firstname =ress[0]['firstname']
                        nin_middlename =ress[0]['middlename']
                        nin_gender =ress[0]['gender']
                        nin_dateofbirth =ress[0]['birthdate']
                        nin_nin =ress[0]['nin']
                        nin_phonenumber =ress[0]['telephoneno']
                        nin_email =ress[0]['heigth']
                        nin_trackingid =ress[0]['trackingId']
                        nin_town =ress[0]['residence_Town']
                        nin_address =ress[0]['residence_AdressLine1']
                        nin_residencelga =ress[0]['residence_lga']
                        nin_residencestate =ress[0]['residence_state']
                        nin_stateoforigin =ress[0]['self_origin_state']
                        nin_noksurname =ress[0]['nok_surname']
                        nin_nokfirstname =ress[0]['nok_firstname']
                        nin_nokmiddlename =ress[0]['nok_middlename']
                        nin_noktown =ress[0]['nok_town']
                        nin_nokstate =ress[0]['nok_state']
                        nin_country =ress[0]['birthcountry']
                        nin_title =ress[0]['title']
                        
                        messages.info(request,nin_Surname,extra_tags='m1')
                        messages.info(request,nin_firstname,extra_tags='m2')
                        messages.info(request,nin_middlename,extra_tags='m3')
                        messages.info(request,nin_gender,extra_tags='m4')
                        messages.info(request,nin_dateofbirth,extra_tags='m5')
                        messages.info(request,nin_nin,extra_tags='m6')
                        messages.info(request,nin_phonenumber,extra_tags='m7')
                        messages.info(request,nin_email,extra_tags='m8')
                        messages.info(request,nin_trackingid,extra_tags='m9')
                        messages.info(request,nin_town,extra_tags='m10')
                        messages.info(request,nin_address,extra_tags='m11')
                        messages.info(request,nin_residencelga,extra_tags='m12')
                        messages.info(request,nin_residencestate,extra_tags='m13')
                        messages.info(request,nin_stateoforigin,extra_tags='m14')
                        messages.info(request,nin_noksurname,extra_tags='m15')
                        messages.info(request,nin_nokfirstname,extra_tags='m16')
                        messages.info(request,nin_nokmiddlename,extra_tags='m17')
                        messages.info(request,nin_noktown,extra_tags='m18')
                        messages.info(request,nin_nokstate,extra_tags='m19')
                        messages.info(request,nin_country,extra_tags='m20')
                        messages.info(request,nin_title,extra_tags='m21')
                        
                        #image 
                        photo = ress[0]['photo']
                        byte_data =f"'{photo}'"
                        b= base64.b64decode(byte_data)
                        data = io.BytesIO(b)
                        data.seek(0)
                        pp = Image.open(data)
                        pp.save(data, "PNG")
                        end = base64.b64encode(data.getvalue())
                        img  = end.decode('utf-8')
                        
                        #sig  
                        photo1 = ress[0]['signature']
                        byte_data1 =f"'{photo1}'"
                        b1= base64.b64decode(byte_data1)
                        data1 = io.BytesIO(b1)
                        data1.seek(0)
                        pp1 = Image.open(data1)
                        pp1.save(data1, "PNG")
                        end1 = base64.b64encode(data1.getvalue())
                        img1  = end1.decode('utf-8')
                        return render(request,'v_by_ninw.html',{"img_data":img,"img_data1":img1,"wallet":ss})
                    
    return render(request, 'v_by_vnin.html',{"wallet":nn})

def wallet(request: HttpRequest) -> HttpResponse:
    user = request.user
    mm = agent.objects.filter(email= user.username).values("wallet_bal")
    nn=mm[0]['wallet_bal']
    if request.method == 'POST':
        payment_form = forms.PaymentForm(request.POST)
        if payment_form.is_valid():
            pay = payment_form.save()
            return render(request,'make_payment.html',{'payment': pay, 'paystack_public_key': settings.PAYSTACK_PUBLIC_KEY})  
    else:
        payment_form = forms.PaymentForm()
    return render(request, 'wallet.html', { 'user':user, 'wallet': nn,'payment_form': payment_form})


def voters(request):
    user = request.user
    mm = agent.objects.filter(email= user.username).values("wallet_bal")
    nn=mm[0]['wallet_bal']
    
    if nn < '300':
        messages.info(request,"Insufficient balance", extra_tags='ans')
        
    else:
        
        if request.method == 'POST':
            me=request.POST["voter_number"]
            url = "https://api.verified.africa/sfx-verify/v3/id-service/"

            payload = {
                "searchParameter": me,
                "countryCode" : "NG",
                "verificationType": "VIN-FULL-DETAILS-VERIFICATION"
            }
            headers = {
                "accept": "application/json",
                "userid": "1647784769854",
                "apiKey": "QMvXdF4ckwLQ2DQkg6OV",
                "content-type": "application/json"
            }

            res = requests.post(url, json=payload, headers=headers).json()
            ress = res['response']
            vs = res['verificationStatus']
            print(ress)
            print(res)
            print(vs)
            if vs == "PENDING":
                messages.info(request,"Something unexpected happened", extra_tags='ans')
            else:
                if vs == "NOT VERIFIED":
                    messages.info(request,"No Record Found", extra_tags='ans')
                else:
                    if vs == "FAILED":
                        messages.info(request,"Third Party System is Unavailable", extra_tags='ans')
                    else:
                        math = int(nn) 
                        i = int(300)
                        done  =  math - i
                        print(done)
                        agent.objects.filter(email = user.username).update(wallet_bal = done)
                        rr = agent.objects.filter(email= user.username).values("wallet_bal")
                        ss=rr[0]['wallet_bal']
                        pass
    
    return render(request, 'voters.html',{"wallet":nn})


def pdf(request):
    request.user
    #pdf
    #template_path = 'Nimc.html'
    
    
    
    context = {'surname':request.session['nin_Surname'],
                'firstname': request.session['nin_firstname'] ,
                'middlename': request.session['nin_middlename'],
                'gender': request.session['nin_gender'],
                'nin': request.session['nin_nin'],
                'tracking': request.session['nin_trackingid'],
                'address': request.session['nin_address'],
                'town': request.session['nin_town'],
                'add_lga': request.session['nin_residencelga'],
                'img':request.session['img']
                
    }
    #response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'filename="report.pdf"'
    # find the template and render it.
    #template = get_template(template_path)
    #html = template.render(context)
    
    # create a pdf
    #pisa_status = pisa.CreatePDF(
    #html, dest=response)  
    
    # if error then show some funny view
    #if pisa_status.err:
       #return HttpResponse('We had some errors <pre>' + html + '</pre>')
    #return response
    return render(request, 'Nimc.html',context)
    


def bvn(request):
    user = request.user
    mm = agent.objects.filter(email= user.username).values("wallet_bal")
    nn=mm[0]['wallet_bal']
    
    if nn < '150':
        messages.info(request,"Insufficient balance", extra_tags='ans')
        
    else:
        
        if request.method == 'POST':
            me=request.POST["bvn_number"]
            url = "https://api.verified.africa/sfx-verify/v3/id-service/"

            payload = {
                "searchParameter": me,
                "verificationType": "BVN-FULL-DETAILS"
            }
            headers = {
                "accept": "application/json",
                "userid": "1647784769854",
                "apiKey": "d7nMevDBwe8gpn0h2aTm",
                "content-type": "application/json"
            }

            res = requests.post(url, json=payload, headers=headers).json()
            ress = res['response']
            vs = res['verificationStatus']
            if vs == "PENDING":
                messages.info(request,"Something unexpected happened", extra_tags='ans')
            else:
                if vs == "NOT VERIFIED":
                    messages.info(request,"No Record Found", extra_tags='ans')
                else:
                    if vs == "FAILED":
                        messages.info(request,"Third Party System is Unavailable", extra_tags='ans')
                    else:
                        math = int(nn) 
                        i = int(150)
                        done  =  math - i
                        print(done)
                        agent.objects.filter(email = user.username).update(wallet_bal = done)
                        rr = agent.objects.filter(email= user.username).values("wallet_bal")
                        ss=rr[0]['wallet_bal']
                        
                        #image 
                        photo_bvn = ress['imageBase64']
                        byte_data_bvn =f"'{photo_bvn}'"
                        b_bvn= base64.b64decode(byte_data_bvn)
                        data_bvn = io.BytesIO(b_bvn)
                        data_bvn.seek(0)
                        pp_bvn = Image.open(data_bvn)
                        pp_bvn.save(data_bvn, "PNG")
                        end_bvn = base64.b64encode(data_bvn.getvalue())
                        img  = end_bvn.decode('utf-8')
                        
                        #sig  
                        photo1 = ress['basicDetailBase64']
                        byte_data1 =f"'{photo1}'"
                        b1= base64.b64decode(byte_data1)
                        data1 = io.BytesIO(b1)
                        data1.seek(0)
                        pp1 = Image.open(data1)
                        pp1.save(data1, "PNG")
                        end1 = base64.b64encode(data1.getvalue())
                        img1  = end1.decode('utf-8')
                        return render(request,'bvn.html',{"img_data":img,"img_data1":img1,"wallet":ss})
                        
    
    return render(request, 'bvn.html',{"wallet":nn})

def dashboard(request):
    user = request.user
    mm = agent.objects.filter(email= user.username).values("wallet_bal")
    nn=mm[0]['wallet_bal']
    
    historys = Payment.objects.filter(email = user.username).all().values()
    pay = historys
    return render(request, 'dashboard.html',{"user":user, "wallet": nn,"trans": pay})

def int_pass(request):
    user = request.user
    mm = agent.objects.filter(email= user.username).values("wallet_bal")
    nn=mm[0]['wallet_bal']
    if nn < '150':
        messages.info(request,"Insufficient balance", extra_tags='ans')
        
    else:
        
        if request.method == 'POST':
            
            me=request.POST["int_pass_number"]
            me1=request.POST["int_pass_surname"]
            url = "https://api.verified.africa/sfx-verify/v3/id-service/"

            payload = {
                "searchParameter": me,
                "verificationType": "PASSPORT-FULL-DETAILS",
                "lastName": me1
            }
            headers = {
                "accept": "application/json",
                "userid": "1647784769854",
                "apiKey": "8Nqd6AxWoXEtEz69VYYZ",
                "content-type": "application/json"
            }

            res = requests.post(url, json=payload, headers=headers).json()
            ress = res['response']
            vs = res['verificationStatus']
            print(res)
            print(ress)
            print(vs)
            if vs == "PENDING":
                messages.info(request,"Something unexpected happened", extra_tags='ans')
            else:
                if vs == "NOT VERIFIED":
                    messages.info(request,"No Record Found", extra_tags='ans')
                else:
                    if vs == "FAILED":
                        messages.info(request,"Third Party System is Unavailable", extra_tags='ans')
                    else:
                        math = int(nn) 
                        i = int(150)
                        done  =  math - i
                        print(done)
                        agent.objects.filter(email = user.username).update(wallet_bal = done)
                        rr = agent.objects.filter(email= user.username).values("wallet_bal")
                        ss=rr[0]['wallet_bal']
                        
                        pass_Surname =ress['last_name']
                        pass_firstname =ress['first_name']
                        pass_middlename =ress['middle_name']
                        pass_gender =ress['gender']
                        pass_dateofbirth =ress['dob']
                        pass_refernce =ress['reference_id']
                        pass_phonenumber =ress['mobile']
                        pass_issue_at =ress['issued_at']
                        pass_issue_date =ress['issued_date']
                        pass_ex_date =ress['expiry_date']
                        
                        messages.info(request,pass_Surname,extra_tags='m1')
                        messages.info(request,pass_firstname,extra_tags='m2')
                        messages.info(request,pass_middlename,extra_tags='m3')
                        messages.info(request,pass_gender,extra_tags='m4')
                        messages.info(request,pass_dateofbirth,extra_tags='m5')
                        messages.info(request,pass_refernce,extra_tags='m6')
                        messages.info(request,pass_phonenumber,extra_tags='m7')
                        messages.info(request,pass_issue_at,extra_tags='m8')
                        messages.info(request,pass_issue_date,extra_tags='m9')
                        messages.info(request,pass_ex_date,extra_tags='m10')
                        
                        #photo12 = ress['photo']
                        #print(photo12)
                        #byte_data12 =f"'{photo12}'"
                        #b12= base64.b64decode(byte_data12)
                        #print(b12)
                        #data12 = io.BytesIO(b12)
                        #data12.seek(0)
                        #pp12 = Image.open(data12)
                        #pp12.save(data12, "PNG")
                        #end12 = base64.b64encode(data12.getvalue())
                        #img12  = end12.decode('utf-8')
                        return render(request,'int_pass.html',{"wallet":ss})
                        
    return render(request, 'int_pass.html',{"wallet":nn})

def bbm(request):
    user = request.user
    mm = agent.objects.filter(email= user.username).values("wallet_bal")
    nn=mm[0]['wallet_bal']
    return render(request, 'bbm.html',{"wallet":nn})


def verify_payment(request: HttpRequest,ref:str) -> HttpResponse:
    user = request.user
    payment = get_object_or_404(Payment, ref=ref) 
    verified = payment.verify_payment()
    if verified:
        messages.success(request, "verification successfull",extra_tags='success')
        p_amount = Payment.objects.filter(ref= ref).values("amount")
        p_list = p_amount[0]['amount']
        p_cal = int(p_list)
        rr = agent.objects.filter(email= user.username).values("wallet_bal")
        ss=rr[0]['wallet_bal']
        a_cal = int(ss)
        math = p_cal + a_cal
        print(math)
        agent.objects.filter(email = user.username).update(wallet_bal = math)
        a_update = agent.objects.filter(email= user.username).values("wallet_bal")
        a_new_amount=a_update[0]['wallet_bal']
        render(request, 'wallet.html',{"wallet":a_new_amount})
    else:
        messages.error(request, "verification Failed",extra_tags='success')
    return redirect('wallet') 


