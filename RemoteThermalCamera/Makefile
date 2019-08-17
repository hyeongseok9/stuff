CC=gcc
CXX=g++
RM=rm -f
#CPPFLAGS=-g $(shell root-config --cflags)
CPPFLAGS=-g -Wall -std=c++11 -I/home/pi/git_repo/mlx90640-library
#LDFLAGS=-g $(shell root-config --ldflags)
LDFLAGS=-g -L/usr/local/lib/ -L:/home/pi/mlx90640-library 
#LDLIBS=$(shell root-config --libs)
LDLIBS= -lzmq -lbcm2835 libMLX90640_API.a /usr/local/lib/libbcm2835.a
INCLUDES= -I/usr/local -I/home/pi/git_repo/mlx90640-library

SRCS=src/rm.cc 
OBJS=$(subst .cc,.o,$(SRCS)) src/fb.o

all: remoteCamera

remoteCamera: $(OBJS) libMLX90640_API.a
	$(CXX) $(CPPFLAGS) $(LDFLAGS) -o rm $(OBJS) $(LDLIBS) 

bcm2835-1.55.tar.gz:	
	wget http://www.airspayce.com/mikem/bcm2835/bcm2835-1.55.tar.gz

bcm2835-1.55: bcm2835-1.55.tar.gz
	tar xzvf bcm2835-1.55.tar.gz

bcm2835: bcm2835-1.55
	cd bcm2835-1.55; ./configure; make; sudo make install


depend: .depend

.depend: $(SRCS)
	$(RM) ./.depend
	$(CXX) $(CPPFLAGS) -MM $^>>./.depend;

clean:
	$(RM) $(OBJS)

distclean: clean
	$(RM) *~ .depend

include .depend
