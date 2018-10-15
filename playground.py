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
    driver.execute_script("arguments[0].setAttribute('style', 'background: #a8c9ff; border: 2px solid #a8c9ff;');", element)#Give blue backgroun to element
    sleep(2)#Show blue background for 2 seconds
    driver.execute_script("arguments[0].setAttribute('style', 'background: none');", element)#Remove blue background

#Scroll to selected element
def moveToElement(element):
    current_element_global = element #Updates the global current element
    driver.execute_script("arguments[0].scrollIntoView(true);", element)#Scrolls the element into view
    highlightElement(element)#Highlights the element

#Call interaction function depending based on type of element
def interactElement(element, direction=0, word=""):
    classes = element.get_attribute("class")#Gets the classes to which the element belongs
    #if("bc-navbar" in classes):
    #    clickButton(element)
    #    new_current_element_global = driver.find_element_by_class_name("bc-1")
    elif("bc-button" in classes):#Clicks the element if it is a button
        clickButton(element)
    elif("bc-slide" in classes):#Slides the element if it is a slider
        if(direction==1):#direction = 1 means the slider is moved right
            slideSlider(element, 1)
        elif(direction==2):#direction = 2 means the slider moves left
            slideSlider(element, 2)
    elif("bc-input" in classes):
        sendInput(element, word)

#Click Selected Button
def clickButton(element):
    element.click()

#Move selected slider
def slideSlider(element, dir):
    move = ActionChains(driver)
    if(dir == 1):
        move.click_and_hold(element).move_by_offset(45, 0).release().perform()
    elif(dir == 2):
        move.click_and_hold(element).move_by_offset(-45, 0).release().perform()
    else:
        print("Not a valid slide option")

#Send keys to text input
def sendInput(element, input_word):
    element.click()
    element.send_keys(input_word)
    print(" sendInput test")

"""
#This is to loop through each interactive element to see if code is working
current_element = getCurrentElement()
moveToElement(current_element)
BEGINNING_CLASS_ID = 3 #Change depending on website
ENDING_CLASS_ID = 17 #Change depending on website
sleep(1)
for i in range(BEGINNING_CLASS_ID, ENDING_CLASS_ID+1):
    next_element = getNextElement(i)
    current_element = next_element
    moveToElement(current_element)
    interactElement(current_element)
    print(current_element_global.get_attribute("class"))
    sleep(1)
"""

