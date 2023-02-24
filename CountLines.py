import requests


# count = 0
# with open('Desktop/git.txt') as file:
#     for line in file:
#         if line.strip():
#             count += 1

# print('Number of Lines', count)

# Holen Sie sich eine Liste von Dateien im Repository
# response = requests.get(url, params={'ref': branch})
# data = response.json()

# # Initialisieren Sie den Zeilenzähler

# # Durchlaufen Sie jede Datei und jeden Ordner im src-Verzeichnis
# for file_or_folder in data:
#     # Ignoriere Dateien, die keine Code-Dateien sind
#     if file_or_folder['type'] == 'file' and not file_or_folder['name'].endswith('.ts'):
#         continue
#     # Wenn es sich um einen Ordner handelt, rufen Sie die API auf, um die Dateien im Ordner abzurufen
#     if file_or_folder['type'] == 'dir':
#         subdir_url = file_or_folder['url']
#         subdir_response = requests.get(subdir_url, params={'ref': branch})
#         subdir_data = subdir_response.json()
#         # Durchlaufen Sie jede Datei im Unterordner und zählen Sie die Zeilen
#         for file in subdir_data:
#             # Ignoriere Dateien, die keine Code-Dateien sind
#             if file['type'] == 'file' and not file['name'].endswith(('.ts', '.py', '.java', '.c', '.cpp', '.h')):
#                 continue
#             if file['type'] == 'dir':
#                 if file_or_folder['type'] == 'dir':
#                     subdir_url = file_or_folder['url']
#                     subdir_response = requests.get(subdir_url, params={'ref': branch})
#                     subdir_data = subdir_response.json()
#                     # Durchlaufen Sie jede Datei im Unterordner und zählen Sie die Zeilen
#                     for file in subdir_data:
#                         # Ignoriere Dateien, die keine Code-Dateien sind
#                         if file['type'] == 'file' and not file['name'].endswith(('.ts', '.py', '.java', '.c', '.cpp', '.h')):
#                             continue
#                         # Zählen Sie die Zeilen in der Datei
#                         file_url = file['download_url']
#                         line_count += count_lines(file_url)
#             # Zählen Sie die Zeilen in der Datei
#             file_url = file['download_url']
#             line_count += count_lines(file_url)
#     else:
#         # Wenn es sich um eine Datei handelt, zählen Sie die Zeilen in der Datei
#         file_url = file_or_folder['download_url']
#         line_count += count_lines(file_url)
# # Gib die Gesamtzahl der Zeilen aus
# print(f"Das Repository hat insgesamt {line_count} Zeilen.")

line_count = 0

url = 'https://api.github.com/repos/TalentLayer/talentlayer-id-subgraph/contents'
branch = 'main'

# Definieren Sie eine Funktion, um die Anzahl der Zeilen in einer Datei zu zählen
def count_lines(file_url):
    count = 0
    file_response = requests.get(file_url)
    file_content = file_response.content.decode('utf-8')
    for line in file_content.splitlines():
        if line.strip():
            count += 1
    return count

def searchFolder(_url, _branch):
    global line_count

    response = requests.get(_url, params={'ref': _branch})
    data = response.json()
    if (response.status_code == 403):
        print("Wir sind am rate limit.")
        exit()

    for file_or_folder in data:
        if file_or_folder['type'] == 'file' and not file_or_folder['name'].endswith('.ts'):
            continue
        if file_or_folder['type'] == 'dir':
            searchFolder(file_or_folder['url'], _branch)
            continue
        file_url = file_or_folder['download_url']
        line_count += count_lines(file_url)

searchFolder(url, branch)
print(f"Das Repository hat insgesamt {line_count} Zeilen.")
