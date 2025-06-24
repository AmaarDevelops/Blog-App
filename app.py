from flask import Flask,request,redirect,render_template,url_for,flash,session
from werkzeug.security import generate_password_hash,check_password_hash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir,'blog.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
class Post(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    title = db.Column(db.String(100),nullable=False)
    content = db.Column(db.Text,nullable=False)
    author = db.Column(db.String(50),nullable=False)
    image = db.Column(db.String(255),nullable=False)


app.secret_key  = 'secret_key'


users = {}


@app.route('/')
def home():
    all_posts = Post.query.all()
    return render_template("home.html",posts=all_posts)

@app.route("/regsiter",methods=["GET","POST"])
def register():
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')

        if username in users:
            flash('Username already exists','info')
        else:
            users[username] = generate_password_hash(password)
            flash('Registered successfuly','success')        
            return redirect(url_for('login'))
    return render_template("register.html") 


@app.route('/login',methods=["GET","POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form['password']
        user_hash = users.get(username)

        if user_hash and check_password_hash(user_hash,password):
            session["user"] = username
            flash("Login successfully",'success')
            return redirect(url_for('home'))
        else:
            flash("Invalid credentials",'danger')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user',None)
    flash('Logged out successfully','danger')
    return redirect(url_for('home'))

@app.route('/create_post',methods=["POST","GET"])
def create_post():
    if request.method=="POST":
        title = request.form['title']
        content = request.form['content']
        author = request.form['author']
        image = request.form['image']

        post = Post(title=title,content=content,author=author,image=image)
        db.session.add(post)
        db.session.commit()

        flash("Post created successfuly",'success')
        return redirect(url_for('home'))
    return render_template("create_post.html")

@app.route('/post/<int:post_id>')
def view_post(post_id):
        post = Post.query.get_or_404(post_id)
        return render_template("post-detail.html",post=post)


if __name__ == "__main__":
    app.run(debug=True)
    