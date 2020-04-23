#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Boolean, Enum, ForeignKey
import enum

Base = declarative_base()


# In[2]:


class ScanResult(Base):
    __tablename__ = 'scanresult'
    id = Column(Integer, primary_key=True)

    host = Column(String)  # "search.yahoo.com"
    ip = Column(String)  # , unique=True)  # "212.82.100.137"
    port = Column(Integer)  # 443
    elapsedTime = Column(Integer)  # 2143
    cipher = Column(String)  # "ECDHE-RSA-AES128-GCM-SHA256 TLScustomer_id = db.Column(db.Integer, db.ForeignKey('customers.id'))
    tempPublicKeyAlg = Column(String)  # "ECDH prime256v1"
    tempPublicKeySize = Column(Integer)  # 256
    secureRenego = Column(Boolean) # true 
    compression = Column(String)  # "NONE"
    expansion = Column(String)  # "NONE"
    sessionLifetimeHint = Column(Integer)  # 100800
    x509ChainDepth = Column(Integer)  # 2
    verifyCertResult = Column(Boolean) # true
    verifyHostResult = Column(Boolean) # true
    ocspStapled = Column(Boolean) # true
    verifyOcspResult = Column(Boolean) # true
    tlsVersions = relationship('TlsVersions', backref='ScanResult')

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)

class TlsVersionsEnum(enum.Enum):
    TLSV1   = "TLSv1"
    TLSV1_1 = "TLSv1_1"
    TLSV1_2 = "TLSv1_2"
    TLSV1_3 = "TLSv1_3"
    
class TlsVersions(Base):
    __tablename__ = 'tlsversions'
    id = Column(Integer, primary_key=True)
    
    scan_id = Column(Integer, ForeignKey('scanresult.id'))
    scan = relationship('ScanResult', foreign_keys=[scan_id])
    
    tlsversion = Column(Enum(TlsVersionsEnum), nullable=True)

class CipherSuite(Base):
    __tablename__ = 'ciphersuite'
    id = Column(Integer, primary_key=True)
    
    placeholder = Column(String) 


class CertificateChain(Base):
    __tablename__ = 'certificatechain'
    id = Column(Integer, primary_key=True)
    
    placeholder = Column(String) 


# In[3]:


engine = create_engine('sqlite:///sqlalchemy.sqlite', echo=True)
Base.metadata.create_all(engine)


# In[4]:


# tworzenie sesji dla danej bazy:
Session = sessionmaker(bind=engine)
session = Session()


# In[15]:


import json

with open('yahoo.json') as f:
    data = json.load(f)


# In[16]:


# data postprocessing
#del data['tlsVersions']
data['tlsVersions'] =  [TlsVersions(tlsversion=TlsVersionsEnum(i)) for i in data['tlsVersions']]
del data['cipherSuite']
del data['certificateChain']
data


# In[17]:


sr = ScanResult(data)
#tr = TlsVersions(scan_id=sr.id, tlsversion=TlsVersionsEnum.TLSV1)
session.add(sr)
#session.add(tr)
session.commit()
print(sr.id)
