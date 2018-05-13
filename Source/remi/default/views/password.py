from django.shortcuts import render, redirect
from default.views.authen import *
from default.logic.userlogic import *
from default.models.models import User
from helper.util import *
from default.logic.userlogic import LoginUser


@check_login
def password(request):
    """
    Change password 
    @param request: 
    @return: 
    """
    user = LoginUser.get_login_user(request)
    target_user = None
    if request.method == 'POST':
        params = request.POST
    else:
        params = request.GET

    # Check if change for own
    user_id = params.get("user_id", "")

    password_form = GacoiForm("password_form", "/password/", "POST")
    if user_id == "":
        password_form.set_view("old_password")
        password_form.set_insert("old_password")
        password_form.set_required("old_password")
    else:
        # Check if have right
        if not user.is_right(ModuleName.User, UserRightType.Update):
            return redirect('/')
        target_user = User.objects.get(pk=int(user_id))
        # password_form.set_info_message("{0}さんのパスワードを変更します。".format(target_user.user_name))

    password_form.set_view("new_password,confirm_password")
    password_form.set_insert("new_password,confirm_password")
    password_form.set_required("new_password,confirm_password")

    password_form.set_type("old_password,new_password,confirm_password", GacoiFormFieldType.Password)
    password_form.set_view_type(GacoiFormViewType.FormView)
    password_form.set_hidden("password_change", "")
    password_form.set_hidden("user_id", user_id)
    password_form.add_user_button(UserButton("Change password", "do_change_password();", True))
    password_form.add_user_button(UserButton("Cancel", "do_close_form();", False))
    password_form.init(request)
    password_form.set_action(GacoiFormAction.InsertStart)
    password_form.set_option_form_label_col(3)
    password_form.set_caption({"old_password": "Old password", "new_password": "New password", "confirm_password": "New password"})
    changed = False
    if params.get("password_change") == "true":
        old_password = params.get('old_password', None)
        new_password = params.get('new_password', None)
        confirm_password = params.get('confirm_password', None)

        if new_password != confirm_password:
            password_form.set_error_message("Confirm password is not correct")
        else:
            if user_id != "":
                changed_user = User.objects.get(id=int(user_id))
                changed_user.password = UserLogic.hash_password(new_password)
                changed_user.save()
                changed = True
            else:
                changed_user = User.objects.get(id=user.id)
                if UserLogic.is_password_match(old_password, changed_user.password):
                    changed_user.password = UserLogic.hash_password(new_password)
                    changed_user.save()
                    changed = True
                else:
                    password_form.set_error_message("旧パスワードが一致しません。")

    context = {
        'changed': changed,
        'password_form': password_form,
        'target_user': target_user,


    }

    return render(request, 'password.html', context)
