from flask import Flask,render_template,redirect,url_for,session,request
import requests
app = Flask(__name__)
app.secret_key = "abc"
admins = {"bzadmin":"admin@beingzero"}
d = {"CMRCET2024P1":"bz-cmrcet-2024-p1","BZKLH1923P1":"bz-klh-23-p1","BZCMRTC2024P1":"bz-cmrtc-2024-p1"}
@app.route('/logout')
def logout():
   # remove the username from the session if it is there
   session.pop('username', None)
   return redirect(url_for('login'))
@app.route('/login', methods = ['GET', 'POST'])
def login():
   if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        if user in admins and admins[user] == password:
          session['username'] = user
          return redirect(url_for('home'))
        else:
            return redirect(url_for('login'))
   return '''
	
   <form action = "" method = "post">
      <input type = text name = username Placeholder="Username">
      <input type = text name = password Placeholder = "Password">
      <input type = submit value = Login>
   </form>
	
   '''
@app.route("/<name>")
def leaderboard(name):
    if name in d:
        r = requests.get("https://scores.mentorpick.com/api/leaderboard/batch/"+d[name])
        s = r.json()
        l1 = ['MENTORPICK','HACKERRANK',  'VJUDGE',  'CODECHEF','CODEFORCES', 'LEETCODE']
        criteria = {
            "HACKERRANK" : { 'ds_score': 50, 'algo_score': 200},
            "MENTORPICK" : {'solved_count': 52},
            "CODEFORCES" : {'solved_count': 20, 'contests_participated': 1, 'user_rating': 600},
            "CODECHEF" : {'solved_count': 25, 'contests_participated': 4, 'user_rating': 1400, 'star_rating': 2},
            "VJUDGE" : {'solved_count': 0},
            "LEETCODE" : {'solved_count': 30, 'contests_participated': 2}
        }
        l2 = ['HACKERRANK','CODECHEF','CODEFORCES', 'LEETCODE']
        for i in range(len(s['data']['leaderboard'])):
            count = 12
            di = s['data']['leaderboard'][i]['stats']
            for j in l2:
                for k in criteria[j]:
                    if criteria[j][k]<= di[j][k]:
                        count-=1
            if di['MENTORPICK']['solved_count']+di['VJUDGE']['solved_count']>=80:
                count-=1
            s['data']['leaderboard'][i]['stats']['count'] = count
        return render_template("index.html",l = s['data']['leaderboard'],l1= l1,criteria = criteria,name = name)
    return redirect(url_for("home"))
@app.route("/")
def home():
    if "username" in session:
        return render_template("home.html",d=d)
    return redirect(url_for("login"))
if __name__ == '__main__':
    app.run(debug=True)