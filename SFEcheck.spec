#
# spec file for package SFEcheck
#
# includes module(s): check
# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=28255&atid=392813&aid=
#
%include Solaris.inc

Name:           SFEcheck
Summary:        Check - An unit testing framework for C
Version:        0.9.8
Source:         %{sf_download}/check/check-%{version}.tar.gz
URL:            http://check.sourceforge.net/
SUNW_BaseDir:   %{_basedir}
BuildRoot:      %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires:       SUNWlibC

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %{name}


%prep
%setup -q -n check-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"

aclocal -I . -I ./m4
autoheader
automake -a -f -c
autoconf

./configure --prefix=%{_prefix}		    \
            --mandir=%{_mandir}             \
            --libdir=%{_libdir}             \
            --infodir=%{_datadir}/info      \
	    --enable-static=no

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.a" -exec rm -f {} ';'
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

# Remove /usr/share/info/dir, it's a generated file and shared by multiple
# packages
rm -f $RPM_BUILD_ROOT%{_datadir}/info/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/aclocal
%{_datadir}/aclocal/*.m4
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%{_datadir}/info

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Mon Oct 19 2009 - brian.cameron@sun.com
- Bump to 0.9.8.  Remove check-01-ansi.diff patch since it is no longer needed.
* Wed Jan 07 2008 - halton.huo@sun.com
- Bump to 0.9.6.
- Seperate -devel pkg
- Remove upstreamed patch suncc-fail.diff
- Add patch ansi.diff.
* Mon Dec 15 2008 - halton.huo@sun.com
- Remove suncc-define.diff since SS12 support __attribute__.
* Tue Mar 06 2007 - nonsea@users.sourceforge.net
- Initial spec file.
