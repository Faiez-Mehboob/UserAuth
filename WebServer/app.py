from Website_Resources import create_app
import argparse
import sys

parser=argparse.ArgumentParser()
parser.add_argument('--AuthHost', help='Set authentication server host', default='localhost')
parser.add_argument('--AuthPort', help='Set authentication server port',type=int, default=9999)
args= parser.parse_args()

app = create_app(AuthHOST=args.AuthHost,AuthPORT=args.AuthPort)

if __name__=="__main__":
    app.run(host='0.0.0.0',debug=True)
