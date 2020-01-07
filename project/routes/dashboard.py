#peoples
#User Profile
#dahboard
#User list
#Analyzer
#Add Users

from flask import Blueprint,render_template,request,json,make_response,session
from project.controllers.admin import login_required
from project.controllers.analyzer import create_path,deleteVideos,captureFrames,deleteFramesFaces,compareFaces,saveEncodings,unknownFaces
import time,os,pdfkit
from project.controllers.dashboard import gettingTheUseage
panel=Blueprint('dashboard',__name__,url_prefix='/dashboard',static_folder='../static',static_url_path="/static")

@panel.route('/')
@login_required
def index():
    return render_template('dashboard.html')

@panel.route('/peoples')
@login_required
def peoples():
    return render_template('tables.html')

@panel.route('/profile')
@login_required
def profile():
    return render_template("profile.html")

@panel.route('/create')
@login_required
def create():
    return render_template("user_registration.html")

#uses as both post and get
@panel.route('/analyzer',methods=["GET","POST"])
@login_required
def analyze():
    deleteVideos()
    deleteFramesFaces()
    if request.method=="POST":
        res=int(time.time())
        videoData=request.files['image']
        path=create_path(res)
        videoData.save(path)
        return str(res)
    return render_template("analyze.html")
##Begning API
@panel.route('/capture',methods=["GET"])
@login_required
def capture():
    if request.method=="GET":
        video=request.args.get("name")
        return captureFrames(video)

@panel.route('/compare',methods=['GET'])
@login_required
def compare():
    if request.method=="GET":
        return compareFaces()

@panel.route('/unknown',methods=['GET'])
@login_required
def config():
    ff=unknownFaces()
    return json.dumps({'result':ff})
## END

@panel.route('/pdf',methods=["POST"])
@login_required
def pdf():
        count=len(os.listdir('project/static/images/frames'))
        persons=json.loads(request.form["person"])
        unknowns=len(json.loads(request.form["unknown"])['result'])

        template=render_template('PDF.html',count=count,persons=persons,unknowns=unknowns)
        config = pdfkit.configuration(wkhtmltopdf=bytes("C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe", 'utf8'))

        options = {
            'encoding': 'base64'
        }
        path='project/static/pdfs/report.pdf'
        pdf=pdfkit.from_string(template,path,configuration=config,options=options)
        return "1"

@panel.route('/uses',methods=["GET"])
@login_required
def dashboardData():
    id = json.loads(session.get("USER"))["id"]
    logs = gettingTheUseage(id)
    return json.dumps(logs)
