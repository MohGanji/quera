def check_registration_rules(*args, **kargs):
    res = []
    for uname, passwd in kargs.items():
        if not (uname == 'quera' or uname == 'codecup' or len(uname) < 4 or passwd.isdigit() or len(passwd) < 6 ):
            res.append(uname)
    return res

# print(check_registration_rules(a="1", b="2", username="password", saeed="123456", sadegh='He3@lsa', quera='kLS45@l$'))