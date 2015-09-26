__author__ = 'Bernard'

from models import Components, Base, Locations, Suppliers
from sqlalchemy import create_engine

engine = create_engine('sqlite:///database//components.db', echo=False)
Base.metadata.bind = engine

from sqlalchemy.orm import sessionmaker
DBSession = sessionmaker()
DBSession.bind = engine
session = DBSession()

# select components.Name as component, suppliers.Name as supplier,
# locations.Name as location
# from components
# left outer join suppliers
# on components.SuppliersID = suppliers.ID
# left outer join locations
# on components.locationsID = locations.ID

# find_statement = select([Components.Name,Suppliers.Name,Locations.Name], use_labels=True).where(
#     Components.SuppliersID==Suppliers.ID and Components.LocationsID==Locations.ID)
# data = session.execute(find_statement)
# for row in data.fetchall():
#     print row['locations_Name'], row['components_Name']
#     print row.keys()

#for name, description, location in
# data = []
# for (name, description, location, datasheet) in \
print "Before query"
q = session.query(Components.Name, Suppliers.Name, Locations.Name).\
        outerjoin(Suppliers, Components.SuppliersID == Suppliers.ID).\
        outerjoin(Locations, Components.LocationsID == Locations.ID).filter(Components.ID == 1).one()
#    data.append((name,description,location))
print "After query"
print "Read:",q
#name, description, location
#data = session.query(Components).all()
# for each_component in data:
#     print each_component.Components_Name, each_component.Suppliers_Name