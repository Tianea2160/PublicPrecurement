from imblearn.over_sampling import ADASYN
from sklearn.feature_extraction import DictVectorizer
import pandas as pd
import re
import json
import joblib
import sys

def make_code_list(data):
    print(data)
    print(type(data))
    # Series -> numpy배열로 바꾸기
    code = data['업종제한내용'].to_numpy()

    # 텍스트와 번호가 같이 있음 -> code 번호만 뽑아오기
    code_list =[]
    for i in range(len(code)):
        numbers = re.findall("\d+", code[i])
        code_list.append(numbers)

    return code_list

##업종명 코드를 리스트로 만드는 함수
def make_industry_name(code_list, read_data):

    industry_name = []

    # code번호 숫자만큼 반복
    for i in range(len(code_list)):

        # code번호가 1개인 것
        if len(code_list[i]) == 1:
            code = int(code_list[i][len(code_list[i])-1]) # code번호
            for key, value in read_data.items(): # 딕션너리 안에 value 값을 코드번호와 비교하면서 해당하는 업종명을 리스트에 추가
                if code in value:
                    industry_name.append(key)
                    break

        # code번호가 여러개인 것
        else:
            a_list = []
            for j in code_list[i]:  # code 번호가 여러개인 것을 하나씩 불러오기
                number = int(j)
                for key, value in read_data.items():  # 딕션너리 안에 value 값을 코드번호와 비교하면서 해당하는 업종명을 리스트에 추가
                    if number in value:
                        a_list.append(key)
                        break
            a_list = list(set(a_list))  # 중복제거하고 다시 리스트로 변환
            industry_name.append(a_list)  # 리스트로 추가
    return industry_name

def modify_data(data, industry_name):
    data['업종명'] = industry_name
    del data['업종제한내용']
    modified_data = data[['낙찰자결정방법', '입찰률', '업종명']]

    return modified_data


def vec_x_data(data):
    #from sklearn.feature_extraction import DictVectorizer

    x_data = data

    # 원 핫 인코딩을 위해 데이터 가공
    df = []
    for i in range(len(x_data)):
        df.append({'낙찰자결정방법': x_data['낙찰자결정방법'][i], '입찰률': x_data['입찰률'][i], '업종명': x_data['업종명'][i]})

    # 원 핫 인코딩
    vec = DictVectorizer(sparse=False, dtype=float)
    df1 = pd.DataFrame(vec.fit_transform(df))
    df1.columns = vec.get_feature_names()  # 컬럼명 변경
    return df1

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
    print(X_data)

    model = joblib.load('./restApi/resource/model.pkl')
    pred = model.predict(X_data.to_numpy())
    return pred
