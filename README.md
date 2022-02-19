# PublicPrecurement

이 프로젝트는 공공조달 open api를 만들기 위해서 만들어진 프로젝트 입니다.

해당 프로젝트에서 사용된 framework는 djangorestframework, sklearn 등 이 있습니다.

api는 심플하게 

~~~
http://127.0.0.1:8000/api/v1/corporation/
~~~
유형 : post(create), get(return all object list)


~~~
http://127.0.0.1:8000/api/v1/corporation/<int:pk>
~~~
유형: put(update), delete, get(return pk number object)


~~~
class Corporation(models.Model):
    howToDecideTheWinner = models.CharField(max_length=20)
    bidRate = models.FloatField()
    industryRestriction = models.CharField(max_length=100)
    # result
    bidOrNot = models.CharField(max_length=2)
    create_data = models.DateTimeField(auto_now_add=True)
~~~

## 제작 도중 생긴 문제점
1. post로 입력이 들어왔을 때 해당 내용을 model에 predict하기 위해 벡터화를 진행해야하는데 백터화를 위한 모델이 존재하지 않아서 에러가 계속 발생
=> 벡터화 모델을 jobilb로 저장이 가능하다면 해당 방법으로 해결을 할 수 있지만 이를 성공하지 못한다면 해당 프로젝트는 그냥 폐기해야한다.
