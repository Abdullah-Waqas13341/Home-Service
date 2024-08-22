from django.shortcuts import render, redirect
from .forms import ServiceForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
@login_required
def services(request):
    return render(request, 'sellers/services.html')
@login_required
def post_service(request):
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.seller = request.user.seller
            service.status = 'Pending'
            service.save()
            messages.success(request, 'Service posted successfully')
            return redirect('sellers:services')  
    else:
        form = ServiceForm()
    
    return render(request, 'sellers/post_service.html', {'form': form})


# Create your views here.
