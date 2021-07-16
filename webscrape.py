from bs4 import BeautifulSoup as soup  # HTML data structure
from urllib.request import urlopen as uReq  # Web client

# URl to web scrap from.
page_url = "https://www.newegg.com/p/pl?d=graphics+cards+3070&cm_sp=KeywordRelated-_-graphics+card-_-graphics+cards+3070-_-INFOCARD&PageSize=96"

# opens the connection and downloads html page from url
uClient = uReq(page_url)

# parses html into a soup data structure to traverse html
page_soup = soup(uClient.read(), "html.parser")
uClient.close()

# finds each product from the store page
containers = page_soup.findAll("div", {"class": "item-container"})

# name the output file to write to local disk
out_filename = "graphics_cards.txt"
# header of csv file to be written
headers = "brand,product_name,shipping,price,price_prev \n"

# opens file, and writes headers
f = open(out_filename, "w")
f.write(headers)

# loops over each product and grabs attributes about each product
for container in containers:
    
    make_rating_sp = container.div.select("a")

    # Grabs the title from the image title attribute
    brand = make_rating_sp[0].img["title"].title()

    # Grabs the text within the second "(a)" tag from within.
    product_name = container.div.select("a")[2].text

    # Grabs the product shipping information by searching
    shipping = container.findAll("li", {"class": "price-ship"})[0].text.strip().replace("$", "").replace(" Shipping", "")

    # Grabs the products price 
    # all lists with "price-current"
    price_now = container.findAll("li", {"class": "price-current"})[0].text.strip().replace("Offers", "")

    # Grabs the product previous price
    price_prev = container.findAll("li", {"class": "price-was"})[0].text.strip()


    # prints the dataset to console
    print("brand: " + brand + "\n")
    print("product_name: " + product_name + "\n")
    print("shipping: " + shipping + "\n")
    print("price_now: " + price_now + "\n")
    print("price_prev: " + price_prev + "\n")

    # writes to file
    f.write(brand + ", " + product_name.replace(",", "|") + ", " + shipping.replace(",", "|") + price_now + price_prev + "\n")

f.close() 
