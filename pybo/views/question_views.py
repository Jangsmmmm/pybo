from django.contrib import messages  # 오류시 메세지발생을 위한 모듈
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone

from ..forms import QuestionForm
from ..models import Question, Category


@login_required(login_url='common:login')
def question_create(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST) # 입력된 인수(subject, content)로 QuestionForm을 생성하여 각 속성에 저장되어 객체생성
        if form.is_valid():
            question = form.save(commit=False) # commit=False는 임시저장 - question에는 create_date가 현재 없기때문(form에서는 subject,content만 있음)
            question.author = request.user # author 속성에 로그인계정 저장
            question.category = get_object_or_404(Category, title=request.POST['category'])
            question.create_date = timezone.now()
            question.save()
            return redirect('pybo:index')
    else:
        form = QuestionForm() # 질문등록 페이지 호출시에는 입력값을 받기위해서 QuestionForm을 인수 없이 생성
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_modify(request, question_id):
    """
    pybo 질문수정
    """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '수정권한이 없습니다') # 넌필드오류 발생시킬경우 사용
        return redirect('pybo:detail', question_id=question.id)

    if request.method == "POST": # POST 방식으로 요청시에 저장함
        form = QuestionForm(request.POST, instance=question) # instance를 기준으로 폼생성하지만, request.POST 값으로 덮어씌어라
        if form.is_valid():
            question = form.save(commit=False)
            question.modify_date = timezone.now()  # 수정일시 저장
            question.save()
            return redirect('pybo:detail', question_id=question.id)
    else: # GET 요청일때는 수정화면만 출력
        form = QuestionForm(instance=question) # 폼 생성시 instance 값을 지정해 폼의 속성값을 입력받은 question으로 설정
    context = {'form': form}
    return render(request, 'pybo/question_form.html', context)

@login_required(login_url='common:login')
def question_delete(request, question_id):
    """
        pybo 질문삭제
        """
    question = get_object_or_404(Question, pk=question_id)
    if request.user != question.author:
        messages.error(request, '삭제권한이 없습니다')
        return redirect('pybo:detail', question_id=question.id)
    question.delete()
    return redirect('pybo:index')