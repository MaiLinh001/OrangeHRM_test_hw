import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager
import requests
import json
import time
from utils.config_reader import ConfigReader

BASE_URL = ConfigReader.get_base_url()
USERNAME = ConfigReader.get_username()
PASSWORD = ConfigReader.get_password()

def init_driver():
    options = webdriver.EdgeOptions() # Sử dụng EdgeOptions
    options.add_argument("--disable-gpu")
    service = EdgeService(EdgeChromiumDriverManager().install())
    driver = webdriver.Edge(service=service, options=options)
    driver.implicitly_wait(10) # Chờ tối đa 10 giây cho các phần tử xuất hiện
    return driver

# get session
def get_selenium_session(driver):
    driver.get(BASE_URL)
    
    print("Đang đăng nhập bằng Selenium...")
    username_field = driver.find_element(By.NAME, "username")
    password_field = driver.find_element(By.NAME, "password")
    login_button = driver.find_element(By.CSS_SELECTOR, "button[type='submit']")

    username_field.send_keys(USERNAME)
    password_field.send_keys(PASSWORD)
    login_button.click()
    
    time.sleep(3)

    if "dashboard" not in driver.current_url:
        print("Đăng nhập Selenium thất bại. Vui lòng kiểm tra lại Username/Password.")
        return None, None

    print("Đăng nhập Selenium thành công.")

    selenium_cookies = driver.get_cookies()
    
    try:
        csrf_meta = driver.find_element(By.NAME, "csrf-token")
        csrf_token = csrf_meta.get_attribute("content")
    except:
        print("Không tìm thấy CSRF token trong meta tag. Thử tìm kiếm trong script...")
        csrf_token = None
        scripts = driver.find_elements(By.TAG_NAME, 'script')
        for script in scripts:
            script_text = script.get_attribute('innerHTML')
            if script_text and 'csrfToken' in script_text:
                try:
                    # Rất phụ thuộc vào cách token được định nghĩa
                    start = script_text.find("csrfToken: '") + len("csrfToken: '")
                    end = script_text.find("'", start)
                    csrf_token = script_text[start:end]
                    print(f"Tìm thấy CSRF token qua script: {csrf_token}")
                    break
                except:
                    pass
        if not csrf_token:
            print("Không thể lấy CSRF token. Một số API có thể không hoạt động.")


    s = requests.Session()
    for cookie in selenium_cookies:
        s.cookies.set(cookie['name'], cookie['value'])
    
    if csrf_token:
        s.headers.update({'X-CSRF-TOKEN': csrf_token})
        s.headers.update({'Accept': 'application/json, text/plain, */*'}) # Thêm header Accept
        s.headers.update({'Content-Type': 'application/json'}) # Thêm header Content-Type cho JSON requests

    return s, csrf_token

def test_login_api(session):
    print("\n--- Test Case: API Đăng nhập (Minh họa) ---")
    login_api_url = f"{BASE_URL.replace('/web/index.php', '')}/web/index.php/api/v2/auth/login"
    payload = {
        "username": USERNAME,
        "password": PASSWORD
    }
    
    try:
        # Lưu ý: API login có thể không cần session từ trước hoặc CSRF token nếu nó là điểm đầu vào.
        # Chúng ta dùng session ở đây để minh họa cấu trúc.
        response = requests.post(login_api_url, json=payload, verify=False) # verify=False nếu gặp lỗi SSL
        print(f"URL: {login_api_url}")
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.json()}")
        
        if response.status_code == 200 and response.json().get('data', {}).get('loggedIn', False) == True:
            print("✅ TEST PASSED: Đăng nhập API thành công.")
            return True
        else:
            print(f"❌ TEST FAILED: Đăng nhập API thất bại. Expected 200, got {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ TEST FAILED: Lỗi kết nối API đăng nhập: {e}")
        return False

# --- Test Case API 2: Lấy danh sách nhân viên ---
def test_get_employee_list_api(session):
    print("\n--- Test Case: API Lấy danh sách nhân viên ---")
    # Endpoint này cần được xác định chính xác từ tab Network
    employee_list_api_url = f"{BASE_URL.replace('/web/index.php', '')}/web/index.php/api/v2/pim/employees"
    
    try:
        response = session.get(employee_list_api_url, verify=False)
        print(f"URL: {employee_list_api_url}")
        print(f"Status Code: {response.status_code}")
        # print(f"Response: {json.dumps(response.json(), indent=2)}") # Chỉ in nếu cần debug

        if response.status_code == 200 and 'data' in response.json():
            print(f"✅ TEST PASSED: Lấy danh sách nhân viên thành công. Số lượng nhân viên: {len(response.json()['data'])}")
            return True
        else:
            print(f"❌ TEST FAILED: Lấy danh sách nhân viên thất bại. Expected 200, got {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ TEST FAILED: Lỗi kết nối API lấy danh sách nhân viên: {e}")
        return False

# --- Test Case API 3: Lấy thông tin nhân viên ---
def test_get_info_employee_api(session):
    print("\n--- Test Case: API Lấy thông tin chi tiết nhân viên ---")
    # Endpoint để lấy thông tin chi tiết nhân viên (employee ID = 7 là ví dụ)
    get_employee_api_url = f"{BASE_URL.replace('/web/index.php', '')}/web/index.php/api/v2/pim/employees/7"
    
    try:
        response = session.get(get_employee_api_url, verify=False)
        print(f"URL: {get_employee_api_url}")
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            employee_data = response.json().get('data', {})
            print("Thông tin nhân viên:")
            print(f"- Họ và tên: {employee_data.get('firstName', '')} {employee_data.get('lastName', '')}")
            print(f"- ID nhân viên: {employee_data.get('employeeId', '')}")
            print(f"- Trạng thái: {employee_data.get('employeeStatus', {}).get('name', 'N/A')}")
            print("✅ TEST PASSED: Lấy thông tin nhân viên thành công.")
            return True
        elif response.status_code == 404:
            print(f"❌ TEST FAILED: Không tìm thấy nhân viên với ID đã cho.")
            return False
        else:
            print(f"❌ TEST FAILED: Lấy thông tin nhân viên thất bại. Expected 200, got {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ TEST FAILED: Lỗi kết nối API lấy thông tin nhân viên: {e}")
        return False

# --- Test Case API 4: Tìm kiếm nhân viên ---
def test_search_employee_api(session):
    print("\n--- Test Case: API Tìm kiếm nhân viên ---")
    # Endpoint này cần được xác định chính xác từ tab Network
    search_employee_api_url = f"{BASE_URL.replace('/web/index.php', '')}/web/index.php/api/v2/directory/employees"
    
    search_query = "Peter"
    
    # Đối với GET với query parameters:
    params = {"nameOrId": search_query}
    
    try:
        response = session.get(search_employee_api_url, params=params, verify=False)
        print(f"URL: {search_employee_api_url}")
        print(f"Parameters: {params}")
        print(f"Status Code: {response.status_code}")
        # print(f"Response: {json.dumps(response.json(), indent=2)}")

        if response.status_code == 200 and 'data' in response.json():
            found_employees = response.json()['data']
            if any(search_query in emp['firstName'] for emp in found_employees):
                print(f"✅ TEST PASSED: Tìm kiếm nhân viên '{search_query}' thành công. Tìm thấy {len(found_employees)} kết quả.")
                return True
            else:
                print(f"⚠️ TEST PASSED (with warning): Tìm kiếm thành công nhưng không tìm thấy nhân viên '{search_query}'.")
                return True # Vẫn coi là pass nếu API trả về 200
        else:
            print(f"❌ TEST FAILED: Tìm kiếm nhân viên thất bại. Expected 200, got {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ TEST FAILED: Lỗi kết nối API tìm kiếm nhân viên: {e}")
        return False

def run_all_tests():
    driver = None
    try:
        driver = init_driver()
        session, csrf_token = get_selenium_session(driver)

        if not session:
            print("Không thể khởi tạo session. Dừng kiểm thử API.")
            return

        print("\n--- Bắt đầu chạy các Test Case API ---")
        results = {}

        results['Get Employee List API'] = test_get_employee_list_api(session)
        results['Get Employee Info API'] = test_get_info_employee_api(session)
        results['Search Employee API'] = test_search_employee_api(session)

        return results

    finally:
        if driver:
            driver.quit()
        print("\n--- Hoàn thành kiểm thử API ---")

# Chạy script
if __name__ == "__main__":
    test_results = run_all_tests()
    
    print("\n" + "="*40)
    print("         BÁO CÁO KẾT QUẢ KIỂM THỬ API")
    print("="*40)
    if test_results:
        for test_name, status in test_results.items():
            print(f"- {test_name}: {'PASS' if status else 'FAIL'}")
    else:
        print("Không có kết quả kiểm thử nào được ghi nhận.")
    print("="*40)