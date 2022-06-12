import requests
from wsgiref import headers
from bs4 import BeautifulSoup
import time
import pandas as pd
from selenium import webdriver
import csv

start_url = "https://en.wikipedia.org/wiki/List_of_brown_dwarfs"
browser = webdriver.Chrome("C:/Users/Home/OneDrive/Desktop/Project-128/chromedriver.exe")
browser.get(start_url)
time.sleep(10)
scraped_data = []
headers = ["Star_name", "Distance", "Mass", "Radius", "Luminosity"]

def scrape():     
        #find <table>
        soup = BeautifulSoup(browser.page_source, "html.parser")
        bright_star_table = soup.find("t", attrs = {"class", "wikitable"})
        #find <tbody>
        table_body = bright_star_table.find_all('tbody')
        #find <tr>
        table_rows = table_body.find_all('tr')
        
        for row in table_rows:
            table_cols = row.find_all('td')
            print(table_cols)
            temp_list = []
            
            for col_data in table_cols:
                data = col_data.text.strip()
                print(col_data.text)
                temp_list.append(data)
            
            scraped_data.append(temp_list)
        
            stars_data = []        
            for i in range(0, len(scraped_data)):
                Star_names = scraped_data[i][1]
                Distance = scraped_data[i][3]
                Mass = scraped_data[i][5]
                Radius = scraped_data[i][6]
                Lum = scraped_data[i][7]
                
                required_data = ['Star_name', 'Distance', 'Mass', 'radius', 'Luminosity']
                
                star_df_1 = pd.DataFrame(stars_data, columns=headers)
                star_df_1.to_csv('scraped_data.csv', index=True, index_label='id')
                
            for ul_tag in soup.find_all("ul", attrs = {"class", "exoplanet"}):
                li_tags = ul_tag.find_all("li")
            temp_list = []
            for index, li_tag in enumerate(li_tags):
                if index == 0:
                    temp_list.append(li_tag.find_all("a")[0].contents[0])
                else:
                    try:
                        temp_list.append(li_tag.contents[0])
                    except:
                        temp_list.append("")
                        
            hyperlink_li_tag = li_tags[0]
            temp_list.append("https://en.wikipedia.org/wiki/List_of_brown_dwarfs"+hyperlink_li_tag.find_all("a", href=True)[0]["href"])
            scraped_data.append(temp_list)
        
scrape()        

new_dwarf_planets_data = []
def scrape_more_data(hyperlink):
    try:
        page = requests.get(hyperlink)
        soup = BeautifulSoup(page.content, "html.parser")
        temp_list = []
        for tr_tag in soup.find_all("tr", attrs={"class":"fact_row"}):
            td_tags = tr_tag.find_all("td")
            for td_tag in td_tags:
                try:
                    temp_list.append(td_tag.find_all("div", attrs={"class":"value"})[0].contents[0])
                except:
                    temp_list.append("")
                    
        new_dwarf_planets_data.append(temp_list)
        
    except:
        time.sleep(1)    
        scrape_more_data(hyperlink)
    
for index, data in enumerate(scraped_data):
    scrape_more_data(data[5])
    print(f"scraping at hyperlink{index+1} is completed")

print(new_dwarf_planets_data[0: 10])
final_drawrf_planet_data = []

for index, data in enumerate(scraped_data):
    new_dwarf_planets_data_element = new_dwarf_planets_data[index]
    new_dwarf_planets_data_element = [elem.replace("\n", "")for elem in new_dwarf_planets_data_element]
    new_dwarf_planets_data_element = new_dwarf_planets_data_element[:7]
    final_drawrf_planet_data.append(data+new_dwarf_planets_data_element)

with open("final.csv", "w") as f:
    csv_writer = csv.writer(f)   
    csv_writer.writerow(headers)
    csv_writer.writerows(final_drawrf_planet_data)
        