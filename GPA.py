import re
import json


def load_json (json_filename):
    """Read the json file and return the content
    """
    print(json_filename)
    _datafile=open(json_filename)
    try:
        jsondata = json.load(_datafile)
    except ValueError as  e:
        print ("{} :  {}".format(json_filename,str(e)))
        print("quitting.")
        quit()
        
    _datafile.close()
    return jsondata
    
    

COURSE_NAME_PATTERN=".*?align\=\"center\">(\w+)\&nbsp;(\d+)</td>.*?grade.*?credits\=\"([0-9]+).*?\".*?<td class\=\"listRow\" align\=\"center\">(.*?)</td>.*?"
course_pat=re.compile(COURSE_NAME_PATTERN, re.DOTALL)
coursestaken={}

json_output_file="GPA.json"

output_json=open(json_output_file, "w")
output_json.write('{\n"COURSES" : {\n')

        
with  open('GPA.txt') as file:
    contents = file.read()
    for entry in contents.split('</tr>'):
        if course_pat.match(entry):
            m=re.match(COURSE_NAME_PATTERN, entry, re.DOTALL)
            print ("*****COURSENAME:{}{},CREDDITS:{},GRADE:{}****".format(m.group(1),m.group(2),m.group(3),m.group(4)))
            # print ("**{}**\n".format(entry))
            jsonstring="\"{}{}\" : {{ \"credits\" : \"{}\", \"grades\" : \"{}\" }},\n".format(m.group(1),m.group(2),m.group(3),m.group(4))
            output_json.write(jsonstring)

output_json.close()

with  open(json_output_file) as file_json:
    contents = file_json.read()
    contents = contents[:-2] 
    
output_json=open(json_output_file, "w")
output_json.write("{}\n".format(contents))
output_json.write('}\n')
output_json.write('}\n')


output_json.close()


total_cred=0
GP=0
transcript = load_json('GPA.json')

for course in (transcript["COURSES"]):
    if transcript["COURSES"][course]["grades"]:
        total_cred+=int(transcript["COURSES"][course]["credits"])
        if (transcript["COURSES"][course]["grades"] == "A+" or transcript["COURSES"][course]["grades"] =="A"):
            grade_gpa=4
        elif (transcript["COURSES"][course]["grades"] == "A-"):
            grade_gpa=3.7
        elif (transcript["COURSES"][course]["grades"] == "B+"):
            grade_gpa=3.3
        elif (transcript["COURSES"][course]["grades"] =="B"):
            grade_gpa=3
        elif (transcript["COURSES"][course]["grades"] =="B-"):
            grade_gpa=2.7
        elif (transcript["COURSES"][course]["grades"] =="C+"):
            grade_gpa=2.3
        elif (transcript["COURSES"][course]["grades"] =="C"):
            grade_gpa=2
        elif (transcript["COURSES"][course]["grades"] =="C-"):
            grade_gpa=1.7
        elif (transcript["COURSES"][course]["grades"] =="D+"):
            grade_gpa=1.3
        elif (transcript["COURSES"][course]["grades"] =="D"):
            grade_gpa=1
        elif (transcript["COURSES"][course]["grades"] =="D-"):
            grade_gpa=0.7
        elif (transcript["COURSES"][course]["grades"] =="F"):
            grade_gpa=0
        GP+=grade_gpa * int(transcript["COURSES"][course]["credits"])

        
print ("Your GPA is {}".format(GP / total_cred))

            
          