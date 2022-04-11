from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from ..models import Question, Answer, Comment, Category
from django.core.paginator import Paginator
from django.contrib import messages # 오류시 메세지발생을 위한 모듈
from django.db.models import Q, Count

def index(request, question_category):
    # 입력 파라미터
    c = Category.objects.get(title=question_category)
    Question = c.question_set.all()
    page = request.GET.get('page', '1')  # 페이지
    kw = request.GET.get('kw', '')  # 검색어
    so = request.GET.get('so', 'recent')  # 정렬기준

    # 정렬
    if so == 'recommend':
        question_list = Question.annotate(num_voter=Count('voter')).order_by('-num_voter', '-create_date')
    elif so == 'popular':
        question_list = Question.annotate(num_answer=Count('answer')).order_by('-num_answer', '-create_date')
    else:  # recent
        question_list = Question.order_by('-create_date')

    # 조회
    if kw:
        question_list = question_list.filter(
            Q(subject__icontains=kw) |  # 제목검색
            Q(content__icontains=kw) |  # 내용검색
            Q(author__username__icontains=kw) |  # 질문 글쓴이검색
            Q(answer__author__username__icontains=kw)  # 답변 글쓴이검색
        ).distinct()

    # 페이징처리
    paginator = Paginator(question_list, 10)  # 페이지당 10개씩 보여주기
    page_obj = paginator.get_page(page)

    context = {'question_list': page_obj, 'category':Category.objects.all(), 'cate':question_category} # question_list는 페이징 객체(page_obj)
    return render(request, 'pybo/question_list.html', context)



def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    page = request.GET.get('page', '1')  # 페이지
    answer_list = question.answer_set.all()
    # 페이징처리
    paginator = Paginator(answer_list, per_page=5)  # 페이지당 10개씩 보여주기
    page_obj = paginator.page(int(page)) # 요청된 페이지에 해당하는 페이징 객체생성

    context = {'answer_list': page_obj, 'question': question}
    return render(request, 'pybo/question_detail.html', context)

