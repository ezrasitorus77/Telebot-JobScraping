import requests, time, telebot
from bs4 import BeautifulSoup
from selenium import webdriver

urlDCS = "https://glints.com/id/opportunities/jobs/explore?keywords=digital%20content%20specialist&sortBy=relevancy&countries=ID&cities=28904"
urlSMA = "https://glints.com/id/opportunities/jobs/explore?sortBy=relevancy&countries=ID&cities=28904&keywords=social%20media%20associate"
urlPRO = "https://glints.com/id/opportunities/jobs/explore?sortBy=relevancy&countries=ID&cities=28904&keywords=producer"

def process_html(url):
    global jobs
    
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(chrome_options = options, executable_path =  "{PATH}")
    driver.get(url)
    time.sleep(3)

    height = 4000
    for scroll in range(0,3):
        driver.execute_script(f"window.scrollTo(0, {height})")
        time.sleep(5)
        height += 4000

    page = driver.execute_script('return document.body.innerHTML')
    body = BeautifulSoup(''.join(page), 'html.parser')
    time.sleep(5)
    driver.close()
    
    boxes = list(body.find_all("div", class_ = "job-card-info CompactOpportunityCardsc__CompactJobCardInfo-sc-1xtox99-7 kTDInJ"))

    jobs = []
    for box, index in zip(boxes, range(1, len(boxes) + 1)):
        first_row = box.find("a", class_ = "gtm-job-card-job-title CompactOpportunityCardsc__JobTitleLink-sc-1xtox99-8 hAEIfu")

        role = first_row.text
        company = box.find("a", class_ = "CompactOpportunityCardsc__CompanyLink-sc-1xtox99-9 gOQwrG").text
        salary = box.find_all("p", class_ = "CompactOpportunityCardsc__OpportunityInfo-sc-1xtox99-13 bhlpvS")[1].text
        if  salary == "":
            salary = "Unknown"
            
        else:
            salary = salary.replace("\xa0", " ")
        link = "https://glints.com" + first_row["href"]

        jobs.append(f"{index}) Role : {role} | Company : {company} | Salary : {salary} | Link : {link}")

token = "{YOUR_TOKEN}"
bot = telebot.TeleBot(token)

@bot.message_handler(commands = ['start'])
def send_welcome(message):
    bot.reply_to(message, "These are two commands you can use: \n\n /glintsDCS: Provides all 'Digital Content Specialist' jobs query results (Location : Jakarta) in Glints \n\n /glintsSMA: Provides all 'Social Media Associate' jobs query results (Location : Jakarta) in Glints \n\n /glintsPRO: Provides all 'Producer' jobs query results (Location : Jakarta) in Glints")

@bot.message_handler(commands = ['glintsDCS'])
def glintsDCS(message):
    bot.reply_to(message, "Please wait")
    
    process_html(urlDCS)
    
    start = 0
    end = 15
    for reply in range(int(len(jobs) / 15)):
        bot.reply_to(message, " \n\n".join(jobs[start:end]))
        
        start = end
        end += 15
    
@bot.message_handler(commands = ['glintsSMA'])
def glintsSMA(message):
    bot.reply_to(message, "Please wait")
    
    process_html(urlSMA)
    
    start = 0
    end = 15
    for reply in range(int(len(jobs) / 15)):
        bot.reply_to(message, " \n\n".join(jobs[start:end]))
        
        start = end
        end += 15

@bot.message_handler(commands = ['glintsPRO'])
def glintsDCS(message):
    bot.reply_to(message, "Please wait")
    
    process_html(urlPRO)
    
    start = 0
    end = 15
    for reply in range(int(len(jobs) / 15)):
        bot.reply_to(message, " \n\n".join(jobs[start:end]))
        
        start = end
        end += 15

while True:
    print ("Is running...")
    
    try:
        bot.polling(none_stop = True)

    except Exception:
        time.sleep(5)
