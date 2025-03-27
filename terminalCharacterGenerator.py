#prompts through the terminal to make non-random character

import pyfiglet
import json
import os
import random
import math

from util import *



commands = {"help" : dnd_help}

backgrounds = {}
classes = {}
races = {}
items = {}
spells = {}
categories = {"backgrounds" : backgrounds, "classes" : classes, "races" : races, "items" : items, "spells" : spells}
categorie_entry_names = {"backgrounds" : "background_name", "classes" : "class_name", "races" : "race_name", "items" : "item_name", "spells" : "spell_name"}


def main():
    for category in categories.keys():
        for category_file in os.scandir(str("data/" + category)):
            with open(category_file, "r") as f:
                categories[category][json.load(f)[categorie_entry_names[category]]] = category_file #this will make it so its "'file'_name" : "file_path" file_name being the name of the class/item/etc in the file
                f.close()
    
    print(pyfiglet.figlet_format("DnD  5e  C. S. G."))
    print('type "help" for list of commands')
    print('type "random" for a random chacter')
    print('type "start" to begin making a character\n')
    
    running = True
    
    while running:
        
        called = input(":")
        
        
        if called == '':
            continue
        elif called == "start":
            character_creator()
        elif called in commands:
            commands[called]()
        else:
            print(f'\nthe command {called} does not exist\ntype "help" for a full list of commands\n')
        
    


def character_creator(checkpoint = "start"):
    creating = True
    while creating:
        if checkpoint == "start":
            
            with open("data/defaults/character_sheet.json", "r") as template:
                character_sheet = json.load(template)
                template.close()
            
            checkpoint = "picking_class"
        
        if checkpoint == "picking_class":
            print("\nchoose a starting class from the following: ")
            print(list(classes.keys()))
            picked_class = input("\n: ")
            
            if picked_class == "back":
                if input("\nare you sure you wanna stop creating the character? (Y/N): ") in ["Y","y"]:
                    checkpoint = creating == False
            
            elif picked_class in list(classes.keys()):
                character_sheet["class"] = picked_class #TODO #ADD CLASS DATA TO SHEET
                
                checkpoint = "picking_race"
            
            else:
                print(f"\nthere is no {picked_class} class, you might have misstyped\n")
                continue
        
        
        if checkpoint == "picking_race":
            print("\nchoose a race from the following: ")
            print(list(races.keys()))
            
            picked_race = input("\n: ")
            
            if picked_race == "back":
                checkpoint = "picking_class"
            
            elif picked_race in list(races.keys()):
                character_sheet["race"] = picked_race #TODO #ADD RACE DATA TO SHEET
                
                checkpoint = "picking_background"
            
            else:
                print(f"\nthere is no {picked_race} race, you might have misstyped\n")
                continue
        
        
        if checkpoint == "picking_background":
            print("\nchoose a background from the following: ")
            print(list(backgrounds.keys()))
            picked_background = input("\n:")
            
            if picked_background == "back":
                checkpoint = "picking_class"
            
            elif picked_background in list(backgrounds.keys()):
                with open(backgrounds[picked_background], "r") as f:
                    background_data = json.load(f)
                    f.close()
                
                print(format_background_data(background_data))
                
                if input(f"are you sure you want the {picked_background} background? (Y/N): ") in ["Y", "y"]:
                    
                    character_sheet["background"] = picked_background
                    
                    #TODO pick background abilities
                    
                    print("")
                    
                    if background_data["background_feat"] not in character_sheet["feats"]:
                        character_sheet["feats"].append(background_data["background_feat"])
                    else:
                        print("background feat already on character") #TODO failsafe so you can go back and pick a new feat if possible
                    
                    
                    
                    if background_data["background_skill_proficiencies"][0] not in character_sheet["skill_proficiencies"]:
                        character_sheet["skill_proficiencies"].append(background_data["background_feat"][0])
                    else:
                        print("background skill proficiency already on character") #TODO failsafe so you can go back and pick a new skill prof if possible
                    
                    if background_data["background_skill_proficiencies"][1] not in character_sheet["skill_proficiencies"]:
                        character_sheet["skill_proficiencies"].append(background_data["background_feat"][1])
                    else:
                        print("background skill proficiency already on character") #TODO failsafe so you can go back and pick a new skill prof if possible
                    
                    
                    
                    if background_data["background_tool_proficiencies"][0] not in character_sheet["tool_proficiencies"]:
                        character_sheet["tool_proficiencies"].append(background_data["background_tool_proficiencies"][0])
                    else:
                        print("background tool proficiency already on character") #TODO failsafe so you can go back and pick a new tool prof if possible
                    
                    
                    picked_background_equipment = False
                    while picked_background_equipment == False:
                        choice = input(f"A or B? (A/B): ")
                        if choice == "A" or choice == "a":
                            picked_background_equipment = True
                            
                            for background_equipment in list(background_data["background_equipment"].keys()):
                                if background_equipment in list(background_data["wealth"].keys()):
                                    character_sheet["wealth"][background_equipment] += background_data["wealth"][background_equipment]
                                    
                                if background_equipment not in list(character_sheet["equipment"].keys()):
                                    character_sheet["equipment"][background_equipment] = background_data["background_equipment"][background_equipment]
                                else:
                                    character_sheet["equipment"][background_equipment] += background_data["background_equipment"][background_equipment]
                            
                            
                        
                        elif choice == "B" or choice == "b":
                            picked_background_equipment = True
                            
                            for coin in list(background_data["wealth"].keys()):
                                character_sheet["wealth"][coin] += background_data["wealth"][coin]
                            
                        
                        else:
                            print(f"{choice} is not a valid option")
                    
                
                
                
                
                
                checkpoint = "picking_ability_scores"
            
            else:
                print(f"\nthere is no {picked_background} background, you might have misstyped\n")
                continue
        
        
        if checkpoint == "picking_ability_scores":
            
            print('''\npick method for rolling ability scores: 
m = manually enter rolls,
r = roll; 4d6 remove one, for each ability,
d20 = roll; 1d20, for each ability
pb = point buy''')
            
            
            ability_roll_method = input("\n: ")
            
            
            
            
            if ability_roll_method in ["m", "M"]:
                for ability in character_sheet["ability_scores"]:
                    picked_ability_stat = False
                    while picked_ability_stat == False:
                        choice = input(f"{ability} : ")
                        if -1 < choice < 21:
                            character_sheet["ability_scores"][ability] += choice
            
            
            elif ability_roll_method in ["r", "R"]:
                pass
            
            elif ability_roll_method in ["d20", "D20"]:
                pass
            
            elif ability_roll_method in ["pb", "Pb", "pB", "PB"]:
                pass
            
            print(f"\nyou have 3 ability points from your background to split between the following abilities: {background_data['background_abilities'][0]}, {background_data['background_abilities'][1]}, {background_data['background_abilities'][2]}")
            character_sheet["ability_scores"][input("point 1: ")] += 1
            character_sheet["ability_scores"][input("point 2: ")] += 1
            character_sheet["ability_scores"][input("point 3: ")] += 1
            
            print("")
            checkpoint = "done"
            
        
        
        if checkpoint == "done":
            print("\n\n\n")
            for key in list(character_sheet.keys()):
                print(key, " : ", character_sheet[key])
            creating = False
        
        

#character creation order:
"""
*-class
*-multiclasses
origin:
    *-species
    *-background
    *-feats
    *-languages
*-profeciencies:
    *-skill profeciencies
    *-tool profeciencies
    --saving throw profeciencies
    *-experties?
--profeciency bonus
*-ability scores
details:
    --class features
    x-saving throws
    x-skills
    --passive perception
    --hit points
    --hit die
    --ac
    --speed
    --initiative
    *-equipment:
    *-spells
    --spell slots
    --attacks
    **description:
        *-alignment
        gender?
        bonds?
        etc
--spell attack bonus
--spell save dc
"""

#things not in creation:
"""


equip...:
    attuned items
    

"""






if __name__ == '__main__':
    main()