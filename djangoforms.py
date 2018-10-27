#######inside the forms.py######

import django
from django import forms
from django.http import HttpResponseRedirect
from django.core.mail import send_mail  # i didnt know this!! :)


class ContactForm(forms.Form):
    subject = forms.CharField()
    email = forms.EmailField(required=False)
    message = forms.CharField(widget=forms.TextArea)

    """adding custom form validation for our django form"""
    def clean_message(self):
        message = self.cleaned_data['message']
        num_words = len(message.split()) # use split method on the message string to break it into individual words and count

        if num_words < 4:
            raise forms.ValidationError("The message you sent was too short. Add some more information and try again.")
        return message  # if you forget the retun method, None will be returned.


>>>>    # testing in the shell
f = ContactForm()
print(f.as_ul())    #prints out the form as a list 
print(f.as_p())    #prints out the form as a paragraph

f.is_bound == True  # because once data is associated with the form class it is bound

f.is_valid == True  # valid if valid values are passed to the form
>>>>
#####in views.py############
def contact(request):   # add an emailing feature for users to send feedback about the site
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            send_mail(
                cd['subject'],
                cd['message'],
                cd.get('email', 'noreply@example.com'), ['siteowner@example.com'],
            )
            return HttpResponseRedirect('/contact/thanks/')
    
    else:
        form = ContactForm()
        initial = {'subject': 'I love your site!'}  # set an initial value for the subject field
    return render(request, 'contact_form.html', {'form': form})


#######inside contact_form.html###############

<html> 
<head> 
    <title>Contact us</title> 
</head> 
<body> 
    <h1>Contact us</h1> 
 
    {% if form.errors %} 
        <p style="color: red;"> 
            Please correct the error{{ form.errors|pluralize }} below. 
        </p> 
    {% endif %}

    <form action="" method="post"> 
        <div class="field"> 
            {{ form.subject.errors }} 
            <label for="id_subject">Subject:</label> 
            {{ form.subject }} 
        </div> 
        <div class="field"> 
            {{ form.email.errors }} 
            <label for="id_email">Your e-mail address:</label> 
            {{ form.email }} 
        </div> 
        <div class="field"> 
            {{ form.message.errors }} 
            <label for="id_message">Message:</label> 
            {{ form.message }} 
        </div> 
        {% csrf_token %} 
        <input type="submit" value="Submit"> 
    </form> 
</body> 
</html>
#####inside urls.py########
from mysite.views import hello, current_datetime, hours_ahead, contact, etc

urlpatterns = [
    .....
    .....
    url(r'^contact/$', contact, name="contact"),
]

####styling the error lists######
<style type="text/css">
    ul.errorlist{
        margin: 0;
        padding: 0;
    }

    .errorlist li{
        background-color: red;
        color: white;
        display: block;
        font-size: 10px;
        margin: 0 0 3px;
        padding: 4px 5px;
    }
</style>

    # the auto-generated error lists use <ul class="errorlist">
