
from default.views.authen import *
from django.shortcuts import render
from helper.lagform import *
from default.logic.testcontentlogic import *
from default.logic.userlogic import LoginUser


@check_login
def video_content(request):

    params = request.GET
    part_id = params.get('part_id', '')
    if part_id != '':
        part_id = int(part_id)
    lag_form = LagForm()
    user = LoginUser.get_login_user(request)
    video_path = CourseListLogic.get_video_path(part_id)
    lag_form.set_image_course(video_path, "Watching this video")
    part = Part.objects.get(pk=part_id)
    part_name = part.name
    summary_path = '/media/{0}/summary/{1}'.format(str(part_id), part.summary)
    context = {
        'lag_form': lag_form,
        'video_path': video_path,
        'lesson_name': part_name,
        'summary_file_url': summary_path,
        'part_id': part_id,
    }

    return render(request, 'video_content.html', context)


