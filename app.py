from elearning import create_app

def run_app():
    app = create_app()
    app.run(debug=True)

if __name__ == '__main__':
    run_app()


"""
# To access the Hello World 

from elearning import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
"""