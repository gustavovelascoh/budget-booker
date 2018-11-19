import requests


URL="https://www.budget.ie/api/rest/v2/booking/quote"

data = {"pickupLocation":"KA","returnLocation":"KA","pickupDatetime":"20180819T1830","returnDatetime":"20180831T1830","cdw":"I","discount":"","currency":"EUR","key":""}


def quote_book(init, end):
    data = {"pickupLocation":"KA","returnLocation":"KA","pickupDatetime":"20180819T1830","returnDatetime":"20180831T1830","cdw":"I","discount":"","currency":"EUR","key":""}
    data["pickupDatetime"] = init
    data["returnDatetime"] = end
    
    response = requests.post(URL, json  =data)
    #print(response.text)
#    print(response.content)
    rate = response.json()["data"]["Rates"]["MDMN"]
#    print(rate)

    if rate[-1] == '0':
        rate = rate[0:-1]
    return float(rate)
    


hour_init = "1830"
date_init = [11,28]
date_end = [12,24]


days = 1

best_opt = {"dates": "", "price_per_day": 0, "total_price": 99999999 }


curr_date = date_init[:]
#for i in range(date_init, date_end):
while curr_date != date_end:

    if curr_date == date_init:
        date_init_str = "2018%02d%02dT1830" % (curr_date[0],curr_date[1])
        date_end_str = "2018%02d%02dT1830" % (date_end[0],date_end[1])

        rate = quote_book(date_init_str, date_end_str)
        ppd = rate/days

        dates = "(a){0}-{1}".format(date_init, date_end)
        rate_str= rate
    else:
        date_init_str = "2018%02d%02dT1830" % (date_init[0],date_init[1])
        date_end_str = "2018%02d%02dT1830" % (curr_date[0],curr_date[1])

        rate1 = quote_book(date_init_str, date_end_str)


        date_init_str = "2018%02d%02dT1830" % (curr_date[0],curr_date[1])
        date_end_str = "2018%02d%02dT1830" % (date_end[0],date_end[1])
        rate2 = quote_book(date_init_str, date_end_str)

        rate = rate1 + rate2
        ppd = rate1/days
        dates = "(b){0}-{1}/{2}-{3}".format(date_init,curr_date,curr_date, date_end)
        rate_str = "{0}+{1}={2}".format(rate1, rate2, rate)
        days += 1
    print ("{0} = {1}, {2} ppd* €/d".format(dates, rate_str, ppd))     

    if curr_date[0] == 8 and curr_date[1] == 31:
        curr_date[0] = 9
        curr_date[1] = 1
    elif curr_date[0] == 9 and curr_date[1] == 30:
        curr_date[0] = 10
        curr_date[1] = 1
    elif curr_date[0] == 10 and curr_date[1] == 31:
        curr_date[0] = 11
        curr_date[1] = 1
    elif curr_date[0] == 11 and curr_date[1] == 30:
        curr_date[0] = 12
        curr_date[1] = 1
    else:
        curr_date[1] += 1

    #days += 1
        
    if rate < best_opt["total_price"]:
        best_opt["total_price"] = rate
        best_opt["dates"] = dates
        #best_opt["price_per_day"] = ppd

print(best_opt)


