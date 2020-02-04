def get_user_status(user):
    prefs = get_user_prefs(user)
    return prefs[0]


def get_user_name(user):
    prefs = get_user_prefs(user)
    return prefs[1]


def get_user_surname(user):
    prefs = get_user_prefs(user)
    return prefs[2]


def get_user_fathername(user):
    prefs = get_user_prefs(user)
    return prefs[3]


def get_user_prefs(user):
    a = user.last_name.split("___")
    return a

def set_user_school(user, id):
    prefs = get_user_prefs(user)
    user.last_name = prefs[0] + '___' + prefs[1] + '___' + prefs[2] + '___' + prefs[3] + '___' + prefs[4].split("=")[0] + '=' + str(id)
    user.save()

def get_user_school(user):
    prefs = get_user_prefs(user)
    return prefs[4].split("=")[1]

def set_user_class(user, id):
    prefs = get_user_prefs(user)
    user.last_name = prefs[0] + '___' + prefs[1] + '___' + prefs[2] + '___' + prefs[3] + '___' + prefs[4] + '___' + prefs[5].split("=")[0] + '=' + str(id)
    user.save()

def get_user_class(user):
    prefs = get_user_prefs(user)
    try:
        return prefs[5].split("=")[1]
    except:
        return 0