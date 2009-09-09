#
# spec file for package SFEethereal
#
# includes module(s): ethereal
#
%include Solaris.inc

Name:         SFEethereal
Summary:      Ethereal - A GUI network protocol analyzer
Version:      0.99.0
Source:       http://www.ethereal.com/distribution/ethereal-0.99.0.tar.bz2
Patch0:       ethereal-01-emem.diff
URL:          http://www.ethereal.com
License:      GPL
SUNW_BaseDir: %{_basedir}
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWopenssl-libraries
Requires: SFElibpcap
BuildRequires: SUNWperl584core
BuildRequires: SUNWgnome-libs-devel
BuildRequires: SUNWopenssl-include
BuildRequires: SFEsed
BuildRequires: SFElibpcap-devel
BuildRequires: SUNWbinutils

%prep
%setup -q -n ethereal-%version
%patch0 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export PATH="/usr/perl5/bin:/usr/gnu/bin:$PATH"
export CPPFLAGS="-I/usr/sfw/include"
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -lgnutls"
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}	     \
            --disable-usr-local              \
            --enable-threads                 \
            --with-ssl=/usr/sfw              \
            --without-net-snmp

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
# Modify path to find GNU strip.
%ifarch sparc
export PATH=/usr/sfw/sparc-sun-solaris2.11/bin:$PATH
%else
export PATH=/usr/sfw/i386-pc-solaris2.11/bin/:$PATH
%endif
make DESTDIR=$RPM_BUILD_ROOT install-strip
[ -d ${RPM_BUILD_ROOT}%{_datadir}/ethereal/image ] || \
  mkdir ${RPM_BUILD_ROOT}%{_datadir}/ethereal/image
cp image/eicon3d32.xpm ${RPM_BUILD_ROOT}%{_datadir}/ethereal/image
cp image/eiconcap32.xpm ${RPM_BUILD_ROOT}%{_datadir}/ethereal/image
cp image/hi32-app-ethereal.png ${RPM_BUILD_ROOT}%{_datadir}/ethereal/image
cp image/lo32-app-ethereal.png ${RPM_BUILD_ROOT}%{_datadir}/ethereal/image
cp image/eicon3d48.xpm ${RPM_BUILD_ROOT}%{_datadir}/ethereal/image
cp image/eiconcap48.xpm ${RPM_BUILD_ROOT}%{_datadir}/ethereal/image
cp image/elogo3d48x48.png ${RPM_BUILD_ROOT}%{_datadir}/ethereal/image
cp image/ethereal48x48-trans.png ${RPM_BUILD_ROOT}%{_datadir}/ethereal/image
cp image/ethereal48x48.png ${RPM_BUILD_ROOT}%{_datadir}/ethereal/image
cp image/hi48-app-ethereal.png ${RPM_BUILD_ROOT}%{_datadir}/ethereal/image
cp image/lo48-app-ethereal.png ${RPM_BUILD_ROOT}%{_datadir}/ethereal/image
[ -d ${RPM_BUILD_ROOT}%{_datadir}/pixmaps ] || \
  mkdir ${RPM_BUILD_ROOT}%{_datadir}/pixmaps
(cd ${RPM_BUILD_ROOT}%{_datadir}/pixmaps ; \
  ln -s ../ethereal/image/elogo3d48x48.png ethereal.png )
[ -d ${RPM_BUILD_ROOT}%{_datadir}/applications ] || \
  mkdir ${RPM_BUILD_ROOT}%{_datadir}/applications
cp ethereal.desktop ${RPM_BUILD_ROOT}%{_datadir}/applications

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr(0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr(0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_datadir}/ethereal
%dir %attr(0755, root, other) %{_datadir}/applications
%dir %attr(0755, root, other) %{_datadir}/pixmaps
%{_datadir}/ethereal/*
%{_datadir}/applications/*
%{_datadir}/pixmaps/*
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/man1/*
%{_mandir}/man4/*

%changelog
* Wed Mar 21 2007 - daymobrew@users.sourceforge.net
- Add BuildRequires SUNWbinutils and set PATH during %install to pick up GNU
  strip which is required (it uses --strip-unneeded parameter).
* Tue Feb 27 2007 - ivwang@gmail.com
- Add icons, strip executables
* Tue Feb 27 2007 - laca@sun.com
- set CFLAGS and LDFLAGS for optimizations
* Mon Feb 26 2007 - ivwang@gmail.com
- Initial version
