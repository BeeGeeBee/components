__author__ = 'Bernard'

from flask import Flask, render_template, request, send_file
from forms import ComponentsForm
from models import Components, Base, Locations, Suppliers
from sqlalchemy import create_engine
engine = create_engine('sqlite:///database//components.db', echo=True)
Base.metadata.bind = engine

from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()


app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showlist/')
def showlist():
    form = ComponentsForm(request.form)
    form.name.value = []
    form.supplier.value = []
    form.location.value = []
    form.datasheet.value = []
    for (name, supplier, location, datasheet) in \
            session.query(Components.Name, Suppliers.Name, Locations.Name, Components.Datasheet).\
            outerjoin(Suppliers, Components.SuppliersID == Suppliers.ID).\
            outerjoin(Locations, Components.LocationsID == Locations.ID).\
            order_by(Components.Name):
        form.name.value.append(name)
        if supplier is not None:
            form.supplier.value.append(supplier)
        else:
            form.supplier.value.append('')
        form.location.value.append(location)
        form.datasheet.value.append(datasheet)
    return render_template('showlist.html', form=form, numrows=len(form.name.value))

@app.route('/docs/<id>')
def show_pdf(id=None):
    if id is not None:
        return send_file("docs/" + id)

app.run(debug=True)