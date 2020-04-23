from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
import json

if __name__ == "__main__":
    engine = create_engine('sqlite:///sqlalchemy.sqlite', echo=True)
    models.Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    with open('out.json', encoding="utf-8-sig") as f:
        dataset = json.load(f)

    for data in dataset:
        if "tlsVersions" in data:
            data['tlsVersions'] = [models.TlsVersions(tlsversion=models.TlsVersionsEnum(i)) for i in data['tlsVersions']]
        data['certificateChain'] = [models.CertificateChain(i) for i in data['certificateChain']]
        if 'cipherSuite' in data:
            del data['cipherSuite']

        sr = models.ScanResult(data)
        session.add(sr)
        session.commit()

