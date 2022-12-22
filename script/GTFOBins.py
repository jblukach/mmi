import zipfile
import pybloomfilter
from pathlib import Path

gtfo = []
gtfo.append('7z')
gtfo.append('ab')
gtfo.append('agetty')
gtfo.append('alpine')
gtfo.append('ansible-playbook')
gtfo.append('aoss')
gtfo.append('apt-get')
gtfo.append('apt')
gtfo.append('ar')
gtfo.append('aria2c')
gtfo.append('arj')
gtfo.append('arp')
gtfo.append('as')
gtfo.append('ascii-xfr')
gtfo.append('ascii85')
gtfo.append('ash')
gtfo.append('aspell')
gtfo.append('at')
gtfo.append('atobm')
gtfo.append('awk')
gtfo.append('aws')
gtfo.append('base32')
gtfo.append('base58')
gtfo.append('base64')
gtfo.append('basenc')
gtfo.append('basez')
gtfo.append('bash')
gtfo.append('bc')
gtfo.append('bconsole')
gtfo.append('bpftrace')
gtfo.append('bridge')
gtfo.append('bundle')
gtfo.append('bundler')
gtfo.append('busctl')
gtfo.append('busybox')
gtfo.append('byebug')
gtfo.append('bzip2')
gtfo.append('c89')
gtfo.append('c99')
gtfo.append('cabal')
gtfo.append('cancel')
gtfo.append('capsh')
gtfo.append('cat')
gtfo.append('cdist')
gtfo.append('certbot')
gtfo.append('check_by_ssh')
gtfo.append('check_cups')
gtfo.append('check_log')
gtfo.append('check_memory')
gtfo.append('check_raid')
gtfo.append('check_ssl_cert')
gtfo.append('check_statusfile')
gtfo.append('chgrp')
gtfo.append('chmod')
gtfo.append('choom')
gtfo.append('chown')
gtfo.append('chroot')
gtfo.append('cmp')
gtfo.append('cobc')
gtfo.append('column')
gtfo.append('comm')
gtfo.append('composer')
gtfo.append('cowsay')
gtfo.append('cowthink')
gtfo.append('cp')
gtfo.append('cpan')
gtfo.append('cpio')
gtfo.append('cpulimit')
gtfo.append('crash')
gtfo.append('crontab')
gtfo.append('csh')
gtfo.append('csplit')
gtfo.append('csvtool')
gtfo.append('cupsfilter')
gtfo.append('curl')
gtfo.append('cut')
gtfo.append('dash')
gtfo.append('date')
gtfo.append('dd')
gtfo.append('debugfs')
gtfo.append('dialog')
gtfo.append('diff')
gtfo.append('dig')
gtfo.append('dmesg')
gtfo.append('dmidecode')
gtfo.append('dmsetup')
gtfo.append('dnf')
gtfo.append('docker')
gtfo.append('dosbox')
gtfo.append('dpkg')
gtfo.append('dvips')
gtfo.append('easy_install')
gtfo.append('eb')
gtfo.append('ed')
gtfo.append('efax')
gtfo.append('emacs')
gtfo.append('env')
gtfo.append('eqn')
gtfo.append('espeak')
gtfo.append('ex')
gtfo.append('exiftool')
gtfo.append('expand')
gtfo.append('expect')
gtfo.append('facter')
gtfo.append('fail2ban-client')
gtfo.append('file')
gtfo.append('find')
gtfo.append('finger')
gtfo.append('fish')
gtfo.append('flock')
gtfo.append('fmt')
gtfo.append('fold')
gtfo.append('fping')
gtfo.append('ftp')
gtfo.append('gawk')
gtfo.append('gcc')
gtfo.append('gcloud')
gtfo.append('gcore')
gtfo.append('gdb')
gtfo.append('gem')
gtfo.append('genie')
gtfo.append('genisoimage')
gtfo.append('ghc')
gtfo.append('ghci')
gtfo.append('gimp')
gtfo.append('ginsh')
gtfo.append('git')
gtfo.append('grc')
gtfo.append('grep')
gtfo.append('gtester')
gtfo.append('gzip')
gtfo.append('hd')
gtfo.append('head')
gtfo.append('hexdump')
gtfo.append('highlight')
gtfo.append('hping3')
gtfo.append('iconv')
gtfo.append('iftop')
gtfo.append('install')
gtfo.append('ionice')
gtfo.append('ip')
gtfo.append('irb')
gtfo.append('ispell')
gtfo.append('jjs')
gtfo.append('join')
gtfo.append('journalctl')
gtfo.append('jq')
gtfo.append('jrunscript')
gtfo.append('jtag')
gtfo.append('knife')
gtfo.append('ksh')
gtfo.append('ksshell')
gtfo.append('kubectl')
gtfo.append('latex')
gtfo.append('latexmk')
gtfo.append('ld.so')
gtfo.append('ldconfig')
gtfo.append('less')
gtfo.append('lftp')
gtfo.append('ln')
gtfo.append('loginctl')
gtfo.append('logsave')
gtfo.append('look')
gtfo.append('lp')
gtfo.append('ltrace')
gtfo.append('lua')
gtfo.append('lualatex')
gtfo.append('luatex')
gtfo.append('lwp-download')
gtfo.append('lwp-request')
gtfo.append('mail')
gtfo.append('make')
gtfo.append('man')
gtfo.append('mawk')
gtfo.append('more')
gtfo.append('mosquitto')
gtfo.append('mount')
gtfo.append('msfconsole')
gtfo.append('msgattrib')
gtfo.append('msgcat')
gtfo.append('msgconv')
gtfo.append('msgfilter')
gtfo.append('msgmerge')
gtfo.append('msguniq')
gtfo.append('mtr')
gtfo.append('multitime')
gtfo.append('mv')
gtfo.append('mysql')
gtfo.append('nano')
gtfo.append('nasm')
gtfo.append('nawk')
gtfo.append('nc')
gtfo.append('neofetch')
gtfo.append('nft')
gtfo.append('nice')
gtfo.append('nl')
gtfo.append('nm')
gtfo.append('nmap')
gtfo.append('node')
gtfo.append('nohup')
gtfo.append('npm')
gtfo.append('nroff')
gtfo.append('nsenter')
gtfo.append('octave')
gtfo.append('od')
gtfo.append('openssl')
gtfo.append('openvpn')
gtfo.append('openvt')
gtfo.append('opkg')
gtfo.append('pandoc')
gtfo.append('paste')
gtfo.append('pax')
gtfo.append('pdb')
gtfo.append('pdflatex')
gtfo.append('pdftex')
gtfo.append('perf')
gtfo.append('perl')
gtfo.append('perlbug')
gtfo.append('pg')
gtfo.append('php')
gtfo.append('pic')
gtfo.append('pico')
gtfo.append('pidstat')
gtfo.append('ping')
gtfo.append('pip')
gtfo.append('pkexec')
gtfo.append('pkg')
gtfo.append('plymouth')
gtfo.append('posh')
gtfo.append('pr')
gtfo.append('pry')
gtfo.append('psftp')
gtfo.append('psql')
gtfo.append('ptx')
gtfo.append('puppet')
gtfo.append('python')
gtfo.append('rake')
gtfo.append('readelf')
gtfo.append('red')
gtfo.append('redcarpet')
gtfo.append('restic')
gtfo.append('rev')
gtfo.append('rlogin')
gtfo.append('rlwrap')
gtfo.append('rpm')
gtfo.append('rpmdb')
gtfo.append('rpmquery')
gtfo.append('rpmverify')
gtfo.append('rsync')
gtfo.append('rtorrent')
gtfo.append('ruby')
gtfo.append('run-mailcap')
gtfo.append('run-parts')
gtfo.append('runc')
gtfo.append('rview')
gtfo.append('rvim')
gtfo.append('sash')
gtfo.append('scanmem')
gtfo.append('scp')
gtfo.append('screen')
gtfo.append('script')
gtfo.append('scrot')
gtfo.append('sed')
gtfo.append('service')
gtfo.append('setarch')
gtfo.append('setfacl')
gtfo.append('sftp')
gtfo.append('sg')
gtfo.append('shuf')
gtfo.append('slsh')
gtfo.append('smbclient')
gtfo.append('snap')
gtfo.append('socat')
gtfo.append('soelim')
gtfo.append('socket')
gtfo.append('sort')
gtfo.append('split')
gtfo.append('sqlite3')
gtfo.append('ss')
gtfo.append('ssh-keygen')
gtfo.append('ssh-keyscan')
gtfo.append('ssh')
gtfo.append('sshpass')
gtfo.append('start-stop-daemon')
gtfo.append('stdbuf')
gtfo.append('strace')
gtfo.append('strings')
gtfo.append('su')
gtfo.append('sysctl')
gtfo.append('systemctl')
gtfo.append('systemd-resolve')
gtfo.append('tac')
gtfo.append('tail')
gtfo.append('tar')
gtfo.append('task')
gtfo.append('taskset')
gtfo.append('tasksh')
gtfo.append('tbl')
gtfo.append('tclsh')
gtfo.append('tcpdump')
gtfo.append('tee')
gtfo.append('telnet')
gtfo.append('tex')
gtfo.append('tftp')
gtfo.append('tic')
gtfo.append('time')
gtfo.append('timedatectl')
gtfo.append('timeout')
gtfo.append('tmate')
gtfo.append('tmux')
gtfo.append('top')
gtfo.append('troff')
gtfo.append('tshark')
gtfo.append('ul')
gtfo.append('unexpand')
gtfo.append('uniq')
gtfo.append('unshare')
gtfo.append('unzip')
gtfo.append('update-alternatives')
gtfo.append('uudecode')
gtfo.append('uuencode')
gtfo.append('valgrind')
gtfo.append('vi')
gtfo.append('view')
gtfo.append('vigr')
gtfo.append('vim')
gtfo.append('vimdiff')
gtfo.append('vipw')
gtfo.append('virsh')
gtfo.append('volatility')
gtfo.append('w3m')
gtfo.append('wall')
gtfo.append('watch')
gtfo.append('wc')
gtfo.append('wget')
gtfo.append('whiptail')
gtfo.append('whois')
gtfo.append('wireshark')
gtfo.append('wish')
gtfo.append('xargs')
gtfo.append('xdotool')
gtfo.append('xelatex')
gtfo.append('xetex')
gtfo.append('xmodmap')
gtfo.append('xmore')
gtfo.append('xpad')
gtfo.append('xxd')
gtfo.append('xz')
gtfo.append('yarn')
gtfo.append('yash')
gtfo.append('yelp')
gtfo.append('yum')
gtfo.append('zathura')
gtfo.append('zip')
gtfo.append('zsh')
gtfo.append('zsoelim')
gtfo.append('zypper')

path = Path.cwd()
sha256 = []

for p in path.rglob("*"):
	if str(p).endswith('.zip'):
		if 'System.map' not in str(p):
			with zipfile.ZipFile(str(p),'r') as zf:
				for name in zf.namelist():
					with zf.open(name) as f:
						for line in f:
							output = line[:-1].decode().split('|')
							fname = output[0].split('/')
							count = len(fname) - 1
							if fname[count] in gtfo:
								sha256.append(output[4])
								sha256.append(output[13])
								sha256.append(output[15])

print(len(sha256))

unique = list(set(sha256))

print(len(unique))

gtfobins = pybloomfilter.BloomFilter(100000, 0.001, 'gtfo.bloom')

for value in unique:
	gtfobins.add(value)

gtfobins.sync()
