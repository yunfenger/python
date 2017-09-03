#coding=utf-8
from selenium import webdriver
from time import sleep
from datetime import datetime
import traceback
from splinter.browser import Browser

PRICE =50
username = "xxxxx"
passwd = "xxxxxxx"
# configure for the auto book operation.
# the www info
LOGIN_URI = 'https://www.amazon.de'

#atami2='https://www.amazon.de/Aptamil-Kindermilch-Jahren-4er-Pack/dp/B00BSNAC9C/ref=sr_1_8?ie=UTF8&qid=1504184373&sr=8-8&keywords=atamil+2'
#atami2_price = 49.75
# B00BSNAC9C
# B00BSNAC9C
# atami2 ='https://www.amazon.de/Aptamil-Kindermilch-Jahren-4er-Pack/dp/B00BSNAC9C/'


#atami2_baijin='https://www.amazon.de/Aptamil-Profutura-Folgemilch-nach-Monat/dp/B016WEDI6K/ref=sr_1_4?s=grocery&ie=UTF8&qid=1504184506&sr=1-4&keywords=atamil'
#atami2_price=77.92
# baijin ='https://www.amazon.de/Aptamil-Profutura-Folgemilch-nach-Monat/dp/B016WEDI6K?language=en_GB'

class Login_info:
    def __init__(self):
        self.name=''
        self.pw = ''
        self.log_sub ='signInSubmit'
        self.e_name=''
        self.e_pw=''
        self.log_head=''    # the info used for to check thr url is the login url
        self.log_check=''   # the info used for to check the login is sucess
        self.LOGIN_URI ='https://www.amazon.de'

class Good_info:
    def __init__(self):
        self.GOOD_URI=''
        self.GOOD_NO = ''
        self.GOOD_PRICE =0
        self.Good_SUBMIT=''

class Good_Status:
    def __init__(self):
        self.GOOD_ATAMI1_STATUS=0
        self.GOOD_ATAMI2_STATUS=0
        self.GOOD_ATAMIProfutura_STATUS =0
        #self.data=datetime.now()
# The elemnet used for login, the info can read from the configure files
LOGIN_E_NAME = 'ap_email'
LOGIN_E_PW='ap_password'
LOGIN_E_SUBMIT = 'signInSubmit'


# GOOD_info
GOOD_URI ='https://www.amazon.de/dp/B01GDZSZ6Q/ref=twister_B013USRV1E?_encoding=UTF8&th=1&language=en_GB'
GOOD_NO = 'B01GDZSZ6Q'
GOOD_PRICE=50

# sub the goods books
# the time for purchase 3,6,9 am, 8:00pm

# the element info for the goods
#  B00BSNACII ======> 4*600 g
# a = brw.find_element_by_xpath("//li[@data-defaultasin='B00BSNACII']")
# # B01GDZSZ6Q ======> 5*600g
# a = brw.find_element_by_xpath("//li[@data-defaultasin='B01GDZSZ6Q']")
# B00LTPUMJ4 ======>12*600g
# a = brw.find_element_by_xpath("//li[@data-defaultasin='B00LTPUMJ4']")
######################### the file operation ###########################################################################
def log(str):
    fo = open(log_file, 'a')
    fo.write(str+'\t'+datetime.now().strftime('%d_%H:%M:%S')+'\n')
    fo.close()

def GetUserFromFile(count):
    with open('usr.txt', 'r') as f:
        line_list = f.readlines()
    username = line_list[2 * count]
    passwd = line_list[2 * count + 1]
    print('user')
    print(line_list[2 * (count - 1)])
    print('passwd')
    print(line_list[2 * count - 1])
    napw = [username,passwd]
    return napw
##########################the end of the file operation ################################################################
def login(username,passwd):
    print('login ')
    try:
        a=brw.find_element_by_id(LOGIN_E_NAME)
        a.clear();
        a.send_keys(username)  #  user name
        a=brw.find_element_by_id(LOGIN_E_PW)
        a.clear()
        a.send_keys(passwd)  # pwd
        sleep(2)
        brw.find_element_by_id(LOGIN_E_SUBMIT).click()

    except Exception as e:
        print(traceback.print_exc())
        return False
    else:
        print('no error')
        return  True
    return
###########################################################################################################
#  check the price and goods for purchase
###########################################################################################################
# function getprice
# input the str from the element.text, which like '5 x 600g\nEUR 49.88 (EUR 16.63 / kg)'
# return 49.88 else return -1
def getprice(str):
    #'5 x 600g\nEUR 49.88 (EUR 16.63 / kg)'
    #print(str)
    index = str.find('EUR', 0, len(str))
    if(index==-1):
        return -1
    index2= str.find('(EUR', 0, len(str))
    if (index == -1):
        return -1
    price= float(str[index+4:index2])
    return price

def getprice2(str):
    price=-1
    index = str.find('EUR', 0, len(str))
    if(index==-1):
        pass
    else:
        price= float(str[index+4:index+10])
    return price

def check_goods_2(url, Goodstr,exp_price):
    status = 0
    price =-1
    pricetest=''
    try:
        brw.get(url)
        sleep(1)
        # get the element of the data  5*600g
        a = brw.find_element_by_xpath("//li[@data-defaultasin='"+Goodstr+"']")
        pricetest=a.text[a.text.find('\n')+1:len(a.text)]
        price = getprice(pricetest)
        a.click()
    except Exception as e:
        pricetest='not found the element'+Goodstr
    # if the good is ok, submit the
    if ((price > 0) & (price <= exp_price)):
        brw.save_screenshot('A'+datetime.now().strftime('%Y-%m-%d_%H_%M_%S')+Goodstr + ".png")
        try:
            process = 2;
            a = brw.find_element_by_id('one-click-button')
            a.click()
            if (brw.title == 'Amazon Sign In'):
                login(username,passwd)
            process = 3;
            a = brw.find_element_by_xpath("//input[@name='continue-bottom']")
            a.click()
            book_status = True
            return
        except Exception as e:
            #print(traceback.print_exc())
            if(process==2):
                print('can not find the one-click-button')
            if(process==3):
                print('can not find the continue-bottom')
            book_status = False
        try:
            #a=brw.find_element_by_id('oneClickSignIn')
            a = brw.find_element_by_xpath("//a[@class='oneClickSignInLink']")
            a.click()
            if (brw.title == 'Amazon Sign In'):
                login(username,passwd)
            #one - click - button
            a = brw.find_element_by_id('one-click-button')
            a.click()
            title = brw.title
            print(brw.title)
            if(brw.title=='Amazon Sign In'):
                login(username, passwd)
            brw.save_screenshot('B'+datetime.now().strftime('%Y-%m-%d_%H_%M_%S') +"_login"+ ".png")
            a = brw.find_element_by_xpath("//input[@name='continue-bottom']")
            a.click()
            status = 1
        except Exception as e:
            print(traceback.print_exc())
            status = 0
    return (status,price,pricetest)


def check_goods_3(url, Goodstr,exp_price):
    status = 0
    price =-1
    pricetest=''
    try:
        brw.get(url)
        sleep(1)
        # get the element of the data  5*600g
        a = brw.find_element_by_id('availability')
        pricetest = a.text
        #print(a.text)
        if(a.text.find('in stock')!=-1):
            b = brw.find_element_by_id('price_feature_div')
          #  print('in stock'+b.text)
            price =getprice2(b.text)
        else:
            b = brw.find_element_by_id('olp_feature_div')
           # print('a'+b.text)
            price = getprice2(b.text)
    except Exception as e:
        pricetest='not found the element'+Goodstr
        status= 0
    # if the good is ok, submit the
    if ((price > 0) & (price <= exp_price)):
        brw.save_screenshot('A'+datetime.now().strftime('%Y-%m-%d_%H_%M_%S')+Goodstr + ".png")
        try:
            process = 2;
            a = brw.find_element_by_id('one-click-button')
            a.click()
            if (brw.title == 'Amazon Sign In'):
                login(username,passwd)
            process = 3;
            a = brw.find_element_by_xpath("//input[@name='continue-bottom']")
            a.click()
            book_status = True
            return
        except Exception as e:
            #print(traceback.print_exc())
            if(process==2):
                print('can not find the one-click-button')
            if(process==3):
                print('can not find the continue-bottom')
            book_status = False
        try:
            #a=brw.find_element_by_id('oneClickSignIn')
            a = brw.find_element_by_xpath("//a[@class='oneClickSignInLink']")
            a.click()
            if (brw.title == 'Amazon Sign In'):
                login(username,passwd)
            #one - click - button
            a = brw.find_element_by_id('one-click-button')
            a.click()
            title = brw.title
            print(brw.title)
            if(brw.title=='Amazon Sign In'):
                login(username, passwd)
            brw.save_screenshot('B'+datetime.now().strftime('%Y-%m-%d_%H_%M_%S') +"_login"+ ".png")
            a = brw.find_element_by_xpath("//input[@name='continue-bottom']")
            a.click()
            status = 1
        except Exception as e:
            print(traceback.print_exc())
            status = 0
    return (status,price,pricetest)
########################################################################################################################
###########################----------end-----################################################################
########################################################################################################################

def book2():
    print('book operation')
    # the four data-defaultasin like
    # data_index={ B00CMLT4QQ,B00BSNACII,B01GDZSZ6Q,B00LTPUMJ4}
    book_status=False
    good_status=Good_Status()
    process=0
    a=False
    count=0
    time=5
    # input
    url=''
    goodstr=''
    exp_price=0
    #output
    price=0
    priceT=''

    while book_status ==False:
        if(good_status.GOOD_ATAMI1_STATUS==0):
            url='https://www.amazon.de/dp/B01GDZSZ6Q/ref=twister_B013USRV1E?_encoding=UTF8&th=1&language=en_GB'
            goodstr='B01GDZSZ6Q'
            exp_price=49.88
            [good_status.GOOD_ATAMI1_STATUS,price,priceT]=check_goods_3(url,goodstr,exp_price)
            print('GOOD_ATAMI1_STATUS:'+str(good_status.GOOD_ATAMI1_STATUS)+'\tprice:'+str(price)+'\t'+priceT)
            log('GOOD_ATAMI1_STATUS:' + str(good_status.GOOD_ATAMI1_STATUS) + '\tprice:' + str(price) +'\t'+ priceT)


        if(good_status.GOOD_ATAMI2_STATUS==0):
            url='https://www.amazon.de/Aptamil-Kindermilch-Jahren-4er-Pack/dp/B00BSNAC9C/?language=en_GB'
            #'https://www.amazon.de/Aptamil-Kindermilch-Jahren-4er-Pack/dp/B00BSNAC9C/?language=en_GB'
            goodstr='B00BSNAC9C'
            exp_price=49.75
            [good_status.GOOD_ATAMI2_STATUS, price, priceT] = check_goods_3(url, goodstr, exp_price)
            print('GOOD_ATAMI2_STATUS:' + str(good_status.GOOD_ATAMI2_STATUS) + '\tprice:' + str(price)+'\t' + priceT)
            log('GOOD_ATAMI2_STATUS:' + str(good_status.GOOD_ATAMI2_STATUS) + '\tprice:' + str(price) +'\t'+ priceT)

        if(good_status.GOOD_ATAMIProfutura_STATUS==0):
            url='https://www.amazon.de/Aptamil-Profutura-Folgemilch-nach-Monat/dp/B016WEDI6K?language=en_GB'
            goodstr='B016WEDI6K'
            exp_price=77.92
            [good_status.GOOD_ATAMIProfutura_STATUS, price, priceT] = check_goods_3(url, goodstr, exp_price)
            print('GOOD_ATAMIPF_STATUS:' + str(good_status.GOOD_ATAMIProfutura_STATUS) + '\tprice:' + str(price)+'\t' + priceT)
            log('GOOD_ATAMIPF_STATUS:' + str(good_status.GOOD_ATAMIProfutura_STATUS) + '\tprice:' + str(
                price) + '\t'+priceT)

        if((good_status.GOOD_ATAMI1_STATUS==1)&(good_status.GOOD_ATAMIProfutura_STATUS==1)&(good_status.GOOD_ATAMI2_STATUS==1)):
            book_status=True
    return True

if __name__ == "__main__":
    # get the user info from the usr txt
    [username, passwd] = GetUserFromFile(0)
    global log_file
    log_file = 'amzon_start' + datetime.now().strftime('%Y-%m-%d_%H_%M_%S')+'.txt'
    log('amzon_start'+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    global brw
    brw = webdriver.Chrome()
    brw.implicitly_wait(1)  # seconds
    #brw.set_window_size(1366, 768)
    brw.get(LOGIN_URI)
    #sleep(2)
    #pngfile=datetime.now().strftime('%Y-%m-%d_%H_%M_%S')+'.png'
    #print(pngfile)
    #brw.save_screenshot(pngfile)
    #sleep(3)
    status =False
    cnt =0;
    # while(status == False):
    #     print('find the login id '+str(cnt))
    #     cnt=cnt+1
    #     try:
    #         brw.find_element_by_id('nav-link-yourAccount').click()
    #         status = login(username,passwd)
    #     except Exception as e:
    #             log(str(traceback.print_exc()))
    #             brw.get(LOGIN_URI)
    #             sleep(10)
    #     if(status ==False):
    #         try:
    #             brw.find_element_by_id('nav-link-accountList').click()
    #             status = login(username,passwd)
    #         except Exception as e:
    #                 log(str(traceback.print_exc()))
    #                 brw.get("https://www.amazon.de")
    #                 sleep(10)
    #
    # #status=True
    #     print("login_"+str(status))
    status = book2()
    log('the book result'+str(status))