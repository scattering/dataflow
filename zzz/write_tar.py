import tarfile
import StringIO

tar = tarfile.TarFile("test.tar","w")

string = StringIO.StringIO()
string.write("hello")
string.seek(0)
info = tarfile.TarInfo(name="foo")
info.size=len(string.buf)
tar.addfile(tarinfo=info, fileobj=string)

tar.close()
