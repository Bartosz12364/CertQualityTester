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

    self_signed = session.query(models.ScanResult).filter(models.ScanResult.verifyCertError == "self signed certificate").count()

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
    return render_template('index.html.jinja2', all=all, expiration=expiration, self_signed=self_signed, depth=depth, tls=tls, cipher=cipher)
