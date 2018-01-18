def hello(who):
    print 'Hello, %s!' % who

if __name__ == '__main__':
    print hello(sys.args[1] if len(sys.args) >= 2 else 'World')
