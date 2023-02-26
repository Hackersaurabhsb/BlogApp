from django.urls import path,re_path as url
from . import views
from .feeds import LatestPostsFeed 
from django.contrib.auth.views import LoginView,LogoutView,PasswordResetForm
urlpatterns=(
    path("",views.login,name="login"),
    path("make_blog",views.make_blog,name="make_blog"),
    path('home/<int:post_id>/',views.post_detail,name="post_detail"),
    path("<int:post_id>/post_share/",views.post_share,name="post_share"),
    path('<int:post_id>', views.post_detail,name='post_detail'),
    path("home/",views.Home,name='home'),
    path("logout/",LogoutView.as_view(),name='logout'),
    path("register/",views.register,name="register"),
    path("my_blogs",views.my_blogs,name="my_blogs"),
    path('<int:post_id>/edit',views.blog_edit_view,name="edit"),
)