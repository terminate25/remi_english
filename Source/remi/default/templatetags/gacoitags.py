# -*- coding: utf-8 -*-

from django import template
from django.contrib.humanize.templatetags.humanize import intcomma

from default.config.config_menu import ScreenName, config_menus
from default.logic.userlogic import LoginUser
from helper.util import GacoiForm, StringBuilder, Format

register = template.Library()


@register.filter
def dict_item(h, key):
    """
    Get value from dict object. Key is parameter. dict is filter object.
    @param h: dict object
    @param key: dict's key
    @return:
    """
    if h is None:
        return None
    if not isinstance(h, dict):
        h = h.__dict__
    if key in h:
        return h[key]
    return None


@register.filter
def dict_item_i(key, h, default=''):
    """
    Get value from dict object, but dict is parameter.
    @param key: dict's key
    @param h: dict object
    @param default:
    @return:
    """
    if h is None:
        return default
    if not isinstance(h, dict):
        h = h.__dict__
    if key in h:
        return h[key]
    return default


@register.filter
def list_item(h, index):
    """
    Get value from list object. index is parameter. list is filter object.
    @param h:
    @param index:
    @return:
    """
    if index < len(h):
        return h[index]
    return None


@register.filter
def list_item_i(index, h):
    """
    Get value from list object. list is parameter. index is filter object.
    @param index:
    @param h:
    @return:
    """
    if index < len(h):
        return h[index]
    return None


@register.filter
def format_number(h, show_zero=False):
    """
    Format number as 1,000,000
    @param h:
    @param show_zero:
    @return:
    """
    if h is None:
        return ""

    if h == 0 and not show_zero:
        return ""

    return intcomma(h, False)


@register.filter
def format_date(h):
    """
    Format date as define in config
    @param h:
    @return:
    """
    return Format.format_date(h)


@register.filter(name='call')
def call_method(obj, method_name):
    """
    Call method by name
    @param obj:
    @param method_name:
    @return:
    """
    method = getattr(obj, method_name)
    if '__callArg' in obj.__dict__:
        ret = method(*obj.__callArg)
        del obj.__callArg
        return ret
    return method()


@register.filter(name='args')
def args(obj, arg):
    """
    Arguments for call method
    @param obj:
    @param arg:
    @return:
    """
    if '__callArg' not in obj.__dict__:
        obj.__callArg = []
    obj.__callArg += [arg]
    return obj


@register.filter(name='loop_times')
def loop_times(number, adjust=0):
    """
    Get range of (numbers - adjust) times
    @param number:
    @param adjust:
    @return:
    """
    return range(number - adjust)


@register.filter(name='subtract')
def subtract(number, param=0):
    """
    Subtract number by param
    @param number:
    @param param:
    @return:
    """
    return number - param


@register.filter
def format_percentage(h, show_zero=False):
    """
    Show as percentage.
    @param h:
    @param show_zero: If false, don't show data if zero
    @return:
    """
    if h is None:
        return ""

    if h == 0 and not show_zero:
        return ""

    return "{0} %".format(intcomma(h, False))


@register.simple_tag
def gacoiform_common_script():
    """
    Render common java script for GacoiForm form.
    @return:
    """
    return GacoiForm.render_common_script()


@register.simple_tag
def appearance_system_name():
    """
    Show system name. Get from config.
    @return:
    """
    from default.config.config_appearance import AppearanceConfig
    return AppearanceConfig.SystemName.value


@register.simple_tag
def appearance_company_name():
    """
    Show company name. Get from config
    @return:
    """
    from default.config.config_appearance import AppearanceConfig
    return AppearanceConfig.CompanyName.value


def create_menu(icon, href, text):
    """
    Create dict of menu info
    @param icon:
    @param href:
    @param text:
    @return:
    """
    return {'icon': icon, 'href': href, 'text': text}


def append_submenu(menu, submenu):
    """
    Add sub menu
    @param menu:
    @param submenu:
    @return:
    """
    if "children" not in menu:
        menu["children"] = []
    menu["children"].append(submenu)


def render_menu(menu, active_id, menu_id):
    """
    Render html of a item of config menu
    @param menu:
    @param active_id:
    @param menu_id:
    @return:
    """
    sb = StringBuilder()

    menu_class = "";
    if active_id == menu_id:
        menu_class = "active"
    elif active_id.startswith("{0}.".format(menu_id)):
        menu_class = "active open"

    class_dropdown_toggle = ''
    if 'children' in menu:
        class_dropdown_toggle = 'class="dropdown-toggle"'



    sb.append('    <li class="{0}">\n'.format(menu_class))
    sb.append('        <a href="{0}" {1}>\n'.format(menu['href'], class_dropdown_toggle))
    sb.append('            <i class="menu-icon fa {0}"></i>\n'.format(menu['icon']))
    sb.append('            <span class="menu-text">{0}</span>\n'.format(menu['text']))
    sb.append('            \n')
    sb.append('        </a>\n')
    sb.append('        <b class="arrow"></b>\n')
    if "children" in menu:
        i = 0
        sb.append('        <ul class="submenu">\n')
        for child in menu['children']:
            i = i + 1
            sb.append(render_menu(child, active_id, "{0}.{1}".format(menu_id, i)))

        sb.append('        </ul>\n')
    sb.append('    </li>\n')
    return str(sb)


@register.simple_tag
def render_gacoi_form_field(form, field, edit_mode=False):
    """
    Render a field of GacoiForm form
    @param form:
    @param field:
    @param edit_mode:
    @return:
    """
    if edit_mode:
        return form.render_field_edit_mode(field)
    else:
        return form.render_field_view_mode(field)


@register.simple_tag
def ace_menu_generate(screen_name):
    """
    Create top menu. Check roles and show only valid menu
    @type screen_name: ScreenName
    @param screen_name: 
    @type user: LoginUser
    @param user: 
    @return: 
    """
    sb = StringBuilder()
    sidebars = []

    user = LoginUser.get_login_user()

    menu_idx = 0
    active_menu_idx = ""
    for menu_info in config_menus:
        if 'screen_name' in menu_info and not user.is_menu_available(menu_info['screen_name']):
            continue
        menu_idx += 1
        sub_menu_idx = 0
        if 'screen_name' in menu_info and screen_name == menu_info['screen_name']:
            active_menu_idx = str(menu_idx)
        menu = create_menu(menu_info['icon'], menu_info['url'], menu_info['name'])
        sidebars.append(menu)
        if 'sub_menu' not in menu_info:
            continue
        for sub_menu_info in menu_info['sub_menu']:
            if 'screen_name' in sub_menu_info and not user.is_menu_available(sub_menu_info['screen_name']):
                continue
            sub_menu_idx += 1
            if 'screen_name' in sub_menu_info and screen_name == sub_menu_info['screen_name']:
                active_menu_idx = str(menu_idx) + "." + str(sub_menu_idx)
            append_submenu(menu, create_menu(sub_menu_info['icon'], sub_menu_info['url'], sub_menu_info['name']))

    sb.append('<ul class="nav nav-list">\n')
    menu_idx = 0
    for menu in sidebars:
        menu_idx += 1
        sb.append(render_menu(menu, active_menu_idx, "{0}".format(menu_idx)))

    # sb.append('     <li class="">\n')
    # sb.append('        <a href="/course_list">\n')
    # sb.append('        <i class="menu-icon fa fa-caret-right"></i>\n')
    # sb.append('        <span class="menu-text">\n')
    # sb.append('             <div class="center">\n')
    # sb.append('	                <img src="/static/images/msmy/MsMy.jpg" style="height: 10vh"/>\n')
    # sb.append('	                <h6><span class="red">REMI ENGLISH</span><span class="white" id="id-text2"></span></h6>\n')
    # sb.append('	                <h6 class="blue" id="id-company-text"><i class="fa fa-mobile"></i> 0873.099.599</h6>\n')
    # sb.append('	                <h6 class="blue" id="id-company-text"><i class="fa fa-mobile"></i> 09.03.03.2014</h6>\n')
    # sb.append('	                <h6 class="blue" id="id-company-text"><i class=""></i> http://remienglish.com</h6>\n')
    # sb.append('             </div>\n')
    # sb.append('         </span>\n')
    # sb.append('         </a>\n')
    # sb.append('         <b class="arrow"></b>\n')
    # sb.append('     </li>\n')
    sb.append('</ul><!-- /.nav-list -->\n')

    return str(sb)


@register.simple_tag
def ace_bread_crumbs_generate(screen_name):
    """
    Render form title bar.
    @type screen_name: ScreenName
    @param screen_name: 
    @return: 
    """

    sb = StringBuilder()

    for menu_info in config_menus:
        if 'screen_name' in menu_info and screen_name == menu_info['screen_name']:
            sb.append('<ul class="breadcrumb">')
            sb.append('<li class="active">')
            sb.append('<i class="ace-icon fa fa-home home-icon"></i>')
            sb.append('<a href="/">{0}</a>'.format(menu_info['name']))
            sb.append('</li>')
            break
        if 'sub_menu' not in menu_info:
            continue
        for sub_menu_info in menu_info['sub_menu']:
            if 'screen_name' in sub_menu_info and screen_name == sub_menu_info['screen_name']:
                sb.append('<ul class="breadcrumb">')
                sb.append('<li>')
                sb.append('<i class="ace-icon fa fa-home home-icon"></i>')
                sb.append('<a href="/">ホーム</a>')
                sb.append('</li>')
                sb.append('<li><a href="#">{0}</a></li>'.format(menu_info['name']))
                sb.append('<li class="active">{0}</li>'.format(sub_menu_info['name']))
                break

    sb.append('</ul>')

    return str(sb)
