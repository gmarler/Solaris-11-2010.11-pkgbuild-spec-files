#
# spec file for package SFEenet
#

%include Solaris.inc

Name:		SFEenet
Summary:	Relatively thin, simple and robust network communication layer on top of UDP
Version:	1.2.2
URL:		http://enet.bespin.org/
Source:		http://enet.bespin.org/download/enet-%{version}.tar.gz
Group:		Development/Libraries
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_basedir}
%include default-depend.inc
Requires:	%{name}


%prep
%setup -q -n enet-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir} \
            --enable-shared \
            --disable-static

make -j$CPUS

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm %{buildroot}%{_libdir}/*.*a

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*

%files devel
%defattr (-, root, bin)
%doc ChangeLog LICENSE README
%{_includedir}/enet/*.h
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Wed Dec 03 2010 - Milan Jurik
- initial spec
