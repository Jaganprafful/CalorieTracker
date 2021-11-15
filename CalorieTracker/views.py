import datetime
from datetime import timedelta

from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.shortcuts import render, redirect

# Create your views here.
from django.utils import timezone
from django.views.generic import CreateView

from CalorieTracker.forms import *
from CalorieTracker.models import *


class SignUpView(CreateView):
    model = User
    form_class = CustomUserCreationForm
    template_name = 'signup.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'client'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        form.save()
        return redirect('login')


def signup(request):
    return render(request, 'signup.html')


@login_required
def home_view(request):
    current_date = datetime.date.today()
    try:
        client = Client.objects.get(user=request.user)
        profile = Profile.objects.filter(relatedClient=client, dateCreated=current_date)
        if profile.exists():
            return render(request, 'home.html', {'records': profile})
        else:
            Profile.objects.create(relatedClient=client, dateCreated=current_date)
            return render(request, 'home.html', {'records': profile})
    except Client.DoesNotExist:
        return render(request, 'home.html')


@login_required
def profile_view(request):
    client = Client.objects.get(user=request.user)
    clientp = Profile.objects.get(relatedClient=client)
    # get calorie count of last 7 days
    some_day_last_week = timezone.now().date() - timedelta(days=7)
    records = Profile.objects.filter(dateCreated__gte=some_day_last_week, dateCreated__lte=timezone.now().date(),
                                     relatedClient=client)
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        cform = ClientProfileForm(request.POST)
        if form.is_valid() and cform.is_valid():
            current_date = datetime.date.today()
            profile = Profile.objects.filter(relatedClient=client, dateCreated=current_date)
            c_goal = request.POST.get('caloriesGoal')
            if profile.exists():
                Profile.objects.filter(relatedClient=client, dateCreated=current_date).update(caloriesGoal=c_goal)
            else:
                Profile.objects.create(relatedClient=client, dateCreated=current_date, caloriesGoal=c_goal)
            age = request.POST.get('age')
            weight = request.POST.get('weight')
            height = request.POST.get('height')
            if age != '' and weight != '' and height != '':
                Client.objects.filter(user=request.user).update(age=age, weight=weight, height=height)

        return render(request, 'profile.html', {'form': form, 'cform': cform, 'records': records})

    else:
        form = ProfileForm(instance=clientp)
        cform = ClientProfileForm(instance=client)

    context = {'form': form, 'cform': cform, 'records': records}
    return render(request, 'profile.html', context)


def food_activities_view(request):
    current_date = datetime.date.today()
    if request.method == "POST":
        food_consumed = request.POST['food_consumed']
        consume = Food.objects.get(id=food_consumed)
        client = Client.objects.get(user=request.user)
        quantity = float(request.POST['quantity'])
        consume = ConsumedFood(relatedClient=client, relatedFood=consume, quantity=quantity)
        consume.save()
        profile = Profile.objects.filter(relatedClient=client, dateCreated=current_date)
        tfCal = consume.relatedFood.calories * quantity
        tfPro = consume.relatedFood.protein * quantity
        tfCrab = consume.relatedFood.carbs * quantity
        tfFats = consume.relatedFood.fats * quantity
        if profile.exists():
            Profile.objects.filter(relatedClient=client, dateCreated=current_date).update(
                totalCalorie=F('totalCalorie') + tfCal, totalProteins=F('totalProteins') + tfPro,
                totalCarbs=F('totalCarbs') + tfCrab, totalFats=F('totalFats') + tfFats)
        else:
            Profile.objects.create(relatedClient=client, dateCreated=current_date,
                                   totalCal=F('totalCal') + tfCal, totalProteins=F('totalProteins') + tfPro,
                                   totalCarbs=F('totalCarbs') + tfCrab, totalFats=F('totalFats') + tfFats)
        foods = Food.objects.all()
    else:
        foods = Food.objects.all()
    client = Client.objects.get(user=request.user)
    consumed_food = ConsumedFood.objects.filter(relatedClient=client, dateCreated=current_date)

    return render(request, 'food_activities.html', {'foods': foods, 'consumed_food': consumed_food})


def delete_consumed_food(request, id):
    consume = ConsumedFood.objects.get(id=id)
    current_date = datetime.date.today()
    if request.method == 'POST':
        client = Client.objects.get(user=request.user)
        profile = Profile.objects.filter(relatedClient=client, dateCreated=current_date)
        tfCal = consume.relatedFood.calories * consume.quantity
        tfPro = consume.relatedFood.protein * consume.quantity
        tfCrab = consume.relatedFood.carbs * consume.quantity
        tfFats = consume.relatedFood.fats * consume.quantity
        if profile.exists():
            Profile.objects.filter(relatedClient=client, dateCreated=current_date).update(
                totalCalorie=F('totalCalorie') - tfCal, totalProteins=F('totalProteins') - tfPro,
                totalCarbs=F('totalCarbs') - tfCrab, totalFats=F('totalFats') - tfFats)
        consume.delete()
        return redirect('food_activities')
    return render(request, 'delete_item.html')


def statistical_view(request):
    current_date = datetime.date.today()
    client = Client.objects.get(user=request.user)
    records = Profile.objects.filter(dateCreated=current_date, relatedClient=client)
    dataList = list(Profile.objects.filter(dateCreated=current_date, relatedClient=client))
    return render(request, 'statistical.html', {'records': records, 'list': dataList})
