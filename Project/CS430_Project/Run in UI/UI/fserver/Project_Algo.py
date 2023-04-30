import sys

class Item:
    def __init__(self, merchandise_id, product_count):
        self.merchandise_id = merchandise_id
        self.product_count = product_count

class Promotion:
    def __init__(self, product, promotion_price):
        self.Items = product
        self.promotion_price = promotion_price


def split_prices(prices_file):
    dict = {}
    with open(prices_file, 'r') as reader:
        for values in reader:
            val1 = values.split()
            val2 = int(val1[0])
            val3 = float(val1[1])
            dict[val2] = val3

    return dict


def split_input(input_file):
    input = []
    with open(input_file, 'r') as reader:
        values = int(reader.readline().strip())
        for i in range(values):
            val1 = reader.readline().strip().split()
            val2 = int(val1[0])
            val3 = int(val1[1])
            input.append(Item(val2, val3))



    return input

def split_promotions(promotions_file):
    promoCode = []

    with open(promotions_file, 'r') as reader:
        promo_val = int(reader.readline().strip())

        for i in range(promo_val):
            val1 = []
            val2 = reader.readline().strip().split()
            val3 = int(val2[0])

            for j in range(1, val3*2+1, 2):
                val1.append(Item(int(val2[j]), int(val2[j+1])))

            promo_price = int(val2[val3*2+1])

            promoCode.append(Promotion(val1, promo_price))


    return promoCode


# define a recursive function to find the best combination of promotions
def outputCalculate(id_promo, actualPrice, items_left, promos_avail, promotions, price_sum, promo_applied):
    boolVal = True
    for key in range(id_promo, len(promotions)):
        discount = promotions[key]
        discount_items = discount.Items
        merchItem_copy = items_left.copy()
        discountItem_copy = []
        total_bill = discount.promotion_price
        if len(discount_items) <= len(merchItem_copy):
            for i in range(len(discount_items)):
                item = discount_items[i]
                boolVal = True
                for task in range(len(merchItem_copy)):
                    req_prod = merchItem_copy[task]
                    if item.merchandise_id == req_prod.merchandise_id:
                        if item.product_count <= req_prod.product_count:
                            if item.product_count < req_prod.product_count:
                                merchItem_copy[task] = Item(req_prod.merchandise_id, req_prod.product_count - item.product_count)   
                            else:
                                merchItem_copy.pop(task)
                            boolVal = True
                        else:
                            boolVal = False
                        break
                    if task == len(merchItem_copy) - 1:
                        boolVal = False
                if not boolVal:
                    break
                discountItem_copy.append(Item(item.merchandise_id, item.product_count))
            if not boolVal:
                if key == len(promotions) - 1:
                    total_temp = 0
                    needed_item = []
                    for i in range(len(items_left)):
                        calitem = items_left[i]
                        total_temp += actualPrice[calitem.merchandise_id] * calitem.product_count
                        needed_item.append(Item(calitem.merchandise_id, calitem.product_count))
                    price_sum += total_temp
                    if promo_applied[0].promotion_price > price_sum:
                        promos_avail.append(Promotion(needed_item, 0))
                        promos_avail[0].promotion_price =price_sum
                        return promos_avail
                    return promo_applied
                else:
                    continue
            else:
                total_temp_copy = price_sum
                promo_copy = promos_avail.copy()
                promo_copy.append(Promotion(discountItem_copy, total_bill))
                total_temp_copy += total_bill
                promo_applied = outputCalculate(key, actualPrice, merchItem_copy, promo_copy, promotions, total_temp_copy, promo_applied)
        else:
            if key == len(promotions) - 1:
                total_temp = 0
                needed_item = []
                for i in range(len(merchItem_copy)):
                    calitem = merchItem_copy[i]
                    total_temp += actualPrice[calitem.merchandise_id] * calitem.product_count
                    needed_item.append(Item(calitem.merchandise_id, calitem.product_count))
                price_sum += total_temp
                if promo_applied[0].promotion_price > price_sum:
                    promos_avail.append(Promotion(needed_item, 0))
                    promos_avail[0].promotion_price = price_sum
                    return promos_avail
                return promo_applied
            else:
                continue
    return promo_applied


def main():
    arg1 = sys.argv[1]  # the first argument passed to script1.py
    arg2 = sys.argv[2]  # the second argument passed to script1.py
    arg3 = sys.argv[3]  # the third argument passed to script1.py
    print(arg1, arg2, arg3)  # prints 'value1 value2 value3'
    # file_input = input("Enter input file path: ")
    # file_prices = input("Enter prices file path: ")    
    # file_promotions = input("Enter promotions file path: ")

    file_input = arg1
    file_prices = arg2
    file_promotions = arg3

    price_data = split_prices(file_prices)
    prod_data = split_input(file_input)
    promo_data = split_promotions(file_promotions)
    
    merch_id =0
    items_discount = []
    discount = []
    discount_used = []
    promotions_got = []
        
    discount_used.append(Promotion(items_discount, float("inf")))
    discount.append(Promotion(items_discount, 0))  

    promotions_got = outputCalculate(merch_id,price_data,prod_data,discount,promo_data,0,discount_used)
    
    with open('output.txt', 'w') as writer:
        print("The output is saved in output.txt file \nPlease see the output in its file path")
        writer.write(f"Total cost = ")
        for promo in promotions_got:
            # print("Offer:")
            for item in promo.Items:
                writer.write(f"{item.merchandise_id} {item.product_count} \t")
            writer.write(f"{ price_data[item.merchandise_id] if promo.promotion_price==0 else promo.promotion_price} \n")
            
if __name__ == "__main__":
    main()
