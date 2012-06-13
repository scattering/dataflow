#---------------------------------------------------------------------------
# Makefile for the Matrix library
# machine-dependent part for Redhat Linux with AFS at PSI
#
# Mark Koennecke, November 1996
# Markus Zolliker, March 2003
# Nick Maliszewskyj, February 2006
#--------------------------------------------------------------------------

CC       = gcc
CFLAGS   = -g $(DFORTIFY) -Wall

OBJ=   matadd.o matcreat.o matdet.o matdump.o matdurbn.o materr.o \
       matinv.o matmul.o matsolve.o matsub.o matsubx.o mattoepz.o \
       mattran.o

all: libmatrix.a

libmatrix.a: $(OBJ)
	- rm -f libmatrix.a
	ar cr libmatrix.a $(OBJ)
	ranlib libmatrix.a

clean:
	rm -f *.o
	rm -f *.a

