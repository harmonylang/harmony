all:
	gcc -pthread -g -Og hny_fuse.c fuse_queue.c -o hny_fuse `pkg-config fuse --cflags --libs` 

clean:
	rm -f *.hvm hny_fuse
