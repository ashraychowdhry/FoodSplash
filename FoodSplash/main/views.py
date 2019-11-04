from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib.auth import login as login_user
from django.contrib.auth import logout as logout_user

from FoodSplash import settings
from . import models
# Create your views here.


def index(request):

    return render(request, 'main/index.html', {})


def signup(request):

    if request.method == "POST":

        if not request.POST.get('password') == request.POST.get('c_password'):
            return render(request, 'main/signup.html', {"toast": {"msg": "passwords do not match", "cls": "red lighten-1"}})

        user = models.User()
        user.username = request.POST.get('email')
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.set_password(raw_password=request.POST.get('password'))
        user.save()

        address = models.Address()
        address.street = request.POST.get('street')
        address.city = request.POST.get('city')
        address.state = request.POST.get('state')
        address.zip = request.POST.get('zip')
        address.save()

        fs = models.FSUser()
        fs.user = user
        fs.address = address
        fs.save()

        return render(request, 'main/signup.html', {"toast": {"msg": "Successful, please login now", "cls": "green lighten-1"}})

    return render(request, 'main/signup.html', {})


def login(request):
    if request.user.is_authenticated:
        return redirect("/console")

    if request.method == 'POST':
        username = request.POST['username'].lower().strip()
        password = request.POST['password'].strip()

        user = authenticate(username=username, password=password)

        if user is not None:
            login_user(request, user)

            if request.GET.get('next') is not None:
                return redirect(request.GET['next'])
            return redirect('/console')

        else:
            return render(request, 'main/login.html', {
                "continue": request.GET.get('next'),
                'error': 'invalid',
            })

    return render(request, 'main/login.html', {"continue": request.GET.get('next')})


@login_required
def logout(request):
    logout_user(request)
    return redirect('/login')


@login_required()
def console(request):
    if request.user.is_staff:
        return redirect('/staff')

    toast = None

    fs = models.FSUser.objects.get(user=request.user)
    drops = models.DropSite.objects.all()
    dons = models.Donation.objects.filter(fs_user=fs)

    if request.method == "POST":
        drop_site = models.DropSite.objects.get(id=request.POST.get("d_id"))

        p = models.Promise()
        p.fs_user = fs
        p.drop_site = drop_site
        p.save()

        send_email(to=fs.user.email, subject="Thank You for committing to donate", body="""
            {}, 
            Thank you for agreeing to help to your community.
            A reminder that you are responsible for making it to the drop site.
            Please see below for information on when and how to make your donation.
            Please check our website for details on donation policy and the points system.
            You will receive an email when an associate has confirmed that you have followed your commitment.
            Please Don't hesitate to reach out to us about any questions at foodsplashnj@gmail.com 
            FoodSplash and your community thank you for your generosity. 

            Drop Site Notes:
            Address: {}

            Instructions: {}

            Contact email: {}

            Thank You,
            - Team FoodSplash

        """.format(fs.user.first_name, drop_site.address, drop_site.notes, drop_site.email))

        toast = {"msg": "Thank You", "cls": "teal white-text"}

    promises = [p.drop_site.id for p in models.Promise.objects.filter(fs_user=fs)]

    return render(request, 'main/console.html', {
        "fs": fs, "drop_sites": drops, "dons": dons, "promises": promises, "toast": toast
    })


@staff_member_required
def staff(request):

    promises = []
    for ds in models.DropSite.objects.all():
        promises.append({
            "dropsite": ds,
            "promises": models.Promise.objects.filter(drop_site=ds)
        })

    if request.method == "POST":

        D = request.POST.get

        if D('form_type') == "verify":
            p_id = D('p_id')
            pr = models.Promise.objects.get(id=p_id)

            u = pr.fs_user
            u.points = u.points + int(D('points'))
            u.save()

            don = models.Donation()
            don.fs_user = pr.fs_user
            don.drop_site = pr.drop_site
            don.points = int(D('points'))
            don.save()

            pr.delete()

            send_email(u.user.email, subject="Your contribution was confirmed", body="""
            {},
            Your contribution was just confirmed by our staff and your {} points have been awarded to you. 
            When you login you will see that the drop site has been reset for you. This is so you can donate again!
            Your community appreciates your contribution!
            
            Thank You,
            - Team FoodSplash
            """. format(u.user.first_name, don.points))

        if D('form_type') == "dropsite":
            address = models.Address()
            address.street = D('street')
            address.city = D('city')
            address.state = D('state')
            address.zip = D('zip')
            address.save()

            ds = models.DropSite()
            ds.address = address
            ds.notes = D('notes')
            ds.email = D('email')
            ds.save()

    return render(request, 'main/staff.html', {
        "promises": promises
    })


def send_email(to, subject, body):
    try:
        if settings.PRODUCTION:
            from google.appengine.api.mail import send_mail
            from google.appengine.ext import deferred
            deferred.defer(send_mail, subject=subject, body=body, sender='FoodSplashNJ@gmail.com', to=to )

    except Exception as e:
        raise e


def createsuperuser(request):
    """
    Creates a superuser only if it does not exist already.
    Should be used on new production environments for easy access to the admin panel
    Redirect to login if successful, else redirect to index
    """

    user = models.User()
    user.username = 'admin'  # change later
    user.email = 'mayaankvad@gmail.com'
    user.set_password("qazwsxed")
    user.is_staff = True
    user.is_superuser = True

    if models.User.objects.filter(username=user.username).exists():
        return redirect('/')
    else:
        user.save()
        return redirect('/console')
