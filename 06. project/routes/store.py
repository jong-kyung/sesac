from flask import Blueprint, render_template, redirect, url_for, request
from common.verify import check_login
from common.sqlite_query import SQLite3_query
import math

store = Blueprint('store', __name__)

@store.route('/store')
@check_login
def store_list():  
    page = request.args.get('page', default=1, type=int) 
    search_name = request.args.get('name', default='', type=str)
    sub_data = request.args.get('sub-data', default='', type=str)
    try:
        per_page = 10
        
        stores = SQLite3_query('stores')
        headers = stores.schema_query() # schema 받아오기
        store_types = stores.find_data_query('Type') # Type 받아오기
        result_datas = [] # 결과 데이터 삽입용
        datas = stores.condition_data_query(page, per_page, 'Name', search_name, 'Type', sub_data)
        print(search_name, sub_data) 

        # -------- 페이지네이션 --------
        total_data_len = datas['data_length'] # 데이터 전체 갯수
        page_range = math.ceil(total_data_len/per_page) # 페이지 갯수 구하기
            # ---- 데이터 자르기 ----
        result_datas = datas['datas'] # 데이터 자르기
        
        # 의도치 않은 페이지 이동시 예외처리
        if page < 1:
            page = 1
            return redirect(url_for('store.sotre_list'))
        elif page > page_range:
            page = page_range
            return redirect(url_for('store.store_list'))

       # 페이지네이션
        start_page = page - (page-1) % 5 # 5개 단위로 끊기
        end_page = min(start_page + 4, page_range) # 끝페이지 정해주기
        
        return render_template('component/store.html', search_name = search_name, sub_data = sub_data, page = page, types = store_types, headers = headers, datas = result_datas, page_range = page_range, start_page = start_page, end_page = end_page)
    
    except TypeError:
        return redirect('store', next='/1')

@store.route('/store/<param>')
@check_login
def store_info(param):
    store = SQLite3_query('stores')
    headers = store.schema_query()
    findData = store.detail_info(param)

    return render_template('search_detail.html', headers=headers,datas=findData)
