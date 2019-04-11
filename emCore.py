import requests as req
import json
key='AIzaSyAcCe0X87lSL9cZzaPZUV8tU2Z2XPh2IqY'
pathLong=20000#in meters
multiplier=200
magnifize=3
samples=pathLong//multiplier
increment=(multiplier/100000)*(-1)#0.0001 ~ 10 metrov

itog=[]
text=""
startpoint={
	'x1':43.528321,#1st from gm
	'y1':39.864248,#2nd from gm
	'x2':(pathLong/multiplier)*increment*(-1),
}
def stlCreate(text):
	with open('temp.stl','wb') as f:
		f.write(bytes('solid em\n'+text+'endsolid em\n','ascii'))

for i in range(pathLong//multiplier):
	answer = req.get('https://maps.googleapis.com/maps/api/elevation/json?key='+key+'&samples='+str(samples)+'&path='+str(startpoint['y1']+increment*i)+','+str(startpoint['x1'])+'|'+str(startpoint['y1']+increment*i)+','+str(startpoint['x2']+startpoint['x1']))
	temp=json.loads(answer.text)
	itog.append([])
	for j in temp['results']:
		itog[len(itog)-1].append(j['elevation'])
	print(answer)
	#print(itog[len(itog)-1])
	print(int((i+1)*100)/int(pathLong//multiplier))
	#sleep(3)
if(len(itog)>1 and len(itog[0])//2!=1):
	for i in range(len(itog)-1):
		for j in range(len(itog[i])-1):
			text+="facet normal 0 0 0\nouter loop\nvertex "+str((i+1)*multiplier)+" "+str((j)*multiplier)+" "+str(round(itog[i+1][j],4)*magnifize)+"\n"
			text+="vertex "+str((i)*multiplier)+" "+str((j+1)*multiplier)+" "+str(round(itog[i][j+1],4)*magnifize)+"\n"
			text+="vertex "+str((i)*multiplier)+" "+str((j)*multiplier)+" "+str(round(itog[i][j],4)*magnifize)+"\n"
			text+="endloop\nendfacet\n\n"

			text+="facet normal 0 0 0\nouter loop\nvertex "+str((i+1)*multiplier)+" "+str((j)*multiplier)+" "+str(round(itog[i+1][j],4)*magnifize)+"\n"
			text+="vertex "+str((i+1)*multiplier)+" "+str((j+1)*multiplier)+" "+str(round(itog[i+1][j+1],4)*magnifize)+"\n"
			text+="vertex "+str((i)*multiplier)+" "+str((j+1)*multiplier)+" "+str(round(itog[i][j+1],4)*magnifize)+"\n"
			text+="endloop\nendfacet\n\n"
stlCreate(text)