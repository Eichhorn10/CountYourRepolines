import requests

line_count = 0

# Counts all written lines
def count_lines(file_url):
    count = 0
    file_response = requests.get(file_url)
    file_content = file_response.content.decode('utf-8')
    for line in file_content.splitlines():
        if line.strip():
            count += 1
    return count

def searchFileOrFolder(_url, _branch):
    global line_count
    global ignore_files
    global ignore_filetypes

    response = requests.get(_url, params={'ref': _branch})
    data = response.json()
    match response.status_code:
        case 403:
            print("Wir sind am rate limit.")
            exit()
        case 404:
            print("The inserted URL does not exist. Try another URL.")
            return
        case _: pass

    for file_or_folder in data:
        if file_or_folder['type'] == 'file' and (((ignore_files != ('',)) and (file_or_folder['name'] in ignore_files)) or ((ignore_filetypes != ('',)) and (file_or_folder['name'].endswith(ignore_filetypes)))):
            continue
        if file_or_folder['type'] == 'dir':
            searchFileOrFolder(file_or_folder['url'], _branch)
            continue
        file_url = file_or_folder['download_url']
        line_count += count_lines(file_url)

while True:
    print("Please read the README.md file before using!!\n")

    print("Which repository should I count?")
    url = input("URL: ").replace("github.com", "api.github.com/repos") + "/contents"
    branch = 'main'
    with open("..\CountYourRepolines\ignoreFiles.txt", "r") as file:
        ignore_files = tuple(file.read().split(','))
    file.close()
    with open("..\CountYourRepolines\ignoreFiletypes.txt", "r") as file:
        ignore_filetypes = tuple(file.read().split(','))
    file.close()

    searchFileOrFolder(url, branch)
    print(f"The repository uses {line_count} lines of code.")
    if ignore_files != ('',):
        print("Ignored files: " + str(ignore_files).replace(',', ''))
    if ignore_filetypes != ('',):
        print("Ignored filetypes: " + str(ignore_filetypes).replace(',', ''))
    print("")

    while True:
        match input("Try another repository? (y/n)\n"):
            case "y":
                line_count = 0
                break
            case "n":
                exit()
            case _:
                print("Wrong input, try again.")