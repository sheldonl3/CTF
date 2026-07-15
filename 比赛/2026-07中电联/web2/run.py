import imp
import sys
import argparse

def main():
    try:
        app_module = imp.load_compiled('app', 'app.pyc')
        
        parser = argparse.ArgumentParser()
        parser.add_argument('--host', default='0.0.0.0')
        parser.add_argument('--port', type=int, default=5000)
        args = parser.parse_args()
        
        print(f"server starting on {args.host}:{args.port}")
        app_module.app.run(host=args.host, port=args.port, debug=False)
    except Exception as e:
        print(f"{str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
    