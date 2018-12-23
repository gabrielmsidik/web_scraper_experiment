import requests
import sys
from bs4 import BeautifulSoup

file_extensions_to_download = [
    'pdf',
    'pptx',
    'ppt',
    'docx',
    'doc'
]
def begin_scraping(root_link, target_download_folder):
    request = requests.get(root_link)

    content = request.content
    html_content = BeautifulSoup(content, 'html.parser')

    for link_element in html_content.select('a'):
        link = link_element['href']
        link_components = link.split('.')
        if (link_components[-1] in file_extensions_to_download):
            print(link)
            try: 
                document_name = link_components[-2].split('/')[-1]
                download_file(link, document_name + '.' + link_components[-1], target_download_folder)
            except Exception:
                print("WARNING: Error occured from file download")


def download_file(download_url, fileName, download_folder_location):

    if download_folder_location[-1] != '/':
        download_folder_location = download_folder_location + '/'

    r = requests.get(download_url, allow_redirects = True)
    open(download_folder_location + fileName, 'wb').write(r.content)

# TODO: Decorator function to wrap around the actual scraping function
def main():

    '''
    HELPER TOOL TO SCRAPE AND DOWNLOAD MULTIPLE FILES FROM A WEBSITE

    ARGUMENTS TO PASS IN:
    1. URL TO WEBPAGE WHERE THE LINKS TO DOWNLOAD ARE
    2. TARGET DOWNLOAD FOLDER (OPTIONAL PARAMETER)
    '''

    target_download_folder = './downloads/'

    try:
        root_link = sys.argv[1]
    except IndexError:
        print('ERROR: Please pass target webpage URL')
        exit()

    if len(sys.argv) == 2:
        begin_scraping(root_link, target_download_folder)
    else:
        target_download_folder = sys.argv[2]
        begin_scraping(root_link, target_download_folder)

main()