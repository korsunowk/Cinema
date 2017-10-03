from django.shortcuts import render_to_response, redirect, HttpResponse, render
from django.views.decorators.csrf import csrf_exempt, csrf_protect
from django.core.paginator import Paginator
from django.contrib import auth
from django.conf import settings

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from datetime import datetime, timedelta

from films.models import Film, Seans, Bilet, Bron, Sell
from kinouser.models import Kinouser
from guest_otziv.models import GuestOtziv, AdminOtziv
from otziv.models import Otziv
from .forms import UserCreateForm


def contact(request):
    args = dict()
    args['user'] = request.user
    return render_to_response('contact.html', args)


@csrf_protect
def guest(request):
    args = dict()
    args['user'] = request.user
    all_otzivs = otzivs = []

    for otziv_ in GuestOtziv.objects.all():
        otzivs.append(otziv_)
        try:
            otzivs.append(AdminOtziv.objects.get(guestOtziv=otziv_))
        except AdminOtziv.DoesNotExist:
            pass

        all_otzivs.append(otzivs.copy())
        otzivs.clear()
    args['otzivs'] = all_otzivs

    if request.POST:
        if request.POST.get('admin', '') == 'false':
            GuestOtziv(name=request.POST.get('name', ''), email=request.POST.get('email', ''),
                       text=request.POST.get('comment', ''), date=datetime.now().date()).save()
        elif request.POST.get('admin', '') == 'true':
            AdminOtziv(text=request.POST.get('comment', ''),
                       guestOtziv=GuestOtziv.objects.get(id=request.POST.get('guest_id', '')))
            .save()

        return redirect('/guest/')

    return render(request, 'guest.html', args)


def logout(request):
    auth.logout(request)
    return redirect("/")


@csrf_protect
def login(request):
    args = dict()
    if request.POST:
        email = request.POST.get('email', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(email=email, password=password)
        if user is not None and user.is_active:
            auth.login(request, user)
            args['user'] = request.user

            return redirect("/")
        else:
            args['login_error'] = "Net takovih"
            return render(request, 'signin.html', args)
    else:
        return render(request, 'signin.html', args)


@csrf_protect
def register(request):
    args = dict()
    args['form'] = UserCreateForm()
    if request.POST:
        newuser_form = UserCreateForm(request.POST)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['email'],
                                        password=newuser_form.cleaned_data['password2'])
            auth.login(request, newuser)

            return redirect('/')

        else:
            args['reg_error'] = 'Error.'
            args['form'] = newuser_form
    return render(request, 'registr.html', args)


def main(request, url_date=datetime.today().date(), page_number=1):
    tmp_args, tmp_args2 = dict(), dict()

    tmp_args['Понедельник'] = tmp_args2['Pon'] = 1
    tmp_args['Вторник'] = tmp_args2['Vt'] = 2
    tmp_args['Среда'] = tmp_args2['Sr'] = 3
    tmp_args['Четверг'] = tmp_args2['Cht'] = 4
    tmp_args['Пятница'] = tmp_args2['Pyat'] = 5
    tmp_args['Суббота'] = tmp_args2['Sub'] = 6
    tmp_args['Воскресенье'] = tmp_args2['Voskr'] = 7

    dates_for_weekday = dates = []
    dates.append((datetime.today().date().strftime('%Y-%m-%d'), 
                  datetime.isoweekday(datetime.today().date())))
    dates_for_weekday.append((datetime.today().date().strftime('%d.%m'), 
                              datetime.isoweekday(datetime.today().date())))

    for i in range(1, 7):
        dates_for_weekday.append(
            ((datetime.today().date() + timedelta(days=i)).strftime('%d.%m'),
             datetime.isoweekday((datetime.today().date() + timedelta(days=i)))))
        dates.append(
            ((datetime.today().date() + timedelta(days=i)).strftime('%Y-%m-%d'),
             datetime.isoweekday((datetime.today().date() + timedelta(days=i)))))

    def reverse_dictionary(dictionary):
        new_dictionary = dict()

        for key in dictionary:
            new_dictionary.setdefault(dictionary[key], key)
        return new_dictionary

    def fill_dates(_args, second_args, _dates):
        new_args = reverse_dictionary(_args)
        new_second_args = reverse_dictionary(second_args)
        for one_date in range(len(_dates)):
            _args[new_args[_dates[one_date][1]]] = _dates[one_date][0]
            second_args[new_second_args[_dates[one_date][1]]] = _dates[one_date][0]
        return _args, second_args

    args, args2 = fill_dates(tmp_args, tmp_args2, dates)

    args.update(args2)
    args['user'] = request.user
    args['date_url'] = str(url_date)
    args['for_date'] = datetime.strptime(str(url_date), '%Y-%m-%d').date()
    if isinstance(url_date, str):
        args['weekday'] = datetime.isoweekday(datetime.strptime(url_date, '%Y-%m-%d').date())
    else:
        args['weekday'] = datetime.isoweekday(url_date)
    seanss = Seans.objects.filter(date=str(url_date))
    a = b = []

    for seans_ in seanss:
        if seans_.film not in a:
            a.append(seans_.film)
            b.append(seans_)

    current_page = Paginator(b, 3)
    args['seanss'] = current_page.page(page_number)
    if len(b) == 0:
        args['net_seansov'] = True
    return render_to_response('test_film.html', args)


def mykino(request):
    args = dict()
    args['user'] = request.user
    return render_to_response('mykino.html', args)


def price(request):
    args = dict()
    args['user'] = request.user
    return render_to_response('price.html', args)


def seans(request, name=''):
    args = dict()
    seans_data = {}
    args['user'] = request.user
    film = Seans.objects.filter(film__url_name=name)

    if film:
        seanss = Seans.objects.filter(film__url_name=name,
                                      date__gt=(datetime.today().date() - timedelta(days=1)))
        args['seanss'] = seanss

        a = 0
        for i in range(10):
            date = datetime.today().date() + timedelta(days=a)
            a += 1
            if Seans.objects.filter(film__url_name=name, date=date):
                seans_data[str(date)] = []
                if (len(Seans.objects.filter(film__url_name=name, date=date))) > 1:
                    for i_ in range(len(Seans.objects.filter(film__url_name=name, date=date))):
                        if Seans.objects.filter(film__url_name=name, date=date)[i_].date == datetime.today().date():
                            seans_data[str(date)].append(
                                'Время сеанса : ' + str(Seans.objects.filter(film__url_name=name, date=date)[i_].time))
                            seans_data[str(date)].append(Seans.objects.filter(film__url_name=name, date=date)[i_].price)
                            seans_data[str(date)].append(
                                'seans_id=' + str(Seans.objects.filter(film__url_name=name, date=date)[i_].id))
                else:
                    if Seans.objects.filter(film__url_name=name, date=date)[0].date >= datetime.today().date():
                        seans_data[str(date)].append(
                            'Время сеанса : ' + str(Seans.objects.filter(film__url_name=name, date=date)[0].time))
                        seans_data[str(date)].append(Seans.objects.filter(film__url_name=name, date=date)[0].price)
                        seans_data[str(date)].append(
                            'seans_id=' + str(Seans.objects.filter(film__url_name=name, date=date)[0].id))

        args['film'] = Film.objects.filter(url_name=name)[0]
        args['seans_data'] = seans_data

        return render_to_response('seans.html', args)

    return redirect('/')


@csrf_exempt
def buy(request, seans_id):
    args = dict()
    if request.method == 'POST':
        user = request.user
        if request.POST.get('usluga', ) == 'buy':
            seans_id = Seans.objects.get(id=request.POST.get('seans_id', ''))
            new_bilets = request.POST.get('tikets', '')[:-1]

            for i in new_bilets.split(','):
                bilet = Bilet(row=i.split(':')[0], 
                              seat=i.split(':')[1], 
                              seans_id=seans_id, price=i.split(':')[2])
                bilet.save()
                user.bilets.add(bilet)

            return HttpResponse('ok', content_type='text/html')

        elif request.POST.get('usluga', ) == 'bron':
            seans_id = Seans.objects.get(id=request.POST.get('seans_id', ''))
            new_bilets = request.POST.get('tikets', '')[:-1]
            name_user = request.user.firstname + " " + request.user.lastname

            for i in new_bilets.split(','):
                bilet = Bron(row=i.split(':')[0], seat=i.split(':')[1], 
                             seans_id=seans_id, forname=name_user,
                             price=i.split(':')[2])
                bilet.save()
                user.bron.add(bilet)

            return HttpResponse('ok', content_type='text/html')
    else:
        seans_ = Seans.objects.filter(id=seans_id)
        args['user'] = request.user
        args['seans'] = seans_[0]
        red_bilet = ''
        black_bilet = ''
        for i in Bilet.objects.filter(seans_id=seans_id):
            red_bilet += (str(i.row) + ',' + str(i.seat)) + ";"

        for i in Bron.objects.filter(seans_id=seans_id):
            black_bilet += (str(i.row) + ',' + str(i.seat)) + ";"

        prices = seans_[0].price.split(',')
        price1 = prices[0]
        price2 = prices[1]
        args['price1'] = price1
        args['price2'] = price2
        args['red_bilet'] = red_bilet
        args['black_bilet'] = black_bilet
        if request.user.is_authenticated():
            args['user_name'] = request.user.firstname + " " + request.user.lastname

        return render(request, 'buy_window.html', args)


def soon(request, page_number=1):
    args = dict()
    args['user'] = request.user

    films = Film.objects.filter(prokat__gt=(datetime.today().date()) + timedelta(days=30))
    current_page = Paginator(films, 3)
    args['films'] = current_page.page(page_number)

    return render_to_response('soon.html', args)


def treler(request, name=''):
    args = dict()
    args['user'] = request.user

    film = Film.objects.filter(url_name=name)
    if film:
        args['filmm'] = film
        args['film'] = film[0]
        return render_to_response('treler.html', args)

    return redirect('/')


@csrf_protect
def otziv(request, name=''):
    args = dict()
    args['user'] = request.user
    args['film'] = Film.objects.filter(url_name=name)[0]
    args['comment'] = Otziv.objects.filter(film__url_name=name)
    if request.method == 'POST':
        Otziv(name=request.POST.get('name', ''), 
              email=request.POST.get('email', ''),
              text=request.POST.get('comment', ''), 
              film=Film.objects.get(url_name=name),
              date=datetime.now().date())
        .save()

        return render(request, 'otziv.html', args)
    else:
        if Film.objects.filter(url_name=name):
            return render(request, 'otziv.html', args)

    return redirect('/')


@csrf_exempt
def test_buy(request):
    seans_id = Seans.objects.get(id=request.POST.get('seans_id', ''))
    new_bilets = request.POST.get('tikets', '')[:-1]

    for i in new_bilets.split(','):
        Bilet(row=i[0], seat=i[2], seans_id=seans_id)

    return HttpResponse('ok', content_type='text/html')


def create_bilet(bilet):
    c = canvas.Canvas(settings.MEDIA_ROOT + "bilets.pdf", pagesize=(607, 265))

    c.drawImage(image="static/img/bilet.png", x=0, y=0)
    pdfmetrics.registerFont(TTFont('font', 'Arial.TTF'))
    pdfmetrics.registerFont(TTFont('test', 'static/fonts/BuxtonSketch.ttf'))
    c.setFont("font", 20)
    c.drawString(130, 170, 'Место в зале:')
    c.drawString(280, 170, 'Ряд: ' + str(bilet.row) + ',')
    c.drawString(360, 170, 'Место: 15' + str(bilet.seat))
    c.setFont("test", 28)
    c.drawString(130, 230, bilet.seans_id.film.name)
    c.setFont("font", 21)
    c.drawString(130, 120, str(bilet.seans_id.date))
    c.drawString(350, 120, bilet.seans_id.time)
    c.setFont("font", 25)
    c.drawString(30, 50, 'Цена: ' + str(bilet.price))
    c.setFont("font", 20)
    c.drawString(520, 230, str(bilet.id))

    c.showPage()

    c.save()

    # startfile(settings.MEDIA_ROOT + "bilets.pdf")


def print_bilet(request):
    admin = 'bilet_true'
    try:
        bilet = Bilet.objects.get(id=request.POST.get('id_bilet', ''))
        create_bilet(bilet)
    except Exception as e:
        print(e)
        admin = 'bilet_false'

    return kabinet(request, admin=admin)


def kabinet(request, page_number=1, admin='0'):
    args = dict()

    user = request.user
    args['user'] = user
    args['admin'] = admin

    if not request.user.is_authenticated():
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
                        if bilet not in bilets:
                            bilets.append(bilet)
                for bron in user.bron.all():
                    if bron.seans_id.date == date:
                        if bron in bilets:
                            pass
                        else:
                            bilets.append(bron)

            current_page = Paginator(bilets, 6)
            args['bilets'] = current_page.page(page_number)

        else:
            if admin == 'bilet_true':
                args['user_name'] = Kinouser.objects.get(
                    bilets=Bilet.objects.get(id=request.POST.get('id_bilet', ''))).lastname
                args['seans_name'] = Bilet.objects.get(id=request.POST.get('id_bilet', '')).seans_id.film.name

            elif admin == 'bilet_false':
                args['error'] = 'Данного билета не существует. Проверьте правильность кода билета.'

            elif admin == 'seans_true':
                my_seans = Seans.objects.get(id=request.POST.get('id_seans', ''))
                args['seans_date'] = my_seans.date
                args['seans_name'] = my_seans.film.name
                args['seans_time'] = my_seans.time

            elif admin == 'seans_false':
                args['seans_false'] = 'На данный сеанс еще не проданы билеты.'

            elif admin == 'date_null' or admin == 'date_false':
                args['date_error'] = 'На данный день нет купленных билетов.'

    return render_to_response('kabinet.html', args)


def print_otchet(request, variety):
    if variety == 'seans':
        admin = 'seans_true'
        try:
            sells = [Sell.objects.get(seans_id=request.POST.get('id_seans', ''))]
            create_otchet(sells, 'seans')
        except Exception as e:
            print(e)
            admin = 'seans_false'

        return kabinet(request, admin=admin)

    elif variety == 'date':
        admin = 'date_true'
        try:
            sells = Sell.objects.filter(seans_id__date=request.POST.get('date_seans', ''))
            if sells.count() > 0:
                create_otchet(sells, 'date')
            else:
                admin = 'date_null'
        except Exception as e:
            print(e)
            admin = 'date_false'

        return kabinet(request, admin=admin)

    elif variety == 'interval':
        admin = 'interval_true'
        try:
            sells = Sell.objects.filter(
                seans_id__date__range=[request.POST.get('date1_seans', ''), 
                                       request.POST.get('date2_seans', '')])
            create_otchet(sells, 'interval')
        except Exception as e:
            print(e)
            admin = 'interval_false'

        return kabinet(request, admin=admin)

    elif variety == 'week':
        admin = 'week_true'
        try:
            today = datetime.now().date()
            week = datetime.today().date() - timedelta(days=7)
            sells = Sell.objects.filter(seans_id__date__range=[week, today])

            create_otchet(sells, 'week')
        except Exception as e:
            print(e)
            admin = 'week_false'

        return kabinet(request, admin=admin)

    elif variety == 'month':
        admin = 'month_true'
        try:
            today = datetime.now().date()
            month = datetime.today().date() - timedelta(days=30)
            sells = Sell.objects.filter(seans_id__date__range=[month, today])

            create_otchet(sells, 'month')
        except Exception as e:
            print(e)
            admin = 'month_false'

        return kabinet(request, admin=admin)
    elif variety == 'halfyear':
        admin = 'half_true'
        try:
            today = datetime.now().date()
            halfyear = datetime.today().date() - timedelta(days=180)
            sells = Sell.objects.filter(seans_id__date__range=[halfyear, today])
            create_otchet(sells, 'halfyear')
        except Exception as e:
            print(e)
            admin = 'half_false'

        return kabinet(request, admin=admin)
    return kabinet(request)


def create_otchet(selss, variety):
    c = canvas.Canvas(settings.MEDIA_ROOT + "report.pdf")
    pdfmetrics.registerFont(TTFont('font', 'Arial.TTF'))
    pdfmetrics.registerFont(TTFont('test', 'static/fonts/BuxtonSketch.ttf'))
    c.setFont("test", 20)

    if variety == 'seans':
        c.drawString(130, 800, 'Отчет по продаже билетов кинотеатра за сеанс')
    elif variety == 'date':
        c.drawString(130, 800, 'Отчет по продаже билетов кинотеатра по дате')
    elif variety == 'interval':
        c.drawString(130, 800, 'Отчет по продаже билетов кинотеатра по датам')
    elif variety == 'week':
        c.drawString(130, 800, 'Отчет по продаже билетов кинотеатра за неделю')
    elif variety == 'month':
        c.drawString(130, 800, 'Отчет по продаже билетов кинотеатра за месяц')
    elif variety == 'halfyear':
        c.drawString(130, 800, 'Отчет по продаже билетов кинотеатра за полгода')

    c.line(50, 780, 550, 780)
    c.line(50, 50, 550, 50)
    y = 740
    k = 1
    index = 1
    for i in selss:
        if k == 6:
            c.showPage()
            c.setFont("test", 20)
            c.drawString(160, 800, 'Отчет по продаже билетов кинотеатра')
            c.line(50, 780, 550, 780)
            c.line(50, 50, 550, 50)
            k = 1
            y = 740
        c.drawString(50, y, str(index))
        c.drawString(100, y, i.seans_id.film.name)
        c.drawString(160, y - 25, 'Дата сеанса:')
        c.drawString(160, y - 50, 'Время сеанса:')
        c.drawString(160, y - 75, 'Количество проданных билетов: ')
        c.drawString(160, y - 100, 'Общая выручка : ')
        c.drawString(465, y - 25, str(i.seans_id.date))
        c.drawString(465, y - 50, str(i.seans_id.time))
        c.drawString(465, y - 75, str(i.kol_bil))
        c.drawString(465, y - 100, str(i.summa) + " грн")
        y -= 140
        k += 1
        index += 1

    c.save()
    c.showPage()

    # startfile(settings.MEDIA_ROOT + 'report.pdf')
