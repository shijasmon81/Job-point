from wehireyou import app
from wehireyou import db
if __name__=="__main__":
    app.run(debug=True)
    db.create_all()