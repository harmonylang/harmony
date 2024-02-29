// Harmony file system implemented in FUSE
// For a great documentation of FUSE API, see 
// https://www.cs.hmc.edu/~geoff/classes/hmc.cs137.201801/homework/fuse/fuse_doc.html 
 
#define FUSE_USE_VERSION 30

#include <fuse.h>
#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/ipc.h>
#include <sys/shm.h>
#include <signal.h>
#include <time.h>
#include <string.h>
#include <stdlib.h>
#include <errno.h>
#include <assert.h>
#include "fuse_queue.h"

static int child_pid = 0;
static struct fuse_queue* fuse_queue;
static int shmid = -1;

// Initialize the file system
static void* hny_init(struct fuse_conn_info *conn)
{
    printf("init: fuse inits\n");

		// use fork to create Harmony server process
		child_pid = fork();
    if (child_pid == -1) {
        perror("hny_init: Error in fork");
        exit(EXIT_FAILURE);
    }
    if (child_pid == 0) {
        // Code for the child process
        printf("This is the child process (PID: %d)\n", getpid());
				execl("../harmony", "harmony", "-d", "fuse_server.hny", NULL);

        // If execl fails
        perror("hny_init: Error in execl");
        exit(EXIT_FAILURE);
    } 
		else {
        // Code for the parent process
        printf("This is the parent process (PID: %d)\n", getpid());
        printf("Child process PID: %d\n", child_pid);

				// Generate a key for the shared memory segment
				key_t key = ftok("./hny_fuse.c", 'q');
				if (key == -1) {
					perror("hny_init: ftok");
					exit(EXIT_FAILURE);
				}

				// Create a shared memory segment
				shmid = shmget(key, sizeof(struct fuse_queue), IPC_CREAT | 0666);
				if (shmid == -1) {
					perror("hny_init: shmget");
					exit(EXIT_FAILURE);
				}

				// Attach to the shared memory segment
				fuse_queue = (struct fuse_queue *)shmat(shmid, NULL, 0);
				if (fuse_queue == (struct fuse_queue *)(-1)) {
					perror("hny_init: shmat");
					exit(EXIT_FAILURE);
				}

				// init shared queue
				fuse_queue_init(fuse_queue);
				printf("hny_init: fuse_queue_init_done\n");
		}

}

// Called when the filesystem exits
static void hny_destroy(void* private_data)
{
    printf("hny_destroy: fuse destroyed\n");

	// Detach from the shared memory segment
    if (shmdt(fuse_queue) == -1) {
        perror("hny_destroy: shmdt");
        exit(EXIT_FAILURE);
    }

  // Remove the shared memory segment (optional)
	if (shmid == -1) {
			perror("hny_destroy: shmid");
			exit(EXIT_FAILURE);
	}

	if (shmctl(shmid, IPC_RMID, NULL) == -1) {
			perror("hny_destroy: shmctl");
			exit(EXIT_FAILURE);
	}

	if (kill(child_pid, SIGKILL) == 0) {
			printf("hny_destroy: SIGKILL signal sent to process %d\n", (int)child_pid);
	} else {
			perror("hny_destroy: kill");
			exit(EXIT_FAILURE);
	}
}

// Return file attributes. 
// The "stat" structure is described in detail in the stat(2) manual page.
static int hny_getattr( const char *path, struct stat *st )
{
	printf( "[getattr] Called\n" );
	printf( "\tAttributes of %s requested\n", path );
	
	st->st_uid = getuid(); // The owner of the file/directory is the user who mounted the filesystem
	st->st_gid = getgid(); // The group of the file/directory is the same as the group of the user who mounted the filesystem
	st->st_atime = time( NULL ); // The last "a"ccess of the file/directory is right now
	st->st_mtime = time( NULL ); // The last "m"odification of the file/directory is right now
	
	if (strcmp(path, "/") == 0) {
		st->st_mode = S_IFDIR | 0755;
		st->st_nlink = 2;
	}
	else if (strcmp(path, "/file0") == 0) {
		st->st_mode = S_IFREG | 0644;
		st->st_nlink = 1;
		struct request *req;
		fuse_queue_alloc_req(fuse_queue, &req);
		req->type = GETSIZE;
		req->data.getsize.ino = 0;
		fuse_queue_req_ready(fuse_queue, req);
		fuse_queue_get_reply(fuse_queue, req);
		assert(req->data.getsize.ino == 0);
		st->st_size = req->data.getsize.res_n_blocks * BLOCK_SIZE;
		fuse_queue_reply_done(fuse_queue, req);
	}
	else if (strcmp(path, "/file1") == 0) {
		st->st_mode = S_IFREG | 0644;
		st->st_nlink = 1;
		struct request *req;
		fuse_queue_alloc_req(fuse_queue, &req);
		req->type = GETSIZE;
		req->data.getsize.ino = 1;
		fuse_queue_req_ready(fuse_queue, req);
		fuse_queue_get_reply(fuse_queue, req);
		assert(req->data.getsize.ino == 1);
		st->st_size = req->data.getsize.res_n_blocks * BLOCK_SIZE;
		fuse_queue_reply_done(fuse_queue, req);
	}
	else
	{
		st->st_mode = S_IFREG | 0644;
		st->st_nlink = 1;
		st->st_size = 1024;
	}
	return 0;
}

// As getattr, but called when fgetattr(2) is invoked by the user program. 
// Usually it can just call getattr.
static int hny_fgetattr(const char* path, struct stat* stbuf, struct fuse_file_info *fi)
{
	fprintf(stderr, "hnh_fgetattr: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// This is the same as the access(2) system call.
static int hny_access(const char* path, int mask)
{
	if ( strcmp( path, "/" ) == 0 )
	{
		return 0;
	}
	else
	{
		fprintf(stderr, "hny_access: directory does not exist\n");
		return ENOENT;
	}
}

// If path is a symbolic link, fill buf with its target, up to size. 
// See readlink(2) for more details
static int hny_readlink(const char* path, char* buf, size_t size)
{
	fprintf(stderr, "hny_readlink: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Open a directory for reading
static int hny_opendir(const char* path, struct fuse_file_info* fi)
{
	if ( strcmp( path, "/" ) == 0 )
	{
		return 0;
	}
	else
	{
		fprintf(stderr, "hny_opendir: directory does not exist\n");
		errno = ENOSYS;
		return -errno;
	}
}

// Return one or more directory entries (struct dirent) to the caller. 
// This is one of the most complex FUSE functions. 
// It is related to, but not identical to, the readdir(2) and getdents(2) 
// system calls, and the readdir(3) library function. 
// Required for essentially any filesystem, since it's what makes ls and a 
// whole bunch of other things work.
static int hny_readdir( const char *path, void *buffer, fuse_fill_dir_t filler, off_t offset, struct fuse_file_info *fi )
{
	printf( "--> Getting The List of Files of %s\n", path );
	
	filler( buffer, ".", NULL, 0 ); // Current Directory
	filler( buffer, "..", NULL, 0 ); // Parent Directory
	
	if ( strcmp( path, "/" ) == 0 ) // If the user is trying to show the files/directories of the root directory show the following
	{
		filler( buffer, "file0", NULL, 0 );
		filler( buffer, "file1", NULL, 0 );
	}
	
	return 0;
}

// Make a plain file, special (device) file, FIFO, or socket. 
// See mknod(2) for most details. 
static int hny_mknod(const char* path, mode_t mode, dev_t rdev)
{
	fprintf(stderr, "hny_mknod: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Make a plain file. This is a less flexible version of mknod. 
static int hny_create(const char* path, mode_t mode, struct fuse_file_info* fi)
{
	fprintf(stderr, "hny_create: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Create a directory with the given name. The directory permissions are 
// encoded in mode. See mkdir(2) for details.
static int hny_mkdir(const char* path, mode_t mode)
{
	fprintf(stderr, "hny_mkdir: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Remove (delete) the given file, symbolic link, hard link, or special node—
// but NOT a directory. See unlink(2) for details.
static int hny_unlink(const char* path)
{
	fprintf(stderr, "hny_unlink: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Remove the given directory. This should succeed only if the directory is 
// empty (except for "." and ".."). See rmdir(2) for details.
static int hny_rmdir(const char* path)
{
	fprintf(stderr, "hny_rmdir: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Create a symbolic link named "from" which, when evaluated, will lead to "to".
static int hny_symlink(const char* to, const char* from)
{
	fprintf(stderr, "hny_symlink: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Rename the file, directory, or other object "from" to the target "to". 
// Note that the source and target don't have to be in the same directory
// Also note that if the target already exists, it must be atomically replaced
static int hny_rename(const char* from, const char* to)
{
	fprintf(stderr, "hny_rename: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Create a hard link between "from" and "to". 
static int hny_link(const char* from, const char* to)
{
	fprintf(stderr, "hny_link: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Change the mode (permissions) of the given object to the given new permissions. 
static int hny_chmod(const char* path, mode_t mode)
{
	fprintf(stderr, "hny_chmod: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Change the given object's owner and group to the provided values. 
// See chown(2) for details. 
// NOTE: FUSE doesn't deal particularly well with file ownership, since it 
// usually runs as an unprivileged user and this call is restricted to the 
// superuser. It's often easier to pretend that all files are owned by the user 
// who mounted the filesystem, and to skip implementing this function.
static int hny_chown(const char* path, uid_t uid, gid_t gid)
{
	fprintf(stderr, "hny_chown: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Truncate or extend the given file so that it is precisely size bytes long. 
// See truncate(2) for details. This call is required for read/write 
// filesystems, because recreating a file will first truncate it.
static int hny_truncate(const char* path, off_t size)
{
	fprintf(stderr, "hny_truncate: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// As truncate, but called when ftruncate(2) is called by the user program. 
// Usually this can just call truncate.
static int hny_ftruncate(const char* path, off_t size, struct fuse_file_info* fi)
{
	fprintf(stderr, "hny_ftruncate: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Update the last access time of the given object from ts[0] and the last 
// modification time from ts[1]. 
static int hny_utimens(const char* path, const struct timespec ts[2])
{
	fprintf(stderr, "hny_utimens: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Open a file. If not using file handles, this function should just check for 
// existence and permissions and return either success or an error code.
static int hny_open(const char* path, struct fuse_file_info* fi)
{
	fprintf(stderr, "hny_open: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Read size bytes from the given file into the buffer buf, beginning offset 
// bytes into the file. See read(2) for full details. Returns the number of 
// bytes transferred, or 0 if offset was at or beyond the end of the file. 
// Required for any sensible filesystem.
static int hny_read(const char *path, char *buf, size_t size, off_t offset, struct fuse_file_info *fi)
{
	// only support reading n contiguous blocks
	// TODO lots of room for improvement - e.g in POSIX, the entire read() call 
	// should be atomic, but here it is not - only each block read is atomic

	// translate byte read to block read
	assert(offset % BLOCK_SIZE == 0);
	assert(size % BLOCK_SIZE == 0);
	printf("--> [Trying to read] path: %s; size: %lu; offset: %lu\n", path, size, offset);
	
	if (strcmp(path, "/file0") == 0) {
		size_t total_read = 0;
		struct request *req;
		while (size > 0) {
			fuse_queue_alloc_req(fuse_queue, &req);
			req->type = READ;
			req->data.read.ino = 0;
			req->data.read.offset = (offset / BLOCK_SIZE);
			fuse_queue_req_ready(fuse_queue, req);
			fuse_queue_get_reply(fuse_queue, req);
			assert(req->data.read.ino == 0);
			if (req->data.read.res_code == 0) {
				// block exists
				memcpy(buf, req->data.read.res_block_data, BLOCK_SIZE);
				fuse_queue_reply_done(fuse_queue, req);
			}
			else {
				// block does not exist
				fuse_queue_reply_done(fuse_queue, req);
				break;
			}
			offset += BLOCK_SIZE;
			size -= BLOCK_SIZE;
			buf += BLOCK_SIZE;
			total_read += BLOCK_SIZE;
		}
		return total_read;
	}
	else if (strcmp(path, "/file1") == 0) {
		size_t total_read = 0;
		struct request *req;
		while (size > 0) {
			fuse_queue_alloc_req(fuse_queue, &req);
			req->type = READ;
			req->data.read.ino = 1;
			req->data.read.offset = (offset / BLOCK_SIZE);
			fuse_queue_req_ready(fuse_queue, req);
			fuse_queue_get_reply(fuse_queue, req);
			assert(req->data.read.ino == 1);
			if (req->data.read.res_code == 0) {
				// block exists
				memcpy(buf, req->data.read.res_block_data, BLOCK_SIZE);
				fuse_queue_reply_done(fuse_queue, req);
			}
			else {
				// block does not exist
				fuse_queue_reply_done(fuse_queue, req);
				break;
			}
			offset += BLOCK_SIZE;
			size -= BLOCK_SIZE;
			buf += BLOCK_SIZE;
			total_read += BLOCK_SIZE;
		}
		return total_read;
	}
	else {
		printf("hny_read: file does not exist!");
		return 0;
	}
}

// As for read above, except that it can't return 0.
static int hny_write(const char* path, const char *buf, size_t size, off_t offset, struct fuse_file_info* fi)
{
	// only support writing an entire block
	// translate byte write to block write
	assert(offset % BLOCK_SIZE == 0);
	assert(size == BLOCK_SIZE);
	assert(strlen(buf) == BLOCK_SIZE);
	printf("--> [Trying to write] path: %s; buf: %s; size: %lu; offset: %lu\n", path, buf, size, offset);
	if (strcmp(path, "/file0") == 0) {
		struct request *req;
		fuse_queue_alloc_req(fuse_queue, &req);
		req->type = WRITE;
		req->data.write.ino = 0;
		req->data.write.offset = (offset / BLOCK_SIZE);
		memcpy(req->data.write.block_data, buf, size);
		fuse_queue_req_ready(fuse_queue, req);
		fuse_queue_get_reply(fuse_queue, req);
		assert(req->data.write.ino == 0);
		fuse_queue_reply_done(fuse_queue, req);
		return size;
	}
	else if (strcmp(path, "/file1") == 0) {
		struct request *req;
		fuse_queue_alloc_req(fuse_queue, &req);
		req->type = WRITE;
		req->data.write.ino = 1;
		req->data.write.offset = (offset / BLOCK_SIZE);
		memcpy(req->data.write.block_data, buf, size);
		fuse_queue_req_ready(fuse_queue, req);
		fuse_queue_get_reply(fuse_queue, req);
		assert(req->data.write.ino == 1);
		fuse_queue_reply_done(fuse_queue, req);
		return size;
	}
	else
	{
		fprintf(stderr, "hny_write: Wrong path\n");
		errno = ENOSYS;
		return -errno;
	}
}

// Return statistics about the filesystem. See statvfs(2) for a description of 
// the structure contents. Usually, the path can be ignored. Not required, but 
// handy for read/write filesystems since this is how programs like df 
// determine the free space.
static int hny_statfs(const char* path, struct statvfs* stbuf)
{
	fprintf(stderr, "hny_statfs: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// This is the only FUSE function that doesn't have a directly corresponding 
// system call, although close(2) is related. Release is called when FUSE is 
// completely done with a file; at that point, you can free up any temporarily 
// allocated data structures. 
static int hny_release(const char* path, struct fuse_file_info *fi)
{
	fprintf(stderr, "hny_release: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// This is like release, except for directories.
static int hny_releasedir(const char* path, struct fuse_file_info *fi)
{
	fprintf(stderr, "hny_releasedir: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Flush any dirty information about the file to disk. 
static int hny_fsync(const char* path, int isdatasync, struct fuse_file_info* fi)
{
	fprintf(stderr, "hny_fsync: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Like fsync, but for directories.
static int hny_fsyncdir(const char* path, int isdatasync, struct fuse_file_info* fi)
{
	fprintf(stderr, "hny_fsyncdir: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Called on each close so that the filesystem has a chance to report delayed errors. 
static int hny_flush(const char* path, struct fuse_file_info* fi)
{
	fprintf(stderr, "hny_flush: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Perform a POSIX file-locking operation.
static int hny_lock(const char* path, struct fuse_file_info* fi, int cmd, struct flock* locks)
{
	fprintf(stderr, "hny_lock: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// This function is similar to bmap(9).
static int hny_bmap(const char* path, size_t blocksize, uint64_t* blockno)
{
	fprintf(stderr, "hny_bmap: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Set an extended attribute. See setxattr(2). This function should be 
// implemented only if the preprocesser constant HAVE_SETXATTR is defined.
static int hny_setxattr(const char* path, const char* name, const char* value, size_t size, int flags)
{
	fprintf(stderr, "hny_setxattr: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Read an extended attribute. See getxattr(2). This function should be 
// implemented only if the preprocesser constant HAVE_SETXATTR defined.
static int hny_getxattr(const char* path, const char* name, char* value, size_t size)
{
	fprintf(stderr, "hny_getxattr: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// List the names of all extended attributes. See listxattr(2). This 
// function should be implemented only if the preprocesser constant 
// HAVE_SETXATTR is defined.
static int hny_listxattr(const char* path, const char* list, size_t size)
{
	fprintf(stderr, "hny_listxattr: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Support the ioctl(2) system call.
static int hny_ioctl(const char* path, int cmd, void* arg, struct fuse_file_info* fi, unsigned int flags, void* data)
{
	fprintf(stderr, "hny_ioctl: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

// Poll for I/O readiness. 
static int hny_poll(const char* path, struct fuse_file_info* fi, struct fuse_pollhandle* ph, unsigned* reventsp)
{
	fprintf(stderr, "hny_poll: Not implemented\n");
	errno = ENOSYS;
	return -errno;
}

static struct fuse_operations hny_operations = {
    .init        = hny_init,
    .destroy     = hny_destroy,
    .getattr     = hny_getattr,
    .fgetattr    = hny_fgetattr,
    .access      = hny_access,
    .readlink    = hny_readlink,
    .readdir     = hny_readdir,
    .mknod       = hny_mknod,
    .mkdir       = hny_mkdir,
    .symlink     = hny_symlink,
    .unlink      = hny_unlink,
    .rmdir       = hny_rmdir,
    .rename      = hny_rename,
    .link        = hny_link,
    .chmod       = hny_chmod,
    .chown       = hny_chown,
    .truncate    = hny_truncate,
    .ftruncate   = hny_ftruncate,
    .utimens     = hny_utimens,
    .create      = hny_create,
    .open        = hny_open,
    .read        = hny_read,
    .write       = hny_write,
    .statfs      = hny_statfs,
    .release     = hny_release,
    .opendir     = hny_opendir,
    .releasedir  = hny_releasedir,
    .fsync       = hny_fsync,
    .flush       = hny_flush,
    .fsyncdir    = hny_fsyncdir,
    .lock        = hny_lock,
    .bmap        = hny_bmap,
    .ioctl       = hny_ioctl,
    .poll        = hny_poll,
#ifdef HAVE_SETXATTR
    .setxattr    = hny_setxattr,
    .getxattr    = hny_getxattr,
    .listxattr   = hny_listxattr,
    .removexattr = hny_removexattr,
#endif
    .flag_nullpath_ok = 0, 
};

static struct fuse_operations operations = {
    .init       = hny_init,
    .destroy    = hny_destroy,
    .getattr	= hny_getattr,
    .readdir	= hny_readdir,
    .read		= hny_read,
};

int main( int argc, char *argv[] )
{
	return fuse_main( argc, argv, &hny_operations, NULL );
}
