import requests
import json
import sys

# Базовый URL вашего сервера
BASE_URL = "http://127.0.0.1:8000/api"

def print_test_result(test_name, status_code, response_data, success_message=None):
    print(f"\n{'='*60}")
    print(f"{test_name}...")
    print(f"   Status: {status_code}")
    
    if 200 <= status_code < 300:
        print(f"{success_message or 'Success!'}")
        if response_data and test_name != "Getting restaurants with filters":
            # Для больших списков показываем только первую запись
            if isinstance(response_data, dict) and 'results' in response_data:
                sample_data = {
                    "count": response_data.get("count"),
                    "sample": response_data["results"][0] if response_data["results"] else "No data"
                }
                print(f"Response: {json.dumps(sample_data, ensure_ascii=False, indent=4)}")
            else:
                print(f"Response: {json.dumps(response_data, ensure_ascii=False, indent=4)}")
    else:
        print(f"Failed!")
        if response_data:
            print(f"Error: {response_data}")

def test_api():
    print("Starting SearchLOC API Tests...")
    print("="*60)
    
    # 1. Health Check
    try:
        response = requests.get(f"{BASE_URL}/health/")
        data = response.json() if response.content else {}
        print_test_result(
            "1. Health check",
            response.status_code,
            data,
            f"{data.get('message', 'API is running')}"
        )
    except Exception as e:
        print(f"Health check failed: {e}")
        # Fallback - попробуем получить рестораны
        try:
            response = requests.get(f"{BASE_URL}/restaurants/")
            status = "API is running (via restaurants)" if response.status_code == 200 else "API issues"
            print(f"1. Health check... Status: {response.status_code} - {status}")
        except:
            print("API is not accessible")
            return
    
    # 2. Get cuisine types
    try:
        response = requests.get(f"{BASE_URL}/cuisines/")
        data = response.json() if response.content else {}
        count = len(data) if isinstance(data, list) else data.get('count', 0)
        print_test_result(
            "2. Get cuisine types",
            response.status_code,
            data,
            f"Found {count} cuisine types"
        )
    except Exception as e:
        print(f"Cuisine types test failed: {e}")
    
    # 3. Get all restaurants
    try:
        response = requests.get(f"{BASE_URL}/restaurants/")
        data = response.json() if response.content else {}
        count = data.get('count', len(data.get('results', [])))
        print_test_result(
            "3. Getting all restaurants",
            response.status_code,
            data,
            f"Found {count} restaurants"
        )
    except Exception as e:
        print(f"Restaurants test failed: {e}")
    
    # 4. Search restaurants
    try:
        response = requests.get(f"{BASE_URL}/restaurants/search/?q=Ruski")
        data = response.json() if response.content else {}
        print_test_result(
            "4. Searching restaurants",
            response.status_code,
            data,
            f"Search completed with query 'Ruski'"
        )
    except Exception as e:
        print(f"Search test failed: {e}")
    
    # 5. Get restaurant details (если есть рестораны)
    try:
        list_response = requests.get(f"{BASE_URL}/restaurants/")
        if list_response.status_code == 200:
            restaurants_data = list_response.json()
            restaurants = restaurants_data.get('results', [])
            if restaurants:
                first_restaurant_id = restaurants[0]['id']
                response = requests.get(f"{BASE_URL}/restaurants/{first_restaurant_id}/")
                data = response.json() if response.content else {}
                print_test_result(
                    "5. Getting restaurant details",
                    response.status_code,
                    data,
                    f"Details for: {data.get('name', 'Unknown')}"
                )
            else:
                print("\n" + "="*60)
                print("5. Getting restaurant details...")
                print("Status: 404")
                print("No restaurants found for details test")
        else:
            print("\n" + "="*60)
            print("5. Getting restaurant details...")
            print("Status: 404")
            print("Cannot get restaurant list")
    except Exception as e:
        print(f"Restaurant details test failed: {e}")
    
    print("\n" + "="*60)
    print("API Testing Completed!")
    print("="*60)

if __name__ == "__main__":
    try:
        requests.get("http://127.0.0.1:8000/", timeout=2)
        test_api()
    except requests.exceptions.ConnectionError:
        print("Ошибка: Django сервер не запущен!")
        print("Запустите сервер командой: python manage.py runserver")
        sys.exit(1)
    except requests.exceptions.Timeout:
        print("Ошибка: Таймаут подключения к серверу!")
        print("Убедитесь что сервер запущен на http://127.0.0.1:8000/")
        sys.exit(1)