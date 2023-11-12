import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
import csv

# URL of the website you want to crawl
url = 'https://www.youtube.com'


# Parse URL
def get_domain(url):
    parsed_uri = urlparse(url)
    return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)


# Perform an HTTP GET request to the URL
response = requests.get(url)

external_resources_script = []
external_resources_img = []

# Check if the request was successful
if response.status_code == 200:
    # Parse the content with BeautifulSoup for better readability
    soup = BeautifulSoup(response.content, 'html.parser')
    hyperlinks = [a.get('href') for a in soup.find_all('a')]
    # Prettify the BeautifulSoup object to print it with nice indentation
    print("html:")
    print(soup.prettify())
    print("************************************")
    print("hyperlinks:")
    print(hyperlinks)
    print("************************************")

    # Find all script tags with a 'src' attribute
    for script in soup.find_all('script', src=True):
        external_resources_script.append(script['src'])

    print("external_resources_script:")
    print(external_resources_script)
    print("************************************")

    # Find all img tags that could be tracking pixels by their size
    for img in soup.find_all('img', {'height': '1', 'width': '1'}):
        external_resources_img.append(img['src'])

    print("external_resources_img:")
    print(external_resources_img)
    print("************************************")

    base_domain = get_domain(url)
    third_party_resources_script = [url for url in external_resources_script if get_domain(url) != base_domain]
    print("third_party_resources_script:")
    print(third_party_resources_script)
    print("************************************")

    third_party_resources_img = [url for url in external_resources_img if get_domain(url) != base_domain]
    print("third_party_resources_img:")
    print(third_party_resources_img)
    print("************************************")

    # Setup WebDriver (assuming you have the appropriate driver installed)
    driver = webdriver.Chrome()

    # Open the target URL
    driver.get(url)

    # Now the page's JavaScript has been executed, we can look for dynamic tracking pixels
    dynamic_pixel_srcs = [img.get_attribute('src') for img in driver.find_elements_by_tag_name('img') if
                          img.size['height'] == 1 and img.size['width'] == 1]

    driver.quit()

    print("dynamic_pixel_srcs:")
    print(dynamic_pixel_srcs)
    print("************************************")

    # Assume 'third_party_resources' contains your third-party URLs
    with open('tracking_pixels.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Resource Type', 'Tracking Pixel URL'])

        # Write URLs from third_party_resources_script with "Script" as the resource type
        for url in third_party_resources_script:
            writer.writerow(['Script', url])

        # Write URLs from third_party_resources_img with "Image" as the resource type
        for url in third_party_resources_img:
            writer.writerow(['Image', url])

else:
    print(f"Failed to retrieve {url}")


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
