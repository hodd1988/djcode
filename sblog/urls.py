from django.conf.urls import patterns, include, url

urlpatterns = patterns('sblog.views',
	url(r'^bloglist/$', 'blog_list', name = 'bloglist'), 
	url(r'^blog/(?P<blog_id>\d+)/$', 'blog_show', name = 'detailblog'),
	url(r'^blog/tag/(?P<blog_id>\d+)/$', 'blog_filter', name = 'filtrblog'),
	url(r'^blog/(?P<blog_id>\w+)/update/$', 'blog_update', name = 'updateblog'),
	url(r'^blog/(?P<blog_id>\w+)/del/$', 'blog_del', name = 'delblog'),
)
urlpatterns += patterns('',
		(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/he/program/djcode/static'}),
)
