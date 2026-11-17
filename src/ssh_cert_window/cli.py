import argparse, json, sys
from pathlib import Path
from .core import inspect_certificate, parse_key_info

def main():
    p=argparse.ArgumentParser(description="Audit OpenSSH certificate validity windows")
    p.add_argument("certificate", help="OpenSSH certificate file")
    p.add_argument("--warn-days",type=int,default=14)
    p.add_argument("--fixture",action="store_true",help="parse ssh-keygen -L text fixture instead of invoking ssh-keygen")
    p.add_argument("--json",action="store_true")
    a=p.parse_args()
    if a.warn_days<0: p.error("--warn-days must be non-negative")
    try:
        result=parse_key_info(Path(a.certificate).read_text(),warn_days=a.warn_days) if a.fixture else inspect_certificate(a.certificate,a.warn_days)
    except (OSError,ValueError,RuntimeError) as e:
        print(f"error: {e}",file=sys.stderr); return 2
    if a.json: print(json.dumps(result,indent=2))
    else:
        print(f"Status: {result['status']}\nKey ID: {result['key_id'] or '(unknown)'}\nPrincipals: {', '.join(result['principals']) or '(none)'}\nValid until: {result['valid_before']}\nDays remaining: {result['days_remaining']}")
    return 1 if result['status'] in {"EXPIRED","EXPIRING_SOON","NOT_YET_VALID"} else 0
if __name__=="__main__": raise SystemExit(main())
