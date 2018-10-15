from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from time import sleep


driver = webdriver.Firefox()
driver.get('https://laksh22.github.io/blinkception-site/index.html')


current_element_global = driver.find_element_by_class_name("bc-3")

#Get BlinkCeption element after current element
def getNextElement(current_class_id):
    next_class_name = "bc-1" #default - Go to first element if currently at last

    current_class_id_name = "bc-" + str(current_id)
    current_element = driver.find_element_by_class_name(current_class_id_name)

    is_last = "bc-last" in current_element.get_attribute("class") #Is the current element the last one

    if(is_last != True):
        next_class_id = current_class_id + 1
        next_class_name = "bc-" + str(next_class_id)
        print(next_class_name)

    next_element = driver.find_element_by_class_name(next_class_name)
    return(next_element)

#Get BlinkCeption element before current element
def getPreviousElement(current_class_id):
    previous_class_name = "bc-last"#default - Go to last element if currently at first

    current_class_id_name = "bc-" + str(current_id)
    current_element = driver.find_element_by_class_name(current_class_id_name)

    is_first = "bc-first" in current_element.get_attribute("class")#Is the current element the first one

    if(is_first != True):
        previous_class_id = current_class_id - 1
        previous_class_name = "bc-" + str(previous_class_id)
        print(previous_class_name)

    previous_element = driver.find_element_by_class_name(previous_class_name)
    return(previous_element)

#Get the current element
def getCurrentElement():
    return(current_element_global)

#Highlights selected element
def highlightElement(element):
    driver.execute_script("arguments[0].setAttribute('style', 'background: #a8c9ff; border: 2px solid #a8c9ff;');", element)
    sleep(2)
    driver.execute_script("arguments[0].setAttribute('style', 'background: none');", element)

#Scroll to selected element
def moveToElement(element):
    current_element_global = element
    driver.execute_script("arguments[0].scrollIntoView(true);", element)
    highlightElement(element)

#Call interaction function depending based on type of element
def interactElement(element, direction=0, word=""):
    classes = element.get_attribute("class")
    if("bc-navbar" in classes):
        clickButton(element)
        new_current_element_global = driver.find_element_by_class_name("bc-1")
    elif(("bc-button" in classes) or ("bc-toggle" in classes)):
        clickButton(element)
    elif("bc-slide" in classes):
        if(direction==1):
            slideSliderRight(element)
        elif(direction==2):
            slideSliderLeft(element)
    elif("bc-input" in classes):
        #TODO Clear global variable if new input field
        sendInput(element, word)

#Click Selected Button
def clickButton(element):
    element.click()

#Send keys to text input
def sendInput(element, input_word):
    #TODO Update global variable on new character entry and send to input field
    element.click()
    element.send_keys(input_word)
    # print(input_word)
    print(" sendInput test")
#Slide a slider to right
def slideSliderRight(element):
    print("Moving right")
    move = ActionChains(driver)
    move.click_and_hold(element).move_by_offset(45, 0).release().perform()

#Slide a slider to left
def slideSliderLeft(element):
    print("Moving left")
    move = ActionChains(driver)
    move.click_and_hold(element).move_by_offset(-45, 0).release().perform()

'''
curr_element_id = 2
current_element = getCurrentElement(2)
moveToElement(current_element)
sleep(2)

nextElement = getNextElement(curr_element_id)
current_element = nextElement
moveToElement(current_element)
interactElement(current_element)
'''

"""
current_element = getCurrentElement()
moveToElement(current_element)
sleep(1)
for i in range(3,17):
    next_element = getNextElement(i)
    current_element = next_element
    moveToElement(current_element)
    interactElement(current_element)
    print(current_element_global.get_attribute("class"))
    sleep(1)
"""
# print(current_element_global.get_attribute("class"))

