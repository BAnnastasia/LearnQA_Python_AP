import requests

def fulfill_requests (mas_obj,is_empty):
    if is_empty ==1:
        print(f"Следующие запросы будут выполены  с параметром method")
        for var in mas_obj:
            print(f"метод: {var.get("method").upper()}, параметр: {var.get("method").upper()}")
            execString = 'requests.' + var.get(
            "method") + '("https://playground.learnqa.ru/ajax/api/compare_query_type", ' + var.get(
            "params") + '={"method":"' + var.get("method").upper() + '"})'
            response1 = eval(execString)
            print(response1.text)
            print(response1.status_code)
        return "Готово"
    else:
        print(f"Следующие запросы будут выполены  без параметра method")
        for var in mas_obj:
            print(f"метод: {var.get("method").upper()}, параметра: нет")
            execString = 'requests.' + var.get(
                "method") + '("https://playground.learnqa.ru/ajax/api/compare_query_type")'
            response1 = eval(execString)
            print(response1.text)
            print(response1.status_code)
        return "Готово"
def test_f(mas_obj, params):
    for var in mas_obj:
        for var2 in params:
            execString = 'requests.' + var.get(
            "method") + '("https://playground.learnqa.ru/ajax/api/compare_query_type", ' + var.get(
            "params") + '={"method":"' + var2 + '"})'
            response1 = eval(execString)

            if (var.get("method").upper() != var2) & (('success' in response1.text) & (response1.status_code == 200)):
                print(f" Типы не совпадают, ответ успешный: {response1.text}! метод: {var.get("method").upper()} параметр: {var2} статус: {response1.status_code}")

            if (var.get("method").upper() == var2) & (('success' not in response1.text) | (response1.status_code != 200)):
                print(f" Типы совпадают, ответ неуспешный: {response1.text}! метод: {var.get("method").upper()} параметр: {var2} статус: {response1.status_code}")

    return "Готово"




method = [{"method": "post","params": "data"},{"method": "get","params": "params"},{"method": "put", "params": "data"}, {"method": "delete", "params": "data"}]
method2 = [{"method": "head", "params": "data"},{"method": "options", "params": "data"},{"method": "patch","params": "data"}]
params_m =["POST","GET","PUT","DELETE","HEAD","OPTIONS","PATH"]


print(f"Тест 1. Исходная строка: {method}")
print(fulfill_requests(method,0)) # 1. Делает http-запрос любого типа без параметра method, описать что будет выводиться в этом случае.

print(f"Тест 2 Исходная строка: {method2}")
print(fulfill_requests(method2,0)) # 2. Делает http-запрос не из списка. Например, HEAD. Описать что будет выводиться в этом случае.

print(f"Тест 3.1 Исходная строка: {method}")
print(fulfill_requests(method,1)) # 3.Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.
print(f"Тест 3.2  Исходная строка: {method2}")
print(fulfill_requests(method2,1)) # 3.Делает запрос с правильным значением method. Описать что будет выводиться в этом случае.

#4. С помощью цикла проверяет все возможные сочетания реальных типов запроса и значений параметра method. Например
# с GET-запросом передает значения параметра method равное ‘GET’, затем ‘POST’, ‘PUT’, ‘DELETE’ и так далее.
# И так для всех типов запроса. Найти такое сочетание, когда реальный тип запроса не совпадает со значением параметра,
# но сервер отвечает так, словно все ок. Или же наоборот, когда типы совпадают, но сервер считает, что это не так

print(f"Тест 4")
print(test_f(method,params_m))
print(test_f(method2,params_m))
