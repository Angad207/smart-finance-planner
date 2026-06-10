import traceback
from urllib import request

from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from datetime import datetime, timezone as tm , timedelta
from zoneinfo import ZoneInfo
import os
from dotenv import load_dotenv
load_dotenv()
import re
import ollama
import random
import json

from django.core.mail import send_mail

# from prometheus_client import values

from FP.models import Contact, Aamount, Aincome, Profile, ADDGOALS, Budget,PasswordResetOTP


# Create your views here.

def index(request):
    return render(request, 'landingpage.html')
    # return HttpResponse("Hello, world. You're at the polls index.")

def goalpage(request):
    return render(request, 'goal.html')


def signuppage(request):
    try:
        return render(request, 'signup.html')
    except Exception as e:
        print('Error:',e)
        print(traceback.format_exc())
        raise

@never_cache
def loginpage(request):
    return render(request, 'login.html')

@login_required
def UI(request):
    if request.user.is_anonymous:
        return render(request, 'login.html')
    else:
        return render(request, "ui.html")
    # return HttpResponse(str(request.user.is_authenticated))

def first(request):
    return render(request, 'myfirst.html')

def base(request):
    return render(request, 'base.html')

def contact(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        password = request.POST.get('password')
        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')
        state = request.POST.get('state')
        zip = request.POST.get('zip')
        print(fname, lname, email, password, address1, address2, city, state)
        contact = Contact(fname=fname, lname=lname, email=email, password = password, address1=address1,
                          address2=address2, city=city, state=state, zip=zip)
        contact.save()
        print("SAVED SUCCESSFULLY")
    return render(request, 'contact.html')


# @login_required
# only send data to list in webpage
def Chart(request):
    data = Aamount.objects.filter(user=request.user)
    date2 = datetime.now()

    labels = []
    values = []
    date = []

    for item in data:
        if item.date.strftime("%B") == date2.strftime("%B") and item.date.year == date2.year:
            labels.append(item.category)
            values.append(item.amount)
            date.append(f"{item.date.day}/{item.date.month}/{item.date.year}")
    print(date)

    return JsonResponse({'labels': labels[::-1], 'values': values[::-1], 'date': date[::-1]})

def ChartIncome(request):
    data = Aincome.objects.filter(user=request.user)
    date2 = datetime.now()

    labels = []
    values = []
    date = []

    for item in data:
        if item.date.strftime("%B") == date2.strftime("%B") and item.date.year == date2.year:
            labels.append(item.category)
            values.append(item.amount)
            date.append(f"{item.date.day}/{item.date.month}/{item.date.year}")
        else:
            continue
    print(date)

    return JsonResponse({'labels': labels[::-1], 'values': values[::-1], 'date': date[::-1]})

#it will save row and modified data for Chart function
def homep(request):
    date2 = datetime.now()
    if request.method == "POST":
        amount = request.POST.get('amount')
        categorye = request.POST.get('category')
        desc = request.POST.get('desc')
        aamount = Aamount(user = request.user,amount=amount, desc=desc, category=categorye)
        aamount.save()
        # aamount.save()
        # print(amount, desc)

        existing = Budget.objects.filter(user=request.user)
        for item in existing:
            if item.category == categorye and date2.strftime("%B") == item.date.strftime("%B"):
                item.spent+=float(amount)
                item.save()
            else:
                continue

        # return redirect(UI)

    return redirect(UI)

def addExpenceOnGoal(request):
    data = ADDGOALS.objects.filter(user=request.user)
    if request.method == "POST":
        amount = request.POST.get('amount')
        goalname = request.POST.get('goalname')
        targetdate = request.POST.get('targetdate')
        targetamount = request.POST.get('targetamount')
        print("collected value " +targetamount, targetdate, goalname, amount)
        # category = request.POST.get('category')
        category = 'Goals'
        desc = request.POST.get('desc')
        aamount = Aamount(user = request.user,amount=amount, desc=desc+': '+goalname+", "+"Target: "+targetdate+", "+targetamount, category=category)
        aamount.save()
        # for item in data:
        #     if item.goalname == goalname and item.goaltype==desc:
        #         item.currentsaving+=float(amount)
        #         item.save()
        #         print("yooooooo")

        # print(amount, category, desc)
        return redirect(goalpage)

def cpy(request):
    data = Aamount.objects.filter(user=request.user)
    result = {}
    date = datetime.now()

    for item in data:
        if item.category in result and item.date.strftime("%B") == date.strftime("%B") and item.date.year == date.year:
            result[item.category] += item.amount
            # result[item.desc] = int(result[item.desc])
            # result[item.desc] += item.amount
            # result[item.desc] = str(result[item.desc])


            # result[item.amount] += int(item.amount)
        elif item.date.strftime("%B") == date.strftime("%B") and item.date.year == date.year:
            result[item.category] = item.amount
        else:
            continue

    # print(type(data["Travel"]))
    labels = list(result.keys())
    # print("data accse successful")
    values = list(result.values())
    return JsonResponse({'labels': labels, 'values': values})

def cpy2(request):
    data = Aincome.objects.filter(user=request.user)
    result = {}
    date = datetime.now()

    for item in data:
        if item.category in result and item.date.strftime("%B") == date.strftime("%B") and item.date.year == date.year:
            result[item.category] += item.amount
            # result[item.desc] = int(result[item.desc])
            # result[item.desc] += item.amount
            # result[item.desc] = str(result[item.desc])


            # result[item.amount] += int(item.amount)
        elif item.date.strftime("%B") == date.strftime("%B") and item.date.year == date.year:
            result[item.category] = item.amount
        else:
            continue

    # print(type(data["Travel"]))
    labels = list(result.keys())
    # print("data accse successful")
    values = list(result.values())
    return JsonResponse({'labels': labels, 'values': values})

def aincome(request):
    if request.method == "POST":
        amount = request.POST.get('iamount')
        category = request.POST.get('category')
        desc = request.POST.get('idesc')
        aincome = Aincome(user = request.user,amount=amount, category=category,desc=desc)
        aincome.save()
        return redirect(UI)
    return render(request, 'ui.html')

def ain(request):

    data = Aincome.objects.filter(user=request.user)
    result = {}
    date = datetime.now()
    for item in data:
        if item.desc in result and item.date.strftime("%B") == date.strftime("%B") and item.date.year == date.year:
            result[item.desc] += item.amount
        elif item.date.strftime("%B") == date.strftime("%B") and item.date.year == date.year:
            result[item.desc] = item.amount
        else:
            continue

    labels = list(result.keys())
    values = list(result.values())
    return JsonResponse({'labels': labels, 'values': values})

def report(request):
    return render(request, 'report.html')

def budget(request):
    return render(request, 'budget.html')

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        emailadderess = request.POST.get('emailadderess')
        createpassword = request.POST.get('createpassword')
        phonenumber = request.POST.get('phonenumber')

        user = User.objects.create_user(username=username, email=emailadderess, password=createpassword)
        Profile.objects.create(user=user, phone=phonenumber)

        return redirect(loginpage)

    return render(request, 'signup.html')

def LOGIN(request):
    if request.method == "POST":
        emailphone = request.POST.get('emailphone')
        loginpassword = request.POST.get('loginpassword')

        try:
            user_obj = User.objects.get(email=emailphone)
        except:
            try:
                user_obj = Profile.objects.get(phone=emailphone).user
            except:
                user_obj = None

        if user_obj:
            user = authenticate(request,username=user_obj.username, password=loginpassword)

            if user:
                print("LOGIN SUCCESSFULLY")
                login(request, user)
                return redirect(UI)
        else:
            print("LOGIN FAILED")
            return redirect(loginpage)
    return render(request, 'login.html')

def LOGOUT(request):
    logout(request)
    return redirect(index)

def barchart(request):
    data = Aamount.objects.filter(user=request.user)
    # data = Aamount.objects.all()
    data1 = Aincome.objects.filter(user=request.user)
    result = {}
    result1 = {}
    sum = 0
    sum1 = 0
    for item in data:
        sum += item.amount
        if item.date.strftime("%B") in result:
            result[item.date.strftime("%B")] += item.amount
        else:
            result[item.date.strftime("%B")] = item.amount

    for item in data1:
        sum1 += item.amount
        if item.date.strftime("%B") in result1:
            result1[item.date.strftime("%B")] += item.amount
        else:
            result1[item.date.strftime("%B")] = item.amount
    # print(result)

    ilabels = list(result.keys())
    elabels = list(result1.keys())
    month_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
                  "November", "December"]
    months =[m for m in month_list if m in (set(ilabels)|set(elabels))]
    month = ["March", "April", "May", "June", "July", "August", "September"]
    evalues = [result.get(m, 0) for m in months]
    ivalues = [result1.get(m, 0) for m in months]
    return JsonResponse({'labels': months[-6:], 'ivalues': ivalues,"evalues": evalues,"sum": sum,"sum1": sum1})

        # date = datetime.strptime(item.desc, '%Y/%m/%d')

    #     date = item.date.month
    #     print(date)
    # else:
    #     print("failed")

def addGoal(request):
    if request.method == "POST":
        goalname = request.POST.get('goalname')
        goaltype = request.POST.get('goaltype')
        targetamount = request.POST.get('targetamount')
        targetdate = request.POST.get('targetdate')
        currentsaving = request.POST.get('currentsaving')
        prioritystatus = request.POST.get('prioritystatus') or 'off'
        aistatus = request.POST.get('aistatus')or 'off'
        category = 'Goals'
        targetdateconvert = datetime.strptime(targetdate, '%Y-%m-%d')

        addgoal = ADDGOALS(user = request.user, goalname=goalname, goaltype=goaltype, targetamount=targetamount, targetdate=targetdate, currentsaving=currentsaving, prioritystatus=prioritystatus, aistatus=aistatus)
        addgoal.save()
        aamount = Aamount(user=request.user, amount=currentsaving, desc=goaltype+": "+goalname+", "+"Target: "+targetdateconvert.strftime('%B')+" "+str(targetdateconvert.year)+", "+targetamount, category=category)
        aamount.save()

        # aamount = Aamount(user=request.user, amount=amount,
        #                   desc=desc + ': ' + goalname + ", " + "Target: " + targetdate + ", " + targetamount,
        #                   category=category)
        aamount.save()

    return redirect(goalpage)

def addGoalJson(request):
    data = ADDGOALS.objects.filter(user=request.user)
    goaldata = Aamount.objects.filter(user=request.user)

    gn =[]
    gt =[]
    ta = []
    td=[]
    cs =[]
    ps = []
    ais =[]
    mra = []
    createddate=[]

    # cd = now
    # (td.year - cd.year) * 12 + (td.month - cd.month)

    for item in data:
        cseving=0
        for i in goaldata:
            if item.goalname in i.desc and item.goaltype in i.desc and item.targetdate.strftime('%B') in i.desc and str(
                    item.targetdate.year) in i.desc and str(int(item.targetamount)) in i.desc:
                cseving += i.amount
                print('Found')
            else:
                # print('Not Found', item.goalname, item.goaltype, item.targetdate.strftime('%B'),
                      # str(item.targetdate.year), str(item.targetamount))
                continue
        item.currentsaving = cseving
        gn.append(item.goalname)
        gt.append(item.goaltype)
        ta.append(item.targetamount)
        td.append(str(item.targetdate.strftime("%B"))+" "+ str(item.targetdate.year))
        cs.append(item.currentsaving)
        cd = datetime.now()
        mra.append((item.targetdate.year-cd.year)*12+(item.targetdate.month-cd.month))
        ps.append(item.prioritystatus)
        ais.append(item.aistatus)
        createddate.append(item.date)
#         prompt = {'goal name':item.goalname,'target amount':item.targetamount,'target date':item.targetdate,
#                   'current saving':item.currentsaving,'monthly need':item.targetamount/item.currentsaving,'priority status':item.prioritystatus,}
#         response = ollama.chat(
#             model='llama3.2:3b',
#             messages=[{'role': 'user','content': f"""You are a goal instructor only for this goal:-{prompt},
# Rules:
# -Reply in exactly 2 bullet points
# -maximum 15 words
# -Give practical advice to achive this goal
# -No introduction
# -No explanation
# -proper answer
# -not allowed any unwanted words
# -currency sign is rupee""",}],
#             options={"num_predict": 40,"temperature": 0.4}
#         )
#
#         answer = response['message']['content']
#         # aijson.append(answer)
    return JsonResponse({'gn':gn,'gt':gt,'ta':ta,'td':td,'cs':cs,'ps':ps,'ais':ais,'mra':mra,'createddate':createddate,})

from groq import Groq

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
def singleGoalAi(request, index):
    goals = ADDGOALS.objects.filter(user=request.user)
    item = goals[int(index)]

    prompt = {'goal name': item.goalname, 'target amount': item.targetamount, 'target date': item.targetdate,
              'current saving': item.currentsaving, 'monthly need': item.targetamount / item.currentsaving,
              'priority status': item.prioritystatus, }
    response = client.chat.completions.create(
        model='llama-3.3-70b-versatile',
        messages=[{'role': 'user', 'content': f"""You are a goal instructor only for this goal:-{prompt},
    Rules: 
    -Reply in exactly 2 bullet points
    -one point should be maximum 10 words
    -Give powerful and practical and useful advice to achive this goal and only related to given goal.
    -No introduction
    -No explanation
    -currency sign is rupee""", }],
        temperature=0.7,
        max_tokens=150
    )

    # answer = response['message']['content']
    answer = response.choices[0].message.content  # your grok api

    return JsonResponse({'reply': answer})



def MonthlyBudget(request):
    if request.method == "POST":
        data = Aamount.objects.filter(user=request.user)
        data1 = Budget.objects.filter(user=request.user)
        date2 = datetime.now()
        category = request.POST.get('budgetcategory')
        spent = 0
        # for item in data:
        #     if category == item.category and item.date.strftime("%B") == date2.strftime("%B") and item.date.year == date2.year:
        #         spent += item.amount
        #         print(item.amount)
        #     else:
        #         continue

        amount = request.POST.get('budgetedamount')

        existing = Budget.objects.filter(user=request.user, category=category).first()

        if existing:
            if existing.date.strftime("%B") == date2.strftime("%B"):
                existing.budgeted += float(amount.replace(',', ''))
                existing.save()
            else:
                Budget.objects.create(
                    user=request.user,
                    category=category,
                    budgeted=float(amount.replace(',', '')),
                    spent=spent
                )

        else:
            Budget.objects.create(
                user=request.user,
                category=category,
                budgeted=float(amount.replace(',', '')),
                spent=spent
            )
        return redirect(budget)
        # return redirect('/MonthlyBudget/')

def budgetJson(request):
    data1 = Budget.objects.filter(user=request.user)
    expense =Aamount.objects.filter(user=request.user)
    date2 = datetime.now()


    for item in data1:
        spent = 0
        for i in expense:
            if item.category == i.category and item.date.year == i.date.year and item.date.month == i.date.month:
                spent += i.amount
            else:
                continue
        item.spent = spent
        item.save()
    result={}
    result1={}
    for item in data1:
        if item.date.strftime("%B") == date2.strftime("%B"):
            if item.category in result:
                result[item.category] += item.budgeted
            else:
                result[item.category] = item.budgeted


            if item.category in result1:
                result1[item.category] += item.spent
                print("1",item.spent)
            else:
                result1[item.category] = item.spent
                print("2",item.spent)
        else:
            continue

    category = list(result.keys())
    budgeted = list(result.values())
    spent = list(result1.values())
    print("here................",category, budgeted, spent)
    return JsonResponse({'category': category, 'budget': budgeted, 'spent': spent,})

def budgetai(request):
    data1 = Budget.objects.filter(user=request.user)

    result = {}
    result1 = {}
    for item in data1:
        if item.category in result:
            result[item.category] += item.budgeted
        else:
            result[item.category] = item.budgeted

        if item.category in result1:
            result1[item.category] += item.spent
        else:
            result1[item.category] = item.spent

        category = list(result.keys())
        budgeted = list(result.values())
        spent = list(result1.values())
        json = []

        for i in range(len(category)):
            json.append({'Category':category[i], 'Budget':budgeted[i], 'Money Spent':spent[i]})
        print(json)

        response = ollama.chat(
            model='phi3',
            messages=[{'role': 'user', 'content': f"""You have to give two alert related to these all budgets for current month:-{json}, there don't matter alert are positive or negative,
        Rules: 
        -Reply in exactly 2 bullet points
        -Use related emojis
        -maximum 20 words
        -No introduction
        -No explanation
        -proper answer
        -not allowed any unwanted words
        -don't mention any word from prompt
        -maintain accuracy and perfection
        -currency sign is rupee""", }],
            options={"num_predict": 80, "temperature": 0.4}
        )

        answer = response['message']['content']
        # aijson.append(answer)
        return JsonResponse({"answer": answer})

def resetbudget(request):
    date2 = datetime.now()
    Budget.objects.filter(user=request.user,date__year =date2.year,date__month =date2.month ).delete()
    print("all wil get deleted, please don't regrate")
    return redirect(budget)



def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get('email')

        if not User.objects.filter(email=email).exists():

            return render(
                request,
                'forgot_password.html',
                {'error': 'Email not registered'}
            )

        otp = str(random.randint(100000, 999999))

        PasswordResetOTP.objects.create(
            email=email,
            otp=otp
        )

        send_mail(
            'Password Reset OTP',
            f'Your OTP is: {otp}',
            'yourgmail@gmail.com',
            [email],
            fail_silently=False
        )

        request.session['reset_email'] = email

        return redirect('/verify-otp/')

    return render(
        request,
        'forgot_password.html'
    )

from datetime import timedelta
from django.utils import timezone


def verify_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get('otp')

        email = request.session.get('reset_email')

        otp_record = PasswordResetOTP.objects.filter(
            email=email,
            otp=entered_otp
        ).last()

        if not otp_record:

            return render(
                request,
                'verify_otp.html',
                {'error': 'Invalid OTP'}
            )

        if timezone.now() - otp_record.created_at > timedelta(minutes=5):

            otp_record.delete()

            return render(
                request,
                'verify_otp.html',
                {'error': 'OTP Expired'}
            )

        request.session['otp_verified'] = True

        otp_record.delete()

        return redirect('/reset-password/')

    return render(
        request,
        'verify_otp.html'
    )


def reset_password(request):

    if not request.session.get('otp_verified'):

        return redirect('/forgot-password/')

    if request.method == "POST":

        password = request.POST.get('password')
        confirm = request.POST.get('confirm')

        if password != confirm:

            return render(
                request,
                'reset_password.html',
                {'error': 'Passwords do not match'}
            )

        email = request.session.get('reset_email')

        user = User.objects.get(email=email)

        user.set_password(password)
        user.save()

        request.session.flush()

        return redirect('/loginpage/')

    return render(
        request,
        'reset_password.html'
    )

# def forget(request):
#     return render(request,
#         'forgot_password.html')


def delete_data(request):
    data = json.loads(request.body)
    desc = data.get('desc')
    types= data.get('type')
    category= data.get('category')
    date= data.get('date')
    a= data.get('amount')
    amount = a.replace('₹','')
    # print('goted value')
    # print(amount)
    # print(date)
    # print(desc)
    # print(category)
    local_dt = datetime.strptime(date,"%d %b %Y, %H:%M:%S")
    print("local_dt :", local_dt)
    aware_dt = local_dt.replace(tzinfo=ZoneInfo("Asia/Kolkata"))
    print("aware_dt :", aware_dt)
    utc_dt = aware_dt.astimezone(ZoneInfo("UTC"))
    print("utc_dt :", utc_dt)
    goaldata = ADDGOALS.objects.filter(user=request.user)

    if types == 'INCOME':
        obj = Aincome.objects.filter(user=request.user,date__gte =utc_dt-timedelta(seconds=1), date__lte =utc_dt+timedelta(seconds=1), desc=desc, amount=float(amount), category=category).first()
        obj.delete()
        # print('Found:', obj.count())
        # status='Income Remove Successful'
    elif types == 'EXPENSE':
        if category == 'Goals':
            for item in goaldata:
                if item.goalname in desc and item.goaltype in desc and item.targetdate.strftime('%B') in desc and str(item.targetdate.year) in desc and str(int(item.targetamount)) in desc:
                    # print('Found')
                    obj = Aamount.objects.filter(user=request.user,desc=desc, amount=float(amount),
                                           category=category).first()
                    # print('Found:', )
                    obj.delete()

                else:
                    print('Not Found',item.goalname,item.goaltype,item.targetdate.strftime('%B'),str(item.targetdate.year),str(item.targetamount))
        else:
            obj = Aamount.objects.filter(user=request.user, date__gte =utc_dt-timedelta(seconds=1), date__lte =utc_dt+timedelta(seconds=1), desc=desc, amount=float(amount), category=category).first()
            obj.delete()
            # print('Found:', obj.count())
            status = 'Expense Remove Successful'
    else:
        status = 'There is something wrong, Check Transaction'

    print(desc)  # Hello Django!

    return JsonResponse({'status': 'Removed Successfully'})


def delete_data_budget(request):
    data = json.loads(request.body)
    spent = data.get('spent')
    cleanspent = re.sub(r"[₹,]","",spent)
    budget = data.get('budget')
    cleanbudget = re.sub(r"[₹,]","",budget)
    category = data.get('category')
    Remain = data.get('Remain')
    date2 = datetime.now()

    data1 = Budget.objects.filter(user=request.user)

    for item in data1:
        if item.spent == float(cleanspent) and item.category == category and item.budgeted == float(cleanbudget) and item.date.strftime('%B') in date2.strftime('%B') and item.date.year == date2.year:
            print("Found Budget")
            item.delete()
        else:
            print("Not Found", f" {item.spent} == {float(cleanspent)} and {item.category} == {category} and {item.budgeted} == {float(cleanbudget)} and {item.date.strftime('%B')} in {date2.strftime('%B')} and {item.date.year} == {date2.year}")

    return JsonResponse({'status': 'Budget removed successfully'})

from django.contrib.auth.models import User
# def user_data(request):
#     data = User.objects.filter(user=request.user)
#     username = request.User.username
#     email = request.user.email
#     date = datetime.today()
#     return JsonResponse({'username': username, 'email': email, 'date': date})

def user_data(request):
    if request.user.is_authenticated:
        return JsonResponse({"username": request.user.username, "email": request.user.email, "date":datetime.now().strftime("%d  %B  %Y")})
    else:
        return JsonResponse({"error":"User not Authenticated"},status=401)

