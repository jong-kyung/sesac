from flask import Blueprint, render_template, redirect, url_for, request
from common.verify import check_login
from common.sqlite_query import SQLite3_query

import math

user = Blueprint('user', __name__)

# TODO : 만약 주소창에 -1을 입력할경우엔 어떻게 할것인지?
@user.route('/user')
@check_login
def user_list():  
    page = request.args.get('page', default=1, type=int) 
    search_name = request.args.get('name', default='', type=str)
    sub_data = request.args.get('sub-data', default='', type=str)
    try:
        per_page = 10

        users = SQLite3_query('users')
        headers = users.schema_query() # schema 받아오기
        result_datas = [] # 결과 데이터 삽입용
        datas = users.condition_data_query(page, per_page, 'Name', search_name, 'Gender', sub_data)

        # -------- 페이지네이션 --------
        total_data_len = datas['data_length'] # 데이터 전체 갯수
        page_range = math.ceil(total_data_len/per_page) # 페이지 갯수 구하기
            # ---- 데이터 자르기 ----
        result_datas = datas['datas'] # 데이터 자르기
        
        # 의도치 않은 페이지 이동시 예외처리
        if page < 1:
            page = 1
            return redirect(url_for('user.user_list'))
        elif page > page_range:
            page = page_range
            return redirect(url_for('user.user_list'))

       # 페이지네이션
        start_page = page - (page-1) % 5 # 5개 단위로 끊기
        end_page = min(start_page + 4, page_range) # 끝페이지 정해주기
        
        return render_template('component/user.html', search_name = search_name, sub_data = sub_data, page = page, headers = headers, datas = result_datas, page_range = page_range, start_page = start_page, end_page = end_page)
    
    except TypeError:
        return redirect('user', next='/1')



@user.route('/user/<param>')
@check_login
def user_info(param):
    user = SQLite3_query('users')
    headers = user.schema_query()
    findData = user.detail_info(param)

    return render_template('component/user_detail.html', headers=headers,datas=findData)
