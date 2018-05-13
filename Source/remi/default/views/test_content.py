from default.views.authen import *
from django.shortcuts import render
from helper.lagform import *
from default.logic.testcontentlogic import *
from django.http import JsonResponse
from default.logic.userlogic import LoginUser
from default.config.config_common import *

@check_login
def test_content(request):
    params = request.GET
    test_id = params.get('test_id', '')
    if test_id != '':
        test_id = int(test_id)
    lag_form = LagForm()
    user = LoginUser.get_login_user(request)
    current_test = Test.objects.get(pk=test_id)
    current_test_type = current_test.type
    current_lesson = current_test.part_id
    percent_goal = current_test.question_percent_goal
    question_goal = current_test.question_number_goal
    current_question = params.get('current_question', '')
    if current_question != '':
        current_question = int(current_question)
    else:
        current_question = 0
    options_dict = TestContentLogic.create_options_dict(current_test_type, test_id, current_question)
    # lag_form.render_question(current_test_type, current_test_type, test_id)
    is_json = params.get('is_json', '')
    if is_json == 'true':
        ret = dict()
        ret['data'] = options_dict[0]
        ret['options_number'] = options_dict[1]
        ret['current_question'] = options_dict[2]
        return JsonResponse(ret, safe=False)
    total_question = params.get('total_question', '')
    if total_question == '':
        total_question = 0
    else:
        total_question = int(total_question)
    correct_question = params.get('correct_question', '')
    if correct_question == '':
        correct_question = 0
    else:
        correct_question = int(correct_question)

    finished = params.get('finished', '')
    if finished == 'true':
        right_question = int(params.get('right_question', ''))
        total_question = int(params.get('total_question', ''))
        test_id = int(params.get('test_id', ''))
        current_part = int(params.get('current_lesson', ''))
        if total_question == 0:
            current_percent = 0
        else:
            current_percent = round(right_question / total_question*100, 2)

        base_user_test = BaseUserStep()
        ret = dict()
        ret['result'] = False
        ret['right_number'] = right_question
        ret['percent'] = current_percent
        base_user_test.is_done = TestResult.Failed.code
        percent_goal = int(params.get('percent_goal', ''))
        question_goal = int(params.get('question_goal', ''))
        if current_percent >= percent_goal and right_question >= question_goal:
            ret['result'] = True
            base_user_test.is_done = TestResult.Done.code

        base_user_test.test_id = test_id
        base_user_test.part_id = current_part
        base_user_test.right_percent = current_percent
        base_user_test.right_number_question = right_question
        base_user_test.user_id = user.id
        base_user_test.save()
        # Get user test list
        # If all done -> set is_done in base_student_lesson table to 1
        # Create new record in base_student_lesson for next order lesson
        TestContentLogic.check_lesson_status(user.id, current_part)
        return JsonResponse(ret, safe=True)

    context = {
        'lag_form': lag_form,
        'test_id': test_id,
        'questions': options_dict[1],
        'correct_question': correct_question,
        'total_question': total_question,
        'options_dict': options_dict[0],
        'current_lesson': current_lesson,
        'percent_goal': percent_goal,
        'question_goal': question_goal,
        'current_test_type': current_test_type
    }

    return render(request, 'test_content.html', context)


