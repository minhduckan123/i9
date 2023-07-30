import sys
import time
import unicodedata
import requests
import random
import pytesseract
import re
import io
from PIL import Image
import base64
from queue import Queue 
import threading


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

pytesseract.pytesseract.tesseract_cmd = "D:/Everything_other/Tesseract/Tesseract-OCR/tesseract.exe"
chromedriver_path = 'chromedriver.exe'
proxy = '52.205.102.3:31112:gripp_of9xwn:V7fFEkOj9bjhICGh_country-vn'
ipp, port, user, pas_ = proxy.split(":")
ip = f"http://{user}:{pas_}@{ipp}:{port}"
proxies = {"http": ip , "https": ip}

def deleteline(filename, text):
    with open(filename, encoding="utf-8") as file:
        data = file.read().splitlines()
        file.close()
        if text in data:
            data.remove(text)
            with open(filename, "w", encoding="utf-8") as file:
                file.write("\n".join(data))
                file.write('\n')
                file.close()
# def getProxyDT(key):
    
#     while True:
#         try:                
#             ip = requests.get(f"https://app.proxydt.com/api/public/proxy/get-new-proxy?license={key}&authen_ips={ip_me}").json()
#             # print(ip)
#         except:
#             continue
#         if ip["code"] == 1:
#             ipcc = ip['data']['http_ipv4']
#             if 'null:' in ipcc:
#                 continue
#             return ipcc
#         else:
#             if "Không tìm thấy license" in str(ip) or "Yêu cầu license key & whitelist Ip!" in str(ip) or 'Token không hợp lệ.' in str(ip):
#                 return "KEYEXPIRED"
#             for ll in range(5, -1, -1):
#                 print(f"Vui lòng đợi {str(ll)} để đổi ip lần nữa        ", end="\r")
#                 time.sleep(1) 
def imgtotext(link: str="https://i9bet41.com/api/0.0/Home/GetCaptchaForRegister"):
    captcha = requests.post(link).json()
    base64_img = captcha["image"]
    value = captcha["value"]
    img = Image.open(io.BytesIO(base64.b64decode(base64_img)))
    text = str(pytesseract.image_to_string(img)).strip()
    # img.show("ci")
    return text, value
def create(key):
    global iterUser, names
    print(f'Luồng {key}: Đang tạo tài khoản!')
    while True:
        # ip = getProxyDT(key)
        # print(ip)
        proxies = {"http": ip , "https": ip}
        def r():
            try:
                text, value = imgtotext()
                if text == '': return r()
                try: username = next(iterUser)
                except: sys.exit()
                try: name = next(names)
                except: sys.exit()
                deleteline("name.txt", name)
                deleteline("username.txt", username)
                letters = re.findall(r'[a-zA-Z]', username)
                password = ''.join(letters) + str(random.randint(100, 999))
                name = unicodedata.normalize('NFD', name).encode('ascii', 'ignore').decode('utf-8').upper()
                dataJson = {"account": username,"password": f"{password}","confirm_Password": f"{password}","moneyPassword":None,"name":name,"countryCode":"63","mobile":None,"email":None,"sex":None,"birthday":None,"idNumber":None,"qqAccount":None,"groupBank":None,"bankName":None,"bankProvince":None,"bankCity":None,"bankAccount":None,"checkCodeEncrypt":value,"checkCode":text,"isRequiredMoneyPassword":False,"dealerAccount":None,"parentAccount":"vip888"}
                reg = requests.post("https://i9bet41.com/api/1.0/member/register", json=dataJson, proxies=proxies)
                if "AccessToken" in reg.text:
                    
                    reg = reg.json()
                    headers = {"Authorization": "Bearer "+reg["Result"]["Token"]["AccessToken"]}
                    dd = diemdanh(headers, proxies)
                    if dd:
                        with open("acc.txt", "a+", encoding="utf-8") as file:
                            file.write(f"%s|{password}|%s\n"%(username, name))
                        print(f"Luồng {key}", username, "tạo và điểm danh thành công!")
                        danhsx(headers, f"%s|{password}|%s"%(username, name))
                    else: 
                        with open("acc.txt", "a+", encoding="utf-8") as file:
                            file.write(f"%s|{password}|%s\n"%(username, name))
                        print(f"Luồng {key}", username, "tạo thành công!")
                        
                elif 'Lỗi mã xác minh hoặc lỗi đầu vào, vui lòng quay lại' in reg.text:
                    # print("Lỗi mã xác minh")
                    return r()
                elif "IP này đã đạt" in reg.text:
                    print("IP đã đạt giới hạn!\nHãy dừng lại!\n\n")
                # else:
                #     print(reg.text)
            except Exception as e: pass
        r()
    
def diemdanh(headers, proxies=""):
    point = 0
    try:
        balance = requests.post('https://i9bet41.com/api/0.0/Account/GetMyBalance', headers=headers, proxies=proxies).text
        dd = requests.post('https://i9bet41.com/api/1.0/checkinOffer/checkIn', headers=headers, proxies=proxies).json()
        # print(dd)
        balance1 = requests.post('https://i9bet41.com/api/0.0/Account/GetMyBalance', headers=headers, proxies=proxies).text
        # print(dd, balance1)
        return balance != balance1
    except Exception as e:
        # point+=1
        # if point >3:
        #     return False
        return diemdanh(headers)
def login(username, pwd):
    try:
        text, value = imgtotext("https://i9bet41.com/api/0.0/Home/GetCaptchaForLogin")
        if text == "": return login(username, pwd)
        dataJson = {"account":username,"password":pwd,"checkCode":text,"checkCodeEncrypt":value,"fingerprint":"75f50996870104695a43fc83e2e56276"}
        lg = requests.post("https://i9bet41.com/api/0.0/Login/login", json=dataJson)
        # print(lg.text)
        if "LoginToken" in lg.text: 
            token = lg.json()["LoginToken"]["AccessToken"]
            return token
        else: return login(username, pwd)
    except: 
        return login(username, pwd)
def autodanhsx(data):
    d = data.split("|")
    username, pwd = d[0], d[1]
    # print(username)
    headers = {"Authorization": "Bearer "+login(username, pwd)}
    # print(headers)
    danhsx(headers, data)
def autodiemdanh(data):
    d = data.split("|")
    username, pwd = d[0], d[1]
    # print(username)
    headers = {"Authorization": "Bearer "+login(username, pwd)}
    dd = diemdanh(headers)
    if dd:
        print(username, "điểm danh thành công!")
        with open("accdiemdanh.txt", "a+", encoding="utf-8") as file:
            file.write("%s\n"%(data))
        deleteline("acc.txt", data)
    else:
        print(username, "điểm danh thất bại!")
def danhsx(headers, data):
    
    # headers = {"Authorization": "Bearer "+login(username, pwd)}
    balance = requests.post('https://i9bet41.com/api/0.0/Account/GetMyBalance', headers=headers).text
    
    def d():
        global iterNum
        try:
            l = requests.get("https://i9bet41.com/api/1.0/account/loginToGame?SupplierType=Tp&gid=1568", headers=headers).json()
            url = l["Result"]["Url"]
            if url is None: return d()
            url = requests.get(url)
            # print(cookie_info)
            url = url.url
            # print(url)
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--log-level=3')
            chrome_options.add_argument('--blink-settings=imagesEnabled=false')
            try:
                driver = webdriver.Chrome(executable_path=chromedriver_path, options=chrome_options)
            except:
                driver = webdriver.Chrome(options=chrome_options)
            
            actions = ActionChains(driver)

            wait = WebDriverWait(driver, 20)
            wait5 = WebDriverWait(driver, 5)
            wait1 = WebDriverWait(driver, 1)
            driver.get(url)
            wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Xổ Số Việt Nam-MIỀN BẮC']"))).click()
            time.sleep(1)
            if "OKBtn" in driver.page_source:
                wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="OKBtn"]'))).click()
            
            cuoc = driver.find_element(By.XPATH, '//div[@id="lotteryInfo"]//div[@class="txtBlue"]').text
            if cuoc == "0": 
                return
            try:
                num = next(iterNum)
            except: 
                iterNum = iter(nums)
                num = next(iterNum)
            if dd == "4D":
                wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "4D")]'))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Đuôi']"))).click()
                # bangsx = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-v-85fcb22a]/div[3]")))
                for i in range(4):
                    so = num[i]
                    wait.until(EC.presence_of_element_located((By.XPATH, f"//div[@data-v-85fcb22a]/div[3]/div[{i+1}]/div[2]/div[text()='{so}']"))).click()
                    
                wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="TicketCheckBtn active"]'))).click()
                for i in str(cuoc):
                    wait.until(EC.element_to_be_clickable((By.XPATH, f'//div[contains(@class, "keyboardNBBtn")][text()="{i}"]'))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Đặt cược']"))).click()
            elif dd == "3D":
                wait.until(EC.element_to_be_clickable((By.XPATH, '//span[contains(text(), "3D")]'))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, "//*[text()='Đuôi']"))).click()
                # bangsx = wait.until(EC.presence_of_element_located((By.XPATH, "//div[@data-v-85fcb22a]/div[2]")))
                if int(num) < 100:
                    wait.until(EC.presence_of_element_located((By.XPATH, f'//div[text()="{num}"]'))).click()
                    
                elif int(num) < 200:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-v-85fcb22a]/div[2]/div[1]/div[2]'))).click()
                    wait.until(EC.presence_of_element_located((By.XPATH, f'//div[@data-v-85fcb22a]/div[2]/div[2]/div[text()="{num}"]'))).click()

                elif int(num) < 300:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-v-85fcb22a]/div[2]/div[1]/div[3]'))).click()
                    wait.until(EC.presence_of_element_located((By.XPATH, f'//div[@data-v-85fcb22a]/div[2]/div[2]/div[text()="{num}"]'))).click()

                elif int(num) < 400:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-v-85fcb22a]/div[2]/div[1]/div[4]'))).click()
                    wait.until(EC.presence_of_element_located((By.XPATH, f'//div[@data-v-85fcb22a]/div[2]/div[2]/div[text()="{num}"]'))).click()

                elif int(num) < 500:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-v-85fcb22a]/div[2]/div[1]/div[5]'))).click()
                    wait.until(EC.presence_of_element_located((By.XPATH, f'//div[@data-v-85fcb22a]/div[2]/div[2]/div[text()="{num}"]'))).click()

                elif int(num) < 600:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-v-85fcb22a]/div[2]/div[1]/div[6]'))).click()
                    wait.until(EC.presence_of_element_located((By.XPATH, f'//div[@data-v-85fcb22a]/div[2]/div[2]/div[text()="{num}"]'))).click()

                elif int(num) < 700:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-v-85fcb22a]/div[2]/div[1]/div[7]'))).click()
                    wait.until(EC.presence_of_element_located((By.XPATH, f'//div[@data-v-85fcb22a]/div[2]/div[2]/div[text()="{num}"]'))).click()

                elif int(num) < 800:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-v-85fcb22a]/div[2]/div[1]/div[8]'))).click()
                    wait.until(EC.presence_of_element_located((By.XPATH, f'//div[@data-v-85fcb22a]/div[2]/div[2]/div[text()="{num}"]'))).click()

                elif int(num) < 900:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-v-85fcb22a]/div[2]/div[1]/div[9]'))).click()
                    wait.until(EC.presence_of_element_located((By.XPATH, f'//div[@data-v-85fcb22a]/div[2]/div[2]/div[text()="{num}"]'))).click()

                elif int(num) < 1000:
                    wait.until(EC.presence_of_element_located((By.XPATH, '//div[@data-v-85fcb22a]/div[2]/div[1]/div[10]'))).click()
                    wait.until(EC.presence_of_element_located((By.XPATH, f'//div[@data-v-85fcb22a]/div[2]/div[2]/div[text()="{num}"]'))).click()

                wait.until(EC.element_to_be_clickable((By.XPATH, '//div[@class="TicketCheckBtn active"]'))).click()
                for i in str(cuoc):
                    wait.until(EC.element_to_be_clickable((By.XPATH, f'//div[contains(@class, "keyboardNBBtn")][text()="{i}"]'))).click()
                wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Đặt cược']"))).click()
            for i in range(30):
                if "Đặt cược thành công" in driver.page_source:
                    print(data, "đánh thành công, số: %s"%num)
                    with open("accdanhsx.txt", "a+", encoding="utf-8") as file:
                        file.write("%s|số đề: %s, số tiền: %s\n"%(data, num, cuoc))
                    deleteline("acc.txt", data)
                    break
                
                time.sleep(0.5)
            driver.quit()
        except Exception as e: 
            # print(e)
            pass

        
    b = int(float(balance))

    if b >= 1:
        d()
def diemdanhdanhsx(data):
    d = data.split("|")
    username, pwd = d[0], d[1]
    # print(username)
    headers = {"Authorization": "Bearer "+login(username, pwd)}
    dd = diemdanh(headers)
    if dd:
        print(username, "điểm danh thành công!")
        danhsx(headers, data)
    else:
        print(username, "điểm danh thất bại!")
ip_me = requests.get('https://api.ipify.org/?format=json').json()["ip"]

# for i in range(0, 100):
#     print(next(iterNum))

jobs = Queue()

indexDD = 0
indexDD2 = 1
indexD = 0
indexD2 = 1
print("""1. Tạo acc
2. Điểm danh
3. Đánh đề (max tiền)
4. Điểm danh + đánh đề(max tiền)""")
choose = input("Vui lòng chọn: ")
print("1. 3D\n2. 4D")
dd = input("Vui lòng chọn loại sx: ")

with open("accdanhsx.txt", "r", encoding='utf-8') as f:
    dsso = f.readlines()[::-1]

if dd == "1":
    dd = "3D"
    nums = []
    for i in range(0, 1000):
        if len(str(i)) < 2:
            nums += ["00"+str(i)]
        elif len(str(i)) < 3:
            nums += ["0"+str(i)]
        else:
            nums += [str(i)]
    
    for i in dsso:
        sodanhcuoi = -1
        if len(i.split("số đề: ")[1].split(", số")[0]) ==3:
            sodanhcuoi = i.split("số đề: ")[1].split(", số")[0]
            break

elif dd == "2":
    dd = "4D"
    nums = []
    for i in range(0, 10000):
        if len(str(i)) < 2:
            nums += ["000"+str(i)]
        elif len(str(i)) < 3:
            nums += ["00"+str(i)]
        elif len(str(i)) < 4:
            nums += ["0"+str(i)]    
        else:
            nums += [str(i)]

    for i in dsso:
        sodanhcuoi = -1
        if len(i.split("số đề: ")[1].split(", số")[0]) ==4:
            sodanhcuoi = i.split("số đề: ")[1].split(", số")[0]
            break
iterNum = iter(nums)
while True:
    try:
        num = next(iterNum)
        if int(num) <= int(sodanhcuoi):
            continue
        break
    except: 
        iterNum = iter(nums)
        break
# choose = "1"
if choose == "1":
    keys = open("keys.txt", encoding="utf-8").read().splitlines()
    nn = open("name.txt", encoding="utf-8").read().splitlines()
    uu = open("username.txt", encoding="utf-8").read().splitlines()
    names = iter(nn)
    iterUser = iter(uu)
    # for i in keys:
    #     create(i)
    def do_stuff(jobs, key):
        while not jobs.empty():
                value = jobs.get()
                create(key)
                jobs.task_done()
    if len(nn)<=len(uu):
        for i in range(len(nn)):
            jobs.put(i)
    else:
        for i in range(len(uu)):
            jobs.put(i)
    if __name__ == "__main__":

        for i in range(len(keys)):
            key = i
            worker = threading.Thread(target=do_stuff, args=(jobs,key,))
            worker.start()
        print("waiting for queue to complete", jobs.qsize(), "tasks")
        jobs.join()
else:
    if choose == "2":
        luong = int(input("Nhập luồng: "))
        
        def do_stuff(jobs, key):
            while not jobs.empty():
                value = jobs.get()
                autodiemdanh(value)
                jobs.task_done()
                
    # print(danhsx("Daison2", "{password}"))
    elif choose == "3":
        luong = int(input("Nhập luồng: "))
        def do_stuff(jobs, key):
            while not jobs.empty():
                value = jobs.get()
                autodanhsx(value)
                jobs.task_done()
    elif choose == "4":
        luong = int(input("Nhập luồng: "))
        def do_stuff(jobs, key):
            while not jobs.empty():
                value = jobs.get()
                diemdanhdanhsx(value)
                jobs.task_done()
    
    for i in open("acc.txt", encoding="utf-8").read().splitlines():
        jobs.put(i)

    if __name__ == "__main__":

        for i in range(luong):
            worker = threading.Thread(target=do_stuff, args=(jobs,i,))
            worker.start()
        print("waiting for queue to complete", jobs.qsize(), "tasks")
        jobs.join()
    
