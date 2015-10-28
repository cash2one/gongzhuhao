# encoding:utf-8
__author__ = 'rambo'


class Error(Exception):
    def __init__(self, err_code='', err_msg=None, err_msg_cn=None, *args):
        if len(args) == 2:
            err_code = args[0]
            err_msg = args[1]
        if len(args) == 3:
            err_msg_cn = args[2]

        if str(err_code) == '0' or err_code == 'ok':
            self.stat = 'ok'
        else:
            self.stat = 'err'
        self.code = str(err_code)
        self.msg = str(err_msg)
        self.msg_cn = str(err_msg_cn)

    def __str__(self):
        return "[%s:%s] %s:%s" % (
            self.stat, str(self.code),
            str(self.msg), str(self.msg_cn))

    def __add__(self, s=None):
        self.msg += s
        return self

if __name__ == "__main__":
    e = Error(0, "succ")
    print e.__dict__
    tup = [100, 'test']
    e = Error(*tup)
    print e.__dict__
