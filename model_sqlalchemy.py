#!/usr/bin/env python
# coding: utf-8

# In[1]:


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
import json


engine = create_engine('sqlite:///sqlalchemy.sqlite', echo=True)
models.Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

with open('out.json', encoding="utf-8-sig") as f:
    data = json.load(f)

if "tlsVersions" in data:
    data['tlsVersions'] = [models.TlsVersions(tlsversion=models.TlsVersionsEnum(i)) for i in data['tlsVersions']]
elif "tlsVersion" in data:
    data['tlsVersions'] = [models.TlsVersions(tlsversion=models.TlsVersionsEnum(data['tlsVersion']))]
data['certificateChain'] = [models.CertificateChain(i) for i in data['certificateChain']]
if 'czipherSuite' in data:
    del data['cipherSuite']


sr = models.ScanResult(data)
session.add(sr)
session.commit()
print(sr.id)
