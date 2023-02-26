from django.shortcuts import render,get_object_or_404,redirect
from .models import Post
from .forms import Emailform,commentform,make_blog_form,registration_form,Login_form
from django.contrib.auth.models import User
from django.http import HttpResponse,HttpResponseRedirect
from taggit.models import Tag      
from django.db.models import Count
from .forms import Emailform, commentform, SearchForm
from haystack.query import SearchQuerySet
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate,login as auth_login
from django.core.mail import send_mail
from django.core.exceptions import ValidationError
def post_search(request):
    cd=''
    results=''
    total_results=''
    form = SearchForm()
    if 'query' in request.GET:
        form = SearchForm(request.GET)
        if form.is_valid():
            cd = form.cleaned_data
            results = SearchQuerySet().models(Post)\
            .filter(content=cd['query']).load_all()
 # count total results
            total_results = results.count()
    return render(request,'search.html',{'form': form,'cd': cd,'results': results,'total_results': total_results})



@login_required
def Home(request,tag_slug=None):
    posts=Post.objects.all()
    tag=None#this is to display all the tags associated to a praticular post
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = posts.filter(tags__in=[tag])
    return render(request,"front.html",{"posts":posts,'tag':tag})




    
def post_detail(request,post_id):
    new_comment=''
    post=get_object_or_404(Post,pk=post_id)
    comments=post.comments.filter(active=True)
    if request.method=='POST':
        print('inside the request post condition')
        comment_form=commentform(data=request.POST)
        if comment_form.is_valid():
            print("inside form valid condition")
            #create  comment object but dont save to the database
            new_comment=comment_form.save(commit=False)
            #assign the current post to the comment
            new_comment.post=post
            new_comment.save()
    
    else:
            #if the comment form is invalid show the comment form again
        print("else is executed from")
        comment_form=commentform()
    # List of similar posts
    post_tags_ids = post.tags.values_list('id', flat=True)
    similar_posts = Post.objects.filter(tags__in=post_tags_ids).exclude(id=post.id)
    similar_posts = similar_posts.annotate(same_tags=Count('tags')).order_by('-same_tags','-publish')[:4]
    return render(request,"detail.html",{'post':post,'comments':comments,'comment_form':comment_form,'similar_posts': similar_posts,"new_comment":new_comment})

################################################################################################
#below function is for sharing posts by email
def post_share(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    sent=False
    if request.method == 'POST':

 # Form was submitted
        form = Emailform(request.POST)
        if form.is_valid():
 # Form fields passed validation
            cd = form.cleaned_data
            post_url=request.build_absolute_uri(post.get_absolute_url())
            subject = f"{cd['name']} recommends you read " f"{post.title}"
            message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
            send_mail(subject, message, 'smartysaurabh88877@gmail.com',[cd['to']])
            sent=True

 # ... send email
    else:
        form = Emailform()
    return render(request, 'email.html', {'post': post,'form': form,'sent':sent})

###############################################################################################


def make_blog(request):
    postobject=Post
    #print(postobject.author)
    if request.method=='POST':
        blogobject=make_blog_form(data=request.POST)
        if blogobject.is_valid():
            blogobject.instance.author=request.user
            blogobject.save()
            return redirect("home")
    else:
        print("else is executed")
        blogobject=make_blog_form()
        print(blogobject)
    return render(request,"make_blog.html",{'blogobject':blogobject})

def login(request,tag_slug=None):
    #login view but cuurerntly it is not working as desired
    if request.method=="POST":
        login_from=Login_form(request.POST)
        try:
            if login_from.is_valid():
                cd=login_from.cleaned_data                  #cd stores valid data
                user=authenticate(username=cd['username'],password=cd['password'])
                if user is not None:
                    if user.is_active:
                        auth_login(request,user)
                        return redirect("home")
                    else:
                        return HttpResponse("User is not active")
        except ValidationError:
            print("error catched")
            return render(request,"registration/login.html",{'login_form':login_from,'error':e})
    else:
        login_from=Login_form()
    return render(request,"registration/login.html",{'login_form':login_from})

def register(request):
    if request.method=="POST":
        reg_form=registration_form(data=request.POST)
        if reg_form.is_valid():
            cd=reg_form.cleaned_data
            new_user=reg_form.save(commit=False)
            new_user.set_password(cd['password2'])
            new_user.save()
            messages.success(request,"Account created successfully.Now You can login")
            return render(request,"registration_done.html")
    else:
        reg_form=registration_form()
    return render(request,"register.html",{'form':reg_form})


def my_blogs(request,tag_slug=None):
    posts=Post.objects.filter(author=request.user.id)
    tag=None#this is to display all the tags associated to a praticular post
    if tag_slug:
        print("inside tag slug")
        tag = get_object_or_404(Tag, slug=tag_slug)
        object_list = posts.filter(tags__in=[tag])
    return render(request,"front.html",{'posts':posts,'tags':tag})




def blog_edit_view(request,post_id):
    ins=get_object_or_404(Post,pk=post_id)
    if request.method=='POST':
        title=request.POST.get("title")
        body=request.POST.get("body")
        print(ins.title)
        print(ins.body)
        ins.title=title
        ins.body=body
        ins.save()
        return redirect("/blog/home/")
    return render(request,"blog_edit.html",{'post':ins})