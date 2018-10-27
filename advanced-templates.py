template = text document or a normal python string that is marked up using django template lang
template tag = a symbol within a template that does something

template tags are surrounded by {%    %}.
    eg. {% if is_logged_in %}
            thanks for logging in!
        {% else %}
            please log in.
        {% endif %}

variable tags = symbol within a template that outputs a value. Surrounded by {{ }}.

context = a (name->value) mapping passed to a template.

template renders a context by replacing the variable with values from context and executing all
    template tags.

# --------------Requestcontext and context processors-------------------
# ----------asdd a context renderer to thid code tonight----------# undone!!
a context can be an instance of django.template.Context,
or a subclass django.template.RequestContext that acts slightly dif.

RequestContext adds a bunch of variables to your template context by default-things like
the HttpRequest object or info about the currently logged_in user.

the render() shortcut creates a RequestContext unless it is passed a dif context instance 
explicitly.

eg.
from django.template import loader, Context
def view1(request):
    t = loader.get_template('template1.html')

    c = Context({
        'app': 'my app',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR']   # from the request object dictionary
        'message': 'i am the second view',
        
    })

    return t.render(c)

def view2(request):
    t = loader.get_template('template2.html')
    c = Context({
        'app': 'my app',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],
        'message': 'i\'m the second view'
    }
    )

    return t.render(c)  # return loaded template with the specified context

# we are deliberately not using the render() shortcut in these examples, we're manually
# loading the templates, constructing the context objects and rendering the templates.

>>Each view passes the same 3 variables to its template. 
>>RequestContext and context processors were created to solve this problem.

>>Context processors let you specifiy a number of vars that get set in each context automatically 
    without you having to specify the vars in each render() call.

>>The catch? You have to use RequestContext instead of Context when you render the template.
>>the most low_level way of using context processors is to create some and pass them to
    RequestContext.
eg.

# the above code written using context processors

from django.template import loader, RequestContext

def custom_proc(request):   # takes in an HttpRequest object and returns a dict of vars to use in the template context
    """a context processor that provides app, user and ip address"""
    return {
        'app': 'my app',
        'user': request.user,
        'ip_address': request.META['REMOTE_ADDR'],

    }

def view1(request):
    t = loader.get_template('template.html')
    c = RequestContext(request, {'message': 'I am view 1'}, processors=[custom_proc])

    return t.render(c)

def view2(request):
    t = loader.get_template('template2.html')
    c = RequestContext(request, {'message': 'i am view2'}, processors=[custom_proc])
    return t.render(c)


# to use ajax in the django project, you need jquery!!
###intregrating ajax/jquery with django
from django.shortcuts import render
from django.http import JsonResponse

def blog_list(request):
    context = {
        'title': 'some title here',
        'description': 'some description as well',
    }
    return JsonResponse(context)

    # when running this view, you will see the output as a JSON object


# simple AJAX and JSON in a django view
# assumes you have a button element in the template

var btn = document.getElementById("btn");
var container = document.getElementById("ourcontainer");
var url = 'http://127.0.0.1:8000/'

$.ajax({
    method: 'GET',
    url: url,
    success: function(data){
        console.log("success")
    },
    error: function(error_data){
        console.log("error")
    }
})


btn.addEventListener("click", function(){
    var ourRequest = new XMLHttpRequest();
    ourRequest.open("GET", url)
    ourRequest.onload = function(){
        console.log(ourRequest.responseText)    # not json formatted
        var ourData = JSON.parse(ourRequest.responseText)  
        console.log(ourData)

    }

    ourRequest.send();  # send the request to the template
})



























