with open('output.txt', 'w') as writer: # writing output.txt.
        print("The output is saved in output.txt file \nPlease see the output in its file path")
        writer.write(f"Total cost = ")
        for promo in promotions_got:
            for item in promo.Items:
                writer.write(f"{item.merchandise_id} {item.product_count} \t")
            writer.write(f"{ price_data[item.merchandise_id] if promo.promotion_price==0 else promo.promotion_price} \n")
        