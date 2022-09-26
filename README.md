## hcache - a tool fork from pcstat, with a feature that showing top X biggest cache files globally

The [pcstat](https://github.com/tobert/pcstat) tool can get page cache statistics for one file by the file's name, or all cached files for a process by the process's pid.

However, I often meet with a question: I know os cached memories by `cat /proc/meminfo` or `free`, but I can't find out those BIG files which is being cached. Of course I can use the `ps aux` command to get those processes who used a lot of memory and get the details by the `pcstat --pid [pid]`, but `pcstat` does not sort the result, and it is not convenient.

So I add a feature to pcstat: you can use the option `--top [X]` to show the top X biggest cached files globally. After that, you can use `lsof` to find out the bad guy.

## Download

I also build a bin file. You can download it from [here](https://silenceshell-1255345740.cos.ap-shanghai.myqcloud.com/hcache), have a try! I have tested it on centos7.2 and ubuntu 16.04.

## Usage

`hcache` has the same options that is used by `pcstat`, and a new option `--top [X]`. Attention, you CANNOT use both `-pid` and `-top`.

```
hcache <-json <-pps>|-terse|-default> <-nohdr> <-bname> file file file
 -json output will be JSON
   -pps include the per-page information in the output (can be huge!)
 -terse print terse machine-parseable output
 -default print ascii tables
 -histo print a histogram using unicode block characters
 -nohdr don't print the column header in terse or default format
 -bname use basename(file) in the output (use for long paths)
 -plain return data with no box characters
 -unicode return data with unicode box characters
 -pid int show all open maps for the given pid
 -top int show top x cached files in descending order
```

## Examples

```
$ sudo hcache --top 3
[sudo] password for silenceshell: 
+-------------------------------------------------+----------------+-------------+----------------+-------------+---------+
| Name                                            | Size           │ Pages       │ Cached Size    │ Cached Pages│ Percent │
|-------------------------------------------------+----------------+-------------+----------------+-------------+---------|
| /opt/apps/cn.google.chrome/files/chrome         | 170.811M       | 43728       | 120.652M       | 30887       | 70.634  |
| /opt/apps/com.visualstudio.code/files/code/code | 125.409M       | 32105       | 92.593M        | 23704       | 73.833  |
| /usr/lib/i386-linux-gnu/libLLVM-11.so.1         | 74.384M        | 19043       | 48.057M        | 12303       | 64.606  |
|-------------------------------------------------+----------------+-------------+----------------+-------------+---------|
│ Sum                                             │ 370.604M       │ 94876       │ 261.301M       │ 66894       │ 70.507  │
+-------------------------------------------------+----------------+-------------+----------------+-------------+---------+
$ 
$ sudo ./hcache --top 3  --bname  
+-----------------+----------------+-------------+----------------+-------------+---------+
| Name            | Size           │ Pages       │ Cached Size    │ Cached Pages│ Percent │
|-----------------+----------------+-------------+----------------+-------------+---------|
| chrome          | 170.811M       | 43728       | 122.030M       | 31240       | 71.442  |
| code            | 125.409M       | 32105       | 92.913M        | 23786       | 74.088  |
| libLLVM-11.so.1 | 74.384M        | 19043       | 44.486M        | 11389       | 59.807  |
|-----------------+----------------+-------------+----------------+-------------+---------|
│ Sum             │ 370.604M       │ 94876       │ 259.430M       │ 66415       │ 70.002  │
+-----------------+----------------+-------------+----------------+-------------+---------+
$ 
$ lsof /usr/lib/x86_64-linux-gnu/libQtWebKit.so.4.10.2 
COMMAND    PID   USER  FD   TYPE DEVICE SIZE/OFF    NODE NAME
quiterss 20630 silenceshell mem    REG    8,5 36462184 3936610 /usr/lib/x86_64-linux-gnu/libQtWebKit.so.4.10.2
```

## Building

hcache needs go version > 1.12 for go mod

```
git clone https://github.com/silenceshell/hcache.git
cd hcache
make build
sudo cp hcache /usr/local/bin/ 
```

## Requirements

Go 1.4 or higher and golang.org/x/sys/unix.

From the mincore(2) man page:

* Available since Linux 2.3.99pre1 and glibc 2.2.
* mincore() is not specified in POSIX.1-2001, and it is not available on all UNIX implementations.
* Before kernel 2.6.21, mincore() did not return correct information some mappings.

## Author

silenceshell

## License

Apache 2.0

## Thanks to

@tobert for pcstat and @mitchellh for go-ps
