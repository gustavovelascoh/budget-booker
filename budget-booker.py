import requests
from datetime import datetime
from datetime import timedelta
import argparse


URL="https://www.budget.ie/api/rest/v2/booking/quote"

data = {"pickupLocation":"KA","returnLocation":"KA","pickupDatetime":"20180819T1830","returnDatetime":"20180831T1830","cdw":"I","discount":"","currency":"EUR","key":""}


def quote_book(init, end):
    data = {"pickupLocation":"KA","returnLocation":"KA","pickupDatetime":"20180819T1830","returnDatetime":"20180831T1830","cdw":"I","discount":"","currency":"EUR","key":""}
    data["pickupDatetime"] = init
    data["returnDatetime"] = end

    #print("data ", data)
    response = requests.post(URL, json  =data)
    #print(response.text)
#    print(response.content)

    try:
        rate = response.json()["data"]["Rates"]["MDMN"]

#    print(rate)
    except KeyError:
        #print("No rate found")
        rate = "99999"
    except:
        rate = "88888"
        print("ERROR")

    if rate[-1] == '0':
        rate = rate[0:-1]
    return float(rate)


def eval_range(init,end):
    init_str = init.strftime("%Y%m%dT%H%M")
    end_str = end.strftime("%Y%m%dT%H%M")
    #print("EVALUATING %s - %s" % (init_str, end_str))
    rate = quote_book(init_str, end_str)
    return rate

def main():

    ap = argparse.ArgumentParser()

    ap.add_argument("-init")
    ap.add_argument("-end")
    ap.add_argument("-init_time",default="18:30")
    ap.add_argument("-end_time",default="18:30")

    args = ap.parse_args()

    date_init = datetime.strptime(args.init + " " + args.init_time, "%Y-%m-%d %H:%M")
    date_end = datetime.strptime(args.end + " " + args.end_time, "%Y-%m-%d %H:%M")

    total = date_end - date_init

    one_day = timedelta(days=1)

    print("Total days %s" % (total.days))

    date_mid = date_init + one_day

    whole = eval_range(date_init, date_end)
    ppdw = whole / total.days

    best_rate = ppdw
    best_rate_str = "Whole: %s €, %4.2f @ day" % (whole, ppdw)

    print(best_rate_str)

    curr_delta = date_mid - date_init

    end_delta = date_end - date_mid

    date_init_str = date_init.strftime("%Y-%m-%d %H:%M")
    date_end_str = date_end.strftime("%Y-%m-%d %H:%M")

    header_str="%16s\t%16s\t%16s\t" % ("Pickup date","Renew date", "Return date")
    header_str += "Total Price\t Par.rates\t Eq.Rate"

    print(header_str)

    while end_delta.days > 0:

        curr_delta = date_mid - date_init
        #print(date_mid)

        rate1 = eval_range(date_init, date_mid)
        rate2 = eval_range(date_mid, date_end)

        date_mid_str = date_mid.strftime("%Y-%m-%d %H:%M")

        if rate1 < 5000:
            curr_rate = (rate1+rate2)/total.days
            curr_str = ("%s\t%s\t%s\t%s+%s=%s €, (%4.2f,%4.2f)@day\t%4.2f@day" %
            (date_init_str, date_mid_str, date_end_str, rate2,
            rate2, rate1+rate2, rate1/curr_delta.days, rate2/(total.days-curr_delta.days),
            curr_rate))
        else:
            curr_str = ("%s\t%s\t%s\t0+0=0€, (0,0)@day\t0@day" %
            (date_init_str, date_mid_str, date_end_str))

        print(curr_str)

        date_mid += one_day
        end_delta = date_end - date_mid

        if (best_rate > curr_rate):
            best_rate = curr_rate
            best_rate_str = curr_str

    print("BEST RATE: € %4.2f @ day" % best_rate)
    print(best_rate_str)



if __name__ == "__main__":
    main()
