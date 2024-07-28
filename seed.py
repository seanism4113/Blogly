from models import User, db
from app import app

db.drop_all()
db.create_all()

User.query.delete()

gandalf = User(first_name="Ian", last_name="McKellen", image_url="https://images3.wikia.nocookie.net/__cb20130209172438/lotr/images/8/8d/Gandalf-2.jpg")
frodo = User(first_name="Elijah", last_name="Wood", image_url="https://static.miraheze.org/greatcharacterswiki/thumb/8/81/FRODO.jpeg/600px-FRODO.jpeg")
samwise = User(first_name="Sean", last_name="Astin", image_url="https://www.theonering.net/torwp/wp-content/uploads/2013/05/samwise-gamgee.jpg")
merry = User(first_name="Dominic", last_name="Monaghan", image_url="https://pm1.aminoapps.com/6262/d3a2f0a556a8c6a9383f04ef956e87b1c46ff174_00.jpg")
pippin = User(first_name="Billy", last_name="Boyd", image_url="https://i.pinimg.com/564x/47/42/9f/47429f0915c1f49766d44dce3b4f148c.jpg")
aragorn = User(first_name="Vigo", last_name="Mortenson", image_url="https://static1.srcdn.com/wordpress/wp-content/uploads/2020/06/Viggo-Mortensen-as-Aragorn-in-Lord-of-the-Rings.jpg")
legolas = User(first_name="Orlando", last_name="Bloom", image_url="https://static1.cbrimages.com/wordpress/wp-content/uploads/2022/01/legolas.jpg")
gimli = User(first_name="John", last_name="Rhys-Davies", image_url="https://www.slashfilm.com/img/gallery/there-was-a-secret-second-actor-playing-gimli-in-the-lord-of-the-rings/l-intro-1660686644.jpg")
arwen = User(first_name="Liv", last_name="Tyler")
boromir = User(first_name="Sean", last_name="Bean")


db.session.add(gandalf)
db.session.add(frodo)
db.session.add(samwise)
db.session.add(merry)
db.session.add(pippin)
db.session.add(aragorn)
db.session.add(legolas)
db.session.add(gimli)
db.session.add(arwen)
db.session.add(boromir)

db.session.commit()