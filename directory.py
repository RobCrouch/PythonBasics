# user/bin/ python 3
import requests
import sys
from bs4 import BeautifulSoup as BS


def directory(f_name, l_name):
    """Searches Oregon State University (OSU) Online directory and returns name title dept and phone/Email"""
    if type(f_name) is not str:
        raise Exception('First name Should be a string')
    if type(l_name) is not str:
        if l_name is not None:
            raise Exception('last name Should be a string')
        
    first_name = f_name
    last_name = l_name
    
    if first_name is None:
        if last_name is None:
            raise Exception('No input for First Name')
    if last_name is None:
        last_name = ''
    if last_name == '':
        search_name = first_name
    else:
        search_name = first_name + '+' + last_name

    domain_search = 'http://directory.oregonstate.edu/?type=search&cn=' + search_name
    page = requests.get(domain_search)
    soup = BS(page.text, 'html.parser')
    is_found = soup.find('h2')
    
    if is_found.string == 'Error: Too many entries returned. Try a more precise search.':
        raise Exception('Your search returned too many entries please refine it and try again.')
    if is_found.string == 'No matches found':
        raise Exception('No matchers were found!\n Please try again')
    if is_found.contents[0] != 'Common Questions':
        multiple_results = True
    else:
        multiple_results = False

    if not multiple_results: # replaced multiple results == False
        # logical statement tpo determine if data has student or facility
        results = soup.find(class_="record")
        results_dd = results.find_all('dd')
        
        if results_dd[1].contents[0] == 'Employee':
            is_employee = True
        else:
            is_employee = False
            
        if is_employee:  # if is_employee == True:
            name = results_dd[0]
            position = results_dd[2]
            department = results_dd[3]
            
            is_phone = results.find_all(text='Office Phone Number')
            is_email = results.find_all(text='Email')
            
            if len(is_phone) == 0:
                have_phone = False
            else:
                have_phone = True
            if len(is_email) == 0:
                have_email = False
            else:
                have_email = True

            print('\n\nName: {0}'.format(name.string))
            print('Position : {0}'.format(position.string))
            print('Department: {0}'.format(department.string))
            
            if not have_phone:
                print('No Phone Number Available.')
                if have_email:
                    email = results_dd[5]
                    print('Email: {0}'.format(email.string))
            else:
                phone = results_dd[4]
                print('Phone: {0}'.format(phone.string))
        else:
            results = soup.find_all(class_="record")
            
            for record in results:
                name = record.contents[1].contents[3]
                department = record.contents[1].contents[7]
                email = record.contents[1].contents[15]

                print('\n\nName: {0}'.format(name.string))
                print('\nDepartment: {0}'.format(department.string))
                print('\nEmail: {0}'.format(email.string))
    else:
        results = soup.find_all(class_="record")
        
        for record in results:
            name = record.contents[1].contents[0]
            department_and_email = record.contents[3]
            department = department_and_email.contents[1]
            email = department_and_email.contents[3].contents[0]

            print('\n\nName: {0}'.format(name.string))
            print('\nDepartment: {0}'.format(department.string))
            print('\nEmail: {0}'.format(email.string))
    return


if __name__ == '__main__':
    """handle bad inputs"""
    try:
        first_name_ = sys.argv[1]
    except IndexError:
        first_name_ = None
    try:
        last_name_ = sys.argv[2]
    except IndexError:
        last_name_ = None
    directory(first_name_, last_name_)
