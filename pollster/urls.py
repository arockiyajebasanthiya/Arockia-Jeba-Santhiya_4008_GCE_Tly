from django.urls import path, include
from django.contrib import admin
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from polls.views import profile

urlpatterns = [
    path('', include('pages.urls')),
    path('polls/', include('polls.urls')),
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),  # Include authentication URLs
    path('accounts/register/', CreateView.as_view(
        template_name='registration/register.html',
        form_class=UserCreationForm,
        success_url=reverse_lazy('login')  # Update the success URL
    ), name='register'),
    path('accounts/profile/', profile, name='profile'),  # Add the custom profile view
]

# Set the LOGIN_REDIRECT_URL
LOGIN_REDIRECT_URL = '/'
