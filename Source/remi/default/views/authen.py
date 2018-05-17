# -*- coding: utf-8 -*-
"""
Authentication Manage Module
"""
from functools import wraps

from django.conf import settings
from django.http import HttpResponseRedirect, QueryDict
from django.shortcuts import resolve_url
from django.utils.decorators import available_attrs
from django.utils.six.moves.urllib.parse import urlparse, urlunparse

REDIRECT_FIELD_NAME = 'next'


def check_login(func=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    @type func:
    @param func:
    @param redirect_field_name: 
    @param login_url: 
    @return: 
    """

    actual_decorator = user_passes_test(
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if func:
        return actual_decorator(func)
    return actual_decorator


def user_passes_test(login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Decorator for views that checks that the user passes the given test,
    redirecting to the log-in page if necessary. The test should be a callable
    that takes the user object and returns True if the user passes.
    """

    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            from default.logic.user_logic import LoginUser
            if request.session.get(LoginUser.login_user_session_key) is not None:
                # Update filter for user
                user = LoginUser.reload(request, view_func)
                if not user.is_view_right():
                    # Return to home if have no right to view
                    return HttpResponseRedirect("/course_list")

                return view_func(request, *args, **kwargs)

            path = request.build_absolute_uri()
            resolved_login_url = resolve_url(login_url or settings.LOGIN_URL)
            # If the login url is the same scheme and net location then just
            # use the path as the "next" url.
            login_scheme, login_netloc = urlparse(resolved_login_url)[:2]
            current_scheme, current_netloc = urlparse(path)[:2]
            if ((not login_scheme or login_scheme == current_scheme) and
                    (not login_netloc or login_netloc == current_netloc)):
                path = request.get_full_path()
            return redirect_to_login(
                path, resolved_login_url, redirect_field_name)

        return _wrapped_view

    return decorator


def redirect_to_login(next_page, login_url=None, redirect_field_name=REDIRECT_FIELD_NAME):
    """
    Redirects the user to the login page, passing the given 'next' page
    """
    resolved_url = resolve_url(login_url or settings.LOGIN_URL)

    login_url_parts = list(urlparse(resolved_url))
    if redirect_field_name:
        querystring = QueryDict(login_url_parts[4], mutable=True)
        querystring[redirect_field_name] = next_page
        login_url_parts[4] = querystring.urlencode(safe='/')

    return HttpResponseRedirect(urlunparse(login_url_parts))


