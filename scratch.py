print("Please enter a multi-line string:")
multi_line_string = ""
    # line = input()
line = """Modify the following code based on the request:\n\n```python\n{user_code}\n```Modification Request: {modification_request}"""
if line:
    multi_line_string += line + "\n"
# Replace newline characters with "\n"
one_line_string = multi_line_string.replace("\n", "\\n")

print("The converted one line string is:")
print(one_line_string)