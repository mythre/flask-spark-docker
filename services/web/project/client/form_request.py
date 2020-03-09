import requests
import tabulate

if __name__ == "__main__":
    headers = {}
    headers['Accept'] = 'application/json'
    params = {}
    base_url = 'http://localhost:5009/'

    print("Available functions: 1.getItemsbyColor 2.getBrandsCount 3.getRecentItems",
          "Enter the name of function: ")
    function = input()

    if function in ('getItemsbyColor',):
        print("Enter the color: ")
        color = input()
        params = {'color': color}
    elif function in ('getBrandsCount', 'getRecentItems'):
        print("Enter the date in YYYY-MM-DD format: ")
        date = input()
        params = {'date': date}
    else:
        print("Invalid function")

    if params:
        new_url = base_url + function
        print("url being hit:",new_url)
        print("parameter being sent:",params)
        response = requests.get(url=new_url, params=params, headers=headers)
        try:
            json_response = response.json()
            if json_response['data']:
                print(tabulate.tabulate(json_response['data'], headers='keys'))
            else:
                print("No records found")
        except:
            print("error resposne")
