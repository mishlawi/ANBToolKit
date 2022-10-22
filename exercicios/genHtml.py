##
### p -> h* , bio, foto
##

## para este caso assumo que .md sao só para biografias .tex para historias .jpg para fotos
import re
import os

html = """<!DOCTYPE html>
<html>
<body>

<h1>"""

dir = str(re.split('/',os.getcwd())[-1])
res_list = []
res_list = re.findall('[A-Z][^A-Z]*', dir)

name = ''
for elem in res_list:
    name+= elem + ' ' 

html+=name + '</h1>'

html+="""
</body>
</html>
"""
#print(html)

files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.getcwd()+'/'+f)]
print(files)



f = open("html/index.html", "w")
f.write(html)
f.close()

def fileList():
    files = [f for f in os.listdir(os.getcwd()) if os.path.isfile(os.getcwd()+'/'+f)]

fileList()


