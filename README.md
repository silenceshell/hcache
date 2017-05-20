## hcache - a tool fork from pcstat, plus showing top X max cache files 

The pcstat tool can get page cache statistics for one file by the file's name,
or all cached files for a process by the process's pid.

However, I often meet with a question: I can find out that the linux os cached 
quite a lot by checking the meminfo, but I do not know which BIG files is being cached.
Of course I can use the `ps aux` command to get those processes who used a lot of 
memory and get the details by the `pcstat --pid [pid]`, but `pcstat` does not sort 
the result, it is not convenient.

So I add a feature to pcstat: you can use the option `--top [X]` to show 
the top X cached files. After that, you can use `lsof` to find out the bad
guy.

## Usage

hcache keep the options use by pcstat, 

```
$ sudo hcache --top 10
[sudo] password for silenceshell: 
+----------------------------------------------------------------------------------+----------------+------------+-----------+---------+
| Name                                                                             | Size (bytes)   | Pages      | Cached    | Percent |
|----------------------------------------------------------------------------------+----------------+------------+-----------+---------|
| /opt/google/chrome/chrome                                                        | 114911208      | 28055      | 25457     | 090.740 |
| /usr/share/code/code                                                             | 67688720       | 16526      | 12274     | 074.271 |
| /home/bottle/Software/pycharm-community-2016.2/lib/pycharm.jar                   | 95177431       | 23237      | 11325     | 048.737 |
| /opt/atom/atom                                                                   | 62641344       | 15294      | 10578     | 069.164 |
| /usr/bin/dockerd                                                                 | 39121168       | 9552       | 7103      | 074.361 |
| /home/bottle/Software/pycharm-community-2016.2/jre/jre/lib/amd64/libjfxwebkit.so | 57455824       | 14028      | 6625      | 047.227 |
| /usr/lib/x86_64-linux-gnu/libQtWebKit.so.4.10.2                                  | 36462184       | 8902       | 6316      | 070.950 |
| /usr/lib/beyondcompare/BCompare                                                  | 30640160       | 7481       | 5505      | 073.586 |
| /usr/bin/SecureCRT                                                               | 29524560       | 7209       | 4806      | 066.667 |
| /usr/share/code/libnode.so                                                       | 21135976       | 5161       | 4588      | 088.898 |
+----------------------------------------------------------------------------------+----------------+------------+-----------+---------+
```

A common question when tuning databases and other IO-intensive applications is,
"is Linux caching my data or not?" pcstat gets that information for you using
the mincore(2) syscall.

The fincore application from [linux-ftools](https://code.google.com/p/linux-ftools/) does the
same thing and I read its source code. I chose not to use it because it appears to be abandoned
and has some build problems.

I wrote this is so that Apache Cassandra users can see if ssTables are being
cached. If $GOPATH/bin is in your PATH, this will get it installed:

    go get golang.org/x/sys/unix
    go get github.com/tobert/pcstat/pcstat
    pcstat /var/lib/cassandra/data/*/*/*-Data.db

If you don't want to mess around with building the software, binaries are provided
in orphaned branches so you can pull them down from Github with curl/wget.

    if [ $(uname -m) == "x86_64" ] ; then
        curl -L -o pcstat https://github.com/tobert/pcstat/raw/2014-05-02-01/pcstat.x86_64
    else
        curl -L -o pcstat https://github.com/tobert/pcstat/raw/2014-05-02-01/pcstat.x86_32
    fi
    chmod 755 pcstat
    ./pcstat /var/lib/cassandra/data/*/*/*-Data.db

## Usage

Command-line arguments are described below. Every argument following the program
flags is considered a file for inspection.

```
pcstat <-json <-pps>|-terse|-default> <-nohdr> <-bname> file file file
 -json output will be JSON
   -pps include the per-page information in the output (can be huge!)
 -terse print terse machine-parseable output
 -default print ascii tables
 -histo print a histogram using unicode block characters
 -nohdr don't print the column header in terse or default format
 -bname use basename(file) in the output (use for long paths)
 -plain return data with no box characters
 -unicode return data with unicode box characters

```

## Examples

### Default output

The default output is designed to be easy for humans to read at a glance
and should look nice in any fixed-width font.

```
atobey@brak ~ $ pcstat testfile3
|-----------+----------------+------------+-----------+---------|
| Name      | Size           | Pages      | Cached    | Percent |
|-----------+----------------+------------+-----------+---------|
| LICENSE   | 11323          | 3          | 0         | 000.000 |
| README.md | 6768           | 2          | 2         | 100.000 |
| pcstat    | 3065456        | 749        | 749       | 100.000 |
| pcstat.go | 9687           | 3          | 3         | 100.000 |
| testfile3 | 102401024      | 25001      | 60        | 000.240 |
|-----------+----------------+------------+-----------+---------|
```

### Terse output

Meant to be machine readable and easy to process with standard shell
tools and scripts. Note: No attempt is made to escape characters for
proper CSV at this time.

```
pcstat -terse -bname *
name,size,timestamp,mtime,pages,cached,percent
LICENSE,11323,1400767725,1400492571,3,0,0
README.md,6185,1400767725,1400767719,2,2,100
pcstat,3065456,1400767725,1400766869,749,749,100
pcstat.go,9687,1400767725,1400766807,3,3,100
testfile3,102401024,1400767725,1400761247,25001,60,0.23999040038398464
```

### JSON output

The 'status' field will always be empty unless you add the -pps flag, which
will cause status to be populated with an array of booleans, one per page
in the file indicated whether it's cached or not. This can get spammy with
big files so it's off by default.

```
atobey@brak ~ $ pcstat -json testfile3 |json_pp
[
 {
   "filename":  "testfile3",
   "size":      102401024,
   "timestamp": "2014-05-22T13:57:19.971348936Z",
   "mtime":     "2014-05-22T12:20:47.940163295Z",
   "pages":     25001,
   "cached":    60,
   "uncached":  24941,
   "percent":   0.23999040038398464,
   "status":    []
 }
]
```

### Histogram output

Your terminal and font need to support the Block Elements section of Unicode
for this to work. Even then, the output is inconsistent in my testing, so
YMMV. See http://www.unicode.org/charts/PDF/U2580.pdf

The number after the filename is the number of pages in the file. This might
be removed in the future.

```
atobey@brak ~ $ pcstat -bname -histo *
LICENSE          3 ▁▁▁
README.md        2 ██
pcstat         749 █████████████████████████████████████████████████
pcstat.go        3 ███
testfile      2560 ▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
testfile2        3 ▁▁▁
testfile3    25001 ▂▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁
```

## Testing

The easiest way to tell if this tool is working is to drop caches and do reads on files to
get things into cache.

```
atobey@brak ~/src/pcstat $ dd if=/dev/urandom of=testfile bs=1M count=10
10+0 records in
10+0 records out
10485760 bytes (10 MB) copied, 0.805698 s, 13.0 MB/s
atobey@brak ~/src/pcstat $ ./pcstat testfile
|--------------------+----------------+------------+-----------+---------|
| Name               | Size           | Pages      | Cached    | Percent |
|--------------------+----------------+------------+-----------+---------|
| testfile           | 10485760       | 2560       | 2560      | 100     |
|--------------------+----------------+------------+-----------+---------|
atobey@brak ~/src/pcstat $ echo 1 |sudo tee /proc/sys/vm/drop_caches
1
atobey@brak ~/src/pcstat $ ./pcstat testfile
|--------------------+----------------+------------+-----------+---------|
| Name               | Size           | Pages      | Cached    | Percent |
|--------------------+----------------+------------+-----------+---------|
| testfile           | 10485760       | 2560       | 0         | 0       |
|--------------------+----------------+------------+-----------+---------|
atobey@brak ~/src/pcstat $ dd if=/dev/urandom of=testfile bs=4096 seek=10 count=1 conv=notrunc
1+0 records in
1+0 records out
4096 bytes (4.1 kB) copied, 0.000468208 s, 8.7 MB/s
atobey@brak ~/src/pcstat $ ./pcstat testfile
|--------------------+----------------+------------+-----------+---------|
| Name               | Size           | Pages      | Cached    | Percent |
|--------------------+----------------+------------+-----------+---------|
| testfile           | 10485760       | 2560       | 1         | 0       |
|--------------------+----------------+------------+-----------+---------|
```

## Building

    git clone https://github.com/tobert/pcstat.git
    cd pcstat
    go build
    sudo cp -a pcstat /usr/local/bin
    pcstat /usr/local/bin/pcstat

## Requirements

Go 1.4 or higher and golang.org/x/sys/unix.

From the mincore(2) man page:

* Available since Linux 2.3.99pre1 and glibc 2.2.
* mincore() is not specified in POSIX.1-2001, and it is not available on all UNIX implementations.
* Before kernel 2.6.21, mincore() did not return correct information some mappings.

## Author

Al Tobey <atobey@datastax.com> @AlTobey

## License

Apache 2.0
