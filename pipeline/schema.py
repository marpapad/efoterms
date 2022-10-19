from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime, String, Boolean, UniqueConstraint, ForeignKey
from sqlalchemy.schema import Index
from sqlalchemy.orm import relationship, backref

Base = declarative_base()

class Pages(Base):
    """
    OLS page inserted table blueprint
    
    """
    __tablename__  = 'pages'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    page = Column('page',Integer, nullable=False)
    elements = Column('elements',Integer, nullable=False)
    createdat = Column('createdat',DateTime, nullable=False)
    
    __table_args__ = (UniqueConstraint('page'),Index('page_idx','page'),)

    def __init__(self, page, elements, createdat):
        self.page = page
        self.elements = elements
        self.createdat = createdat

    def __repr__(self):
        return "<Pages(page='{}', elements='{}', created={})>"\
                .format(self.page, self.elements, self.createdat)
                
                
class Term(Base):
    """
    EFO term table blueprint
    
    """
    __tablename__ = 'term'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    label = Column('label',String, nullable=False)
    iri = Column('iri',String, nullable=False)
    is_obsolete = Column('is_obsolete',Boolean)
    term_replaced_by = Column('term_replaced_by',String)
    is_defining_ontology = Column('is_defining_ontology',Boolean)
    has_children = Column('has_children',Boolean)
    is_root = Column('is_root',Boolean)
    is_preferred_root = Column('is_preferred_root',Boolean)
    createdat = Column('createdat',DateTime, nullable=False)
    
    __table_args__ = (UniqueConstraint('iri'),Index('term_label_idx','label'),)
        
    def __init__(self, label, iri, is_obsolete, term_replaced_by, is_defining_ontology, has_children, is_root, is_preferred_root, createdat):
        self.label = label
        self.iri = iri
        self.is_obsolete = is_obsolete
        self.term_replaced_by = term_replaced_by
        self.is_defining_ontology = is_defining_ontology
        self.has_children = has_children
        self.is_root = is_root
        self.is_preferred_root = is_preferred_root
        self.createdat = createdat

    def __repr__(self):
        return "<Term(label='{}', iri='{}', is_obsolete='{}', term_replaced_by='{}', is_defining_ontology='{}', has_children='{}', is_root='{}', is_preferred_root='{}', created={})>"\
                .format(self.label, self.iri, self.is_obsolete, self.term_replaced_by, self.is_defining_ontology, self.has_children, self.is_root, self.is_preferred_root, self.createdat)

                
class Description(Base):
    """
    EFO term descriptions table blueprint
    
    """
    __tablename__ = 'description'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    description = Column('label',String,nullable=False)
    term_id = Column('term_id', Integer, ForeignKey("term.id", ondelete="CASCADE"),index=True,nullable=False)
    term = relationship("Term", backref=backref("description", uselist=False, lazy="joined", cascade="delete-orphan,all"))   
    
    def __init__(self,description,term):
        self.description = description
        self.term = term
    
    def __repr__(self):
        return "<Description(description='%s')>" % self.description

    
class Synonym(Base):
    """
    EFO term synonyms table blueprint
    
    """
    __tablename__ = 'synonym'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    synonym = Column('synonym',String, nullable=False)
    term_id = Column('term_id', Integer, ForeignKey("term.id", ondelete="CASCADE"),index=True,nullable=False)
    term = relationship("Term", backref=backref("synonym", uselist=False, lazy="joined", cascade="delete-orphan,all"))
    
    def __init__(self,synonym,term):
        self.synonym = synonym
        self.term = term 
        
    def __repr__(self):
        return "<Synonym(synonym='%s')>" % self.synonym   

        
class Ontology(Base):
    """
    EFO term ontology table blueprint
     
    """
    __tablename__ = 'ontology'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    ontology = Column('ontology',String, nullable=False)
    term_id = Column('term_id', Integer, ForeignKey("term.id", ondelete="CASCADE"),index=True,nullable=False)
    term = relationship("Term", backref=backref("ontology", uselist=False, lazy="joined", cascade="delete-orphan,all"))
    
    def __init__(self,ontology,term):
        self.ontology = ontology
        self.term = term
    
    def __repr__(self):
        return "<Ontology(ontology='%s')>" % self.ontology      

    
class MeSH(Base):
    """
     MeSH term references table blueprint
     
    """
    __tablename__ = 'mesh'
    
    pid = Column('id',Integer, primary_key=True, autoincrement=True)
    database = Column('database',String, nullable=False)
    id = Column('ref_id',String, nullable=False)
    description = Column('description',String)
    url = Column('url',String)
    term_id = Column('term_id', Integer, ForeignKey("term.id", ondelete="CASCADE"),index=True,nullable=False)
    term = relationship("Term", backref=backref("mesh", uselist=False, lazy="joined", cascade="delete-orphan,all"))
    
    def __init__(self,database,id,description,url,term):
        self.database = database
        self.id = id
        self.description = description
        self.url = url
        self.term = term
           
    def __repr__(self):
        return "<MeSH(database='{}', ref_id='{}', description='{}', url='{}')>"\
                .format(self.database, self.id, self.description, self.url)

    