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
 -top int show top x cached files
```

## Examples

```
$ sudo hcache --top 10
[sudo] password for silenceshell: 
+----------------------------------------------------------------------------------+----------------+------------+-----------+---------+
| Name                                                                             | Size (bytes)   | Pages      | Cached    | Percent |
|----------------------------------------------------------------------------------+----------------+------------+-----------+---------|
| /opt/google/chrome/chrome                                                        | 114911208      | 28055      | 25457     | 090.740 |
| /usr/share/code/code                                                             | 67688720       | 16526      | 12274     | 074.271 |
| /home/silenceshell/Software/pycharm-community-2016.2/lib/pycharm.jar                   | 95177431       | 23237      | 11325     | 048.737 |
| /opt/atom/atom                                                                   | 62641344       | 15294      | 10578     | 069.164 |
| /usr/bin/dockerd                                                                 | 39121168       | 9552       | 7103      | 074.361 |
| /home/silenceshell/Software/pycharm-community-2016.2/jre/jre/lib/amd64/libjfxwebkit.so | 57455824       | 14028      | 6625      | 047.227 |
| /usr/lib/x86_64-linux-gnu/libQtWebKit.so.4.10.2                                  | 36462184       | 8902       | 6316      | 070.950 |
| /usr/lib/beyondcompare/BCompare                                                  | 30640160       | 7481       | 5505      | 073.586 |
| /usr/bin/SecureCRT                                                               | 29524560       | 7209       | 4806      | 066.667 |
| /usr/share/code/libnode.so                                                       | 21135976       | 5161       | 4588      | 088.898 |
+----------------------------------------------------------------------------------+----------------+------------+-----------+---------+
$ 
$ sudo ./hcache --top 3  --bname  
+-------------+----------------+------------+-----------+---------+
| Name        | Size (bytes)   | Pages      | Cached    | Percent |
|-------------+----------------+------------+-----------+---------|
| chrome      | 114911208      | 28055      | 25476     | 090.807 |
| pycharm.jar | 95177431       | 23237      | 11479     | 049.400 |
| atom        | 62641344       | 15294      | 10578     | 069.164 |
+-------------+----------------+------------+-----------+---------+ 
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

silenceshell <hubottle@gmail.com> @datastart.cn

## License

Apache 2.0

## Thanks to

@tobert for pcstat and @mitchellh for go-ps
