#holds all the commands accesable by the terminal
import randomCharacterGenerator

def dnd_help():
    instructions = {"help" : "returns this list", "random" : "creates a random character sheet"}
    command_spacing = "          "
    instruction_spacing = "                                                                  "
    print('\n+------------+--------------------------------------------------------------------+')
    for command in list(instructions.keys()):
        print(f'| {command}{command_spacing[len(command)-1:len(command_spacing)-1]} | {instructions[command]}{instruction_spacing[len(instructions[command])-1:len(instruction_spacing)-1]} |')
    print('+------------+--------------------------------------------------------------------+\n')


def format_background_data(background_data : dict):
    string = '\n'
    for entry in background_data.keys():
        if entry == "background_equipment":
            string += "choose between A or B:\n"
            string += f"A: {entry} : {background_data[entry]}\n"
        elif entry == "wealth":
            string += f"B: {entry} : {background_data[entry]}\n"
        else:
            string += f"{entry} : {background_data[entry]}\n"
    return string


