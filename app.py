from flask import *
from xlrd import open_workbook
from xlutils.copy import copy
import xlwt

app = Flask(__name__)
app.secret_key='djskgaheoihgarg'

fp = open('question.txt','r',encoding='utf-8')

@app.route('/',methods=['GET'])
def welcome():
	return render_template('welcome.html')

@app.route('/',methods=['POST'])
def welcome_button():
	return redirect(url_for('question'))
	
@app.route('/question/',methods=['GET'])
def question():
	fp.seek(0,0)
	question=fp.readline()
	choiceA=fp.readline()
	choiceB=fp.readline()
	choiceC=fp.readline()
	choiceD=fp.readline()
	choiceE=fp.readline()
	choiceF=fp.readline()
	filep=fp.tell()
	return render_template('question.html',question=question,choiceA=choiceA,choiceB=choiceB,choiceC=choiceC,choiceD=choiceD,choiceE=choiceE,choiceF=choiceF,filep=filep,choices='')
	
@app.route('/question/',methods=['POST'])
def question_button():
	choice=request.values.get('choice')
	filep=request.values.get('filep')
	choices=request.values.get('choices')+choice
	fp.seek(int(filep),0)
	question=fp.readline()
	if question=='END':
		oldbook=open_workbook('answer.xls')
		oldsheet=oldbook.sheet_by_index(0)
		i=int(oldsheet.cell(0,0).value)
		newbook=copy(oldbook)
		sheet1=newbook.get_sheet(0)
		sheet1.write(i,0,i)
		j=1
		for x in choices:
			sheet1.write(i,j,x)
			j=j+1
		i=i+1
		sheet1.write(0,0,i)
		newbook.save('answer.xls')
		return redirect(url_for('thank'))
	choiceA=fp.readline()
	choiceB=fp.readline()
	choiceC=fp.readline()
	choiceD=fp.readline()
	choiceE=fp.readline()
	choiceF=fp.readline()
	filep=fp.tell()
	return render_template('question.html',question=question,choiceA=choiceA,choiceB=choiceB,choiceC=choiceC,choiceD=choiceD,choiceE=choiceE,choiceF=choiceF,filep=filep,choices=choices)
	
@app.route('/thank/',methods=['GET'])
def thank():
	return render_template('thank.html')
	
if __name__=='__main__':
    app.run(host='0.0.0.0',port=14250,threaded = True)