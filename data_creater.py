import json

#this python file is for appending new entries like classes, races, items etc


folder_names = {"class" : "classes", "item" : "items", "race" : "races", "spell" : "spells", "background" : "backgrounds"}


def main():
    entry_type = input("pick a template type: ")
    
    
    
    with open(f"templates/{entry_type}_template.json", "r") as f:
        entry_template = json.load(f)
        f.close()
    
    
    
    if entry_type == "item":
        item_type = input("pick a item type: ")
        
        entry_template["equipment_type"] == item_type
        
        if item_type != "":
            with open(f"templates/{item_type}_template.json", "r") as f:
                entry_template["equipment_type_details"] = json.load(f)
                f.close()
    
    filled_dict = filling_dict(entry_template)
    
    with open(f"{folder_names[entry_type]}/{input('enter name for file: ')}.json", "x") as f:
        f.write(json.dumps(filled_dict, indent=4))
        f.close()
    
    
    print("entry created successfully")
    if input("would you like to make another entry? (y/n): ") == "y":
        main()


def filling_dict(dictionary):
    for data_point in dictionary:
        
        if data_point == "equipment_type":
            continue
        
        elif type(dictionary[data_point]) == int:
            dictionary[data_point] = int(input(f"{data_point} : "))
        
        elif type(dictionary[data_point]) == str:
            dictionary[data_point] = input(f"{data_point} : ")
        
        elif type(dictionary[data_point]) == float:
            dictionary[data_point] = float(input(f"{data_point} : "))
        
        elif type(dictionary[data_point]) == bool:
            dictionary[data_point] = bool(input(f"{data_point} : "))
        
        elif type(dictionary[data_point]) == list:
            filling = True
            while filling:
                list_point = input(f"{data_point} : ")
                if list_point.isdigit():
                    dictionary[data_point].append(int(list_point))
                
                elif list_point.isdecimal:
                    dictionary[data_point].append(float(list_point))
                
                else:
                    dictionary[data_point].append(list_point)
        
        elif type(dictionary[data_point]) == dict:
            dictionary[data_point] = filling_dict(dictionary[data_point])
        
    
    return dictionary
    



if __name__ == '__main__':
    main()