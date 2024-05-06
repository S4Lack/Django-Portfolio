from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name='home'),
	path('posts/', views.posts, name='posts'),
	path('post/<str:slug>', views.post, name='post'),	
	
	#Auth URLs
 	path('login/', views.index, name="login"),
	path('register/', views.index, name="register"),
	path('logout/', views.index, name="logout"),

	path('account/', views.userAccount, name="account"),
	path('update_profile/', views.updateProfile, name="update_profile"),
 
	#CRUD URLs
	path('create_post/', views.index, name="create_post"),
	path('update_post/<slug:slug>/', views.index, name="update_post"),
	path('delete_post/<slug:slug>/', views.index, name="delete_post"),


	path('send_email/', views.index, name="send_email"),


]
