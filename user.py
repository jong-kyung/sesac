users = [
    {"name": "Alice", "age": 25, "location": "Seoul", "car": "BMW"},
    {"name": "Bob", "age": 30, "location": "Busan", "car": "Mercedes"},
    {"name": "Charlie", "age": 35, "location": "Daegu", "car": "Audi"},
]

# 이름을 입력 받아 사용자 정보(딕셔너리)를 반납하시오.
search_bob = {
    'name':'Bob',
    'age':30
}

def find_users(search_user):
    result = []

    for user in users:
        if user['name'] == search_user['name'] and user['age'] == search_user['age']:
            result.append(user)

    return result

result = find_users(search_bob)
print(result)