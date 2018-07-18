# -*- coding: utf-8

from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from dbaseop import Pysql

app = Flask(__name__)

# Cross Domain Solve
CORS(app, origins='*', allow_headers='*')

# Utilities Functions
def authenticationCheck(req):
    # check for signed in status
    if "uid" in req:
        return True
    else: return False

def getCatName(id):
    # get category name by id
    db = Pysql()

    if int(id) == 0:
        return "根节点"

    res = db.selectAll(sql="""
        select name from category where id=%s;
    """, params=(id,))

    if res["success"] == True and res["count"]>0:
        return res["data"][0]["name"]
    else:
        return False

def getUserName(id):
    # get user name by id
    db = Pysql()

    res = db.selectAll(sql="""
        select username from user where id=%s;
    """, params=(id,))

    if res["success"] == True and res["count"]>0:
        return res["data"][0]["username"]
    else: return ""


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # get authetication
        username = request.form['username']
        password = request.form['password']

        # print(username, password)

        db = Pysql()

        # 0 - Admin
        res = db.selectAll(sql="""
            select * from user where username=%s and role=0;
        """, params=(username,))

        if res["success"] == True:
            if res["count"] == 0:
                return jsonify(success=False, reason="Wrong password/username!")
            else:
                d = res["data"][0]
                if password != d["password"]:
                    return jsonify(success=False, reason="Wrong password/username!")
                else:
                    return jsonify(success=True, data=d)
        else: return jsonify(success=False, reason="Internal wrong!")

    elif request.method == 'GET':
        # return login page
        return render_template('login.html')

@app.route("/logout")
def logout():
    return redirect(url_for("login"))



@app.route("/index")
def index():
    if authenticationCheck(request.cookies) == True:
        username = request.cookies.get("username")
        return render_template('index.html',username=username)
    else:
        # redirect to login
        return redirect(url_for("login"))

@app.route("/productlist")
def productlist():
    if authenticationCheck(request.cookies) == True:
        username = request.cookies.get("username")
        return render_template('productlist.html',username=username)
    else:
        return redirect(url_for("login"))

@app.route("/api/getAllProducts")
def getAllProducts():
    db = Pysql()

    res = db.selectAll(sql="""
        select * from product;
    """)

    if res["success"] == True:
        return jsonify(success=True,html=render_template("producttable.html",products=res["data"]))
    else: return jsonify(success=False, reason="Internal Wrong!")

@app.route("/api/onProduct/<id>")
def onProduct(id):
    id = int(id)

    db = Pysql()

    res = db.modify(sql="""
        update product set status=1 where id=%s;
    """, params=(id,))

    if res["success"] == True:
        return jsonify(success=True)
    else: return jsonify(success=False, reason="Internal Wrong!")

@app.route("/api/downProduct/<id>")
def downProduct(id):
    id = int(id)

    db = Pysql()

    res = db.modify(sql="""
        update product set status=2 where id=%s;
    """, params=(id,))

    if res["success"] == True:
        return jsonify(success=True)
    else: return jsonify(success=False, reason="Internal Wrong!")

@app.route("/api/deleteProduct/<id>")
def deleteProduct(id):
    id = int(id)

    db = Pysql()

    res = db.modify(sql="""
        update product set status=3 where id=%s;
    """, params=(id,))

    if res["success"] == True:
        return jsonify(success=True)
    else: return jsonify(success=False, reason="Internal Wrong!")

@app.route("/api/inProduct", methods=["POST"])
def inProduct():
    id = int(request.form["id"])
    in_stock = int(request.form["in_stock"])
    uid = int(request.cookies.get("uid"))

    db = Pysql()

    res = db.modify(sql="""
        update product set stock=stock+%s, updated_time=now(), updated_user=%s where id=%s;
    """, params=(in_stock,uid,id))

    if res["success"] == True:
        return jsonify(success=True)
    else: return jsonify(success=False, reason="Internal Wrong!")

@app.route("/api/createProduct", methods=["POST"])
def createProduct():
    name = request.form["name"]
    category_id = int(request.form["category_id"])
    price = float(request.form["price"])
    stock = int(request.form["stock"])
    status = int(request.form["status"])
    uid = int(request.cookies.get("uid"))

    db = Pysql()

    res = db.insert(sql="""
        insert into product (category_id,name,price,stock,status,created_time,created_user,updated_time,updated_user) values
        (%s,%s,%s,%s,%s,now(),%s,now(),%s);
    """, params=(category_id,name,price,stock,status,uid,uid))

    if res["success"] == True:
        return jsonify(success=True)
    else: return jsonify(success=False, reason="Internal Wrong!")

@app.route("/api/editProduct", methods=["POST"])
def editProduct():
    id = int(request.form["id"])
    name = request.form["name"]
    category_id = int(request.form["category_id"])
    price = float(request.form["price"])
    stock = int(request.form["stock"])
    status = int(request.form["status"])
    uid = int(request.cookies.get("uid"))

    db = Pysql()

    res = db.modify(sql="""
        update product set name=%s, category_id=%s, price=%s, stock=%s, status=%s, updated_time=now(), updated_user=%s where id=%s;
    """, params=(name,category_id,price,stock,status,uid,id))

    if res["success"] == True:
        return jsonify(success=True)
    else: return jsonify(success=False, reason="Internal Wrong!")



@app.route("/typelist")
def typelist():
    if authenticationCheck(request.cookies) == True:
        username = request.cookies.get("username")
        return render_template('typelist.html',username=username)
    else:
        return redirect(url_for("login"))

@app.route("/api/getFirstCats")
def getFirstCats():
    db = Pysql()

    res = db.selectAll(sql="""
        select * from category where parent_id=0;
    """)

    if res["success"] == True:
        return jsonify(success=True,html=render_template("typecontainer.html",hier=0,catCount=res["count"],cats=res["data"],parent_id=0))
    else:
        return jsonify(success=False,reason="Internal Wrong!")

@app.route("/api/getFollowingCats/<hier>/<id>")
def getFollowingCats(hier,id):
    parent_id = int(id)
    curHier = int(hier)+1

    db = Pysql()

    res = db.selectAll(sql="""
        select * from category where parent_id=%s;
    """,params=(parent_id,))

    if res["success"] == True:
        return jsonify(success=True,html=render_template("typecontainer.html",hier=curHier,catCount=res["count"],cats=res["data"],parent_id=parent_id))
    else: return jsonify(success=False,reason="internal Wrong!")

@app.route("/api/getCatDetail/<id>")
def getCatDetail(id):
    id = int(id)

    db = Pysql()

    res = db.selectAll(sql="""
        select * from category where id=%s;
    """, params=(id,))

    parent_id=res["data"][0]["parent_id"]
    created_uid = res["data"][0]["created_user"]
    updated_uid = res["data"][0]["updated_user"]

    if res["success"] == True:
        return jsonify(success=True,html=render_template("typedetailcontainer.html",item=res["data"][0],parent_name=getCatName(parent_id),created_user=getUserName(created_uid),updated_user=getUserName(updated_uid)))
    else:
        return jsonify(success=False,reason="Internal Wrong!")

@app.route("/api/createCat", methods=["POST"])
def createCat():
    hier = request.form["hier"]
    parent_id = request.form["parent_id"]
    name = request.form["name"]
    status = int(request.form["status"])
    uid = int(request.cookies.get("uid"))

    db = Pysql()

    res = db.insert(sql="""
        insert into category (parent_id,name,status,created_time,created_user,updated_time,updated_user) values
        (%s,%s,%s,now(),%s,now(),%s);
    """,params=(parent_id,name,status,uid,uid))

    if res["success"] == True:
        return jsonify(success=True)
    else: return jsonify(success=False, reason="Internal Wrong!")

@app.route("/api/editCat", methods=["POST"])
def editCat():
    id = request.form["id"]
    name = request.form["name"]
    status = int(request.form["status"])
    uid = int(request.cookies.get("uid"))

    db = Pysql()

    res = db.modify(sql="""
        update category set name=%s, status=%s, updated_time=now(), updated_user=%s where id=%s;
    """, params=(name,status,uid,id))

    if res["success"] == True:
        return jsonify(success=True)
    else: return jsonify(success=False, reason="Internal Wrong!")

@app.route("/api/discardCat/<id>")
def discardCat(id):
    id = int(id)
    uid = int(request.cookies.get("uid"))

    db = Pysql()

    res = db.modify(sql="""
        update category set status=2, updated_time=now(), updated_user=%s where id=%s;
    """, params=(uid,id))

    if res["success"] == True:
        return jsonify(success=True)
    else: return jsonify(success=False, reason="Internal Wrong!")

@app.route("/api/reuseCat/<id>")
def reuseCat(id):
    id = int(id)
    uid = int(request.cookies.get("uid"))

    db = Pysql()

    res = db.modify(sql="""
        update category set status=1, updated_time=now(), updated_user=%s where id=%s;
    """, params=(uid,id))

    if res["success"] == True:
        return jsonify(success=True)
    else: return jsonify(success=False, reason="Internal Wrong!")

@app.route("/orderlist")
def orderlist():
    if authenticationCheck(request.cookies) == True:
        username = request.cookies.get("username")

        db = Pysql()

        res = db.selectAll(sql="""
            select * from `order`;
        """)

        if res["success"] == True:
            return render_template('orderlist.html',username=username,orders=res["data"])
        else: return jsonify(success=False, reason="Internal Wrong!")

    else:
        return redirect(url_for("login"))

@app.route("/api/closeOrder/<id>")
def closeOrder(id):
    id = int(id)

    db = Pysql()

    res = db.modify(sql="""
        update `order` set status=60, updated_time=now() where id=%s;
    """, params=(id,))

    if res["success"] == True:
        return jsonify(success=True)
    else: return jsonify(success=False)

@app.route("/api/paidOrder/<id>")
def paidOrder(id):
    id = int(id)

    db = Pysql()

    res = db.modify(sql="""
        update `order` set status=20, updated_time=now() where id=%s;
    """, params=(id,))

    if res["success"] == True:
        return jsonify(success=True)
    else: return jsonify(success=False)

@app.route("/api/shippedOrder/<id>")
def shippedOrder(id):
    id = int(id)

    db = Pysql()

    res = db.modify(sql="""
        update `order` set status=40, updated_time=now() where id=%s;
    """, params=(id,))

    if res["success"] == True:
        return jsonify(success=True)
    else: return jsonify(success=False)

if __name__ == "__main__":
    app.run(debug=True)
