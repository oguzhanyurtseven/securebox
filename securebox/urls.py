from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from securebox import settings
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'securebox.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'securebox.views.home_page', name='home'),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login',
        {'template_name': 'login.html'}),
    url(r'^accounts/logout/$', 'django.contrib.auth.views.logout',
        {'next_page': '/'}),
    url(r'^new_user/$', 'securebox.views.new_user'),
    url(r'^send_mail/$', 'securebox.views.send_mail'),
    url(r'^public_key_page/(.+)/$', 'securebox.views.public_key_page'),
    url(r'^decrypt_page/$', 'securebox.views.decrypt_page_input'),
) + staticfiles_urlpatterns() + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
