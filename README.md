# PublicPrecurement

이 프로젝트는 공공조달 open api를 만들기 위해서 만들어진 프로젝트 입니다.


### 프로젝트 요약
> 사용자로부터 request를 받아서 request에 포함된 정보들('낙찰자결정방법','입찰률','업종제한내용')을 가지고 '낙찰여부'를 response하는 api입니다.
>
> 해당 기능을 구현하기 위해서 python을 사용하는 django, djangorestframework, drf-yasg를 사용하였고, 이를 통해 사용자가 간단한게 open api를 가져다가 저희의 결과물을 사용할 수 있도록 편의성을 제공합니다.
>
> 또한 문서 자동화를 통해 api documentation을 보기 쉽도록 부가적으로 구현했습니다.

# version
~~~
django	4.0.2	
djangorestframework	3.13.1	
drf-yasg	1.20.0	
joblib	1.1.0	
numpy	1.22.2	
pandas	1.4.1	
python	3.10.0	
scikit-learn	1.0.1
scipy	1.8.0	
~~~

# how to use
1. 아래 링크에 접속해서 model.pkl을 다운 받습니다.

https://drive.google.com/file/d/1VuH2gpFx6_EGruDjYkiYwIYhUL5Dafb1/view?usp=sharing

2. git clone
3. restApi/resource/ 폴터안에 model.pkl을 넣어줍니다.
4. 다음 명령어를 실행합니다.
~~~
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
~~~

- url
~~~
http://127.0.0.1:8000/api/corporation/
~~~
<img width="1428" alt="스크린샷 2022-02-24 오후 1 55 20" src="https://user-images.githubusercontent.com/73744183/155482471-0a2d0dbb-6f14-4f7c-919b-00607ddcd418.png">
기본적인 curd 기능은 모두 구현을 하였고 server를 실행하고 swagger를 통해 문서 자동화를 구현해 놓았기 때문에 보고서 사용하면 됩니다.

* api documentation url
~~~
http://127.0.0.1:8000/api/swagger/
~~~



## 제작 도중 생긴 문제점
1. post로 입력이 들어왔을 때 해당 내용을 model에 predict하기 위해 벡터화를 진행해야하는데 백터화를 위한 모델이 존재하지 않아서 에러가 계속 발생
=> 벡터화 모델을 jobilb로 저장이 가능하다면 해당 방법으로 해결을 할 수 있지만 이를 성공하지 못한다면 해당 프로젝트는 그냥 폐기해야한다.
=> 다행히 벡터화 모델을 joblib로 저장하여서 사용할 수 있었고 해당 부분을 수정하여  정상적으로 동작하는 것을 확인하였다.

2. model.pkl이 100mb를 넘어서 git에 저장하기 부담스럽다.
=> git fls 를 사용하면 100mb가 넘는 파일을 저장할 수 있지만 그렇게 하지 않고 구글 드라이브에 저장을 해두고 사용자가 다운을 받을 수 있도록 해결하였다.

3. 학습시킨 모델의 사이킷런 버전과 불러와서 사용하는 모델의 사이킷런 버전의 불일치 문제
=> 일반적으로 버전이 조금 다르더라도 모듈을 사용함에 있어서 문제는 되지 않지만 기존에는 0.24 version이고, api에서는 1.0.1 version인데 앞자리 숫자가 달라져서 실행중에 경고문이 동작한다.
하지만 사용하는 것에 있어서 문제가 없기에 경고를 무시하고 그냥 사용하기로 마무리지었다.

## 학습 코드와 다른점 
데이터 학습 코드에서는 코드를 재실행하면 매번 학습데이터를 다시 불러와서 처음부터 다시 학습을 진행한 뒤 모델을 생성합니다. 

하지만 api에서는 그렇게 코드가 동작하면 시간이 오래걸리고 사용하기에 적합하기 않기 때문에 joblib 묘듈을 이용해서 학습시킨 객체를 .pkl 파일로 만들고 결과를 예측해야할 때에 저장해둔 파일을 통해 객체를 다시 생성하여 사용합니다.

이런 방법을 적용하는 곳이 정확히 다음과 같이 2군데 입니다.
1. 사용자로부터 request를 받았을 때 해당 정보를 벡타화할 때(vec.pkl)
~~~
def vec_x_data(data):
    #from sklearn.feature_extraction import DictVectorizer

    x_data = data

    df = []
    for i in range(len(x_data)):
        df.append({'낙찰자결정방법': x_data['낙찰자결정방법'][i], '입찰률': x_data['입찰률'][i], '업종명': x_data['업종명'][i]})
        
    # 해당 부분 수정 start
    filename = "./restApi/resource/vec.pkl"
    vec = joblib.load(filename)
    df1 = pd.DataFrame(vec.transform(df))
    # 수정 end
    
    df1.columns = vec.get_feature_names()  # 컬럼명 변경
    return df1
~~~


2. 벡터화한 정보를 바탕으로 결과를 예측할 때(model.pkl)

~~~
def run_data(data):
    # input : dict
    sys.modules['sklearn.externals.joblib'] = joblib

    # dict to df
    data = dict(data)
    df = pd.DataFrame(data, index=[1])
    df.columns = ['낙찰자결정방법','입찰률','업종제한내용']
    df = df.dropna()
    df = df.reset_index(drop=True)

    file_path = "./restApi/resource/code_list.json"

    with open(file_path, "r") as f:
        read_data = json.load(f)
    code_list = make_code_list(df)
    industry_name = make_industry_name(code_list, read_data)
    data = modify_data(df, industry_name)
    X_data = vec_x_data(data)

    # 수정 start
    model = joblib.load('./restApi/resource/model.pkl')
    pred = model.predict(X_data.to_numpy())
    # end
    
    return pred
~~~

* 실제 동작 화면


<img width="1282" alt="스크린샷 2022-02-24 오후 2 39 18" src="https://user-images.githubusercontent.com/73744183/155484924-8258ab2d-f7a5-476f-9d06-41e863efcb4f.png">



