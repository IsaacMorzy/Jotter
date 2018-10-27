# ---------simple authentication tutorial using inbuilt user model------
# from django.contrib.auth.forms import UserCreationForm
#from django.core.urlresolvers import reverse
# from django.views.generic import CreateView
# to automatically create a new user using built-in UserRegistrationForm 

# the createview can display a modelform using a template and on submission can either redisplay 
# the page with errors if the form data was invalid or call the save method on the form and 
# redirect user to a configurable url

# ----------inside views.py of accounts app
class UserRegistrationView(CreateView):
    form_class = UserCreationForm()
    template_name = 'user_registration.html' 

    def get_success_url(self):
        return reverse('home)


# --------in the urls.py
# from django.conf.urls import url, include
# from django.contrib import admin
# from django.views.generic import TemplateView
# from accounts.views import UserRegistrationView

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'^new_user/$', UserRegistrationView.as_view(), name='user_registration'),
]

# a simple view to edit blog posts
# from django.utils import timezone
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)    # remember to define a ModelForm for the form
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

# a simple view to create a new post in blog model
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

# -----------how to restrict creation of a new model object using 
#restrict the blog creation view to only allow users to create a
# blog if they don't already have one. Import HttpResponseForbidden and the Blog
# model in blog/views
from django.http.response import HttpResponseForbidden
from .models import Blog
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

# add a dispatch method to the NewBlogView class

# dispatch method is one of the most useful methods to override on generic
# views. It is the frst method that is called when the view URL is hit, and decides
# based on the request type whether to call the get or post methods on the view class
# to process the request

@method_decorator(login_required)
def dispatch(self, request, *args, **kwargs):
    user = request.user
    if Blog.objects.filter(owner=user).exists():
        return HttpResponseForbidden('You cannot create more than one blog per account')
    else:
        return Super(NewBlogView, self).dispatch(request, *args, **kwargs)

