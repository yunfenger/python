#coding=utf-8
from selenium import webdriver
from time import sleep
from datetime import datetime
import traceback
from splinter.browser import Browser

PRICE =50
username = "yongyaqin1225@126.com"
passwd = "yongyaqin1225"


#username = line_list[2 * count ].line.split(" ")[-1]
#passwd = line_list[2 * count + 1].line.split(" ")[-1]
######################### the file operation ###########################################################################
def log(str):
    fo = open("log.txt", "a")
    fo.write(str+'\n')
    fo.close()

def getusr(count):
    with open('usr.txt', 'rb') as f:
        line_list = f.readlines()
        #for line in line_list:
        #    print(line.strip())  # 把末尾的'\n'删掉
    username = line_list[2 * count]
    passwd = line_list[2 * count + 1]
    print('user')
    print(line_list[2 * (count - 1)])
    print('passwd')
    print(line_list[2 * count - 1])
    napw = [username, passwd]
    return napw

def GetUserFromFile(count):
    with open('usr.txt', 'rb') as f:
        line_list = f.readlines()
    #    for line in line_list:
    #       print(line.strip())  # 把末尾的'\n'删掉
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
        #brw.get("https://www.amazon.com")
        #brw.find_element_by_id('nav-link-accountList').click()
        a=brw.find_element_by_id('ap_email')
        a.clear();
        a.send_keys(username)  #  user name
        a=brw.find_element_by_id('ap_password')
        a.clear()
        a.send_keys(passwd)  # pwd
        brw.find_element_by_id('signInSubmit').click()

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
    print(str)
    index = str.find('\nEUR', 0, len(str))
    if(index==-1):
        return -1
    index2= str.find('(EUR', 0, len(str))
    if (index == -1):
        return -1
    price= float(str[index+4:index2])
    return price


def check_goods():
    status = False
    try:
        #brw.get("https://www.amazon.de/dp/B01GDZSZ6Q/ref=twister_B013USRV1E?_encoding=UTF8&th=1")
        brw.get("https://www.amazon.de/dp/B01GDZSZ6Q/ref=twister_B013USRV1E?_encoding=UTF8&th=1&language=en_GB")
        sleep(15)
        # get the element of the data  5*600g
        a = brw.find_element_by_xpath("//li[@data-defaultasin='B01GDZSZ6Q']")
        #a.click();
        price = getprice(a.text)
        #log(a.text)
        log('price:' + str(price))
        a.click()
        # check the price
        if((price>0)&(price<50.00)):
            status= True
        else:
            status=False
    except Exception as e:
        print(traceback.print_exc())
        status= False
    return status
        #  B00BSNACII ======> 4*600 g
        # a = brw.find_element_by_xpath("//li[@data-defaultasin='B00BSNACII']")
        # # B01GDZSZ6Q ======> 5*600g
        # a = brw.find_element_by_xpath("//li[@data-defaultasin='B01GDZSZ6Q']")
        #B00LTPUMJ4 ======>12*600g
        # a = brw.find_element_by_xpath("//li[@data-defaultasin='B00LTPUMJ4']")
########################################################################################################################
###########################----------end-----################################################################
########################################################################################################################
def book():
    print('book operation')
    # the four data-defaultasin like
    # data_index={ B00CMLT4QQ,B00BSNACII,B01GDZSZ6Q,B00LTPUMJ4}
    book_status=False
    a=False
    count=0
    time=200
    while book_status ==False:
        while check_goods()==False:
            log('check the goods num'+str(count)+'at time \t'+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            count=count+1
            sleep(time)
        #a = brw.find_element_by_xpath("//a[@class='oneClickSignInLink']")
        brw.save_screenshot(str(count)+"_count.png")
        try:
            a = brw.find_element_by_xpath("//li[@data-defaultasin='B01GDZSZ6Q']")
            a.click()
        except Exception as e:
            print('can not find the goods B01GDZSZ6Q ')
            book_status = False
            continue
        try:
            a = brw.find_element_by_id('one-click-button')
            a.click()
            a = brw.find_element_by_xpath("//input[@name='continue-bottom']")
            a.click()
            book_status = True
            return
        except Exception as e:
            print(traceback.print_exc())
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
                login('yongyaqin1225@126.com','yongyaqin1225')


        # check the Select shipping address

            # submit the order
            brw.save_screenshot(str(count) +"_login"+ "_count.png")
            a = brw.find_element_by_xpath("//input[@name='continue-bottom']")
            a.click()
            book_status = True
        except Exception as e:
            print(traceback.print_exc())
            book_status = False
        # check the order is OK

    return True



if __name__ == "__main__":
    # get the user info from the usr txt
    line_l = GetUserFromFile(0)
    log('amzon_start'+datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
    global brw
    brw = webdriver.Chrome()
    brw.implicitly_wait(3)  # seconds
    brw.set_window_size(1366, 768)
    brw.get("https://www.amazon.de")
    sleep(10)
    status =False
    cnt =0;
    while(status == False):
        print('find the login id '+str(cnt))
        cnt=cnt+1
        try:
            brw.find_element_by_id('nav-link-yourAccount').click()
            status = login(username,passwd)
        except Exception as e:
                log(str(traceback.print_exc()))
                brw.get("https://www.amazon.de")
                sleep(10)
        if(status ==False):
            try:
                brw.find_element_by_id('nav-link-accountList').click()
                status = login(username,passwd)
            except Exception as e:
                    log(str(traceback.print_exc()))
                    brw.get("https://www.amazon.de")
                    sleep(10)

    #status=True
        print("login"+str(status))
    status = book()
    log('the book result'+status)