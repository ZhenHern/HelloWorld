import pandas as pd
import difflib

sugg = []

'''
build_range
Purpose:
- creates another dataframe (df_cpy1) containing the stalls and the number of items for each
- creates global variables defines the range of index for each stall in the dataframe (df)
Method: Append the index of items from the same stall to a list, since the items are consecutive, only the first and last value is needed
'''
def build_range(df):
    total = []                                                                                                  # create empty list
    global df_cpy1                                                                                              # set the dataframe (df_cpy1) that will be created as a global variable
    df_cpy1 = df["stall_name"].value_counts()                                                                   # create new dataframe (df_cpy1) that will contain the stalls in df and the number of items under them
    df_cpy1 = df_cpy1.reset_index()                                                                             # insert new index for easier calling
    df_cpy1 = df_cpy1.rename(columns={"index": "stall", "stall_name": "quantity"})                              # rename column header for easier understanding
    for i in range(0,df_cpy1.shape[0]):                                                                         # for every row in df_cpy1
        total = []                                                                                              # reset the list
        for j in range(0,df.shape[0]):                                                                          # for every row in df
            if df["stall_name"][j].lower() == df_cpy1["stall"][i].lower():                                      # check the stall of every row in df with the stall in df_cpy1
                total.append(j)                                                                                 # Append the index of items under corresponding stall
        a = df_cpy1["stall"][i].lower()
        globals()[f"range_{a}"] = [total[0],total[len(total)-1]+1]                                              # creating the range for each stall as global variables

'''
PrintMenu function
Purpose:
-to print the menu list (everything inside the excel file >> stall_name, item_name, price and delivery_service)
-after printing the menu, ask the user to enter the food they want
-and if the user still undecided, ask them would they want to see the sorted menu 
'''
def PrintMenu(res,df) :
    res+= "I will now print the menu to you.\n\n"
    res+= "{:<42}{:^15}{:^30}".format("Food","Price (RM)","Delivery Service") + "\n"                                #set the space for three column, then print the header of the menu (food, price and delivery service)                                  

    
    for i in range(0,df_cpy1.shape[0]):                                                                             #go through every row of the list (excel file data)                                        
        res+= "\n<<" + df_cpy1["stall"][i].capitalize() +">>\n\n"                                                   #print the cuisine type with the first letter caps before printing every food of that cuisine
        a = df_cpy1["stall"][i].lower()                                                                             #define a as the variable for the stall name
        b = globals()[f"range_{a}"]                                                                                 #define b as the variable for the range of item in the stall
        for i in range(b[0],b[1]):                                                                                  #for loop that loop for every cuisine 
            res+="{:<42}{:^15}{:^20}".format(df['item_name'][i],df['price'][i],df['delivery_service'][i]) + "\n"    #print the food, price and delivery availability with the space set for three column
    res+= "\nEnter the food you want to order.\n"
    res+= "Or if you are still undecided, would you like to see a sorted list of the menu?\n"
    
    return res

'''
PrintSortedMenu function
Purpose:
-to print a sorted menu list
-for printing the menu for specific cuisine based on the user command
-variable choosen_type takes the input for what kind of cuisine the user wish to sort
-the sorted menu will sort the choosen cuisine for their delierability also
'''

def PrintSortedMenu(res,df,choosen_type):
    count = 0                                                                                       #define variable count for counter
    for i in range(0,df_cpy1.shape[0]):
       if choosen_type == df_cpy1["stall"][i].lower() :                                             #compare if the choosen type matches the cuisine name 
            res+="\n<<"+ choosen_type.capitalize() + ">>\n\n"                                       #print the name of the choosen type cuisine with first letter caps
            res+="{:<42}{:^15}".format("Food","Price (RM)") + "\n"
            res+="\n[Deliverable]\n"
            a = df_cpy1["stall"][i].lower()                                                         #define a as the variable for the stall name
            b = globals()[f"range_{a}"]                                                             #define b as the variable for the range of item in the stall
            for j in range(b[0],b[1]):                                                              #the range of index for the choosen stall 
                if df['delivery_service'][j] == "yes":                                              #sort the deliverability of the food in the choosen stall
                    res+="{:<42}{:^15}".format(df['item_name'][j],df['price'][j]) + "\n"
                    count += 1                                                                      #count will increase by 1 whenever a food with delivery available detected
            if count < len(range(b[0],b[1])):                                                       #if count lesser than the length for the range of index of the choosen stall, then will start detecting the food which cannot delivered
                res+="\n[Pick up only]\n"
                for k in range(b[0],b[1]):
                    if df['delivery_service'][k] == "no":
                        res+="{:<42}{:^15}".format(df['item_name'][k],df['price'][k]) + "\n"

    return res

'''
PriceSort
Purpose:
- Rearrange the items in the big menu according to their price, for each stall
Method: For each stall, first a new dataframe is created consisting of only items within the stall.
        Sort the "price" column of the newly defined dataframe
        return the string of the newly sorted dataframe
'''
def PriceSort(res,df,price_type,l):
    index = price_type.index(l)                                                                                                 # find the index on the list for the keyword that corresponds to the token

    #low to high
    if index <= 1:                                                                                                              # keywords on the list (price_type) with index 1 and below represents Low to High
        res+= "\n"+"{:<42}{:^15}{:^30}".format("Food","Price (RM)","Delivery Service")                                          # print header
        for i in range(0,df_cpy1.shape[0]):                                                                                     # for each stall
            # determining the variables to call:
            a = df_cpy1["stall"][i].lower()                                                                                     
            b = globals()[f"range_{a}"]                                                                                         # get the range of the stall defined in build_range function
            c = globals()[f"df_{a}"] = []                                                                                       # dynamically create an empty variable

            c = df.loc[b[0]:b[1]]                                                                                               # define the new variable as a dataframe consisting of only items within the stall
            res+= "\n<<" + df_cpy1["stall"][i].capitalize() +">>\n\n"                                                           # Show the stall name
            c = c.sort_values(by="price",ignore_index=True)                                                                     # sort the "price" column of the newly defined dataframe
            for j in range(0,c.shape[0]):
                res+="{:<42}{:^15}{:^20}".format(c['item_name'][j],c['price'][j],c['delivery_service'][j]) + "\n"               # print all the newly sorted items under the stall 

    #high to low
    else:                                                                                                                       # all other keywords on the list (price_type) represents High to Low
        res+= "\n"+"{:<42}{:^15}{:^30}".format("Food","Price (RM)","Delivery Service")                                          # print header
        for i in range(0,df_cpy1.shape[0]):                                                                                     # for each stall
            # determining the variables to call:
            a = df_cpy1["stall"][i].lower()                                                                                     
            b = globals()[f"range_{a}"]                                                                                         # get the range of the stall defined in build_range function
            c = globals()[f"df_{a}"] = []                                                                                       # dynamically create an empty variable

            c = df.loc[b[0]:b[1]]                                                                                               # define the new variable as a dataframe consisting of only items within the stall
            res+= "\n<<" + df_cpy1["stall"][i].capitalize() +">>\n\n"                                                           # Show the stall name
            c = c.sort_values(by="price",ignore_index=True,ascending=False)                                                     # sort the "price" column of the newly defined dataframe
            for j in range(0,c.shape[0]):
                res+="{:<42}{:^15}{:^20}".format(c['item_name'][j],c['price'][j],c['delivery_service'][j]) + "\n"               # print all the newly sorted items under the stall
    return res

'''
PriceSubSort
Purpose:
- Rearrange the items in the small menu according to their price, for one stall only
Method: Same method as PriceSort
        First a new dataframe is created consisting of only items within the stall.
        Sort the "price" column of the newly defined dataframe
        return the string of the newly sorted dataframe
'''
def PriceSubSort(res,df,price_type,k,temp):
    index = price_type.index(k)                                                                                                 # find the index on the list for the keyword that corresponds to the token
    # determine which stall to sort
    for i in range(0,df_cpy1.shape[0]):                                                                                         
        if temp == df_cpy1["stall"][i].lower():                                                                                 # if the stall is found on the corresponding list
            # determining the variables to call:
            a = df_cpy1["stall"][i].lower()
            b = globals()[f"range_{a}"]

            df_cpy = df.loc[b[0]:b[1]]                                                                                          # define df_cpy as a dataframe consisting of only items within the stall
    #low to high
    if index <= 1:                                                                                                              # keywords on the list (price_type) with index 1 and below represents Low to High
        res+= "\n"+"{:<42}{:^15}{:^30}".format("Food","Price (RM)","Delivery Service")                                          # print header
        res+= "\n<<" + temp +">>\n\n"                                                                                           # Show the stall name
        df_cpy = df_cpy.sort_values(by="price",ignore_index=True)                                                               # sort the "price" column of the newly defined dataframe
        for i in range(0,df_cpy.shape[0]):
            res+="{:<42}{:^15}{:^20}".format(df_cpy['item_name'][i],df_cpy['price'][i],df_cpy['delivery_service'][i]) + "\n"    # print all the newly sorted items under the stall
    #high to low
    else:                                                                                                                       # all other keywords on the list (price_type) represents High to Low
        res+= "\n"+"{:<42}{:^15}{:^30}".format("Food","Price (RM)","Delivery Service")                                          # print header
        res+= "\n<<" + temp +">>\n\n"                                                                                           # Show the stall name
        df_cpy = df_cpy.sort_values(by="price",ignore_index=True,ascending=False)                                               # sort the "price" column of the newly defined dataframe
        for i in range(0,df_cpy.shape[0]):
            res+="{:<42}{:^15}{:^20}".format(df_cpy['item_name'][i],df_cpy['price'][i],df_cpy['delivery_service'][i]) + "\n"    # print all the newly sorted items under the stall
    return res

'''
Deliverable
Purpose:
- Rearrange the items in the big menu according to their delivery availability, for each stall
Method: For each stall, first print out all items that has value "yes" in the 'delivery_service' column of the df
        if number of item printed is not total item in the stall, there are items that are pickup only
        then proceed to print items that has value "no" in the 'delivery_service' column of the df
'''
def Deliverable(res,df):
    res+="{:<42}{:^15}".format("Food","Price (RM)") + "\n"                                                                      # print header
    for i in range(0,df_cpy1.shape[0]):                                                                                         # for each stall
        count = 0                                                                                                               # reset count for each stall
        # determining the variables to call:
        a = df_cpy1["stall"][i].lower()
        b = globals()[f"range_{a}"]
        
        res+="\n"+ df_cpy1["stall"][i].capitalize() + "\n"                                                                      # Show the stall name
        res+="\n[Deliverable]\n"                                                                                                # Show the catagory
        for j in range(b[0],b[1]):                                                                                              # for all items in the stall
            if df['delivery_service'][j] == "yes":                                                                              # check the 'delivery_service' column of df for yes
                res+="{:<42}{:^15}".format(df['item_name'][j],df['price'][j]) + "\n"                                            # print item name and price of items that are deliverable
                count += 1                                                                                                      # count number of item printed
        if count < len(range(b[0],b[1])):                                                                                       # check if all items in the stall has been printed
            res+="\n[Pick up only]\n"                                                                                           # Show the catagory
            for k in range(b[0],b[1]):                                                                                          # for all items in the stall
                 if df['delivery_service'][k] == "no":                                                                          # check the 'delivery_service' column of df for no
                     res+="{:<42}{:^15}".format(df['item_name'][k],df['price'][k]) + "\n"                                       # print item name and price of items that are pickup only
    return res

'''
get_food
Purpose:
- Check whether the item name given is in the database and if not, is there any item with similar name
Method: the difflib.SequenceMatcher function is used to compare the msg received with every item name in the df
        proceed to another stage if a 100% similarity is found
        show a list of suggest if one or more item in the df has a similarity ratio of 0.6 or greater with the msg
        Apologize and ask for another input if no similar match found
'''
def get_food(msg,df,res,stage,temp) :
    # Reset variables
    temp_sugg = []
    ratio = []
    flag1 = 0
    flag = 0

    # Check similarity
    for i in range(0,df.shape[0]):                                                                                              # for every item in df
        if difflib.SequenceMatcher(None, msg, df['item_name'][i].lower()).ratio() > 0.6 :                                       # if msg is 60% similar to an item in df
            if difflib.SequenceMatcher(None, msg, df['item_name'][i].lower().strip()).ratio() == 1 :                            # if msg is 100% similar to an item in df
                temp = i                                                                                                        # store index of item in variable
                res+= "How many quantity of this item would you want ?"                                                         # print question to prompt for subsequent commands
                stage = 6                                                                                                       # set the next stage
                flag = 3                                                                                                        # change flag variable to be passed back
                flag1 = 2                                                                                                       # set variable to be used in the next section
                break
            elif difflib.SequenceMatcher(None, msg, df['item_name'][i].lower()).ratio() != 1 :                                  # if msg similarity ratio is between 0.6 and 1
                temp_sugg.append(df['item_name'][i])                                                                            # append item name to a list to be shown as suggestion
                ratio.append(difflib.SequenceMatcher(None, msg, df['item_name'][i].lower()).ratio())                            # append the similarity ratio to another list
                flag1 = 1                                                                                                       # set variable to be used in the next section

    # check flag1 variable state
    # no 100% match
    if flag1 == 1:
        df_sugg = pd.DataFrame({'name': temp_sugg, 'ratio': ratio})                                                             # create new dataframe containing the similar item names and their ratio
        df_sugg.sort_values(by='ratio',ignore_index=True,inplace=True,ascending=False)                                          # sort according to similarity ratio
        res+= "\nDid You Mean:\n"
        for i in range(0,df_sugg.shape[0]):                                                                                     # list down all similar item names
            res+= df_sugg['name'][i] + "\n"

        # looking for top 3 similar items
        if df_sugg.shape[0] < 3:                                                                                                # append all item if there is less than 3 similar
            for i in range(0,df_sugg.shape[0]):
                sugg.append(df_sugg["name"][i])
        else:                                                                                                                   # append only top 3 if more than 3 similar
            for i in range(0,3):
                sugg.append(df_sugg["name"][i])
        flag = 3                                                                                                                # change flag variable to be passed back
        stage = 5                                                                                                               # set the next stage
    # if no similar detected
    elif flag1 == 0:
        res+= "Unfortunately I cannot find the food you are looking for.\nPlease try again."
        flag = 3                                                                                                                # change flag variable to be passed back
    
    return flag , res , stage , temp

'''
get_quantity
Purpose:
- Determine the quantity the user inputted and add accordingly to the item_list(shopping cart)
Method: Append the index for the number of times the user give
'''
def get_quantity(msg_list,df,res,temp,item_list):
    sugg.clear()                                                                                                                # reset the list
    
    for i in range(0,int(msg_list[0])):                                                                                         # run for the given number of times
      item_list.append(temp)

    res += "Would you like to continue shopping or would you like to proceed to checkout? "
    
    return res , item_list

'''
Print_cart function
Purpose:
-to print out the cart to the user after ordered the food and proceed to checkout
-the quantity of the food ordered,
-the name of the food ordered,
-the price of the food ordered (quantity*individual price),
-the total price after summing all the item 
'''
def Print_cart(res ,item_list, df , msg_list):
    price_list =[]                                                                                  #price_list is for storing the price of the food ordered
    price_total = 0                                                                                 #price_total is taking the total price of the order                           
    res+= "\n" + "Here is your cart.\n"                                                             #print the header for the cart                                                             
    res+= "\n" + "-"*80 + "\n"                                                                      #print the header for the cart
    res+=  "\n"+"{:^80}".format("University of Nottingham Malaysia Cafeteria\n")                    #print the header for the cart
    res+= "\n" + "-"*80                                                                             #print the header for the cart
    res+= "\n"+"{:<5}{:<42}{:^15}{:^20}".format("Qt","Food","Price (RM)","Delivery Service")+"\n"   #print the header for the cart
    my_count=[[x,item_list.count(x)] for x in set(item_list)]                                       #based on the food(this is the index of the food in excel file data) and quantity ordered, store them into a nested list
    for i in range(0,len(my_count)):
        index = my_count[i][0]                                                                      #obtain the index (the food) from the nested list                                                        
        quantity = my_count[i][1]                                                                   #obtain the quantity of the food ordered from the nested list
        price = float(quantity) * float(df['price'][index])                                         #used the index to get the price from the excel file data then mutiply the quantity ordered
        price=round(price,2)                                                                        #round up the price
        price_list.append(price)                                                                    #store the price into price_list
        res+="{:<5}{:<42}{:^15}{:^20}".format(str(quantity)+"x",df['item_name'][index],str(price),df['delivery_service'][index]) + "\n" #print the quantity, food ordered, price and deliverability with 4 length of space set

    for j in price_list:                                                                            #getting the total price using for loop
        price_total = price_total + j

    res+= "-"*80 + "\n"
    res+= "\n"+"{:<15}{:>40}".format("Total Price (RM)", str(price_total))                          #print the total price
    
    return res
    
'''
Remove_item
Purpose:
Purpose:
- Check whether the item name given is in the database and if not, is there any item with similar name
Method: the difflib.SequenceMatcher function is used to compare the msg received with every item name in the df
        proceed to another stage if a 100% similarity is found
        show a list of suggest if one or more item in the df has a similarity ratio of 0.6 or greater with the msg
        Apologize and ask for another input if no similar match found
        * Works similarly to get_food function only with different output msg*
'''    
def Remove_item(msg,df,res,stage,temp) :
    temp_sugg = []
    ratio = []
    flag1 = 0
    flag = 0
    for i in range(0,df.shape[0]):
        if difflib.SequenceMatcher(None, msg, df['item_name'][i].lower()).ratio() > 0.6 :
            if difflib.SequenceMatcher(None, msg, df['item_name'][i].lower().strip()).ratio() == 1 :
                temp = i
                res+= "How many quantity of this item do you want to remove ?"
                stage = 11
                flag = 3
                flag1 = 2
                break
            elif difflib.SequenceMatcher(None, msg, df['item_name'][i].lower()).ratio() != 1 :
                temp_sugg.append(df['item_name'][i])
                ratio.append(difflib.SequenceMatcher(None, msg, df['item_name'][i].lower()).ratio())
                flag1 = 1
    if flag1 == 1:
        df_sugg = pd.DataFrame({'name': temp_sugg, 'ratio': ratio})
        df_sugg.sort_values(by='ratio',ignore_index=True,inplace=True,ascending=False)
        res+= "\nDid You Mean:\n"
        for i in range(0,df_sugg.shape[0]):
            res+= df_sugg['name'][i] + "\n"
        if df_sugg.shape[0] < 3:
            for i in range(0,df_sugg.shape[0]):
                sugg.append(df_sugg["name"][i])
        else:
            for i in range(0,3):
                sugg.append(df_sugg["name"][i])
        flag = 3
        stage = 10
    elif flag1 == 0:
        res+= "Unfortunately I cannot find the food you are looking for.\nPlease try again."
        flag = 3
    
    return flag , res , stage , temp

'''
Final_checkout function
Purpose:
-to check the deliverability for all the food
-if all the food is able for delivery, ask the user if they want to pick up or delivery
-else if at least one of the item is unable to deliver, ask the user if they want to proceed to pick up
-else if all the item is unable to deliver, ask the user if they want to proceed to pick up
'''
def Final_checkout(res ,item_list, df , msg_list ):
    yes=[]                                                                      #variable yes is to store the item whihc is deliverable
    no=[]                                                                       #variable no is to store the item whihc is not deliverable
    for i in item_list:
        if df['delivery_service'][i].lower() == "yes":                                                      #check the deliverability of every item(food) ordered
            yes.append(i)                                                                                   #if deliverable, add the index(food) into yes[]                       
        elif df['delivery_service'][i].lower() == "no":
            no.append(i)                                                                                    #if not deliverable, add the index(food) into no[] 
    if len(item_list) == len(yes):                                                                          #if length of item_list (the food ordered) equal to length of yes, temp = 1 (all the item ordered is available for both delivery and self pick up)
        temp = 1
        res += "\nWould you like to have the item deliver or would you like to self pick up?\n"
    elif len(item_list) == len(no):                                                                         #if length of item_list (the food ordered) equal to length of no, temp = 1 (all the item ordered is only available for self pick up)
        temp = 2
        res+= "\nAll the item you selected are only available for pick up. Confirm to pick up?\n"

    elif len(item_list) > len(yes):                                                                         #if length of item_list (the food ordered) more than length of yes, temp = 1 (at least one of the item ordered isavailable for self pick up only)
        temp = 3
        res+= "\nAt least one of the item you selected is only available for pick up. Do you wish to proceed to pick up?\n"
   
    return res, temp                                                            #return res anf temp

'''
FAQ function
Purpose:
-print the frequently asked qeustion of to the user
'''
def FAQ(msg_list,res,df, msg):
    Ques_num =[]                                                                #Ques_num is the list for storing the question number                 
    faq_list = ["What is the operating hour of the chatbot?", "How long is the delivery time?" , "Are Kimchi Fried Rice deliverable?","What is the price for Nasi goreng pattaya?","How many type of cuisine are there?" , "Is there a minimum order for delivery?"]

    res += "What is the quesiton you wish to ask ? You can search the price and deliverability of the food you want here.\n"
    res +="Here are some of the frequently asked question:\n\n"

    for k in range(0,len(faq_list)):                                            #adding the question number into Ques_num
        Ques_num.append(k+1)
    j=1
    for i in faq_list :                                                         #printing the frequently asked question
        res += str(j) + "." + i + "\n\n"
        j+=1
        
    return res, Ques_num, faq_list                                              #return response, question number and the list of frequently asked question

'''
FAQ_deliver_service function
Purpose:
-to deal with the question asked in the faq question
-able to answer the deliverability of a specific food the user search for
-able to answer the duration for delivery service
-able to answer if there is minimum order for delivery service
'''
def FAQ_deliver_service(msg , msg_list , df , temp , res , option , option2 , option3 ,option5):
    flag = 0                                                        #variable to carry out error detection(invalid input)
    temp_list = []                                                  #variable to store the food the user asked for the deliverability

    for l in range(0,df.shape[0]):                                  #go through the excel file data  
        if df['item_name'][l].lower().strip() in msg.lower():
            temp_list.append(df['item_name'][l].lower().strip())    #store the food that matches the user input into temp_list

    if temp_list != []:                                             #if temp_list is not empty
        flag = 1                                                    #set flag = 1
        item = max(temp_list, key = len)                            #find the longest string in temp_list and put it into variable item
        for l in range(0,df.shape[0]):                              #go through every item in excel file data
            if item == df['item_name'][l].lower().strip():          #if item matches one of the food in excel file data
                if df['delivery_service'][l].lower().strip() == option2 :                                                   #check the deliverability of the item if it matches option2,option2 = "yes"
                    res += df['item_name'][l].strip().title() + " is available for both delivery and self pick up.\n\n"     #if matches option2, tell the user the food they looking for is able for both delivery and pick up
                elif df['delivery_service'][l].lower().strip() == option3 :                                                 #else if item not matches option2, check the deliverability of the item if it matches option3,option3 = "no"
                    res += df['item_name'][l].strip().title() + " is only available for self pick up.\n\n"                  #if matches option3, tell the user the food they looking for is oni available for pick up
                break
    
    for i in msg_list:                                              
        for m in option:
            #question for estimated delivery time
            if difflib.SequenceMatcher(None, i, m).ratio() > 0.6 :  #check if the input message matches option, option=["time", "long"], if matches, print the answer for delivery time   
                
                res += "\nThe estimated delivery time for I-Block residents will be around 10-15 mins whereas for J-Block residents will be around 15-20 mins.\n"
           
                flag = 1                                            #set flag = 1
            break
        #question for is there a minimum order
        if difflib.SequenceMatcher(None, i, option5).ratio() > 0.75 :                   #check if the input message matches option5, option5= "minimum", if matches, print the asnwer 
            res += "\nNo worries. There is no minimum order for delivery service.\n"
           
            flag = 1                                                                    #set flag = 1
            break

    if flag == 0:                                                                       #if flag equal 0, means invalid input, ask the user to enter the question again
        res+= "Sorry, I don't understand your question. Can you please try again?\n"

    return res


'''
FAQ_price function
Purpose:
-to deal with the question asked in the faq question
-able to answer the price of a specific food the user search for
'''
def FAQ_price(msg , msg_list , df , res ):
    flag = 0                                                                            #variable to carry out error detection(invalid input)
    temp_list = []                                                                      #variable to store the food the user asked for the price

    for l in range(0,df.shape[0]):                                                      #go through the excel file data  
        if df['item_name'][l].lower().strip() in msg.lower():
            temp_list.append(df['item_name'][l].lower().strip())                        #store the food that matches the user input into temp_list

    if temp_list != []:                                                                 #if temp_list is not empty
        flag = 1                                                                        #set flag = 1
        item = max(temp_list, key = len)                                                #find the longest string in temp_list and put it into variable item
        for l in range(0,df.shape[0]):                                                  #go through every item in excel file data
            if item == df['item_name'][l].lower().strip():                              #if item matches one of the food in excel file data
                res += "The price for " + df['item_name'][l].strip().title() + " is RM " + str(df['price'][l])      #print the price for the matches food
               
                break
            
    if flag == 0:                                                                       #if flag equal 0, means invalid input, ask the user to enter the question again
        res+= "Sorry, I don't understand your question. Can you please try again?\n"
        
    return res

def chatbot_response(msg,df,stage,temp,item_list,faq_Ques):
    w = 1                                                                                                       # variable to set while loop to vbe True
    build_range(df)                                                                                             # function to define index range of each stall
    res = ""
    
    while w:

        # process message
        msg = msg.lower()
        msg_list = msg.split()

        # Global Commands for back/undo and quit
        back = ["back", "undo"]                                                                                 # back function keywords
        for i in msg_list:
            for b in back:                                                                                      # check 'back' keywords
                if difflib.SequenceMatcher(None, i, b).ratio() > 0.9 :
                    temp = "clear"                                                                              # pass to GUI to clear chatlog
                    if stage == 2 or stage == 13 or stage == 15 or stage == 17:                                 # reset to main menu
                        item_list.clear()                                                                       # clear shopping cart
                        stage = 0                                                                               # set next stage
                        w = 1                                                                                   # set while loop True
                    elif stage == 1 :                                                                           # reset to main menu
                        stage = 0                                                                               # set next stage
                        w = 1                                                                                   # set while loop True   
                    else:                                                                                       # bring back to ordering menu
                        # manipulate input to enter ordering menu
                        msg ="order"
                        msg = msg.lower()
                        msg_list = msg.split()
                        
                        stage = 1                                                                               # set next stage
                        w = 1                                                                                   # set while loop True

                elif i == "quit" or i == "exit":                                                                # exit function keywords
                    stage = 14                                                                                  # set next stage
                    w = 0                                                                                       # set while loop False

        # Main Menu (skip on 1st run)
        if stage == 0 :
            res+= "[Main Menu]\nHow can I help you?"
            stage = 1
            w = 0

        # take input from Main Menu
        elif stage == 1:
            flag = 0
            order = ["order","tapao","food","browse","find","look for","menu"]                                  # order function keywords
            faq = "faq"                                                                                         # faq function keywords
            for i in msg_list:
                for j in order:
                    if difflib.SequenceMatcher(None, i, j).ratio() > 0.7 :                                      # if order function keywords match
                        res = PrintMenu(res,df)                                                                 # function to print menu
                        stage = 2                                                                               # set next stage
                        flag = 1                                                                                # set variable to confirm successful detection
                        break
                    elif difflib.SequenceMatcher(None, i, faq).ratio() > 0.7 :                                  # if faq function keywords match
                        res, Ques_num, faq_list = FAQ(msg_list,res,df, msg)                                     # function to print faq menu
                        temp = Ques_num                                                                         # list of number corresponding to faq questions
                        faq_Ques = faq_list                                                                     # list of possible faq questions
                        stage = 15                                                                              # set next stage
                        flag = 1                                                                                # set variable to confirm successful detection
                        break
                if flag == 1:                                                                                   # stop detecting
                    break
            if flag != 1:                                                                                       # if no valid input is detected
                res+= "Sorry I cannot understand this command, please try again."
                stage = 1                                                                                       # set to loop back to same stage
        
            w = 0

        # take input from order menu: sort or get food
        elif stage == 2:
            flag = 0
            cuisine = "cuisine"                                                                                 # sort by cuisine keywords
            price = "price"                                                                                     # sort by price keywords
            price_type = ("l","low","h","high")                                                                 # price sorting method keywords
            deliver = "delivery"                                                                                # sort by delivery keywords

            for i in msg_list:
                choosen_type=""
                for k in range(0,df_cpy1.shape[0]):
                    if difflib.SequenceMatcher(None, i, df_cpy1["stall"][k].lower()).ratio() > 0.7 :            # detect which stall/cuisine to sort by
                        choosen_type = df_cpy1["stall"][k].lower()
                        res = PrintSortedMenu(res,df,choosen_type)                                              # function to print menu for only one stall/cuisine
                        flag = 3                                                                                # set variable to what time of detection
                        temp = choosen_type                                                                     # save stall/cuisine type to a variable
                        stage = 4                                                                               # set next stage
                        break
                    
                if difflib.SequenceMatcher(None, i, cuisine).ratio() > 0.7 :                                    # user ask to sort by cuisine without providing which
                    res+= "Please choose the cuisine you would like to sort.\n\n"
                    flag = 3                                                                                    # set variable to what type of detection
                    break
                elif difflib.SequenceMatcher(None, i, price).ratio() > 0.7 :                                    # user ask to sort by price
                    flag = 2                                                                                    # set variable to what type of detection
                elif difflib.SequenceMatcher(None, i, deliver).ratio() > 0.7 :                                  # user ask to sort by deliverability
                    res = Deliverable(res,df)                                                                   # function to print menu sorted by delivery
                    flag = 3
                    stage = 4
                    break
                if flag == 2:                                                                                   # check if user provided price sort method after price keyword
                    for l in price_type:
                        if difflib.SequenceMatcher(None, i, l).ratio() > 0.7 :
                            res = PriceSort(res,df,price_type,l)                                                # function to sort menu by price
                            flag = 3
                            stage = 5
                            break
            # msg_list end
            if flag == 0:
                flag , res , stage , temp = get_food(msg,df,res,stage,temp)                                     # check whether user input is food
                if flag == 0:                                                                                   # Invalid Input
                    res+= "Sorry I cannot understand this command, please try again."
            elif flag == 2:                                                                                     # user wants to sort by price without providing method
                res+= "Would you like to sort from low to high or high to low?"
                stage = 3
            w = 0                                                                                               # terminate while loop by default for this stage

        # if user wants to sort by price without providing method
        elif stage == 3:
            flag = 0
            for i in msg_list:
                price_type = ("l","low","h","high")
                for k in price_type:
                    if difflib.SequenceMatcher(None, i, k).ratio() > 0.7 :                                      # if sorting method is detected
                        res = PriceSort(res,df,price_type,k)                                                    # function to sort menu by price
                        flag = 1
                        break
                if flag == 1:                                                                                   # a valid input is found
                    break
            if flag == 0:                                                                                       # no valid input found
                res+= "Sorry I cannot understand this command, please try again.\n"
                res+= "Would you like to sort from low to high or high to low?"
            w = 0                                                                                               # terminate while loop by default for this stage

        # user looking at menu sorted by cuisine/stall
        # possible input : sort or order food
        elif stage == 4:
            flag = 0
            for i in msg_list:
                price_type = ("l","low","h","high")
                for k in price_type:
                    if difflib.SequenceMatcher(None, i, k).ratio() > 0.7 :                                      # detect that user wants to sort menu
                        res = PriceSubSort(res,df,price_type,k,temp)                                            # function to sort menu for one cuisine/stall only
                        flag = 1
                        break
                if flag == 1:                                                                                   # a valid input is found
                    break
            if flag == 0:                                                                                       # check to see if user is trying to order food
                sugg = []
                flag , res , stage , temp  = get_food(msg,df,res,stage,temp)                                    # food ordering function
            w = 0                                                                                               # terminate while loop by default for this stage

        # look for food item as input
        elif stage == 5:
            sugg = []
            flag , res , stage , temp  = get_food(msg,df,res,stage,temp)                                        # food ordering function
            w = 0                                                                                               # terminate while loop by default for this stage

        # ask for quantity after detecting food
        elif stage == 6:
            for i in msg_list:
                if i.isnumeric() == True :                                                                      # check if input is a number
                    res , item_list = get_quantity(msg_list,df,res,temp,item_list)                              # function to detect quantity and add to cart
                    stage = 7                                                                                   # set next stage
                    w = 0                                                                                       # terminate while loop
                else:                                                                                           # error if input not a number
                    res+= "Sorry, I do not recognize this input, please input again.\n"
                    res+= "How many of the quantity of the item would you want?\n"
                    stage = 6                                                                                   # set to repeat this stage
                    w = 0                                                                                       # terminate while loop
                    break
        # added an item to cart, ask to continue shopping or proceed to checkout
        elif stage == 7:
            flag = 0
            option=["add", "continue", "shopping" , "another"]                                                  # keywords for continuing shopping
            option1=["checkout", "cart" , "done", "finish", "proceed"]                                          # keywords for done and proceed to checkout
            for i in msg_list:
                for j in option:
                    if difflib.SequenceMatcher(None, i, j).ratio() > 0.7 :                                      # detected keywords for continuing shopping
                        stage = 1                                                                               # proceed back to print ordering menu
                        flag = 1
                        w = 1                                                                                   # set while loop True
                        msg = "order"                                                                           # change msg to enter ordering menu
                for k in option1:
                    if difflib.SequenceMatcher(None, i, k).ratio() > 0.7 :                                      # detected keywords for for done and proceed to checkout
                        stage = 8                                                                               # set next stage
                        flag = 1
                        w = 1                                                                                   # set while loop True

            if flag == 0 :                                                                                      # if no valid input detected
                res+= "Sorry, I do not recognize this input, please input again.\n"
                res+="Would you like to  continue shopping or proceed to checkout\n"
                stage = 7                                                                                       # set to repeat detection
                w = 0                                                                                           # terminate while loop

        # print content of shopping cart        
        elif stage == 8:
            res = Print_cart(res ,item_list, df , msg_list)                                                     # function to print cart
            res+= "\nIs the item in your cart correct?\n"
            res+= "Would you like to add more, remove any item or confirm your order?\n"

            stage = 9                                                                                           # set next stage
            w = 0

        # commands after looking at cart
        elif stage == 9:
            flag = 0
            option = ["add", "continue", "shopping" , "another"]                                                # keywords for continuiong shopping
            option1 = ["remove", "delete", "cancel"]                                                            # keywords for removing item from cart
            option2 = ["confirm", "order" , "done", "finish"]                                                   # keywords to proceed to checkout
            for i in msg_list:
                for j in option:
                    if difflib.SequenceMatcher(None, i, j).ratio() > 0.7 :                                      # detected keywords for continuiong shopping
                        stage = 1                                                                               # return to ordering menu
                        flag = 1
                        w = 1                                                                                   # set while loop True
                        msg = "order"
                        break
                for k in option1:
                    if difflib.SequenceMatcher(None, i, k).ratio() > 0.7 :                                      # detected keywords for removing item from cart
                        if len(item_list) != 0 :                                                                # if cart not empty
                            res+= "Which is the item you would like to remove?\n"
                            stage = 10                                                                          # set next stage
                            flag = 1
                            w = 0
                            break
                        else :                                                                                  # error if cart is already empty
                            res+= "Your cart is empty.\n"
                            res = Print_cart(res ,item_list, df , msg_list)                                     # print cart again
                            stage = 9                                                                           # repeat current stage
                            flag = 1
                            w = 0
                            break
                if flag == 1:
                    break
                for l in option2:
                    if difflib.SequenceMatcher(None, i, l).ratio() > 0.7:                                       # detected keywords to proceed to checkout
                        res = Print_cart(res ,item_list, df , msg_list)                                         # print shopping cart
                        res, temp  = Final_checkout(res ,item_list, df , msg_list )                             # function to detect content of cart before checkout
                        stage = 12                                                                              # set next stage
                        flag = 1
                        w = 0
                        break
            if flag == 0 :                                                                                      # no valid input detected
                res+= "Sorry, I do not recognize this input, please input again.\n"
                res+="Would you like to add more, remove any item or confirm your order?\n"
                stage = 9                                                                                       # repeat stage
                w = 0

        # detect which food to remove    
        elif stage == 10:
            flag , res , stage , temp  = Remove_item(msg,df,res,stage,temp)
            w = 0

        # detect quantity of item to delete
        elif stage == 11 :
            flag = 0
            if msg.isnumeric() == True :                                                                        # check if input is number
                my_count=[[x,item_list.count(x)] for x in set(item_list)]                                       # check quantity of items in cart
                for i in range(0,len(my_count)):
                    index = my_count[i][0]
                    if temp == index:
                        flag = 1
                        if int(msg) <= my_count[i][1]:                                                          # check if item to be remove is less than or equal to items in cart
                            for i in range(0,int(msg)):                                                         # use for loop to remove the exact number of item
                                item_list.remove(temp)

                            res += "Your item has been deleted"
                            stage = 8                                                                           # move back to print shopping cart
                            w = 1
                            break
                        else:                                                                                   # if user is trying to remove more than there is in cart
                            res+= "You are removing more items than in the cart. Please try again."
                            stage = 11                                                                          # repeat stage
                            w = 0
                            break
                    if flag == 0:
                        w = 0
                if flag == 0:                                                                                   # user trying to delete item not found in cart
                    res+= "Item not in cart. Please try again"
                    stage = 10                                                                                  # try to detect item again
                    w = 0
                    
            else:                                                                                               # invalid input
                res+= "Sorry, I do not recognize this input, please input again.\n"
                res+= "How many of the quantity of the item do you want to remove?\n"
                stage = 11                                                                                      # repeat stage
                w = 0

        elif stage == 12:                                                                           #stage 12 is for confirming order after the user checkout
            flag = 0
            option = ["deliver", "delivery","delivered"]                                            #keywords for if the user choose delivery service
            option1 = ["pick", "self", "proceed" , "confirm"]                                       #keywords for if the user choose self-pick up
            option2 = "yes"                                                                         #keywords for if the user say yes to proceed to self pick up
            option3 = "no"                                                                          #keywords for if the user say no to proceed to self pick up 
            for i in msg_list:
                for j in option:
                    if difflib.SequenceMatcher(None, i, j).ratio() > 0.7 :                           #if option matches msg_list, means user choose to delivery service
                        if temp == 1:                                                                #temp == 1 is from Final_checkout function
                            res = Print_cart(res ,item_list, df , msg_list)                          #print the cart to the user
                            res += "\n\nThank you for ordering with us! Your order is on the way.\n" #reply to the user after they confirm for delivery
                            flag = 1                                                                 #set flag = 1
                            w = 0                                                                    #variable to control while loop
                            res+= "Would you like to return to the main menu?\n"
                            stage = 13                                                               #go to stage 13
                            break

                for k in option1:                                                                   
                    #if option matches msg_list, means user confirm for self-pick up
                    if difflib.SequenceMatcher(None, i, k).ratio() > 0.7 or difflib.SequenceMatcher(None, i, option2).ratio() > 0.7  :
                        if temp in range(1,4):                                                                      #temp == 1 ,2 or 3 is from Final_checkout function
                            res = Print_cart(res ,item_list, df , msg_list)                                         #print the cart to the user
                            res += "\n\nThank you for ordering with us! Your order is preparing to be pick up.\n"   #reply to the user after they confirm for self pick up
                            flag = 1                                                                                #set flag = 1
                            w = 0                                                                                   #variable to control while loop
                            res+= "Would you like to return to the main menu?\n"
                            stage = 13                                                                              #go to stage 13
                            break

                if difflib.SequenceMatcher(None, i, option3).ratio() > 0.7 :                                        #if msg matches option3
                    stage = 8                                                                                       #stage set to 8
                    flag = 1                                                                                        #set flag = 1                                                                   
                    w = 1                                                                                           #variable to control while loop
                elif flag == 1:
                    break
   
            if flag == 0:                                                                                           #if flag equal 0, means invalid input, ask the user to enter the question again
                res+= "Sorry, I do not recognize this input, please input again.\n\n"
                stage = 12                                                                                          # set stage to 12
                w = 0
      
        elif stage == 13:                                                                           #stage = 13 is for asking the user if they want to go back to main menu after checkout and confirm order 
            option = ["main", "menu", "return", "yes"]                                              #keywords for want to go back to main menu
            option1 = "no"                                                                          #keywords for do not want to go back to main menu
            for i in msg_list:
                for j in option:
                    if difflib.SequenceMatcher(None, i, j).ratio() > 0.7 :                          #if option in msg_list  
                        item_list.clear()                                                           #clear the item_list, item list is the food ordered during the last order
                        temp = "clear"                                                              #clear the chatlog
                        stage = 0                                                                   #set the stage to 0, the starting of the program
                        w = 1                                                                       #variable to control while loop
                        break
                if difflib.SequenceMatcher(None, i, option1).ratio() > 0.7 :                        #if option1 in msg_list, go to stage = 14
                    stage = 14
                    w = 0

        elif stage == 15:                                                                           #stage = 15 is for testing faq question
            flag = 0                                                                                #variable for invalid input
            flag1 = 0                                                                               #variable for testing question how many type of cuisine are there in FAQ section 
            flag2 = 0
            option = ["time","long"]                                                                #keywords for question how long is delivery time
            option1 = ["deliverable", "delivery","deliver","delivered","self" , "pick" , "up"]      #keywords for question about delivery service            
            option2 = "yes"
            option3 = "no"                                                                          
            option4 = ["operating" ,"hour"]                                                         #keywords for question about operating hour
            option5 = "minimum"                                                                     #keywords for question about minimum order for delivery service                                                       
            option6 = "type"                                                                        #keywords for question about how many type of cuisine are there
            option7 = "cuisine"                                                                     #keywords for question about how many type of cuisine are there 
            option8 = ["price", "cost"]                                                             #keywords for question about price of the food
           
            for i in msg_list:
               
                for k in option1:
                    if difflib.SequenceMatcher(None, i, k).ratio() > 0.9 :                          #if option1 in msg_list, means matches words such as deliver/pick up, then go into FAQ_deliver_service function
                        
                        res = FAQ_deliver_service(msg , msg_list , df , temp , res , option , option2 , option3 ,option5)
                        w = 0                                                                       #variable to control while loop
                        flag = 1                                                                    #set flag = 1
                        flag2 = 1                                                                   #set flag2 = 1
                        break
                       
                        
                for n in option4 :
                    if difflib.SequenceMatcher(None, i, n).ratio() > 0.75 :                         #if option4 in msg_list , option4= ["operating" ,"hour"] 
                        res += "\nThe operating hour for the chatbot will be 9am to 6pm.\n"         
                        w = 0                                                                       #variable to control while loop
                        flag = 1                                                                    #set flag = 1
                        flag2 = 1                                                                   #set flag2 = 1
                    break
                
                for o in option8:
                    if difflib.SequenceMatcher(None, i, o).ratio() > 0.9:                           #if option8 in msg_list, go into FAQ_price function
                        
                        res = FAQ_price(msg , msg_list , df , res )
                        w = 0                                                                       #variable to control while loop
                        flag = 1                                                                    #set flag = 1
                        flag2 = 1                                                                   #set flag2 = 1
                        break
            
            
                if difflib.SequenceMatcher(None, i, option6 ).ratio() > 0.75 :                      #if option6 in msg_list, option6="type", set flag1 =1
                    
                    flag1 = 1
                    flag = 1                                                                        #set flag = 1
                    w = 0                                                                           #variable to control while loop
                   
              
                if difflib.SequenceMatcher(None, i, option7 ).ratio() > 0.75:                       #if option7 in msg_list, option6="cuisine",      
                    
                    if flag1 == 1:                                                                  #if flag1 = 1, means the question have the word "type", which means input msg have both the word "type" and "cuisine"
                        num_stall = df_cpy1.shape[0]
                        res += "\nThere are "+ str(num_stall) +" type of cuisine available: "       #use for loop to print out the type of cuisine available
                        for i in range(0,num_stall):
                            if i == (num_stall-1):
                                res+= "and " + df_cpy1["stall"][i].capitalize()
                            elif i == (num_stall-2):
                                res+= df_cpy1["stall"][i].capitalize() + " "
                            else:
                                res += df_cpy1["stall"][i].capitalize() + ", "
                        w = 0                                                                       #variable to control while loop
                        flag = 1                                                                    #set flag = 1
                    break
                
                for p in temp:                                                                      #temp is a list of [1,2,3,4,5,6....] depending on how many quesiton are there in the frequently asked question                                                                     
                    
                    if i == str(p):                                                                 #if msg_list matches element in list temp
                        stage = 17                                                                  #set the stage to 17
                        w = 1                                                                       #variable to control while loop
                        flag = 1                                                                    #set flag = 1
                        flag2 = 1                                                                   #set flag2 = 1
                    
              
                if flag2 == 1:                                                                      #if flag2 = 1 then break to make sure the output answer only run once
                    break

            if flag == 0:                                                                           #if flag equal 0, means invalid input, ask the user to enter the question again
                res += "Sorry, I could not answer this question. Try ask another question.\n\n"
                stage = 15                                                                          #if invalid input go to stage 15 again
                w = 0                                                                               #variable to control while loop     

        elif stage == 17:                                                                           #stage = 17 is for when user enter 1, 2, 3... , the program will detect it as the coresponding ques in the faq question list
            
            for j in range(0,len(temp)):                                                            #use for loop based on how many quesiton are there in the faq section
                if i == str(temp[j]):                                                               #if the msg matches the element in list temp
                    stage = 15                                                                      #go to stage 15
                    w = 1                                                                           #variable to control while loop
                    msg = faq_Ques[j]                                                               #msg equal to the coresponding quesiton in the faq section, for example, if msg equal to 1, then the next msg the program detect will be the first quesiton in the faq section 
             

    return res , stage , temp , item_list, faq_Ques


    
