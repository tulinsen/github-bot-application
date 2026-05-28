from selenium import webdriver
from userinfo import username, password
import time
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC



class GitHub:
    def __init__(self):
        
        self.chrome_driver_path = ""
        self.browser = webdriver.Edge()
        self.baseUrl = "https://github.com/"
        self.username = username
        self.password = password

    def signIn(self):
        self.browser.get(self.baseUrl + "login")
        time.sleep(2) 
        
        self.browser.find_element(By.NAME, "login").send_keys(self.username) 
        self.browser.find_element(By.NAME, "password").send_keys(self.password)
        self.browser.find_element(By.NAME, "commit").click()
        time.sleep(5)  

    def findRepositories(self, keyword):
        self.browser.get(self.baseUrl)
        time.sleep(3)
        
     
        arama_butonu = self.browser.find_element(By.CLASS_NAME, "header-search-button")
        arama_butonu.click()
        time.sleep(2)
        
        
        searchInput = self.browser.find_element(By.NAME, "query-builder-test")
        searchInput.send_keys(keyword)
        time.sleep(1)
        searchInput.send_keys(Keys.ENTER)
        time.sleep(5) # Arama sonuçları sayfasının tamamen yüklenmesi için bekle
        
        
        repos = self.browser.find_elements(By.CSS_SELECTOR, 'div[data-testid="results-list"] > div')
        
      
        for repo in repos:
            try:
               
                anchor = repo.find_element(By.CSS_SELECTOR, 'h3 a')
                repoName = anchor.text
                repoLink = anchor.get_attribute('href')
                
             
                try:
                    # Sadece o repoya ait açıklama metnini içeren seçici:
                    description_element = repo.find_element(By.CSS_SELECTOR, 'span.Box-sc-17scv9u-0')
                    description = description_element.text
                except:
                    description = "Açıklama belirtilmemiş."
                
       
                r = {
                    "name": repoName,
                    "link": repoLink,
                    "description": description
                }
                
                print(r)
                print("-" * 50)
                
            except Exception as e:
             
                continue
                
        time.sleep(10)

    def getFollowers(self):
        # 1. Sayfaya git
        self.browser.get("https://github.com/sadikturan?tab=followers")
        
        # 2. Sabit sleep yerine, elementlerin yüklenmesini maksimum 10 saniye bekle (Yüklendiği an geçer)
        wait = WebDriverWait(self.browser, 10)
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.d-table.table-fixed')))
        except Exception:
            print("Sayfa yüklenirken hata oluştu veya element bulunamadı.")
            return

        # Kartları bul
        follower_cards = self.browser.find_elements(By.CSS_SELECTOR, 'div.d-table.table-fixed')
        print(f"Toplam {len(follower_cards)} takipçi kartı algılandı. Bilgiler ayrıştırılıyor...\n")
        
        for card in follower_cards:
            try:
                # 1. Kullanıcı adını güncel CSS seçici ile al (Genellikle f4 veya f5 sınıfı altındaki linktedir)
                username_element = card.find_element(By.CSS_SELECTOR, 'a.Link--primary span.Link--secondary, span.Link--secondary')
                # Eğer yukarıdaki seçici de boş dönerse alternatif olarak direkt linkin text'ini almayı deneyelim:
                if not username_element:
                    username_element = card.find_element(By.CSS_SELECTOR, 'a[data-hovercard-type="user"]')
                    
                username = username_element.text.strip()
                
                # 2. Gerçek adı almayı dene
                try:
                    real_name_element = card.find_element(By.CSS_SELECTOR, 'span.f4.Link--primary')
                    real_name = real_name_element.text.strip()
                except Exception:
                    real_name = "Gerçek ad belirtilmemiş."
                    
                if username:
                    print(f"Kullanıcı Adı: {username} -> Gerçek Adı: {real_name}")
                    print("-" * 30)
                    
            except Exception as e:
                # Hatanın ne olduğunu terminalde görebilmek için burayı geçici olarak yazdıralım:
                print(f"Bir kart okunurken hata oluştu: {e}")
                continue
            time.sleep(10)
   # def __del__(self):
       # time.sleep(35)
        #self.browser.quit()

app = GitHub()

#app.signIn()
app.getFollowers()
#app.findRepositories('python')