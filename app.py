import time, cv2, pytesseract, requests
from click import *
from PIL import Image
from flask import Flask, render_template, request

app = Flask(__name__)

RUN_URL = u'http://api.hackerearth.com/code/run/'
CLIENT_SECRET = '2f9675ec9f0bc4a636794bfd720d52abeeba9d05'
x = ''

@app.route('/')
def index():
        return render_template("index.html")

@app.route('/',methods=['POST'])
def capture():
        c = Clickonacci()                                        
        c.run()
        x = ''
        x += pytesseract.image_to_string(Image.open('C:/Python27/output.png'))

        lang = ''
        if('include' in x and 'std::' not in x and 'namespace' not in x):
                lang = 'C'
        elif('include' in x):
                lang = 'C++'
        elif('php' in x):
                lang = 'PHP'
        elif('func main' in x):
                lang = 'GO'
        elif('def' in x):
                lang = 'RUBY'
        elif('write' in x or 'writeln' in x):
                lang = 'PERL'
        elif('using System' in x):
                lang = 'C#'
        else:
                lang = 'JAVA'
        def fix(x):
                if(lang == 'C'):
                        x = x.replace('%If','%lf')
                elif(lang == 'JAVA'):
                        while(x.count('|') != 0):
                                a = x.index('|')
                                if(x[a+1] == 'n' and x[a+2] == 't'):
                                        x = x.replace(x[a],'I')
                                else:
                                        x = x.replace(x[a],'l')
                        x = x[2:len(x)]
                elif(lang == 'C#'):
                        x = x.replace('Tolnt','ToInt')
                elif(lang == 'GO' or lang == 'RUBY'):
                        x = x.replace('|','l')
        fix(x)
        x = x.decode('utf-8')
        data = {
            'client_secret': CLIENT_SECRET,
            'async': 0,
            'source': x,
            'lang': lang,
            'time_limit': 5,
            'memory_limit': 262144,
        }
        r = requests.post(RUN_URL, data=data)
        out = r.json()
        next_out = out['run_status']
        output = ''
        for element in next_out:
                if(element != 'output_html'):
                        output += (str(element)+' : '+str(next_out[element]))
                        output += '\n'

        output = output.decode('utf-8')
        
        return render_template('index.html',lang=lang,input1 = x, output = output)

@app.route('/code/',methods=['POST'])
def doit():
        x = request.form['input']
        x = str(x)
        lang = ''
        if('include' in x and 'std::' not in x and 'namespace' not in x):
                lang = 'C'
        elif('include' in x):
                lang = 'C++'
        elif('php' in x):
                lang = 'PHP'
        elif('func main' in x):
                lang = 'GO'
        elif('def' in x):
                lang = 'RUBY'
        elif('write' in x or 'writeln' in x):
                lang = 'PERL'
        elif('using System' in x):
                lang = 'C#'
        else:
                lang = 'JAVA'
        data = {
            'client_secret': CLIENT_SECRET,
            'async': 0,
            'source': x,
            'lang': lang,
            'time_limit': 5,
            'memory_limit': 262144,
        }
        r = requests.post(RUN_URL, data=data)
        out = r.json()
        next_out = out['run_status']
        output = ''
        for element in next_out:
                if(element != 'output_html'):
                        output += (str(element)+' : '+str(next_out[element]))
                        output += '\n'
        output = output.decode('utf-8')

        return render_template('index.html',lang=lang,input1 = x, output = output)

if __name__=="__main__":
        app.run(debug = True)
