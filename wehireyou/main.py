from bs4 import BeautifulSoup
import requests
import pandas as pd
import lxml
from datetime import date

today = date.today()

# get input from user for job title and location
# job_title = input('Enter job title: ')
# job_location = input('Enter location for job: ')
# experience_level = input('Choose experience category(Entry, Mid, Senior): ')

job_title = ''
job_location = 'india'
experience_level = ''

# assign experience level to corresponding url format using conditional
# if experience_level.lower()[0] == 'e':
#     experience_level = 'entry_level'
# elif experience_level.lower()[0] == 'm':
#     experience_level = 'mid_level'
# elif experience_level.lower()[0] == 's':
#     experience_level = 'senior_level'


# function to replace spaces/commas in title and location for url format
def format_strings(user_input):
    user_input = user_input.replace(' ', '%20')
    user_input = user_input.replace(',', '%2C')
    return user_input


# call to function to format the user input
job_title = format_strings(job_title)
job_location = format_strings(job_location)

# initialize empty list for jobs to be added to
job_list = []

# loop and increment count to switch over to next page of jobs
count = 0
for count in range(0, 40, 10):
    # fill in indeed url with given user input
    url = 'https://in.indeed.com/jobs?q={}&l={}&explvl={}&sort=date&start={}'.format(job_title.lower(), job_location,
                                                                                      experience_level, count)
    print(url)

    # get source code from website using requests library
    source = requests.get(url).text

    # pass website into beautiful soup
    soup = BeautifulSoup(source, 'html.parser')

    # find all job postings using the div found in the html
    posts = soup.select('a[class*="tapItem fs-unmask result"]')

    # loop through the div to get info for csv
    for post_info in posts:
        # get title from html using the second occurence of span
        try:
            title = post_info.find_all('span')[1].text
            #print(title)
        except Exception as e:
            title = 'NA'
            #print(title)

        # get company name
        try:
            company_name = post_info.find('span', class_='companyName').a.text
            #print(company_name)
        except Exception as e:
            company_name = 'NA'
            #print(company_name)

        # get location of job
        try:
            location = post_info.find('div', class_='companyLocation').text
            #print(location)
        except Exception as e:
            location = 'NA'
            #print(location)

        # get company pay
        try:
            pay = post_info.find('span', class_='salary-snippet').text
            #print(pay)
        except Exception as e:
            pay = 'NA'
            #print(pay)

        # get job summary bullest
        try:
            # get summary of job ([-1] so we do not get the more section on bottom)
            job_summary = post_info.find_all('li')[:-3]
            if len(job_summary) == 0:
                summary_bullets = 'NA'
                #print(summary_bullets)
            else:
                for summary_bullets in job_summary:
                    summary_bullets = '•{}'.format(summary_bullets.text)
                    #print(summary_bullets)
        except Exception as e:
            summary_bullets = 'NA'
            #print(summary_bullets)

        # get vjk for the url
        job_jk = post_info.get(('data-jk'))
        post_url = 'https://www.indeed.com/viewjob?jk={}'.format(job_jk)
        #print(post_url)
        #print()

        # get posting date
        # try:
        #     posting_date = post_info.find('span', class_='date').text
        #     print(posting_date)
        # except Exception as e:
        #     posting_date = 'NA'
        #     print(posting_date)

        #print()

        # save info into dict for importing into csv
        job_info = {
            'title': title,
            'company_name': company_name,
            'location': location,
            'pay': pay,
            'summary_bullets': summary_bullets,
            'post_url': post_url
        }
        print(job_info)
        # status = 1;
        # created_date = today.strftime("%d/%m/%Y");
        
        # jobData=Jobs(title=title,company_name=company_name,location=location,pay=pay,summary_bullets=summary_bullets,post=post_url, created_date=created_date)
        # # append jobs to list
        # try:
        #     db.session.add(jobData)
        # except Exception as e:
        #     print(e)
        job_list.append(job_info)

#print('job list')
print(job_list)

#add the data to the csv file
#display job_list dict as data frame
df = pd.DataFrame(job_list)

#get clean looking file name for user
csv_title = '{}Jobs'.format(job_title)
suffix = '.csv'
csv_title = csv_title.replace('%20', '_')
csv_title = csv_title + suffix

#write the data to the file
df.to_csv(csv_title)
print('Data added to .csv file')