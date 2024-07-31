def generate_json(ruta_csv, ruta_txt):
    import pandas as pd
    import json
    import re
    csvfile = pd.reader_csv(ruta_csv)
    for i in csvfile:
        regex = "\w"


    