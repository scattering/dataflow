#---------------------------------------------------------------------------
# Makefile for the PyUB 
# machine-dependent part for Redhat Linux with AFS at PSI
#
# Mark Koennecke, November 1996
# Markus Zolliker, March 2003
# Nick Maliszewskyj, February 2006
#--------------------------------------------------------------------------

CC	= gcc
CFLAGS	= -mno-cygwin  
LIBDIRS = c:/ubmatrix/matrix \
	c:/python24/libs \
	c:/python24/PCBUILD
LIBS	= -L matrix -lmatrix 
#LIBS = matrix/libmatrix.a
LDFLAGS = -shared -s


OBJ=	trigd.o \
	cell.o
all: cell

cell:	$(OBJ)
	$(CC) $(CFLAGS) $(LDFLAGS) $(OBJ) $(LIBS) -o cell

trigd.o:	trigd.c trigd.h 
cell.o:	cell.c cell.h trigd.h

clean:
	rm -f *.o
	rm -f *.a
	rm -R build

