from flask import Flask, request, render_template, url_for
from werkzeug.utils import redirect
import dbConnector, A32
import api

app = Flask(__name__)
app.config['SECRET_KEY'] = 'zubur1'

app.route('stop_server')


@app.route('/data/<version>', methods=['GET'])
def buildVersion(version):
    try:
        if request.method == 'GET':
            versionInfo = dbConnector.getVersion(version)
            if versionInfo == None:
                return {'status': 'error', 'version': 'no such version'}
            print(versionInfo)
            if versionInfo:
                return {'status': 'ok', 'allInfo': versionInfo}, 200
            else:
                return {'status': 'error', 'version': 'no such version'}, 201

    except:
        print("Error in DB - From GET")
        return {'status': 'error', 'reason': 'Error in DB'}, 500


@app.route('/data/versionNum/<version>/', methods=['GET'])
def verNumToVersion(version):
    try:
        if request.method == 'GET':
            versionNum = dbConnector.getVersionNu(version)
            if versionNum:
                return {'status': 'ok','version': version, 'ver_number': versionNum}, 200
            else:
                return {'status': 'error', version: 'no such version'}, 201
    except:
        print("Error in DB - From GET")
        return {'status': 'error', 'reason': 'Error in DB'}, 500



@app.route('/data/buildNum/<version>/', methods=['GET', 'POST', 'DELETE', 'PUT'])
def buildNumToVersion(version):
    try:
        if request.method == 'GET':
            buildNum = dbConnector.getBuildNu(version)
            if buildNum:
                return {'status': 'ok', 'version': version, 'build_number': buildNum}, 200
            else:
                return {'status': 'error', version: 'no such version'}, 201
    except:
        print("Error in DB - From GET")
        return {'status': 'error', 'reason': 'Error in DB'}, 500


@app.route('/', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('welcome'))
    return render_template('login.html', error=error)


@app.route('/data', methods=['GET', 'PUT', 'POST'])
def updateBuilds():
    error = None
    if request.method == 'POST':
        if request.form['version'] != None:
            print('here')
        if request.form['verNum'] != None:
            print('here1')
            dbConnector.updateVersion(request.form['version'], request.form['verNum'])
        if request.form['build'] != None:
            print('here3')
            dbConnector.updateBuild(request.form['version'], request.form['build'])
        if request.form['appBuild'] != None:
            print('here4')
            dbConnector.updateappBuild(request.form['version'], request.form['appBuild'])
            A32.newlist.append('10dswf')
            print(A32.newlist)
        return redirect(url_for('welcome'))
    elif request.method == 'GET':
        return render_template('index.html', error=error)


@app.route('/data/version/<version>/<verNum>', methods=['POST', 'PUT'])
def insertNewVer(version, verNum):
    if request.method == 'POST':
        insertVersionNum = dbConnector.insertVersion(version, verNum)
        print(insertVersionNum)
        return insertVersionNum
    elif request.method == 'PUT':
        updateVersion = dbConnector.updateVersion(version, verNum)
        print(updateVersion)
        return updateVersion


@app.route('/data/build/<version>/<buildNum>', methods=['POST', 'PUT'])
def insertNewBuild(version, buildNum):
    if request.method == 'POST':
        insertbuildNumNum = dbConnector.insertBuild(version, buildNum)
        print(insertbuildNumNum)
        return insertbuildNumNum
    elif request.method == 'PUT':
        updateBuild = dbConnector.updateBuild(version, buildNum)
        print(updateBuild)
        creatingUpgradeFormat(version)

        return updateBuild


@app.route('/data/appBuild/<version>/<appBuildNum>', methods=['POST', 'PUT'])
def insertappBuild(version, appBuildNum):
    if request.method == 'POST':
        insertappbuildNumNum = dbConnector.insertappBuild(version, appBuildNum)
        print(insertappbuildNumNum)
        return insertappbuildNumNum
    elif request.method == 'PUT':
        updateAppBuild = dbConnector.updateappBuild(version, appBuildNum)
        print(updateAppBuild)
        creatingUpgradeFormat(version)

        return updateAppBuild


@app.route('/buildsinfo')
def buildinfo():
    return render_template('builds.html')


@app.route("/home")
def welcome():
    if request.method == 'GET':
        return render_template("welcomePage.html")


@app.route('/data/delete/<version>', methods=['DELETE'])
def deleteFromTable(version):
    try:
        delete_the_column = dbConnector.deleteAllFromColumn(version)
        print(delete_the_column)
        if delete_the_column:
            return {'status': 'ok', 'data in column was deleted ': version}, 200
    except:
            return {'status': 'error', 'reason': 'Error in DB'}, 500



@app.route("/builds/<version>")
def creatingUpgradeFormat(version):
    global versionFormat
    versionBuildNu = dbConnector.getVersion(version)
    print(versionBuildNu)
    versionNu = versionBuildNu["version"]
    if versionNu == None:
        return {'status': 'error', None: 'no such version', }, 201
    elif version == 'A32' or 'A32Old':
        versionFormat = str('3200.0.' + str(versionNu))
        print(versionFormat)
    elif version == 'A3210' or 'A3210Old':
        versionFormat = str('3200.10.' + str(versionNu))
        print(versionFormat)
    else:
        return {'status': 'error', version: 'no such version', }, 201
    buildNu = str(versionBuildNu["build"])
    print(buildNu)
    if buildNu == None:
        return {'status': 'error', version: 'no such version', }, 201
    appBuild = str(versionBuildNu["appBuild"])
    print(appBuild)
    if appBuild == None:
        return {'status': 'error', version: 'no such version', }, 201
    else:
        applianceUpgrade = 'wget http://builds.algosec.com/builds/algosec-appliance/' + versionFormat + '/algosec-appliance-' + versionFormat + '-'+appBuild+'-el7.x86_64.run --no-check-certificate'
        print(applianceUpgrade)
        faUpgrade = 'wget http://builds.algosec.com/builds/fa/' + versionFormat + '/UNVERIFIED/fa-' + versionFormat + '-'+buildNu+'.x86_64.run --no-check-certificate'
        print(faUpgrade)
        ffUpgrade = 'wget http://builds.algosec.com/builds/fireflow/' + versionFormat + '/UNVERIFIED/fireflow-' + versionFormat + '-'+buildNu+'.x86_64.run --no-check-certificate'
        print(ffUpgrade)
        allWget = applianceUpgrade, faUpgrade, ffUpgrade
        if version == 'A32' or 'A32Old':
            afaAndFFName = 'A32.0.'+ versionFormat + '-' + buildNu
            appName = 'A32.0.'+ versionFormat + '-' + appBuild
            print(afaAndFFName)
            print(appName)
        if version =='A3210' or 'A3210Old':
            afaAndFFName = 'A32.10.' + versionFormat + '-' + buildNu
            appName = 'A32.10.' + versionFormat + '-' + appBuild
            print(afaAndFFName)
            print(appName)

        if request.method == 'GET':
            return {'status': 'ok', 'appliance': applianceUpgrade, 'fa': faUpgrade, 'ff': ffUpgrade, 'version': version, 'build_number': buildNu, 'version_number': versionNu, 'afaAndFF': afaAndFFName, 'appname': appName}, 200
            # return {'status': 'ok', 'appliance': applianceUpgrade, 'fa': faUpgrade, 'ff': ffUpgrade, 'version': version, 'build_number': buildNu, 'version_number': versionNu}, 200
        else:
            return {'status': 'error', version: 'no such version', }, 201


app.run(host='127.0.0.1', debug=True, port=5000)



