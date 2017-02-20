from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.request
import pymysql

# MySQL Connection DB ID and PW have been removed
# conn = pymysql.connect(host='localhost', user=****, password=****, db='daza', charset='utf8', port = 3306, autocommit=True)
# Cursor creation
curs = conn.cursor()

# Recipe category to parse
base_url="https://www.cookipedia.co.uk/recipes_wiki/Category:British_recipes"
soup = BeautifulSoup(urlopen(base_url).read(), "html.parser")
h1 = soup.findAll("h1", "firstHeading")
category = h1[0].contents[0]
category = category[9:] # to be innserted into food(category)
links = soup.find("div", "mw-category-generated")

cnt = 0
for i in links:
    a = i.findAll('a')
    for j in a:
        dl = a[cnt]['href']
        r_url = "https://www.cookipedia.co.uk{0}".format(dl)
        soup2 = BeautifulSoup(urlopen(r_url).read(), "html.parser")
        ## Getting dish's name (food table)
        name = soup2.findAll("h1")
        foodname = name[0].contents[0]
        foodname = foodname.replace('"', "&quot;")
        sql = "INSERT INTO `food` (category, fid, name) VALUES (\"{0}\", \"id_{1}\", \"{2}\")".format(category, foodname, foodname)
        curs.execute(sql)
        print("#######",foodname )
        ## Getting ingredients
        links = soup2.findAll("span", "recipeIngredient")
        iorderno = 1
        for k in links:
            output =""
            for l in k.contents:
                if l.find("<a") != -1:
                    output = output + l.contents[0]
                else:
                    output = output + l
            output = output.replace('"', "&quot;")
            print(output)
            sql = "INSERT INTO `ingredient` (ingredient, fid, iorder) VALUES (\"{0}\", \"id_{1}\", \"{2}\")".format(output, foodname,iorderno)
            curs.execute(sql)
            iorderno = iorderno + 1
        # urllib.request.urlretrieve("https://www.cookipedia.co.uk{0}".format(dl), "{0}.html".format(dl[14:])) # download pages into your local machine
        #
        ## Getting recipe steps
        links = soup2.findAll("span", "recipeInstructions")
        step = 1
        for k in links:
            output =""
            for l in k.contents:
                if l.find("<a") != -1:
                    output = output + l.contents[0]
                else:
                    output = output + l
            output = output.replace('"', "&quot;")
            print('step', step,':', output)
            sql = "INSERT INTO `step` (step, stepDesc, fid) VALUES (\"{0}\", \"{1}\", \"id_{2}\")".format(step, output, foodname)
            curs.execute(sql)
            step = step + 1
        cnt = cnt+1
# db connection close
conn.close()
