
def edit_block(config_data):

    temp_filename = "temp_config.txt"
    with open(temp_filename, "w") as temp_file:
        temp_file.write(config_data)


    # editor_command = ["code", "--wait", temp_filename]
    # editor_command = ["vi", temp_filename]
    editor_command = ["vim", temp_filename]

    subprocess.run(editor_command)

    # Read the modified config data from the temporary file

    with open(temp_filename, "r") as temp_file:
        modified_block = temp_file.read()

    # Remove the temporary file
    os.remove(temp_filename)

    return modified_block