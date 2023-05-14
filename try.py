string = "%0A%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20Kraków%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20%20%20%20%20Warszawa%0A%20%20%20%20%20%20%20%20%20%20%20%20%0A%20%20%20%20%20%20%20%20"
# Remove leading and trailing whitespace
string = string.strip()

# Split the string by '%0A%20' to create an array
array = string.split('%0A%20')

# Remove the first element of the array since it's empty
array.pop(0)

# Replace '%20' with a space in all elements of the array
array = [element.replace('%20', ' ').strip() for element in array]

# Remove any empty elements and consecutive spaces
array = [element for element in array if element and not element.isspace()]

print(array)