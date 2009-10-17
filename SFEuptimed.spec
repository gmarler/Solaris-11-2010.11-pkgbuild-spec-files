#
# spec file for package SFEuptimed
#

%include Solaris.inc

%define src_name uptimed

Name:		SFEuptimed
Summary:	An uptime daemon
Version:	0.3.16
URL:		http://podgorny.cz/uptimed/
Source:		%{url}releases/%{src_name}-%{version}.tar.bz2
Source1:	uptimed.xml
Source2:	svc-uptimed
Patch1:		uptimed-utmpx.diff
License:	GPL
Group:		System Environment/Daemons

SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
Uptimed is an uptime record daemon keeping track of the highest 
uptimes the system ever had. Instead of using a pid file to 
keep sessions apart from each other, it uses the system boot 
time. 

Uptimed has the ability to inform you of records and milestones 
though syslog and e-mail, and comes with a console front end to 
parse the records, which can also easily be used to show your 
records on your Web page


%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

%build 

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

libtoolize -f -c
aclocal
autoheader
autoconf -f
./configure --prefix=%{_prefix}	\
	--bindir=%{_bindir}	\
	--libdir=%{_libdir}	\
	--sbindir=%{_sbindir}	\
	--sysconfdir=%{_sysconfdir}	\
	--mandir=%{_mandir}	\
	--disable-static	\
	--enable-shared

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a
install -d 0755 $RPM_BUILD_ROOT/var/svc/manifest/system
install -m 0644 %{SOURCE1} $RPM_BUILD_ROOT/var/svc/manifest/system
install -d 0755 $RPM_BUILD_ROOT/lib/svc/method
install -m 0644 %{SOURCE2} $RPM_BUILD_ROOT/lib/svc/method
mv $RPM_BUILD_ROOT%{_sysconfdir}/uptimed.conf-dist $RPM_BUILD_ROOT%{_sysconfdir}/uptimed.conf

# no section 8
install -d 0755 $RPM_BUILD_ROOT%{_datadir}/man/man1m
for i in $RPM_BUILD_ROOT%{_datadir}/man/man8/*.8
do
  base=`basename $i 8`
  name1m=${base}1m
  mv $i $RPM_BUILD_ROOT%{_datadir}/man/man1m/${name1m}
done
rmdir $RPM_BUILD_ROOT%{_datadir}/man/man8
for i in $RPM_BUILD_ROOT%{_datadir}/man/*/*
do
  sed 's/(8)/(1M)/g' $i | sed '/^\.TH/s/ \"8\" / \"1M\" /g' > $i.new
  mv $i.new $i
done


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/uprecords
%dir %attr (0755, root, bin) %{_sbindir}
%{_sbindir}/uptimed
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/uprecords.1
%dir %attr (0755, root, bin) %{_mandir}/man1m
%{_mandir}/man1m/uptimed.1m

%files root
%defattr (-, root, sys)
%dir %attr (0755, root, sys) %{_sysconfdir}
%{_sysconfdir}/uptimed.conf
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%attr (0755, root, bin) /lib/svc/method/svc-uptimed
%dir %attr (0755, root, sys) %{_localstatedir}
%dir %attr (0755, root, sys) %{_localstatedir}/svc
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/system
%class(manifest) %attr(0444, root, sys) %{_localstatedir}/svc/manifest/system/uptimed.xml
%dir %attr (0755, root, bin) %{_localstatedir}/spool
%dir %attr (0755, root, bin) %{_localstatedir}/spool/uptimed


%changelog
* Sat Oct 17 2009 - Milan Jurik
- Initial spec
