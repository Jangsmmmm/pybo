from django import forms
from pybo.models import Question, Answer,Comment, Category
class QuestionForm(forms.ModelForm): # ModelForm을 사용해서 연결된 모델의 데이터를 저장할 수 있는 폼
    class Meta: # 모델폼은 이너클래스인 Meta클래스가 반드시 필요.

        model = Question
        fields = ['subject', 'content'] # 모델폼은 사용할 모델과 모델의 속성을 적는다.
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'row': 10}),
        }
        labels = {
            'subject' : '제목',
            'content' : '내용',
        }


class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        labels = {
            'content': '댓글내용',
        }