#
# spec file for package SFElibmusicbrainz3
#
# includes module(s): libmusicbrainz3
#
%include Solaris.inc

%define	src_ver 3.0.2
%define	src_name libmusicbrainz
%define	src_url	ftp://ftp.musicbrainz.org/pub/musicbrainz

Name:		SFElibmusicbrainz3
Summary:	library for accesing MusicBrainz servers
Version:	%{src_ver}
License:	LGPL 2.1
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires: SUNWcmake
%if %(pkginfo -q SUNWneon && echo 1 || echo 0)
Requires: SUNWneon
%else
Requires: SFEneon
%endif
BuildRequires: SFElibdiscid-devel
Requires: SFElibdiscid

%description
The MusicBrainz client library allows applications to make metadata
lookup to a MusicBrainz server, generate signatures from WAV data and
create CD Index Disk ids from audio CD roms.

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#export LDFLAGS="%_ldflags -i -lstdc++"
export LDFLAGS="%_ldflags -i"

cmake	-DCMAKE_INSTALL_PREFIX:PATH=%{_prefix}				\
	-DCMAKE_BUILD_TYPE=Release					\
	-DCMAKE_C_COMPILER:FILEPATH=$(CC)				\
	-DCMAKE_C_FLAGS:STRING="%optflags"				\
	-DCMAKE_CXX_COMPILER:FILEPATH=/usr/sfw/bin/g++			\
	-DCMAKE_CXX_FLAGS_RELEASE:STRING="-O4 -fno-omit-frame-pointer"	\
	-DCMAKE_VERBOSE_MAKEFILE=1
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT CMAKE_INSTALL_PREFIX=/usr
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
* Wed Aug 19 2009 - brian.cameron@sun.com
- Bump to 3.0.2.
* Sun Jun 29 2008 - river@wikimedia.org
- when using the default SFE environment, -lstdc++ causes the build to fail...
* Fri Jan 18 2008 - moinak.ghosh@sun.com
- Add -lstdc++ to LDFLAGS otherwise build fails
* Wed Oct 17 2007 - laca@sun.com
- use /usr/sfw/bin/g++ because /usr/gnu/bin/g++ uses gld and ldflags
  are incompatible
* Mon Jul 30 2007 - dougs@truemail.co.th
- Initial spec
