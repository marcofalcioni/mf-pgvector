import sys
from loguru import logger
from pgvector.psycopg import register_vector, Bit
import psycopg
from rdkit import Chem
from rdkit.Chem import AllChem


def generate_fingerprint(fpgen, molecule):    
    return fpgen.GetFingerprintAsNumPy(Chem.MolFromSmiles(molecule))

def init_connection(conninfo):
    conn = psycopg.connect(conninfo, autocommit=True)

    register_vector(conn)

    conn.execute('DROP TABLE IF EXISTS molecules')
    conn.execute('CREATE TABLE molecules (id text PRIMARY KEY, fingerprint bit(2048))')
    return conn
    
def load_molecules(fpgen, molecules, conn):
    with open(molecules, 'r') as f:
        for row in f.readlines():
            molecule = row.strip()
            fingerprint = generate_fingerprint(fpgen, molecule)
            conn.execute('INSERT INTO molecules (id, fingerprint) VALUES (%s, %s)', (molecule, Bit(fingerprint)))

    
def main(argv):
    if len(argv) != 3:
        print("Usage: %s <query_molecule> <molecules>" % argv[0])
        sys.exit(1)
    query_molecule = argv[1]
    molecules = argv[2]
    
    fpgen = AllChem.GetMorganGenerator()

    conninfo='postgresql://postgres:postgres@localhost/postgres'
    conn = init_connection(conninfo)
    
    load_molecules(fpgen, molecules, conn)

    query_fingerprint = generate_fingerprint(fpgen, query_molecule)
    result = conn.execute('SELECT id, fingerprint <%%> %s AS distance FROM molecules ORDER BY distance LIMIT 5', (Bit(query_fingerprint),)).fetchall()
    for row in result:
        logger.info(row)
    
    
if __name__ == '__main__':
    main(sys.argv)