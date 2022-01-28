from kubeql.db_driver import get_new_db, clear_collection
from crawler import load_into_db
from kubeql.constants import KUBE_MANIFEST_DB, MANIFEST_COLLECTION

import sys
db = None

def main():
    global db
    db = get_new_db(KUBE_MANIFEST_DB)
    clear_collection(db, MANIFEST_COLLECTION)
    load_into_db(db, sys.argv[1], True)
    print("db object now available!")


if __name__ == "__main__":
    if len(sys.argv) <= 1:
        print("expect one arg, dir")
        sys.exit(1)
    main()
