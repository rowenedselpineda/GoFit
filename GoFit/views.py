from django.shortcuts import render, get_object_or_404, redirect
from .forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login
from .models import *
from .forms import LoginForm


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Replace 'home' with the desired URL after successful login
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


def home_view(request):
    return render(request, 'home.html')


def class_list(request):
    classes = FitnessClass.objects.all()  # Retrieve all classes from the database
    print("Classes:", classes)  # Print the retrieved classes
    return render(request, 'class_list.html', {'classes': classes})


def class_detail(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)
    return render(request, 'class_detail.html', {'fitness_class': fitness_class})


@user_passes_test(lambda u: u.groups.filter(name='Trainer').exists())
@login_required
def add_class(request):
    if request.method == 'POST':
        form = FitnessClassForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = FitnessClassForm()
    return render(request, 'add_class.html', {'form': form})


@user_passes_test(lambda u: u.groups.filter(name='Trainer').exists())
@login_required
def delete_class(request, class_id):
    class_obj = get_object_or_404(FitnessClass, id=class_id)
    if request.method == 'POST':
        class_obj.delete()
        return redirect('class_list')
    return render(request, 'class_delete.html', {'class': class_obj})


def update_class(request, class_id):
    class_obj = get_object_or_404(FitnessClass, id=class_id)

    if request.method == 'POST':
        form = FitnessClassForm(request.POST, instance=class_obj)
        if form.is_valid():
            form.save()
            return redirect('class_list')
    else:
        form = FitnessClassForm(instance=class_obj)

    return render(request, 'update_class.html', {'form': form})


@login_required
def apply_class(request, class_id):
    fitness_class = get_object_or_404(FitnessClass, id=class_id)
    membership, created = Membership.objects.get_or_create(user=request.user, fitness_class=fitness_class)
    membership.is_member = True
    membership.save()
    return redirect('class_detail', class_id)


@login_required
def leave_class(request, membership_id):
    membership = get_object_or_404(Membership, id=membership_id, user=request.user)
    membership.is_member = False
    membership.save()
    return redirect('class_detail', membership.fitness_class.id)

