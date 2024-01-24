from io import BytesIO, IOBase

from ctgp7tools import vprint

class IPS:
    @staticmethod
    def patch(file, patch):
        fi = file
        fp = patch

        if not isinstance(file, IOBase):
            fi = open(file, "r+b")
        if not isinstance(patch, IOBase):
            fp = BytesIO(patch)
        
        vprint(f"Patching {fi.name} from {fp.name if hasattr(fp,'name') else '<bytes>'}...")
        
        if fp.read(5)!=b'PATCH':
            fi.close(); fp.close()
            raise Exception("Patch file is not a valid IPS")

        while True:
            off = fp.read(3)
            if off == b"EOF": break
            off = int.from_bytes(off, "big")
            size = int.from_bytes(fp.read(2), "big")
            fi.seek(off)
            if size == 0:
                size = int.from_bytes(fp.read(2), "big")
                fi.write(fp.read(1)*size)
            else:
                fi.write(fp.read(size))
        
        off = fp.read(3)
        if len(off) == 3:
        	fi.truncate(int.from_bytes(off, "big"))
            
        fi.close(); fp.close()