from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase 


config = {
  "apiKey": "AIzaSyAaZnCFf9yVMhOPZPbmiTmNxuUNdGhHJSg",
  "authDomain": "starlink-3b3e2.firebaseapp.com",
  "databaseURL": "https://starlink-3b3e2-default-rtdb.europe-west1.firebasedatabase.app",
  "projectId": "starlink-3b3e2",
  "storageBucket": "starlink-3b3e2.appspot.com",
  "messagingSenderId": "615721289202",
  "appId": "1:615721289202:web:9e192646fc2eb487a6976b",
  "measurementId": "G-73CNFEWW29"
}


firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db=firebase.database()

UPLOAD_FOLDER = 'static/images/posts'
ALLOWED_EXTENSIONS = ['png', 'jpg', 'jpeg']

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here

# random = {"word":"egg"}
# db.push(random)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def upload_file(file):
    if request.method == 'POST':
        if file and allowed_file(file.filename):
            filename = file.filename
            file.save(UPLOAD_FOLDER + "/" + filename)


@app.route('/', methods = ['GET', 'POST'])
def homepage():
    return render_template("homepage.html")

#def gotosignin():s
    #return redirect(url_for('signin'))
#def gotologin():
   # return redirect(url_for('signup'))   

@app.route('/signin', methods =[ 'GET', 'POST'])
def signin():
    error=""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        try:
            login_session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('home'))
        except:
            error = "Authentication failed"
            return render_template("login.html")
    else:
        return render_template("login.html")  


@app.route('/signup', methods = ['GET', 'POST'])
def signup():
    error = ""
    if request.method =='POST':
        name = request.form['name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        bio = request.form['bio']
        try:
            login_session['user'] = auth.create_user_with_email_and_password(email, password)
            return redirect(url_for('signin'))
        except:
            error = "Authentication failed"
            return render_template("signup.html")
    else: 
        return render_template("signup.html")
 
@app.route('/home', methods = ['GET', 'POST'])     
def home():
    posts = db.child("Photos").get().val()

    return render_template("index.html", posts = posts)


@app.route('/post', methods=['GET', 'POST'])
def add_post():
    # posts = db.child("Photo").child(login_session['user']['localId']).get().val()

    if request.method == 'POST':
        caption = request.form['caption']
        photo = request.files['post']
        upload_file(photo)
        UID = login_session['user']['localId']
        post = {"caption": caption, "photo": photo.filename, "user_id": UID}
        # db.child("Photos").child(UID).push(post)
        db.child("Photos").push(post)
        posts = db.child("Photos").get().val()


        return render_template('index.html', posts = posts)
    else:
        posts = db.child("Photos").get().val()
        print(posts)
        return render_template('index.html', posts = posts)

users = { "email":"request.form['email']", "name":"request.form['name']", "username":"request.form['username']", "bio":"request.form['bio']"}


#Code goes above here

if __name__ == '__main__':
    app.run(debug=True)



