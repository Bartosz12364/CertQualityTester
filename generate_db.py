from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
import json
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("input", type=str, help="Input .json file")
    args = parser.parse_args()
    engine = create_engine('sqlite:///sqlalchemy.sqlite', echo=True)
    models.Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    with open(args.input, encoding="utf-8-sig") as f:
        dataset = json.load(f)

    for data in dataset:
        if "tlsVersions" in data:
            data['tlsVersions'] = [models.TlsVersions(tlsversion=models.TlsVersionsEnum(i)) for i in
                                   data['tlsVersions']]
        data['certificateChain'] = [models.CertificateChain(i) for i in data['certificateChain']]
        if "cipherSuite" in data:
            data['cipherSuite'] = [models.CipherSuite(cipherSuite=i) for i in data['cipherSuite']["supported"]]

        sr = models.ScanResult(data)
        session.add(sr)
    session.commit()