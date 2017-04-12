
from django.conf.urls import patterns, url
from rango import views
from rango.models import Category, Page, Loan


urlpatterns = patterns('',
        url(r'^$', views.index, name='index'),
        url(r'^about/$', views.about, name='about'),
        url(r'^log/$', views.log, name='log'),
        url(r'^select_loan/$', views.select_loan, name='select_loan'),
        url(r'^add_category/$', views.add_category, name='add_category'),
        url(r'^add_notice/$', views.add_notice, name='add_notice'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/(?P<user_name>[\w\-]+)/add_page/$', views.add_page, name='add_page'),
        url(r'^page/(?P<title_name>[\w\-]+)/(?P<user_name>[\w\-]+)/add_comment/$', views.add_comment, name='add_comment'),
        #url(r'^register/$', views.register, name='register'),
        #url(r'^login/$', views.user_login, name='login'),
        url(r'^restricted/', views.restricted, name='restricted'),
        url(r'^search/', views.search, name='search'),
        url(r'^goto/$', views.track_url, name='goto'),
        url(r'^like_category/$', views.like_category, name='like_category'),
        #url(r'^logout/$', views.user_logout, name='logout'),
        url(r'^category/(?P<category_name_slug>[\w\-]+)/$', views.category, name='category'),
        url(r'^loan/(?P<loan_name>[\w\-]+)/$', views.loan, name='loan'),
        url(r'^product/(?P<product_name>[\w\-]+)/$', views.product, name='product'),
        url(r'^file_download/profile_file/(?P<file_name>.+)/$', views.file_download, name='file_download'),
        url(r'^page/(?P<page_name>[\w\-]+)/$', views.page, name='page'),
        url(r'^notice/(?P<notice_name>[\w\-]+)/$', views.notice, name='notice'),
        )
        