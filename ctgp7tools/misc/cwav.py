import struct

class CWAV:
  _STRUCT_ = ("<4sH","H II HH IIII")

  def __init__(self, fd):
    off = fd.tell()
    
    magic, self.endian = struct.unpack(self._STRUCT_[0], fd.read(struct.calcsize(self._STRUCT_[0])))
    self.endian = ">" if self.endian == 0xFFFE else "<"

    assert(magic == b'CWAV')

    a,a,self.fileSize,a,a,a,a,a,a = \
      struct.unpack(self.endian + self._STRUCT_[1], fd.read(struct.calcsize("<"+self._STRUCT_[1])))

    fd.seek(off)
    self.data = fd.read(self.fileSize)
