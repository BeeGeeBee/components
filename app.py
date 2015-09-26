__author__ = 'Bernard'

from flask import Flask, render_template, request, send_file
from forms import ComponentsForm
from models import Components, Base, Locations, Suppliers, Categories, Definitions, Features
from sqlalchemy import create_engine, func
from wtforms import StringField
from wtforms.validators import Length

class Category(object):
    def __init__(self):
        self.id = []
        self.name = []
        self.listorder = []


engine = create_engine('sqlite:///database//components.db', echo=True)
Base.metadata.bind = engine

from sqlalchemy.orm import sessionmaker

DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/showlist/')
def showlist():
    form = ComponentsForm(request.form)
    form.name.value = []
    form.id.value = []
    form.currentstock.value = []
    form.unitprice.value = []
    form.supplier.value = []
    form.location.value = []
    form.datasheet.value = []
    for (componentid, name, currentstock, unitprice, supplier, location, datasheet) in \
            session.query(Components.ID, Components.Name, Components.CurrentStock, Components.UnitPrice,
                          Suppliers.Name, Locations.Name, Components.Datasheet). \
                    outerjoin(Suppliers, Components.SuppliersID == Suppliers.ID). \
                    outerjoin(Locations, Components.LocationsID == Locations.ID). \
                    order_by(Components.Name):
        form.id.value.append(componentid)
        form.name.value.append(name)
        form.currentstock.value.append(currentstock)
        form.unitprice.value.append(unitprice)
        form.supplier.value.append('')
        if supplier:
            form.supplier.value[-1] = supplier
        form.location.value.append('')
        if location:
            form.location.value[-1] = location
        form.datasheet.value.append(datasheet)
    return render_template('showlist.html', form=form, numrows=len(form.name.value))


@app.route('/docs/<docid>')
def show_pdf(docid=None):
    if docid is not None:
        return send_file("docs/" + docid)

catsearch = Category()

@app.route('/categorysearch/<categorylevel>/<categoryid>')
def categorysearch(categorylevel=None, categoryid=None):
    if categorylevel is not None and categoryid is not None:
        categories = Category()
        # for sublist in session.query(Definitions).\
        #         filter(Definitions.CategoriesID == categoryid).\
        #         filter(Definitions.CategoryOrder == 2).distinct():
        #     print "Subselect:",sublist.ComponentID
        catlevel = int(categorylevel)
        catlevel += 1
        catid = int(categoryid)
        if catid > 0:
            #Test if it is a component. First get category name
            cat = session.query(Categories.Name).filter(Categories.ID == catid).one()
            print "Category:",cat[0]
            compexists = session.query(func.count(Components.Name)).filter(Components.Name == cat[0]).scalar()
            print "Component ?",compexists
            if compexists > 0:
                compid = session.query(Components.ID).filter(Components.Name == cat[0]).one()
                return showcomponents(componentid=compid[0])
        for category in session.query(Categories.Name, Categories.ID). \
            join(Definitions, Definitions.CategoriesID == Categories.ID). \
            filter(Definitions.CategoryOrder == catlevel).order_by(Categories.Name).distinct():
            categories.id.append(category.ID)
            categories.listorder.append(catlevel)
            categories.name.append(category.Name)
            print category.Name
        return render_template("categorysearch.html", categories=categories, numcats=len(categories.id))


@app.route('/showcomponents/<componentid>')
def showcomponents(componentid=None):
    form = ComponentsForm()
    q = session.query(Components, Suppliers, Locations).\
                outerjoin(Suppliers, Components.SuppliersID == Suppliers.ID). \
                outerjoin(Locations, Components.LocationsID == Locations.ID). \
                filter(Components.ID == componentid).one()
    print q
    form.name.data = q.Components.Name
    form.description.data = ''
    if q.Components.Description is not None:
        form.description.data = q.Components.Description
    form.ordercode.data = ''
    if q.Components.OrderCode is not None:
        form.ordercode.data = q.Components.OrderCode
    form.supplier.data = ''
    if q.Suppliers is not None:
        form.supplier.data = q.Suppliers.Name
    form.location.data = ''
    form.sublocation.data = ''
    if q.Locations is not None:
        form.location.data = q.Locations.Name
        if q.Locations.Sublocation is not None:
            form.sublocation.data = q.Locations.Sublocation
    form.datasheet.data = ''
    if q.Components.Datasheet is not None:
        form.datasheet.data = q.Components.Datasheet
    form.currentstock.data = q.Components.CurrentStock
    form.reorderlevel.data = q.Components.ReorderLevel
    form.categoryid.id = []
    form.categoryid.name = []
    form.categoryid.listorder = []
    catsearch.id = []
    catsearch.name = []
    catsearch.listorder = []
    catsearchindex = 0
    for category in session.query(Definitions, Categories). \
            join(Categories, Definitions.CategoriesID == Categories.ID). \
            filter(Definitions.ComponentID == componentid).order_by(Definitions.CategoryOrder):
        form.categoryid.id.append(category.Categories.ID)
        form.categoryid.name.append(category.Categories.Name)
        form.categoryid.listorder.append(category.Definitions.CategoryOrder)
        catsearch.listorder.append(catsearchindex)
        catsearch.id.append([])
        catsearch.name.append([])
        catsearch.id[catsearchindex] = category.Categories.ID
        catsearch.name[catsearchindex] = category.Categories.Name
        catsearchindex += 1
    print catsearch.listorder
    print catsearch.name
    form.feature.label = []
    form.feature.name = []
    for feature in session.query(Features). \
            filter(Features.CategoriesID == form.categoryid.id[-1]).order_by(Features.ListOrder):
        form.feature.label.append(feature.Name)
        if feature.StrValue is not None:
            form.feature.name.append(feature.StrValue)
        else:
            form.feature.name.append(str(feature.IntValue))

    return render_template('componentform.html', form=form, numcats=len(form.categoryid.id),
                           numfeatures = len(form.feature.label))

app.run(debug=True)