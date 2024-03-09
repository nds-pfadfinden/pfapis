
def split_address(address):
    """ Konvert a string of full address into two parts.
    Thh String is splitted by first position a number is founded.
    Example:

    address = "Donnerschweer Str. 26a"

    street, number = split_address(address) 
    #street: Donnerschweer Str.
    #number: 26a

    """
 
    split_index = None
    for index,letter in enumerate(address):
        if letter.isnumeric():
            split_index = index - 1
 
    street=address[0:split_index].strip()
    number=address[split_index:].strip()
 
    return street, number