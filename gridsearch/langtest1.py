import joblib

class JobWrapper(object):

    def run(self):
        print('hello world')

j = JobWrapper()

joblib.dump(j, 'j.gz', compress=('gzip', 3))

jj = joblib.load('j.gz')
jj.run()