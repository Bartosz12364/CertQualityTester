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
    secureRenego = Column(Boolean)  # true
    compression = Column(String)  # "NONE"
    expansion = Column(String)  # "NONE"
    sessionLifetimeHint = Column(Integer)  # 100800
    x509ChainDepth = Column(Integer)  # 2
    verifyCertResult = Column(Boolean)  # true
    verifyHostResult = Column(Boolean)  # true
    ocspStapled = Column(Boolean)  # true
    verifyOcspResult = Column(Boolean)  # true
    tlsVersions = relationship('TlsVersions', backref='ScanResult')
    certificateChain = relationship('CertificateChain', backref='ScanResult')

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)


class TlsVersionsEnum(enum.Enum):
    TLSV1 = "TLSv1"
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
    scan_id = Column(Integer, ForeignKey('scanresult.id'))
    scan = relationship('ScanResult', foreign_keys=[scan_id])
    version = Column(Integer)    # "version": 3,
    subject = Column(String)    # "subject": "CN=e-sett.ffrontier.com; OU=Mizuho Financial Group 1; O=Mizuho Bank, Ltd.; L=CHIYODA-KU; ST=Tokyo; C=JP; serialNumber=010001008845; jurisdictionC=JP; businessCategory=Private Organization",
    issuer = Column(String)   # "issuer": "CN=DigiCert SHA2 Extended Validation Server CA; OU=www.digicert.com; O=DigiCert Inc; C=US",
    subjectCN = Column(String)   # "subjectCN": "e-sett.ffrontier.com",
    subjectAltName = Column(String)   # "subjectAltName": "DNS:e-sett.ffrontier.com",
    signatureAlg = Column(String)  # "signatureAlg": "sha256WithRSAEncryption",
    notBefore = Column(String)   # "notBefore": "Feb 20 00:00:00 2020 GMT",
    notAfter = Column(String)   # "notAfter": "Apr 27 12:00:00 2021 GMT",
    expired = Column(String)  # "expired": false,
    serialNo = Column(String)   # "serialNo": "0E:C3:1E:88:84:56:4A:06:2D:55:6B:D4:23:A3:C6:A1",
    keyUsage = Column(String)   # "keyUsage": "Digital Signature, Key Encipherment critical",
    extKeyUsage = Column(String)   # "extKeyUsage": "TLS Web Server Authentication, TLS Web Client Authentication",
    publicKeyAlg = Column(String)  # "publicKeyAlg": "RSA",
    publicKeySize = Column(Integer)  # "publicKeySize": 2048,
    basicConstraints = Column(String)   # "basicConstraints": "CA:FALSE",
    subjectKeyIdentifier = Column(String)   # "subjectKeyIdentifier": "F2:3C:C5:53:CD:E6:74:2D:FA:8D:A3:BF:53:47:04:0B:D2:FB:71:50",
    sha1Fingerprint = Column(String)  # "sha1Fingerprint": "CD:B8:A2:E0:A6:6D:E2:DA:56:4A:D2:78:0D:58:40:48:8E:FA:8B:35"

    def __init__(self, dictionary):
        for k, v in dictionary.items():
            setattr(self, k, v)