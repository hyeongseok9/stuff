from flask_restful import reqparse
import hsnam.persist as persist

class Job(Resource):
    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('namespace', type=str)
        parser.add_argument('data_url', type=str)
        parser.add_argument('sarima_config', type=list)
        parser.add_argument('ntest', type=int)
        args = parser.parse_args()

        namespace = args['namespace']
        dataUrl = args['data_url']
        sarimaConfig = args['sarima_config']
        ntest = args['ntest']

        doc = dict(data_url = data_url,sarima_config=sarimaConfig,  ntest = ntest)
        helper = persist.getPersistHelper()
        docid = helper.save(namespace=namespace, doc=json.dumps(doc), queue='pending')
        queueHelper = persist.getQueueHelper()
        queueHelper.put(namespace,'pending', docid)

        return {'status': 'success', 'doc':doc}

    def get(self):
        pass