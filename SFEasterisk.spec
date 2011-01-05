#
# spec file for package SFEasterisk
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define src_name   asterisk
%define src_version    1.8.1.1

Name:         	SFE%{src_name}
Summary:      	Asterisk : Complete IP PBX in software
Version:      	%{src_version}
License:      	GPL
Group:          Communication
Source:         http://downloads.digium.com/pub/asterisk/releases/%{src_name}-%{version}.tar.gz
Patch1:        	asterisk-01-oss.diff
Patch2:         asterisk-02-ifr_hwaddr.diff
URL:            http://www.asterisk.org
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description 
Asterisk is a complete IP PBX in software. It runs on a wide variety of operating systems and provides all of the features one would expect from a PBX including many advanced features that are often associated with high end (and high cost) proprietary PBXs. Asterisk supports Voice over IP in many protocols, and can interoperate with almost all standards-based telephony equipment using relatively inexpensive hardware.

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep 
%setup -q -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1

%build
export CC=/usr/gcc/4.3/bin/gcc
export CXX=/usr/gcc/4.3/bin/g++
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix} --sysconfdir=%{_sysconfdir}

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

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

# run dir is swap
rmdir $RPM_BUILD_ROOT%{_localstatedir}/run/%{src_name}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,bin)
%{_sbindir}
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%files devel
%defattr (-, root, bin)
%{_includedir}

%files root
%defattr (-, root, sys)
%{_sysconfdir}
%dir %attr (0755, root, bin) %{_localstatedir}/spool
%{_localstatedir}/spool/*
%dir %attr (0755, root, sys) %{_localstatedir}/run
%dir %attr (0755, root, sys) %{_localstatedir}/log
%{_localstatedir}/log/%{src_name}
%dir %attr (0755, root, other) %{_localstatedir}/lib
%{_localstatedir}/lib/%{src_name}


%changelog
* Wed Jan 05 2011 - Milan Jurik 
- bump to 1.8.1.1
* Fri Nov 26 2010 - Milan Jurik
- major update to 1.8.0
* Sun Oct 14 2007 - laca@sun.com
- fix some directory attributes
* Sat Aug 11 2007 - <shivakumar dot gn at gmail dot com>
- Initial spec.
