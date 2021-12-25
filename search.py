# Importing required packages
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import requests


# Function search product online
def search_online(product):
    # preparing the URL to search the product on flipkart
    flipkart_url = "https://www.flipkart.com/search?q=" + product

    # requesting the webpage from the internet
    uClient = uReq(flipkart_url)

    # reading the webpage
    flipkartPage = uClient.read()

    # closing the connection to the web server
    uClient.close()

    # parsing the webpage as HTML
    flipkart_html = bs(flipkartPage, "html.parser")

    # searching for appropriate tag to redirect to the product link
    bigboxes = flipkart_html.findAll("div", {"class": "_1AtVbE col-12-12"})

    # the first 3 members of the list do not contain relevant information, hence deleting them
    del bigboxes[0:3]

    # taking the first iteration (for demo)
    box = bigboxes[0]

    # extracting the actual product link
    productLink = "https://www.flipkart.com" + box.div.div.div.a['href']

    # getting the product page from server
    prodRes = requests.get(productLink)

    # parsing the product page as HTML
    prod_html = bs(prodRes.text, "html.parser")

    # finding the HTML section containing the customer comments
    commentboxes = prod_html.find_all('div', {'class': "_16PBlm _3_IKGE"})

    # initializing an empty list for reviews
    reviews = []

    #  iterating over the comment section to get the details of customer and their comments
    for commentbox in commentboxes:
        try:
            name = commentbox.div.div.find_all('p', {'class': '_2sc7ZR _2V5EHH'})[0].text
        except:
            name = 'No Name'

        try:
            rating = commentbox.div.div.div.div.text
        except:
            rating = 'No Rating'

        try:
            commentHead = commentbox.div.div.div.p.text
        except:
            commentHead = 'No Comment Heading'

        try:
            comtag = commentbox.div.div.find_all('div', {'class': ''})
            custComment = comtag[0].div.text
        except:
            custComment = 'No Customer Comment'

        # saving that detail to a dictionary
        mydict = {"Product": product, "Name": name, "Rating": rating, "CommentHead": commentHead,
                  "Comment": custComment}

        # appending the comments to the review list
        reviews.append(mydict) 

    # return reviews
    return reviews
