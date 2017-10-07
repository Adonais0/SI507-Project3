from bs4 import BeautifulSoup
import unittest
import requests
import io
import sys
import socket
socket.gethostbyname("")

#sys.stout = io.TextIOWrapper(sys.stdout.buffer, encoding = 'gbk')
#########
## Instr note: the outline comments will stay as suggestions, otherwise it's too difficult.
## Of course, it could be structured in an easier/neater way, and if a student decides to commit to that, that is OK.

## NOTE OF ADVICE:
## When you go to make your GitHub milestones, think pretty seriously about all the different parts and their requirements, and what you need to understand. Make sure you've asked your questions about Part 2 as much as you need to before Fall Break!


######### PART 0 #########
print(10*"*"+"Part_0"+10*"*")
# Write your code for Part 0 here.
try:
    gallery_data = open("gallery.html",'r').read()
except:
    gallery_data = requests.get("http://newmantaylor.com/gallery.html").text
    f = open("gallery.html",'w')
    f.write(gallery_data)
    f.close

soup = BeautifulSoup(gallery_data,'html.parser')
alt_list = soup.find_all('img')
for alt in alt_list:
    print(alt.get('alt','No alternative text provided'))

######### PART 1 #########
print(10*"*"+"Part_1"+10*"*")
# Get the main page data...
def Cache(state_name, init, tag):
    try:
        data = open(str(state_name+"_data.html"),'r').read()
    except:
        data = requests.get(str("http://www.nps.gov/"+tag+init+"index.html")).text
        f = open(str(state_name + "_data.html"),'w', encoding = 'utf-8')
        f.write(data)
        f.close()
    return data

gov_data = Cache("nps_gov","","")

# Try to get and cache main page data if not yet cached
# Result of a following try/except block should be that
# there exists a file nps_gov_data.html,
# and the html text saved in it is stored in a variable
# that the rest of the program can access.

# We've provided comments to guide you through the complex try/except, but if you prefer to build up the code to do this scraping and caching yourself, that is OK.


# Get individual states' data...
# ca_data = Cache("california","ca/","state/")
# mi_data = Cache("michigan","mi/","state/")
# ar_data = Cache("arkansas","ar/","state/")
# Result of a following try/except block should be that
# there exist 3 files -- arkansas_data.html, california_data.html, michigan_data.html
# and the HTML-formatted text stored in each one is available
# in a variable or data structure
# that the rest of the program can access.

# TRY:
# To open and read all 3 of the files

# But if you can't, EXCEPT:

# Create a BeautifulSoup instance of main page data
# Access the unordered list with the states' dropdown
gov_soup = BeautifulSoup(gov_data,'html.parser')
drop_list = gov_soup.find("ul",{"class":"dropdown-menu SearchBar-keywordSearch"})
#print(type(drop_list))
#print(drop_list)
# Get a list of all the li (list elements) from the unordered list, using the BeautifulSoup find_all method
list_of_li = drop_list.find_all("li")
list_of_href = []

# Use a list comprehension or accumulation to get all of the 'href' attributes of the 'a' tag objects in each li, instead of the full li objects
for li in list_of_li:
    list_of_href.append(li.find("a")['href'])
#print(list_of_href)
list_of_useful_href = []
# Filter the list of relative URLs you just got to include only the 3 you want: AR's, CA's, MI's, using the accumulator pattern & conditional statements
for href in list_of_href:
    if "ar" in href or "ca" in href or "mi" in href:
        list_of_useful_href.append(href)
print(list_of_useful_href)

# Create 3 URLs to access data from by appending those 3 href values to the main part of the NPS url. Save each URL in a variable.
url_ar = "http://www.nps.gov"+list_of_useful_href[0]
url_ca = "http://www.nps.gov"+list_of_useful_href[1]
url_mi = "http://www.nps.gov"+list_of_useful_href[2]
print(url_mi)
## To figure out what URLs you want to get data from (as if you weren't told initially)...
# As seen if you debug on the actual site. e.g. Maine parks URL is "http://www.nps.gov/state/me/index.htm", Michigan's is "http://www.nps.gov/state/mi/index.htm" -- so if you compare that to the values in those href attributes you just got... how can you build the full URLs?
def Cache_url(state_name, url):
    try:
        data = open(str(state_name+"_data.html"),'r').read()
    except:
        data = requests.get(url).text
        f = open(str(state_name + "_data.html"),'w', encoding = 'utf-8')
        f.write(data)
        f.close()
    return data
# Finally, get the HTML data from each of these URLs, and save it in the variables you used in the try clause
# (Make sure they're the same variables you used in the try clause! Otherwise, all this code will run every time you run the program!)
ar_data = Cache_url("arkansas",url_ar)
mi_data = Cache_url("michigan",url_mi)
ca_data = Cache_url("california",url_ca)

# And then, write each set of data to a file so this won't have to run again.

######### PART 2 #########
#create a nationalsite class
## Before truly embarking on Part 2, we recommend you do a few things:
print(10*"*"+"Part_2"+10*"*")
# - Create BeautifulSoup objects out of all the data you have access to in variables from Part 1
# - Do some investigation on those BeautifulSoup objects. What data do you have about each state? How is it organized in HTML?
ar_soup = BeautifulSoup(ar_data,'html.parser')
mi_soup = BeautifulSoup(mi_data,'html.parser')
ca_soup = BeautifulSoup(ca_data,'html.parser')
# HINT: remember the method .prettify() on a BeautifulSoup object -- might be useful for your investigation! So, of course, might be .find or .find_all, etc...
#print(ar_soup.prettify())

# HINT: Remember that the data you saved is data that includes ALL of the parks/sites/etc in a certain state, but you want the class to represent just ONE park/site/monument/lakeshore.
ar_ul = ar_soup.find('ul',{'id':'list_parks'})
ar_park_list = ar_ul.find_all('li')
p_list = []

#print(div_list)

#print(ar_park_list[0].find('h4').text)#link to the basic information
def get_url_data(url,index):
    try:
        data = open((str(index)+'temp.html'),'r').read()
    except:
        data = requests.get(url).text
        f = open((str(index)+'temp.html'),'w', encoding = 'utf-8')
        f.write(data)
        f.close()
    return data
def return_list_address(soup):#input is a state soup object and return the list of mailing address(string) of that state
    div_list = soup.find_all('div',{'class':'stateListLinks'})
    basic_info_link_list = []
    for div in div_list:
        basic_info_link_list.append((((div.find('ul')).find_all('li'))[1]).find('a').get('href'))
    index = 0
    list_of_address = []
    for link in basic_info_link_list:
        data = get_url_data(link,index)#basic information html data
        address_soup = BeautifulSoup(data,'html.parser')
        index = index + 1
        list_of_address.append((address_soup.find('span',{'itemprop':'streetAddress'}).text)[2:-2]+'/'+(address_soup.find('span',{'itemprop':'addressLocality'}).text)+'/'+(address_soup.find('span',{'itemprop':'addressRegion'}).text)+'/'+(address_soup.find('span',{'itemprop':'postalCode'}).text))
    #print(list_of_address)
    return list_of_address
return_list_address(mi_soup)

# for li in ar_park_list:
#     i = 0
#     if li.find('h4'):
#         print(li.find('h4').text)
#         p_dict = {
#             'location' : li.find('h4').text,
#             'name': (li.find('h3')).find('a').text,
#             'park_type': li.find('h2').text,
#             'description': li.find('p').text,
#             'mail_address':return_list_address(ar_soup)[i],
#         }
#         p_list.append(p_dict)
#         i = i+1
#     else:
#         li = None
#         i = i+1
# #print(p_list)

def return_park_list(soup):#input a state soup, return a list of park information dictionaries
    park_list = []
    ul = soup.find('ul',{'id':'list_parks'})
    pa_list = ul.find_all('li')
    for li in pa_list:
        i = 0
        if li.find('h4'):
            park_dict = {
                'location': li.find('h4').text,
                'name': (li.find('h3')).find('a').text,
                'park_type': li.find('h2').text,
                'description': li.find('p').text,
                'mail_address':return_list_address(soup)[i],
            }
            park_list.append(park_dict)
            i = i+1
        else:
            li = None
            i = i+1
    return park_list

#print(return_park_list(ar_soup))#list of dictionaries
# We have provided, in sample_html_of_park.html an HTML file that represents the HTML about 1 park. However, your code should rely upon HTML data about Michigan, Arkansas, and Califoria you saved and accessed in Part 1.

# However, to begin your investigation and begin to plan your class definition, you may want to open this file and create a BeautifulSoup instance of it to do investigation on.

# Remember that there are things you'll have to be careful about listed in the instructions -- e.g. if no type of park/site/monument is listed in input, one of your instance variables should have a None value...
#One park object
class NationalSite:
    def __init__(self,park_dict):#take a dict as input
        self.location = park_dict['location']
        self.name = park_dict['name']
        self.park_type = park_dict['park_type']
        self.description = park_dict['description']
        self.address = park_dict['mail_address']
    def __str__(self):
        return str(self.name+" | "+self.location)
    def get_mailing_address(self):
        return park_dict['mail_address']
    def __contain__(self,item):
        return item in self.name

inst = NationalSite(return_park_list(ar_soup)[0])#format to use NationalSite
print(inst)


## Define your class NationalSite here:





## Recommendation: to test the class, at various points, uncomment the following code and invoke some of the methods / check out the instance variables of the test instance saved in the variable sample_inst:
#
# f = open("sample_html_of_park.html",'r')
# soup_park_inst = BeautifulSoup(f.read(), 'html.parser') # an example of 1 BeautifulSoup instance to pass into your class
# sample_inst = NationalSite(soup_park_inst)
# f.close()


######### PART 3 #########
print(10*"*"+"Part_3"+10*"*")
# Create lists of NationalSite objects for each state's parks.

# HINT: Get a Python list of all the HTML BeautifulSoup instances that represent each park, for each state.
california_natl_sites = []#list of park instances
arkansas_natl_sites = []
michigan_natl_sites = []
for i in return_park_list(ca_soup):#i is a dictionary
    california_natl_sites.append(NationalSite(i))
for i in return_park_list(ar_soup):#i is a dictionary
    arkansas_natl_sites.append(NationalSite(i))
for i in return_park_list(mi_soup):#i is a dictionary
    michigan_natl_sites.append(NationalSite(i))
##Code to help you test these out:
for p in california_natl_sites:
	print(p)
for a in arkansas_natl_sites:
	print(a)
for m in michigan_natl_sites:
	print(m)



######### PART 4 #########
print(10*"*"+"Part_4"+10*"*")
## Remember the hints / things you learned from Project 2 about writing CSV files from lists of objects!
outfile = open('arkansas.csv',"w")
outfile.write("Name, Location, Type, Address, Description\n")
for park in arkansas_natl_sites:
    outfile.write('"{}","{}","{}","{}","{}"\n'.format(park.name,park.location,park.park_type,park.address,park.description))

outfile = open('california.csv',"w")
outfile.write("Name, Location, Type, Address, Description\n")
for park in california_natl_sites:
    outfile.write('"{}","{}","{}","{}","{}"\n'.format(park.name,park.location,park.park_type,park.address,park.description))

outfile = open('michigan.csv',"w")
outfile.write("Name, Location, Type, Address, Description\n")
for park in michigan_natl_sites:
    outfile.write('"{}","{}","{}","{}","{}"\n'.format(park.name,park.location,park.park_type,park.address,park.description))
## Note that running this step for ALL your data make take a minute or few to run -- so it's a good idea to test any methods/functions you write with just a little bit of data, so running the program will take less time!

## Also remember that IF you have None values that may occur, you might run into some problems and have to debug for where you need to put in some None value / error handling!
