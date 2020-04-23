from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import models
import collections
import matplotlib.pyplot as plt


def plot_counter(w, title, xlabel, ylabel):
    plt.bar(w.keys(), w.values())
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.show()


if __name__ == "__main__":
    engine = create_engine('sqlite:///sqlalchemy.sqlite', echo=True)
    models.Base.metadata.create_all(engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    scanresults = session.query(models.ScanResult).all()

    size = len(scanresults)
    tls_distrib = collections.Counter([x.tlsVersion for x in scanresults])
    chain_depths = collections.Counter([x.x509ChainDepth for x in scanresults])

    #   plot_counter(tls_distrib, f'TLS version used ({size} hosts)', 'TLS version', 'number of hosts')
    plot_counter(chain_depths, f'X509 chain depth plot ({size} hosts scanned)', 'X509 chain depth', 'X509 chain depth')

    print(tls_distrib)
    print(chain_depths)
