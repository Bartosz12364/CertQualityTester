from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

app = Flask(__name__)
engine = create_engine('sqlite:///sqlalchemy.sqlite', echo=True)
models.Base.metadata.create_all(engine)


@app.route('/')
def index():
    Session = sessionmaker(bind=engine)
    session = Session()
    all = session.query(models.ScanResult).count()
    results = session.execute(
        'SELECT x, count(x) FROM (SELECT max(expired) as x FROM certificatechain group by scan_id) group by x')
    expiration = {x[0]: x[1] for x in list(results)}

    self_signed = session.query(models.ScanResult).filter(
        models.ScanResult.verifyCertError == "self signed certificate").count()

    results = session.execute(
        'select x509ChainDepth, count(id) from scanresult group by x509ChainDepth')
    depth = {x[0]: x[1] for x in list(results)}

    results = session.execute(
        'select tlsversion, count(id) from tlsversions group by tlsVersion')
    tls = {x[0]: x[1] for x in list(results)}

    results = session.execute(
        'select cipherSuite, count(id) from ciphersuite group by cipherSuite')
    cipher = {x[0]: x[1] for x in list(results)}
    print(cipher.keys())
    del tls["UNKNOWN"]

    results = session.execute(
        'select signatureAlg, count(id) from certificatechain group by signatureAlg')
    signature_alg = {x[0]: x[1] for x in list(results)}

    s = set()
    for cipher_suite in cipher.keys():
        for name in cipher_suite.split('-'):
            s.add(name)
    d = dict.fromkeys(s, None)
    print(d)
    for cipher_name in s:
        for cipher_suite in cipher.keys():
            if cipher_name in cipher_suite.split('-'):
                print(f'true, {cipher_name}, {cipher_suite}')
                cipher_tup = [cipher_suite, cipher[cipher_suite]]
                print(cipher_tup)
                if d[cipher_name] is None:
                    d[cipher_name] = list()
                d[cipher_name].append(cipher_tup)

    for key in d.keys():
        print(key)
        print(f'    {d[key]}')

    del d["256"]
    del d["128"]

    results = session.execute(
        'select tempPublicKeyAlg, count(id) from scanresult group by tempPublicKeyAlg')
    tempPublicKeyAlg = {x[0]: x[1] for x in list(results)}
    return render_template('index.html.jinja2', all=all, tempPublicKeyAlg=tempPublicKeyAlg, expiration=expiration,
                           self_signed=self_signed, depth=depth, tls=tls, cipher=cipher, cipherDict=d,
                           signature_alg=signature_alg)


@app.route('/keywords')
def keywords():
    Session = sessionmaker(bind=engine)
    session = Session()
    all = session.query(models.ScanResult).count()
    results = session.execute(
        'SELECT x, count(x) FROM (SELECT max(expired) as x FROM certificatechain group by scan_id) group by x')
    expiration = {x[0]: x[1] for x in list(results)}

    self_signed = session.query(models.ScanResult).filter(
        models.ScanResult.verifyCertError == "self signed certificate").count()

    results = session.execute(
        'select x509ChainDepth, count(id) from scanresult group by x509ChainDepth')
    depth = {x[0]: x[1] for x in list(results)}

    results = session.execute(
        'select tlsversion, count(id) from tlsversions group by tlsVersion')
    tls = {x[0]: x[1] for x in list(results)}

    results = session.execute(
        'select cipherSuite, count(id) from ciphersuite group by cipherSuite')
    cipher = {x[0]: x[1] for x in list(results)}
    print(cipher.keys())
    del tls["UNKNOWN"]

    results = session.execute(
        'select signatureAlg, count(id) from certificatechain group by signatureAlg')
    signature_alg = {x[0]: x[1] for x in list(results)}

    s = set()
    for cipher_suite in cipher.keys():
        for name in cipher_suite.split('-'):
            s.add(name)
    d = dict.fromkeys(s, None)
    print(d)
    for cipher_name in s:
        for cipher_suite in cipher.keys():
            if cipher_name in cipher_suite.split('-'):
                print(f'true, {cipher_name}, {cipher_suite}')
                cipher_tup = [cipher_suite, cipher[cipher_suite]]
                print(cipher_tup)
                if d[cipher_name] is None:
                    d[cipher_name] = list()
                d[cipher_name].append(cipher_tup)

    for key in d.keys():
        print(key)
        print(f'    {d[key]}')

    del d["256"]
    del d["128"]

    return render_template('keywords.html.jinja2', all=all, expiration=expiration, self_signed=self_signed, depth=depth,
                           tls=tls, cipher=cipher, cipherDict=d, signature_alg=signature_alg)
