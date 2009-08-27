#
# spec file for package SFElibdvdread
#
# includes module(s): libdvdread
#
%include Solaris.inc

Name:                    SFElibdvdread
Summary:                 libdvdread  - libdvdread provides a simple foundation for reading DVD video disks
Version:                 4.1.3
Source:                  http://www1.mplayerhq.hu/MPlayer/releases/dvdnav/libdvdread-%{version}.tar.bz2
SUNW_BaseDir:            %{_basedir}
buildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFElibdvdcss

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name
BuildRequires: SFElibdvdcss-devel

%prep
%setup -q -n libdvdread-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

./configure2 --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*


%changelog
* Sat Jun 13 2009 - Milan Jurik
- new upstream, version 4.1.3
* Sat Jun 14 2008 - trisk@acm.jhu.edu
- Update download link
* Mon Jun 12 2006 - laca@sun.com
- renamed to SFElibdvdread
- changed to root:bin to follow other JDS pkgs.
* Mon May 8 2006 - drdoug007@yahoo.com.au
- Initial version
