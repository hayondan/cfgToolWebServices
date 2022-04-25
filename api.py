import requests
import dbConnector


def updateSetUpVer(version, vernum):
    try:
        route = dbConnector.createRoute(version, vernum)
        print(route)
        res = requests.put(route)
        if res.status_code == 500:
            raise Exception('Error')
        else:
            print(res)

    except:
        print('user_already_exist')

