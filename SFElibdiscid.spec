#
# spec file for package SFElibdiscid
#
# includes module(s): libdiscid
#
%include Solaris.inc

%define	src_ver 0.2.2
%define	src_name libdiscid
%define	src_url	http://users.musicbrainz.org/~matt

Name:		SFElibdiscid
Summary:	Library for creating MusicBrainz DiscIDs
Version:	%{src_ver}
License:	LGPL v2.1
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
Patch1:		libdiscid-01-solaris.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%description
libdiscid is a C library for creating MusicBrainz DiscIDs from audio
CDs. It reads a CD's table of contents (TOC) and generates an
identifier which can be used to lookup the CD at MusicBrainz.
Additionally, it provides a submission URL for adding the DiscID to
the database.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version
cp src/disc_linux.c src/disc_solaris.c
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

libtoolize --copy --force
aclocal
autoconf -f
autoheader
automake -a -f
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-static			\
	    --enable-shared			\
	    --disable-debug

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Mon Jul 30 2007 - dougs@truemail.co.th
- Initial spec
