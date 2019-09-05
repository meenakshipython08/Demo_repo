import requests
from bs4 import BeautifulSoup
import pandas as pd


rest_list=[]
city_list=[]
restaurant_name_list=[]
restaurant_city_list=[]
restaurant_country_list=[]
restaurant_address_list=[]
restaurant_contact_list=[]
restaurant_website_list=[]
restaurant_email_list=[]
total_pages=0
city_url='https://www.tripadvisor.in/Restaurants-g155033-Quebec_City_Quebec.html'
print("City url=",city_url)
### getting information from each div ####
change=30
page=1
total_pages=44
while(1):

	if(int(page)> total_pages):
		break
	print("Retrieving data from page",page,"Please wait!!!!!")
	try:
		res=requests.get(city_url)
		soup=BeautifulSoup(res.text,'lxml')
	
		for i in soup.select('.property_title'):
			try:
				new_url='https://www.tripadvisor.in'+str(i['href'])
				res_link=requests.get(new_url)
				res_soup=BeautifulSoup(res_link.text,'lxml')

				## Website and Email Id ##
				soup_data=str(res_soup)
				soup_data=soup_data.split(' ')
				found_website=0
				found_email=0
				website=''
				email=''
				for word in soup_data:
					if(('"website":"http' in word) and found_website==0):
							website=word.split(',')[1].replace('website','').replace('"','').replace(',','').replace(':','')
							website=website.replace('https//','https://')
							website=website.replace('http//','http://')
							if('http' not in website):
								website="Not found"
							found_website=1
					
					if(('"email":"' in word) and found_email==0):
							email=word.split('"email":')[1].replace('"','').split(',')[0]
							found_email=1
							break;
				restaurant_email_list.append(email)
				restaurant_website_list.append(website)

				## Getting Name, Address, Country and Contact
				for res_details in res_soup.select("#taplc_resp_rr_top_info_rr_resp_0"):
					
					## Restaurant name ##
					rest_name=res_details.find_all('h1', class_='ui_header')
					rest_name=(str(rest_name)[26:]).replace('</h1>]','')
					#print("Name is: ",rest_name)
					restaurant_name_list.append(rest_name)

					## Restaurant Address ##
					street_addr=res_details.find_all('span',class_='street-address')
					street_addr=(str(street_addr)[30:]).replace('</span>]','')
					#print("Street: ",street_addr)

					## Restaurant city ##
					city_addr=res_details.find_all('span',class_='locality')
					city_addr=(str(city_addr)[24:]).replace(', </span>]','')
					#print("City: ",city_addr)

					## Restaurant Country ##
					rest_country=res_details.find_all('span',class_='country-name')
					rest_country=(str(rest_country)[28:]).replace('</span>]','')
					#print("Country: ",rest_country)

					## Creating list for address, city and country ##
					restaurant_address_list.append(street_addr+','+city_addr+','+rest_country)
					restaurant_city_list.append(city_addr)
					restaurant_country_list.append(rest_country)

					## Contact No. ##
					try:
						rest_contact=res_details.find_all('span',class_='detail')
						rest_contact=str(rest_contact[1])
						rest_contact=(rest_contact[38:]).replace('</span>','')
						#print("Contact: ",rest_contact)
					except Exception as e:
						rest_contact.append('Not Found')
					if('span' in str(rest_contact)):
						restaurant_contact_list.append('Not found')
					else:
						restaurant_contact_list.append(rest_contact)

			except Exception as e:
				pass				
				
		## Next page Link ##				
		site_nm=city_url.split('-')[0]
		first_no=city_url.split('-')[1]
		last_nm=city_url.rsplit('-')[-1]
		city_url=site_nm+'-'+first_no+'-oa'+str(change)+'-'+last_nm
		change+=30
		page+=1

	except Exception as e:
		print("No further pages")
		break
		
# print(">>>>>>>>>>>>>>>>>>>>>>>>>>Restaurant Names: ",restaurant_name_list)
# print("Restaurant name: ",restaurant_name_list,len(restaurant_name_list))
# print("Restaurant City: ",restaurant_name_list,len(restaurant_city_list))
# print("Restaurant Country: ",restaurant_country_list,len(restaurant_country_list))
# print("Restaurant Address: ",restaurant_address_list,len(restaurant_address_list))
# print("Restaurant Phone No.: ",restaurant_contact_list,len(restaurant_contact_list))


print("########## Creating Excel file ###########")
try:
	data={
	'Name':restaurant_name_list,
	'Contact_no':restaurant_contact_list,
	'Email_Id':restaurant_email_list,
	'Website':restaurant_website_list,
	'City':restaurant_name_list,
	'Country':restaurant_country_list,
	'Address':restaurant_address_list,
				
		}

	file_name='Quebec.xlsx'
	df=pd.DataFrame(data=data)
	df.to_excel(file_name)
except Exception as e:
	print("Error:::",e)
print("########## done ###########")

