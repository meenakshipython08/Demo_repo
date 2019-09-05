from django.conf import settings
from django.shortcuts import render
from django.views.generic.base import TemplateView

import requests
from bs4 import BeautifulSoup

import pandas as pd

from django.views.decorators.csrf import csrf_exempt

from .models import scraping_info



import sys 


# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'

'''global url_list;

url_list={'Mumbai':'https://www.tripadvisor.in/Restaurants-g304554-Mumbai_Maharashtra.html',
		'Delhi':'https://www.tripadvisor.in/Restaurants-g304551-New_Delhi_National_Capital_Territory_of_Delhi.html',
		'Kolkata':'https://www.tripadvisor.in/Restaurants-g304558-Kolkata_Calcutta_Kolkata_District_West_Bengal.html',
		'Chennai':'https://www.tripadvisor.in/Restaurants-g297595-Raipur_Raipur_District_Chhattisgarh.html',
		'Bangalore':'https://www.tripadvisor.in/Restaurants-g304556-Chennai_Madras_Chennai_District_Tamil_Nadu.html',
		'Hyderabad':'https://www.tripadvisor.in/Restaurants-g297628-Bengaluru_Bangalore_District_Karnataka.html',
		'Jaipur':'https://www.tripadvisor.in/Restaurants-g297586-Hyderabad_Hyderabad_District_Telangana.html',
		'Lucknow':'https://www.tripadvisor.in/Restaurants-g662320-Ranchi_Ranchi_District_Jharkhand.html',
		'Patna':'https://www.tripadvisor.in/Restaurants-g304555-Jaipur_Jaipur_District_Rajasthan.html',
		'Bhopal':'https://www.tripadvisor.in/Restaurants-g297684-Lucknow_Lucknow_District_Uttar_Pradesh.html',
		'Thiruvananthapuram':'https://www.tripadvisor.in/Restaurants-g297592-Patna_Patna_District_Bihar.html',
		'Chandigarh':'https://www.tripadvisor.in/Restaurants-g297596-Chandigarh.html',
		'Raipur':'https://www.tripadvisor.in/Restaurants-g319726-Bhopal_Bhopal_District_Madhya_Pradesh.html',
		'Ranchi':'https://www.tripadvisor.in/Restaurants-g12080450-Thiruvananthapuram_District_Kerala.html',
		'Srinagar':'https://www.tripadvisor.in/Restaurants-g297623-Srinagar_Srinagar_District_Kashmir_Jammu_and_Kashmir.html'}
'''


def get_cities(url):
	city_list=[]
	res = requests.get(url)
	soup=BeautifulSoup(res.text,'lxml')
	for i in soup.select('b > a'):
		if(len(i.text)>2):
			city_list.append(i.text)
	#print(city_list)
	return city_list



  
def getdetails(request,):	
	city_list=get_cities('https://en.wikipedia.org/wiki/List_of_million-plus_urban_agglomerations_in_India')
	
	details={'city_list':city_list}

	return render(request,'data_page.html',{'details':details})


global country_name, city_links,index, saved_files_list, in_progress_files_list,message,city_list;
city_links=[]
index=-1
saved_files_list=[]
in_progress_files_list=[]
message=''
city_list=[]

@csrf_exempt
def showcities(request,):
	global city_links,saved_files_list, in_progress_files_list, country_name;
	ab=sys.path("var/www/Projects/try_test/testing_file.py")


	print("&&&&&&& data= ",ab)
	city_links=[]	
	city_list=[]
	if(request.method=='POST'):
		country_name=request.POST.get('countryname')
		if(country_name=='Canada'):
			res = requests.get('https://www.tripadvisor.in/Restaurants-g153339-Canada.html#LOCATION_LIST')
			
		if(country_name=='Australia'):
			res = requests.get('https://www.tripadvisor.in/Restaurants-g255055-Australia.html')
			
		if(country_name=='USA'):
			res = requests.get('https://www.tripadvisor.in/Restaurants-g191-United_States.html')
			

		soup=BeautifulSoup(res.text,'lxml')
		for i in soup.select('.geo_name > a'):
			#### city names ####
			city_name=i.text
			city_list.append(city_name.replace('Restaurants',''))

			#### city links ####
		for i in soup.select('.geo_image'):
			link='https://www.tripadvisor.in/'+i.findAll('a')[0]['href']
			city_links.append(link)	
		#print(city_links)		


		## Accessing Database files ###
		saved_files = scraping_info.objects.all().values('saved_files')
		for val in saved_files:
			saved_files_list.append(val['saved_files'])

		inprogress_files= scraping_info.objects.all().values('in_progress_files')
		for val in inprogress_files:
			if('done' in str(val)):
				pass
			else:
				in_progress_files_list.append(val['in_progress_files'])			

		# print("&&&&&&&&&&&&&&&&&&&&",saved_files_list)
		# print("&&&&&&&&&&&&&&&&&&&&",in_progress_files_list)

		saved_files_list = list(dict.fromkeys(saved_files_list))
		in_progress_files_list = list(dict.fromkeys(in_progress_files_list))


	return render(request,'data_page.html',{'city_list':city_list,'saved_files_list':saved_files_list,'in_progress_files_list':in_progress_files_list, 'country_name':country_name})


def searchrestaurants(request,):
	global city_links,message,city_list;
	rest_list=[]
	restaurant_name_list=[]
	restaurant_city_list=[]
	restaurant_country_list=[]
	restaurant_address_list=[]
	restaurant_contact_list=[]
	restaurant_website_list=[]
	restaurant_email_list=[]
	total_pages=0
	db_found=0
	if(request.method=='POST'):
		
		city_name=request.POST.get('cityname')
		print("You have selected ",city_name)
		city_name=city_name.split(' ')[0]
		
		### Checking selected city name in links #####
		for city in city_links:
			if(city_name in city):
				city_url=city
				break

		## Checking weather the file already exists or not ##
		
		saved_files = scraping_info.objects.all().values('saved_files')
		for val in saved_files:
			if(city_name in str(val['saved_files'])):
				db_found=1
		if(db_found==1):
			message="You have already scraped the data of "+city_name
			print(message)
			return render(request,'data_page.html',{'city_list':city_list,'saved_files_list':saved_files_list,'in_progress_files_list':in_progress_files_list, 'country_name':country_name,'message':message})
		else:
			### getting information from each div ####
			change=30
			page=1
			while(1):

				if((int(page)>int(total_pages)) and int(total_pages)!=0):
					break
				print("Retrieving data from page",page,"Please wait!!!!!")
				try:
					res=requests.get(city_url)
					soup=BeautifulSoup(res.text,'lxml')

					## Getting total pages ##				
					for pg_info in soup.select('.deckTools'):
						all_links=pg_info.find_all('a')
						total_pages=all_links[len(all_links)-1].text
					#print("Tatal pages:::::::",total_pages)
					
					
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
			folder_name='Data/'+country_name+'/'
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

				file_name=folder_name+city_name+'_City'+'.xlsx'
				df=pd.DataFrame(data=data)
				df.to_excel(file_name)
			except Exception as e:
				print("Error:::",e)
			print("########## done ###########")

			## Storing details in Database ##
			print('############storing in database##########')
			file_name=file_name.replace('Data/','')
			insert_data=scraping_info(saved_files=file_name,in_progress_files='done')
			insert_data.save()
			print("##########done##############")
		return render(request,'home.html')



def datapage(request,):
	print("entered!!!!!!!!!!!!!!!!!!!!!!!!")
