
"""
commannd line
- takes command in a loop
- Ctrl C
- exit functions in future

input
- binary file

output
- dump in hex format


commands
- operations on the input file


"""
import sys

LINE_LIMIT = 80


def read_file(filename: str):
    try:
        with open(filename, "rb") as file:
            data = file.read()
        return True, data
    except FileNotFoundError as e:
        print(e)
    except Exception as e:
        print(e)
    return False, None


def convert_data(binary_slice, output_type):
    match output_type:
        case "oct":
            # convert up to target bytese
            converted_data = []
            for byte in binary_slice:
                try:
                    converted_byte = oct(byte)
                    converted_data.append(converted_byte)
                except UnicodeDecodeError as e:
                    continue

            return "".join(converted_data)
        case "text":
            converted_data = []
            for byte in binary_slice:
                converted_byte = str(byte)
                converted_data.append(converted_byte)

            return "".join(converted_data)
        case _:
            return binary_slice.hex()


def dump_file(command_tokens: list[str], binary_data: bytearray):
    if len(command_tokens) > 1:
        output_type = command_tokens[1]
    else:
        output_type = "hex"

    # handle configurable max bytes
    if len(command_tokens) > 2:
        converted_byte_length = int(command_tokens[2])
    else:
        converted_byte_length = len(binary_data)

    # convert up to target output up to limit first 
    converted_data = convert_data(binary_slice=binary_data[:converted_byte_length], output_type=output_type)

    # print 80 chars until end of data
    index = 0
    while index < converted_byte_length:
        converted_slice = converted_data[index:index + LINE_LIMIT]
        # convert here
        print(converted_slice)
        index += LINE_LIMIT


def solution():
    args = sys.argv

    filename = args[1]
    successful_read, binary_data = read_file(filename=filename)
    if not successful_read:
        exit()

    # handel commands for a successful read
    while True:
        print("Please enter a command --> ", end="")
        command = input()
        command_tokens = command.strip().lower().split(" ")
        action = command_tokens[0]

        match action:
            case "quit":
                exit()
            case "dump":
                dump_file(command_tokens, binary_data)
            case _:
                print(f"Unknown command {command}")


"""
input
    starts program
    default output is hex

    "dump <format>"
        - format can be hex, text, oct

loop commands

output
    
    indicdate the type of output
"""

if __name__ == "__main__":
    solution()

