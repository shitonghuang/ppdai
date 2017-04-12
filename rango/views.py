# -*- coding:utf-8 -*-

from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse
from rango.models import Category,Page,Comment,Notice,Loan,Product
from rango.forms import CategoryForm
from rango.forms import PageForm,CommentForm,NoticeForm
from rango.forms import UserForm, UserProfileForm
from django.contrib.auth import authenticate, login
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from datetime import datetime
from registration.backends.simple.views import RegistrationView
from rango.bing_search import run_query
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import os.path
import random
from django.http import StreamingHttpResponse


def index(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    visits = request.session.get('visits')
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]
    notice_list = Notice.objects.order_by('-time')[:5]
    context_dict = {'categories': category_list, 'pages': page_list, 'visits': visits, 'notices': notice_list}

    # Return a rendered response to send to the client.
    # We make use of the shortcut function to make our lives easier.
    # Note that the first parameter is the template we wish to use.
    
    
    
    reset_last_visit_time = False

    response = render(request, 'rango/index.html', context_dict)

    if not visits:
        visits = 1
    reset_last_visit_time = False

    last_visit = request.session.get('last_visit')
    if last_visit:
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")

        if (datetime.now() - last_visit_time).seconds > 0:
            # ...reassign the value of the cookie to +1 of what it was before...
            visits = visits + 1
            # ...and update the last visit cookie, too.
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so create it to the current date/time.
        reset_last_visit_time = True

    if reset_last_visit_time:
        request.session['last_visit'] = str(datetime.now())
        request.session['visits'] = visits
    context_dict['visits'] = visits


    response = render(request,'rango/index.html', context_dict)

    return response


def select_loan(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    flag = random.randint(0,99)
    if flag < 30:
        loan_list = Loan.objects.order_by('-amount')[:4]
    elif (flag > 30 and flag < 60):
        loan_list = Loan.objects.order_by('-rate')[:4]
    else:
        loan_list = Loan.objects.order_by('-months')[:4]
    
    context_dict = {'loans': loan_list}
    
    return render(request, 'rango/investment_strategy.html', context_dict)


def about(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
    if request.session.get('visits'):
        count = request.session.get('visits')
    else:
        count = 0


# remember to include the visit data
    return render(request, 'rango/about.html', {'visits': count})

def log(request):
    # Construct a dictionary to pass to the template engine as its context.
    # Note the key boldmessage is the same as {{ boldmessage }} in the template!
# remember to include the visit data
    return render(request, 'rango/investment_log.html')


def loan(request, loan_name):
    context_dict = {}
    
    try:
        loan = Loan.objects.get(title=loan_name)
        #comment = Comment.objects.filter(page=page)
        context_dict['title'] = loan.title
        context_dict['amount'] = loan.amount
        context_dict['creditcode'] = loan.creditcode
        context_dict['listingid'] = loan.listingid
        context_dict['months'] = loan.months
        context_dict['payway'] = loan.payway
        context_dict['rate'] = loan.rate
        #context_dict['comment'] = comment

        
    except Page.DoesNotExist:
        pass

    return render(request, 'rango/loan_info.html', context_dict)

def product(request, product_name):
    context_dict = {}
    
    try:
        product = Product.objects.get(title=product_name)
        #comment = Comment.objects.filter(page=page)
        context_dict['title'] = product.title
        context_dict['amount'] = product.amount
        context_dict['charge'] = product.charge
        context_dict['rate'] = product.rate
        #context_dict['comment'] = comment

        
    except Page.DoesNotExist:
        pass

    return render(request, 'rango/product_info.html', context_dict)
    

def category(request, category_name_slug):
    context_dict = {}
    context_dict['result_list'] = None
    context_dict['query'] = None
    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

            context_dict['result_list'] = result_list
            context_dict['query'] = query
    
    #新增
    loan_list1 = Loan.objects.order_by('-amount')[:5]
    loan_list2 = Loan.objects.order_by('-rate')[:5]
    loan_list3 = Loan.objects.order_by('-months')[:5]
    loan_list4 = Loan.objects.order_by('-creditcode')[:5]
    context_dict2 = {'loans1':loan_list1,'loans2':loan_list2,'loans3':loan_list3,'loans4':loan_list4,}
    product_list1 = Product.objects.order_by('-amount')[:5]
    product_list2 = Product.objects.order_by('-rate')[:5]
    product_list3 = Product.objects.order_by('-charge')[:5]
    product_list4 = Product.objects.order_by('-rate')[:5]
    context_dict3 = {'product1':product_list1,'product2':product_list2,'product3':product_list3,'product4':product_list4,}

    try:
        category = Category.objects.get(slug=category_name_slug)
        context_dict['category_name'] = category.name
        pages = Page.objects.filter(category=category).order_by('-views')
        context_dict['pages'] = pages
        context_dict['category'] = category
    except Category.DoesNotExist:
        pass

    #if not context_dict['query']:
    #    context_dict['query'] = category.name

    print category_name_slug
    if category_name_slug == "2":
        return render(request, 'rango/loan_list.html', context_dict2)
    elif category_name_slug == "1":
        return render(request, 'rango/investment_strategy.html', context_dict)
    elif category_name_slug == "0":
        return render(request, 'rango/product_list.html', context_dict3)
    else:
        return render(request, 'rango/investment_log.html', context_dict)


def page(request, page_name):
    context_dict = {}
    
    try:
        page = Page.objects.get(title=page_name)
        comment = Comment.objects.filter(page=page)
        context_dict['title'] = page.title
        context_dict['page'] = page
        context_dict['author'] = page.author
        context_dict['time'] = page.time
        context_dict['update_time'] = page.update_time
        context_dict['contents'] = page.contents
        context_dict['sourcefile'] = page.sourcefile
        context_dict['comment'] = comment

        
    except Page.DoesNotExist:
        pass

    return render(request, 'rango/page.html', context_dict)




def add_category(request):
    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # Have we been provided with a valid form?
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
    else:
        # If the request was not a POST, display the form to enter details.
        form = CategoryForm()

    # Bad form (or form details), no form supplied...
    # Render the form with error messages (if any).
    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug, user_name='author'):
    

    
    try:
        cat = Category.objects.get(slug=category_name_slug)
        
    except Category.DoesNotExist:
                cat = None

    if request.method == 'POST':

        form = PageForm(request.POST,request.FILES)
        if form.is_valid():

            if cat:
                page = form.save(commit=False)
                page.category = cat
                page.author = user_name

                page.save()
                # probably better to use a redirect here.
                #return category(request, cat.name)
                url = '/rango/category/' + cat.name
                return redirect(url)
        else:
            print form.errors
        
    else:
        form = PageForm()

    context_dict = {'form':form, 'category': cat , 'slug': cat.slug}

    return render(request, 'rango/add_page.html', context_dict)

'''
def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Did the user provide a profile picture?
            # If so, we need to get it from the input form and put it in the UserProfile model.
            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'rango/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )
'''
'''
def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/rango/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your Rango account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'rango/login.html', {})
'''
@login_required
def restricted(request):
    return HttpResponse("Since you're logged in, you can see this text!")
'''
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/rango/')
'''

def search(request):

    result_list = []

    if request.method == 'POST':
        query = request.POST['query'].strip()

        if query:
            # Run our Bing function to get the results list!
            result_list = run_query(query)

    return render(request, 'rango/search.html', {'result_list': result_list})


def track_url(request):
    page_id = None
    url = '/rango/'
    if request.method == 'GET':
        if 'page_id' in request.GET:
            page_id = request.GET['page_id']
            try:
                page = Page.objects.get(id=page_id)
                page.views = page.views + 1
                page.save()
                url = page.url
            except:
                pass

    return redirect(url)


@login_required
def like_category(request):

    cat_id = None
    if request.method == 'GET':
        cat_id = request.GET['category_id']

    likes = 0
    if cat_id:
        cat = Category.objects.get(id=int(cat_id))
        if cat:
            likes = cat.likes + 1
            cat.likes =  likes
            cat.save()

    return HttpResponse(likes)




def file_download(request,file_name):
    # do something...

    def file_iterator(file_name, chunk_size=512):
        file_name = os.path.join(os.path.dirname(__file__), '../media/profile_file/').replace('\\','/') + file_name
        print os.path.join(os.path.dirname(__file__), '../media/profile_file/').replace('\\','/')
        with open(file_name) as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    the_file_name = file_name
    the_file_name = the_file_name.encode('utf-8')
    response = StreamingHttpResponse(file_iterator(the_file_name))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{0}"'.format(the_file_name)

    return response



#3.22

def add_comment(request, title_name, user_name='authors'):
    

    
    try:
        pa = Page.objects.get(title=title_name)
        
    except Page.DoesNotExist:
        pa = None

    if request.method == 'POST':

        form = CommentForm(request.POST)
        if form.is_valid():

            if pa:
                comment = form.save(commit=False)
                comment.page = pa
                comment.author = user_name

                comment.save()
                # probably better to use a redirect here.
                #return category(request, cat.name)
                url = '/rango/page/' + pa.title
                return redirect(url)
        else:
            print form.errors
        
    else:
        form = CommentForm()

    context_dict = {'form':form, 'page': pa }

    return render(request, 'rango/add_comment.html', context_dict)



#3.22

def add_notice(request):
    

    if request.method == 'POST':

        form = NoticeForm(request.POST)
        if form.is_valid():
            # Save the new category to the database.
            form.save(commit=True)

            # Now call the index() view.
            # The user will be shown the homepage.
            return index(request)
        else:
            # The supplied form contained errors - just print them to the terminal.
            print form.errors
        
    else:
        form = NoticeForm()

    context_dict = {'form':form}

    return render(request, 'rango/add_notice.html', context_dict)

#3.22

def notice(request, notice_name):
    context_dict = {}
    
    try:
        notice = Notice.objects.get(title=notice_name)
        context_dict['title'] = notice.title
        context_dict['time'] = notice.time
        context_dict['contents'] = notice.contents

        
    except Notice.DoesNotExist:
        pass

    return render(request, 'rango/notice.html', context_dict)


