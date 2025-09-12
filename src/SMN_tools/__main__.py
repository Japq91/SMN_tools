# __main__.py
#### EJEMPLO DE EJECCUCION
# python -m SMN_tools --modelo WRF --gribfile WRFPRS_d01.00 --out ./salida --tipo pr wind10m
 
##############################################
import argparse
from . import extrac_ETA, extrac_WRF

def main():
    parser = argparse.ArgumentParser(description="Extraer variables de ETA o WRF")
    parser.add_argument("--modelo", choices=["ETA","WRF"], required=True)
    parser.add_argument("--gribfile", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--tipo", nargs="+", required=True)
    args = parser.parse_args()

    if args.modelo == "ETA":
        extrac_ETA(args.out, args.gribfile, args.tipo)
    elif args.modelo == "WRF":
        extrac_WRF(args.out, args.gribfile, args.tipo)

if __name__ == "__main__":
    main()

