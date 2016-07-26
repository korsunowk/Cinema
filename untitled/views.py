from django.shortcuts import render_to_response, redirect, HttpResponse
from django.core.context_processors import csrf
from films.models import Film, Seans, Bilet, Bron, Sell
from django.core.paginator import Paginator
from datetime import datetime, timedelta
from django.contrib import auth
from django.core.mail import send_mail
from .forms import UserCreateForm
from kinouser.models import Kinouser
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.csrf import csrf_exempt
from otziv.models import Otziv
from guest_otziv.models import GuestOtziv, AdminOtziv
from os import startfile
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from django.conf import settings

def contact(request):
    args={}
    args.update(csrf(request))
    args['user'] = request.user
    return render_to_response('contact.html',args)

def guest(request):
    args={}
    args.update(csrf(request))
    args['user'] = request.user
    all_otzivs = []
    otzivs = []
    for otziv in GuestOtziv.objects.all():
        otzivs.append(otziv)
        try:
            otzivs.append(AdminOtziv.objects.get(guestOtziv=otziv))
        except AdminOtziv.DoesNotExist:
            pass

        all_otzivs.append(otzivs.copy())
        otzivs.clear()
    args['otzivs'] = all_otzivs

    if request.POST:
        if request.POST.get('admin','') == 'false':
            GuestOtziv(name=request.POST.get('name',''),email=request.POST.get('email',''),\
                text=request.POST.get('comment',''),date=datetime.now().date()).save()
        elif request.POST.get('admin','') == 'true':
            AdminOtziv(text=request.POST.get('comment',''),\
                       guestOtziv=GuestOtziv.objects.get(id=request.POST.get('guest_id',''))).save()

        return redirect('/guest/')

    return render_to_response('guest.html',args)


def logout(request):
    auth.logout(request)
    return redirect("/")

def login(request):
    args={}
    args.update(csrf(request))
    if request.POST:
        email = request.POST.get('email','')
        password = request.POST.get('password','')
        user= auth.authenticate(email=email,password=password)
        if user is not None and user.is_active:
            auth.login(request,user)
            args['user'] = request.user

            return redirect("/")
        else:
            args['login_error'] = "Net takovih"
            return render_to_response('signin.html',args)
    else:
        return render_to_response('signin.html',args)


def register(request):
    args={}
    args.update(csrf(request))
    args['form'] = UserCreateForm()
    if request.POST:
        newuser_form = UserCreateForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['email'], \
                                        password = newuser_form.cleaned_data['password2'])
            auth.login(request,newuser)

            return redirect('/')

        else:
            args['reg_error'] = 'Error.'
            args['form'] = newuser_form
    return render_to_response('registr.html', args)



def main(request,url_date=datetime.today().date(), page_number=1):
    args={}
    args.update(csrf(request))
    args['user'] = request.user

    dates_for_weekday=[]
    dates = []
    dates.append(datetime.today().date().strftime('%Y-%m-%d'))
    dates_for_weekday.append(datetime.today().date().strftime('%d.%m'))

    for i in range(1,8):
        dates_for_weekday.append((datetime.today().date() + timedelta(days=i)).strftime('%d.%m'))
        dates.append((datetime.today().date() + timedelta(days=i)).strftime('%Y-%m-%d'))

    date_iterator = datetime.weekday(datetime.today().date())


    args['weekday'] = datetime.weekday(datetime.strptime(str(url_date),'%Y-%m-%d').date())

    if date_iterator == 0:
        args['Понедельник'] = dates_for_weekday[0]
        args['Вторник'] = dates_for_weekday[1]
        args['Среда'] = dates_for_weekday[2]
        args['Четверг'] =dates_for_weekday[3]
        args['Пятница'] = dates_for_weekday[4]
        args['Суббота'] = dates_for_weekday[5]
        args['Воскресенье'] =dates_for_weekday[6]
        args['Pon'] = dates[0]
        args['Vt'] = dates[1]
        args['Sr'] = dates[2]
        args['Cht'] = dates[3]
        args['Pyat'] = dates[4]
        args['Sub'] = dates[5]
        args['Voskr'] = dates[6]
    elif date_iterator == 1:
        args['Понедельник'] = dates_for_weekday[6]
        args['Вторник'] = dates_for_weekday[0]
        args['Среда'] = dates_for_weekday[1]
        args['Четверг'] =dates_for_weekday[2]
        args['Пятница'] = dates_for_weekday[3]
        args['Суббота'] = dates_for_weekday[4]
        args['Воскресенье'] =dates_for_weekday[5]
        args['Pon'] = dates[6]
        args['Vt'] = dates[0]
        args['Sr'] = dates[1]
        args['Cht'] = dates[2]
        args['Pyat'] = dates[3]
        args['Sub'] = dates[4]
        args['Voskr'] = dates[5]
    elif date_iterator == 2:
        args['Понедельник'] = dates_for_weekday[5]
        args['Вторник'] = dates_for_weekday[6]
        args['Среда'] = dates_for_weekday[0]
        args['Четверг'] =dates_for_weekday[1]
        args['Пятница'] = dates_for_weekday[2]
        args['Суббота'] = dates_for_weekday[3]
        args['Воскресенье'] =dates_for_weekday[4]
        args['Pon'] = dates[5]
        args['Vt'] = dates[6]
        args['Sr'] = dates[0]
        args['Cht'] = dates[1]
        args['Pyat'] = dates[2]
        args['Sub'] = dates[3]
        args['Voskr'] = dates[4]
    elif date_iterator == 3:
        args['Понедельник'] = dates_for_weekday[4]
        args['Вторник'] = dates_for_weekday[5]
        args['Среда'] = dates_for_weekday[6]
        args['Четверг'] =dates_for_weekday[0]
        args['Пятница'] = dates_for_weekday[1]
        args['Суббота'] = dates_for_weekday[2]
        args['Воскресенье'] =dates_for_weekday[3]
        args['Pon'] = dates[4]
        args['Vt'] = dates[5]
        args['Sr'] = dates[6]
        args['Cht'] = dates[0]
        args['Pyat'] = dates[1]
        args['Sub'] = dates[2]
        args['Voskr'] = dates[3]
    elif date_iterator == 4:
        args['Понедельник'] = dates_for_weekday[3]
        args['Вторник'] = dates_for_weekday[4]
        args['Среда'] = dates_for_weekday[5]
        args['Четверг'] =dates_for_weekday[6]
        args['Пятница'] = dates_for_weekday[0]
        args['Суббота'] = dates_for_weekday[1]
        args['Воскресенье'] =dates_for_weekday[2]
        args['Pon'] = dates[3]
        args['Vt'] = dates[4]
        args['Sr'] = dates[5]
        args['Cht'] = dates[6]
        args['Pyat'] = dates[0]
        args['Sub'] = dates[1]
        args['Voskr'] = dates[2]
    elif date_iterator == 5:
        args['Понедельник'] = dates_for_weekday[2]
        args['Вторник'] = dates_for_weekday[3]
        args['Среда'] = dates_for_weekday[4]
        args['Четверг'] =dates_for_weekday[5]
        args['Пятница'] = dates_for_weekday[6]
        args['Суббота'] = dates_for_weekday[0]
        args['Воскресенье'] =dates_for_weekday[1]
        args['Pon'] = dates[2]
        args['Vt'] = dates[3]
        args['Sr'] = dates[4]
        args['Cht'] = dates[5]
        args['Pyat'] = dates[6]
        args['Sub'] = dates[0]
        args['Voskr'] = dates[1]
    elif date_iterator == 6:
        args['Понедельник'] = dates_for_weekday[1]
        args['Вторник'] = dates_for_weekday[2]
        args['Среда'] = dates_for_weekday[3]
        args['Четверг'] =dates_for_weekday[4]
        args['Пятница'] = dates_for_weekday[5]
        args['Суббота'] = dates_for_weekday[6]
        args['Воскресенье'] =dates_for_weekday[0]
        args['Pon'] = dates[1]
        args['Vt'] = dates[2]
        args['Sr'] = dates[3]
        args['Cht'] = dates[4]
        args['Pyat'] = dates[5]
        args['Sub'] = dates[6]
        args['Voskr'] = dates[0]


    args['date_url'] = str(url_date)
    args['for_date'] = datetime.strptime(str(url_date),'%Y-%m-%d').date()

    seanss = Seans.objects.filter(date=str(url_date))
    a = b = []
    
    for seans in seanss:
        if seans.film not in a:
            a.append(seans.film)
            b.append(seans)


    current_page = Paginator(b,3)
    args['seanss'] = current_page.page(page_number)
    if len(b) == 0:
        args['net_seansov'] = True
    return render_to_response('test_film.html',args)

def mykino(request):
    args={}
    args.update(csrf(request))
    args['user'] = request.user
    return render_to_response('mykino.html',args)

def price(request):
    args={}
    args.update(csrf(request))
    args['user'] = request.user
    return render_to_response('price.html',args)

def seans(request, name=''):
    args={}
    args.update(csrf(request))
    seans_data = {}
    args['user'] = request.user
    film=Seans.objects.filter(film__url_name=name)

    if film:
        seanss = Seans.objects.filter(film__url_name=name, \
                        date__gt=(datetime.today().date() - timedelta(days=1)))
        args['seanss'] = seanss

        a = 0
        for i in range(10):
            date = datetime.today().date() + timedelta(days=a)
            a+=1
            if Seans.objects.filter(film__url_name=name,date=date):
                seans_data[str(date)] = []
                if (len(Seans.objects.filter(film__url_name=name,date=date))) > 1:
                    for i in range(len(Seans.objects.filter(film__url_name=name,date=date))):
                        #if datetime.strptime(Seans.objects.filter(film__url_name=name,date=date)[i].time,'%H:%M').time()<=datetime.now().time()\
                        #        and Seans.objects.filter(film__url_name=name,date=date)[i].date == datetime.today().date():
                        #    pass
                        if Seans.objects.filter(film__url_name=name,date=date)[i].date == datetime.today().date():
                        #else:
                            seans_data[str(date)].append('Время сеанса : '+ str(Seans.objects.filter(film__url_name=name,date=date)[i].time))
                            seans_data[str(date)].append(Seans.objects.filter(film__url_name=name,date=date)[i].price)
                            seans_data[str(date)].append('seans_id='+str(Seans.objects.filter(film__url_name=name,date=date)[i].id))
                else:
                    #if datetime.strptime(Seans.objects.filter(film__url_name=name,date=date)[0].time,'%H:%M').time()<=datetime.now().time()\
                    #    and Seans.objects.filter(film__url_name=name,date=date)[0].date >= datetime.today().date():
                    #    pass
                    #else:
                    if Seans.objects.filter(film__url_name=name,date=date)[0].date >= datetime.today().date():
                        seans_data[str(date)].append('Время сеанса : '+ str(Seans.objects.filter(film__url_name=name,date=date)[0].time))
                        seans_data[str(date)].append(Seans.objects.filter(film__url_name=name,date=date)[0].price)
                        seans_data[str(date)].append('seans_id='+str(Seans.objects.filter(film__url_name=name,date=date)[0].id))

        args['film'] = Film.objects.filter(url_name=name)[0]
        args['seans_data'] = seans_data
		
		
        return render_to_response('seans.html',args)
	
    return redirect('/')

@csrf_exempt
def buy(request, seans_id):
    args = {}
    args.update(csrf(request))
    if request.method == 'POST':
        user = request.user
        if request.POST.get('usluga',) == 'buy':
            seans_id = Seans.objects.get(id=request.POST.get('seans_id',''))
            new_bilets = request.POST.get('tikets','')[:-1]

            for i in new_bilets.split(','):
                bilet = Bilet(row=i.split(':')[0],seat=i.split(':')[1],seans_id=seans_id,price=i.split(':')[2])
                bilet.save()
                user.bilets.add(bilet)


            return HttpResponse('ok', content_type='text/html')

        elif request.POST.get('usluga',) == 'bron':
            seans_id = Seans.objects.get(id=request.POST.get('seans_id',''))
            new_bilets = request.POST.get('tikets','')[:-1]
            name_user = request.user.firstname + " " + request.user.lastname

            for i in new_bilets.split(','):
                bilet = Bron(row=i.split(':')[0],seat=i.split(':')[1],seans_id=seans_id,forname=name_user,price=i.split(':')[2])
                bilet.save()
                user.bron.add(bilet)

            return HttpResponse('ok', content_type='text/html')
    else:
        seans = Seans.objects.filter(id=seans_id)
        args['user'] = request.user
        args['seans'] = seans[0]
        red_bilet = ''
        black_bilet = ''
        for i in Bilet.objects.filter(seans_id=seans_id):
            red_bilet+=(str(i.row)+','+str(i.seat))+";"

        for i in Bron.objects.filter(seans_id=seans_id):
            black_bilet+=(str(i.row)+','+str(i.seat))+";"

        prices = (seans[0].price).split(',')
        price1=prices[0]
        price2=prices[1]
        args['price1'] = price1
        args['price2'] = price2
        args['red_bilet']=red_bilet
        args['black_bilet']=black_bilet
        if request.user.is_authenticated():
            args['user_name'] = request.user.firstname + " " + request.user.lastname

        return render_to_response('buy_window.html',args)

def soon(request, page_number=1):
    args={}
    args.update(csrf(request))
    args['user'] = request.user

    films = Film.objects.filter(prokat__gt=(datetime.today().date())+timedelta(days=30))
    current_page = Paginator(films,3)
    args['films'] = current_page.page(page_number)

    return render_to_response('soon.html',args)

def treler(request, name=''):
    args={}
    args.update(csrf(request))
    args['user'] = request.user

    film = Film.objects.filter(url_name=name)
    if film:
        args['filmm'] = film
        args['film'] = film[0]
        return render_to_response('treler.html',args)

    return redirect('/')

def otziv(request, name=''):
    args={}
    args.update(csrf(request))
    args['user'] = request.user
    args['film'] = Film.objects.filter(url_name=name)[0]
    args['comment'] = Otziv.objects.filter(film__url_name=name)
    if request.method == 'POST':
        Otziv(name=request.POST.get('name',''),email=request.POST.get('email',''),\
              text=request.POST.get('comment',''),film=Film.objects.get(url_name=name),date=datetime.now().date()).save()

        return render_to_response('otziv.html',args)
    else:
        if Film.objects.filter(url_name=name):
            return render_to_response('otziv.html',args)

    return redirect('/')

@csrf_exempt
def test_buy(request):
    seans_id = Seans.objects.get(id=request.POST.get('seans_id',''))
    new_bilets = request.POST.get('tikets','')[:-1]

    for i in new_bilets.split(','):
        Bilet(row=i[0],seat=i[2],seans_id=seans_id)

    return HttpResponse('ok', content_type='text/html')

def create_bilet(bilet):

    c = canvas.Canvas(settings.MEDIA_ROOT+"bilets.pdf",pagesize=(607,265))

    c.drawImage(image="static/img/bilet.png",x=0,y=0)
    pdfmetrics.registerFont(TTFont('font','Arial.TTF'))
    pdfmetrics.registerFont(TTFont('test','static/fonts/BuxtonSketch.ttf'))
    c.setFont("font",20)
    c.drawString(130,170,'Место в зале:')
    c.drawString(280,170,'Ряд: '+str(bilet.row)+',')
    c.drawString(360,170,'Место: 15'+str(bilet.seat))
    c.setFont("test",28)
    c.drawString(130,230, bilet.seans_id.film.name)
    c.setFont("font",21)
    c.drawString(130,120, str(bilet.seans_id.date))
    c.drawString(350,120, bilet.seans_id.time)
    c.setFont("font",25)
    c.drawString(30,50,'Цена: '+str(bilet.price))
    c.setFont("font",20)
    c.drawString(520,230, str(bilet.id))

    c.showPage()

    c.save()

    startfile(settings.MEDIA_ROOT+"bilets.pdf")

def print_bilet(request):
    admin = 'bilet_true'
    try:
        bilet = Bilet.objects.get(id=request.POST.get('id_bilet',''))
        create_bilet(bilet)
    except:
        admin = 'bilet_false'

    return kabinet(request,admin=admin)

def kabinet(request, page_number=1,admin='0'):
    args={}
    args.update(csrf(request))
    user = request.user
    args['user'] = user
    args['admin'] = admin


    if request.user.is_authenticated() == False:
        return redirect('/')
    else:
        if not request.user.is_superuser:

            dates = []
            for bilet in user.bilets.all():
                dates.append(Seans.objects.get(id=bilet.seans_id.id).date)

            for bron in user.bron.all():
                dates.append(Seans.objects.get(id=bron.seans_id.id).date)
            dates.sort()
            dates.reverse()
            bilets = []

            for date in dates:
                for bilet in user.bilets.all():
                    if bilet.seans_id.date == date:
                        if bilet in bilets:
                            pass
                        else:
                            bilets.append(bilet)
                for bron in user.bron.all():
                    if bron.seans_id.date == date:
                        if bron in bilets:
                            pass
                        else:
                            bilets.append(bron)

            current_page = Paginator(bilets,6)
            args['bilets'] = current_page.page(page_number)

        else:
            if admin == 'bilet_true':
                args['user_name'] = Kinouser.objects.get(bilets=Bilet.objects.get(id=request.POST.get('id_bilet',''))).lastname
                args['seans_name'] = Bilet.objects.get(id=request.POST.get('id_bilet','')).seans_id.film.name

            elif admin == 'bilet_false':
                args['error'] = 'Данного билета не существует. Проверьте правильность кода билета.'

            elif admin == 'seans_true':
                my_seans = Seans.objects.get(id=request.POST.get('id_seans',''))
                args['seans_date'] = my_seans.date
                args['seans_name'] = my_seans.film.name
                args['seans_time'] = my_seans.time

            elif admin == 'seans_false':
                args['seans_false'] = 'На данный сеанс еще не проданы билеты.'

            elif admin == 'date_null' or admin == 'date_false':
                args['date_error'] = 'На данный день нет купленных билетов.'

    return render_to_response('kabinet.html',args)


def print_otchet(request,variety):

    if variety == 'seans':
        admin = 'seans_true'
        try:
            sells = [Sell.objects.get(seans_id=request.POST.get('id_seans',''))]
            create_otchet(sells,'seans')
        except:
            admin = 'seans_false'

        return kabinet(request,admin=admin)

    elif variety == 'date':
        admin = 'date_true'
        try:
            sells = Sell.objects.filter(seans_id__date=request.POST.get('date_seans',''))
            if sells.count() > 0 :
                create_otchet(sells,'date')
            else:
                admin = 'date_null'
        except:
            admin = 'date_false'

        return kabinet(request,admin=admin)

    elif variety == 'interval':
        admin = 'interval_true'
        try:
            sells = Sell.objects.filter(seans_id__date__range=[request.POST.get('date1_seans',''),request.POST.get('date2_seans','')])
            create_otchet(sells,'interval')
        except:
            admin = 'interval_false'

        return kabinet(request,admin=admin)

    elif variety == 'week':
        admin = 'week_true'
        try:
            today = datetime.now().date()
            week = datetime.today().date()-timedelta(days=7)
            sells = Sell.objects.filter(seans_id__date__range=[week, today])

            create_otchet(sells,'week')
        except:
            admin = 'week_false'

        return kabinet(request,admin=admin)

    elif variety == 'month':
        admin = 'month_true'
        try:
            today = datetime.now().date()
            month = datetime.today().date()-timedelta(days=30)
            sells = Sell.objects.filter(seans_id__date__range=[month, today])

            create_otchet(sells,'month')
        except:
            admin = 'month_false'

        return kabinet(request,admin=admin)
    elif variety == 'halfyear':
        admin = 'half_true'
        try:
            today = datetime.now().date()
            halfyear = datetime.today().date()-timedelta(days=180)
            sells = Sell.objects.filter(seans_id__date__range=[halfyear, today])
            create_otchet(sells,'halfyear')
        except:
            admin = 'half_false'

        return kabinet(request,admin=admin)
    return kabinet(request)


def create_otchet(selss, variety):

    c = canvas.Canvas(settings.MEDIA_ROOT+"report.pdf")
    pdfmetrics.registerFont(TTFont('font','Arial.TTF'))
    pdfmetrics.registerFont(TTFont('test','static/fonts/BuxtonSketch.ttf'))
    c.setFont("test",20)

    if variety == 'seans':
        c.drawString(130,800,'Отчет по продаже билетов кинотеатра за сеанс')
    elif variety == 'date':
        c.drawString(130,800,'Отчет по продаже билетов кинотеатра по дате')
    elif variety == 'interval':
        c.drawString(130,800,'Отчет по продаже билетов кинотеатра по датам')
    elif variety == 'week':
        c.drawString(130,800,'Отчет по продаже билетов кинотеатра за неделю')
    elif variety == 'month':
        c.drawString(130,800,'Отчет по продаже билетов кинотеатра за месяц')
    elif variety == 'halfyear':
        c.drawString(130,800,'Отчет по продаже билетов кинотеатра за полгода')

    c.line(50,780,550,780)
    c.line(50,50,550,50)
    y = 740
    k=1
    index=1
    for i in selss:
        if (k==6):
            c.showPage()
            c.setFont("test",20)
            c.drawString(160,800,'Отчет по продаже билетов кинотеатра')
            c.line(50,780,550,780)
            c.line(50,50,550,50)
            k=1
            y=740
        c.drawString(50,y, str(index))
        c.drawString(100,y, i.seans_id.film.name)
        c.drawString(160,y-25,'Дата сеанса :')
        c.drawString(160,y-50,'Время сеанса :')
        c.drawString(160,y-75,'Количество проданных билетов : ')
        c.drawString(160,y-100,'Общая выручка : ')
        c.drawString(465,y-25, str(i.seans_id.date))
        c.drawString(465,y-50, str(i.seans_id.time))
        c.drawString(465,y-75, str(i.kol_bil))
        c.drawString(465,y-100, str(i.summa)+" грн")
        y-=140
        k+=1
        index+=1

    c.save()
    c.showPage()

    startfile(settings.MEDIA_ROOT+'report.pdf')
