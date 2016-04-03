from selenium.webdriver.common.keys import Keys
from selenium import webdriver
import time

d = webdriver.Firefox()
d.maximize_window()
d.get('https://ideone.com')

py = ['import','def','print','input','print(','input(','and','or','elif','from']
c = ['#include','int main()','void main()']
java = ['public static void main','static void main']

k  = open('code.txt','rb')
py_l  = False
java_l = False
c_l = False
code = []

for line in k :
    code.append(line)
    if(java_l == False and c_l == False and py_l == False) :
        if('public static void main' in line or 'static void main' in line):
            java_l = True
        elif('#include' in line or 'int main()' in line or 'scanf' in line or 'printf' in line):
            c_l = True
        for word in line :
            if(word in py):
                py_l = True
                break
k.close()

#time.sleep(0.6)
if(py_l == True):
    a = d.find_element_by_id('lang-dropdown-menu-button')
    a.click()
    a = d.find_element_by_link_text('Python 3')
    a.click()
    lang = "py"
elif(c_l == True):
    a = d.find_element_by_id('lang-dropdown-menu-button')
    a.click()
    a = d.find_element_by_link_text('C#')
    a.click()
    lang = "c"
else:
    lang = "java"

def number_of_inputs(lang,code):
    n = 0
    if(lang == 'c'):
        for i in range(len(code)):
            k = code[i]
            if('scanf' in k):
                l = k.find('"')
                m = k.find('"',l+1)
                n  += k[l:m].count('%')
    elif(lang == 'py'):
        for i in range(len(code)):
            k = code[i]
            if('input' in k):
                l = k.find('=')
                n += (1 + k[0:l].count(','))
    else:
        name = ""
        for i in range(len(code)):
            k = code[i]
            if('Scanner' in k and 'java.util' not in k):
                l = k.find('Scanner')
                m = k.find('=')
                name = k[l+7:m].strip()
                break
            if('BufferedReader' in k):
                l = k.find('BufferedReader')
                m = k.find('=')
                name = k[l+14:m].strip()
                break
        for i in range(len(code)):
            k = code[i]
            if(name+'.' in k and 'Scanner' not in k and 'BufferedReader' not in k):
                n += 1
    return n

time.sleep(1)
a = d.find_element_by_class_name('ace_text-input')
time.sleep(1)
a.send_keys(Keys.CONTROL + 'a')
time.sleep(1)
a.send_keys(Keys.BACKSPACE)
time.sleep(1)
x = ""

for i in range(len(code)):
    if(lang == "java"):
        if(i == len(code)-1):
            break
        x += code[i].strip()+'\n'
    else:
        x += code[i]

a.send_keys(x)
inputs = number_of_inputs(lang,code)

if(inputs != 0):
    kk = d.find_element_by_xpath('//button[@data-toggle="button"]')
    kk.click()
    b = d.find_element_by_id('input')
    b.send_keys('There are '+str(inputs)+' inputs required in the code snippet. Please analyze the code accordingly, REMOVE ALL THIS TEXT, enter the input and run the code.')
else:
    a.send_keys(Keys.CONTROL + Keys.ENTER)
    time.sleep(4)
    a = d.find_element_by_id('output-text')
    print("Output : ",a.text)
