"""
Student name: Sushil Bhusal,
Student ID: 200574321,
Email: sushilbhusal363@gmail.com,
Last Modified Date: 2024-03-19 05:20 PM
"""
# Importing necessary libraries
import requests
import os
import re
from os.path import basename
from bs4 import BeautifulSoup

#url for scraping data
url = "https://www.ourcommons.ca/Members/en/search"

# get request for data
res = requests.get(url)

# formation of soup object
soup = BeautifulSoup(res.text, "lxml")

# Initialize a container to store the extracted data
info = []

# Function to extract names of members
def get_names():
    # Find all divs with class "ce-mip-mp-name"
    names = soup.find_all("div", attrs={"class": "ce-mip-mp-name"})
    if names:
        # Iterate over found names and print each
        for name in names:
            print("Name:", name.get_text())
    else:
        print("No names found")
    return names

# Call the function to extract names (This is done throguh out the project to close the function)
names = get_names()

# Function to determine gender based on name
def get_gender(name):
    # generate names of female members
    females = gender_female()
    if name in females:
        return "Female"
    else:
        return "Male"

# Functions to extract names of female members
def gender_female():
    #url of female webpage
    url_female = "https://www.ourcommons.ca/members/en/search?caucusId=all&province=all&gender=F"
    #get request to access data
    r_female = requests.get(url_female)
    # formation of soup object
    soup_female = BeautifulSoup(r_female.text, "lxml")
    # creation of empty container to store female data
    female_gender = {}
    # Find all divs with class "ce-mip-mp-name"
    names_female = soup_female.find_all("div", class_="ce-mip-mp-name")
    return names_female

# Function to extract provinces of members
def get_province():
    # Find all divs with class "ce-mip-mp-province"
    provinces = soup.find_all("div", attrs={"class": "ce-mip-mp-province"})
    if provinces:
        # Iterate over found provinces and print each
        for province in provinces:
            print("Province:", province.get_text())
    else:
        print("No provinces found")
    return provinces

# Call the function to extract provinces
provinces = get_province()

# Function to extract parties of members
def get_parties():
    # Find all divs with class "ce-mip-mp-party"
    parties = soup.find_all("div", attrs={"class": "ce-mip-mp-party"})
    if parties:
        # Iterate over found parties and print each
        for party in parties:
            print("Party:", party.get_text())
    else:
        print("No party found")
    return parties

# Call the function to extract parties
parties = get_parties()

# Function to extract URLs of member pages
def get_links():
    # finding all anchor tags with class "ce-mip-mp-tile"
    links = soup.find_all("a", attrs={"class": "ce-mip-mp-tile"})
    if links:
        # This is done to go through the availabe link and priint each link
        for link in links:
            href = link.get("href")
            full_url = f"https://www.ourcommons.ca{href}"
            print("Link:", full_url)
    else:
        print("No tile found")
    return links

# calling function for link
links = get_links()

#function is created for the xtraction of images of memers
def get_images():
    # finding all the images inside image tags and class "ce-mip-mp-picture visible-lg visible-md img-fluid"
    images = soup.find_all("img", attrs={"class": "ce-mip-mp-picture visible-lg visible-md img-fluid"})
    if images:
        # This is done to go through the availabe image link and generate   each image full link
        for image in images:
            img = image['src']  # Access the 'src' attribute of each image tag
            img_url = f"https://www.ourcommons.ca{img}"
            # saving the image in a directory
            with open(basename(img_url), "wb") as i:
                i.write(requests.get(img_url).content)
            print("Image URL:", img_url)
    else:
        print("No image found")
    return images

# Call the function to extract images
images = get_images()


#create a html file named list.html in a directory
with open('list.html', 'w') as f:
    f.write('<table border="1">\n')  # initializing the table with border
    f.write('<tr><th>Serial No.</th><th>Image</th><th>Name</th><th>Gender</th><th>Province</th><th>Party</th><th>Link</th></tr>\n')
    # using for loop in each member's details, here one function zip has been used to combine the elements together and pairing them
    for i, (image, name, province, party, link) in enumerate(zip(images, names, provinces, parties, links), start=1):
        # obtaining the URL from the link element
        href = link.get("href")
        # formation of full URL
        full_url = f"https://www.ourcommons.ca{href}"
        # formation of full URL of image
        img_url = f"https://www.ourcommons.ca{image['src']}"
        gender = get_gender(name)
        # Write each row directly to the file
        f.write(
            f'<tr><td>{i}</td><td><img src="{img_url}"</td><td>{name.get_text()}</td><td>{gender}</td><td>{province.get_text()}</td><td>{party.get_text()}</td><td><a href="{full_url}">{full_url}</a></td></tr>\n')
    # closing the table
    f.write('</table>\n')

print("HTML has been written to List.html")
