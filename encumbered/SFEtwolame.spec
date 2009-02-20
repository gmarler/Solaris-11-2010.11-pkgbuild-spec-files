#
# spec file for package SFEtwolame
#
# includes module(s): twolame

# bugdb: http://sourceforge.net/tracker/index.php?func=detail&group_id=136040&atid=735435&aid=
#
%include Solaris.inc

%define SFElibsndfile   %(/usr/bin/pkginfo -q SFElibsndfile && echo 1 || echo 0)

Name:                    SFEtwolame
Summary:                 twolame - MP3 Encoder
Version:                 0.3.12
Source:                  http://downloads.sourceforge.net/twolame/twolame-%{version}.tar.gz
# date:2008-08-17 owner:halton type:bug bugid:2054218
Patch1:			 twolame-01-configure.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%if %SFElibsndfile
BuildRequires: SFElibsndfile-devel
Requires: SFElibsndfile
%else
BuildRequires:	SUNWlibsndfile
Requires:	SUNWlibsndfile
%endif

Requires: SUNWlibms

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n twolame-%version
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags -xcrossfile=1"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal -I ."

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoheader
automake -a -c -f
autoconf
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Tue Feb 17 2009 - Thomas Wagner
- make (Build-)Requires conditional SUNWlibsndfile|SFElibsndfile(-devel)
- removed BuildRequires: SFElibsndfiles-devel from package -devel
* Tue Sep 02 2008 - nonsea@users.sourceforge.net
- Add libtoolize/aclocal/autoheader/automake/autoconf before ./configure
* Sat Aug 16 2008 - nonsea@users.sourceforge.net
- Bump to 0.3.12
- Remove patch crossfile_inline.diff and reorder
* Tue Feb 12 2008 - pradhap@gmail.com
- Fixed links
* Sun Nov 4 2007 - markwright@internode.on.net
- Bump to 0.3.10.  Bump patch1 and patch2.
* Fri Jun 23 2006 - laca@sun.com
- rename to SFEtwolame
- delete -share subpkg
- update file attributes
- add missing dep
* Mon Jun 13 2006 - drdoug007@yahoo.com.au
- Initial version
