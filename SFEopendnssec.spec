#
# spec file for package SFEopendnssec.spec
#
# includes module(s): opendnssec
#
%include Solaris.inc

%define src_name	opendnssec

Name:		SFEopendnssec
URL:		http://www.opendnssec.org/
Summary:	OpenDNSSEC secures zone data just before it is published in an authoritative name server
Version:	1.1.3
Group:		Applications/System 
License:	BSD
Source:		http://www.opendnssec.org/files/source/%{src_name}-%{version}.tar.gz 
Patch1:		opendnssec-01-std99.diff
Patch2:		opendnssec-02-sunstudio.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:	%name-root
BuildRequires:	SFErubygem-dnsruby
Requires:	SFErubygem-dnsruby
BuildRequires:	SFEpython-4Suite-XML
Requires:	SFEpython-4Suite-XML
BuildRequires:	SFEldns-devel
Requires:	SFEldns
BuildRequires:	SUNWopenssl-include
Requires:	SUNWopenssl-libraries


%description
OpenDNSSEC was created as an open-source turn-key solution for DNSSEC. It secures zone data just before it is published in an authoritative name server.

%package root
Summary:	%summary - platform dependent files, / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
./configure --prefix=%{_prefix}	\
	--sysconfdir=%{_sysconfdir} \
	--localstatedir=%{_localstatedir} \
	--disable-static	\
	--disable-pedantic	\
	--disable-strict

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

rmdir $RPM_BUILD_ROOT%{_localstatedir}/run/%{src_name}
rmdir $RPM_BUILD_ROOT%{_localstatedir}/run

rm -f $RPM_BUILD_ROOT%{_libdir}/*.la
rm $RPM_BUILD_ROOT%{_datadir}/%{src_name}.spec

# no section 8
install -d 0755 %{buildroot}%{_datadir}/man/man1m
for i in %{buildroot}%{_datadir}/man/man8/*.8
do
  base=`basename $i 8`
  name1m=${base}1m
  mv $i %{buildroot}%{_datadir}/man/man1m/${name1m}
done
rmdir %{buildroot}%{_datadir}/man/man8
for i in %{buildroot}%{_datadir}/man/*/*
do
  sed 's/(8)/(1M)/g' $i | sed '/^\.TH/s/ \"8\" / \"1M\" /g' > $i.new
  mv $i.new $i
done

# no section 7
install -d 0755 %{buildroot}%{_datadir}/man/man5
for i in %{buildroot}%{_datadir}/man/man7/*.7
do
  base=`basename $i 7`
  name1m=${base}1m
  mv $i %{buildroot}%{_datadir}/man/man1m/${name1m}
done
rmdir %{buildroot}%{_datadir}/man/man7
for i in %{buildroot}%{_datadir}/man/*/*
do
  sed 's/(7)/(1M)/g' $i | sed '/^\.TH/s/ \"7\" / \"1M\" /g' > $i.new
  mv $i.new $i
done

mkdir -p $RPM_BUILD_ROOT/lib/svc/method/opendnssec
install -c -m 755 tools/solaris/ods-signerd.init $RPM_BUILD_ROOT/lib/svc/method/opendnssec/
install -c -m 755 tools/solaris/ods-enforcerd.init $RPM_BUILD_ROOT/lib/svc/method/opendnssec/
mkdir -p $RPM_BUILD_ROOT%{_localstatedir}/svc/manifest/site/
install -c -m 644 tools/solaris/ods-signerd-smf.xml $RPM_BUILD_ROOT%{_localstatedir}/svc/manifest/site/
install -c -m 644 tools/solaris/ods-enforcerd-smf.xml $RPM_BUILD_ROOT%{_localstatedir}/svc/manifest/site/

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_sbindir}
%{_libdir}
%{_prefix}/libexec/opendnssec
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}
%{_mandir}/man1/*
%{_mandir}/man1m/*
%{_mandir}/man5/*

%files root
%defattr (0755, root, sys)
%{_sysconfdir}/%{src_name}
%dir %attr (0755, root, bin) /lib
%dir %attr (0755, root, bin) /lib/svc
%dir %attr (0755, root, bin) /lib/svc/method
%dir %attr (0755, root, bin) /lib/svc/method/opendnssec
%attr (0755, root, bin) /lib/svc/method/opendnssec/ods-enforcerd.init
%attr (0755, root, bin) /lib/svc/method/opendnssec/ods-signerd.init
%{_localstatedir}/%{src_name}
%dir %attr (0755, root, sys) %{_localstatedir}/svc/manifest/site
%class(manifest) %attr (0444, root, sys) %{_localstatedir}/svc/manifest/site/ods-signerd-smf.xml
%class(manifest) %attr (0444, root, sys) %{_localstatedir}/svc/manifest/site/ods-enforcerd-smf.xml

%files devel
%defattr (-, root, bin)
%{_includedir}

%changelog
* Fri Sep 24 2010 - Milan Jurik
- bump to 1.1.3
* Sun Jun 10 2010 - Milan Jurik
- Initial version
