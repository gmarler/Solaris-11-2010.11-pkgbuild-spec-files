#
# spec file for package SFEportaudio.spec
#
# includes module(s): portaudio
#
%include Solaris.inc

%define src_name	portaudio
%define src_url		http://www.portaudio.com/archives

Name:                   SFEportaudio
Summary:                Portable cross-platform Audio API
Version:                v19_20071207
Source:                 %{src_url}/pa_stable_%{version}.tar.gz
Source1:                soundcard.h
Patch1:			portaudio-01-pthread.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_prefix}
%include default-depend.inc

%prep
%setup -q -n %{src_name}
%patch1 -p1
mkdir -p src/os/unix/sys
cp %{SOURCE1} src/os/unix/sys

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi


libtoolize --force --copy
aclocal
autoconf --force

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export CPPFLAGS="-I${PWD}/src/os/unix"
export LDFLAGS="%_ldflags"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static		\
	    --without-jack		\
	    --enable-cxx
make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*.*a


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755,root,bin) %{_libdir}
%{_libdir}/lib*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755,root,bin) %{_libdir}
%dir %attr (0755,root,other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Tue Feb 24 2009 - Albert Lee
- Use included sys/soundcard.h
* Fri Mar 14 2008 - brian.cameron@sun.com
- Bump to the new 20071207 version.  Remove upstream portaudio-01-oss.diff.
* Sat Sep 22 2007 - dougs@truemail.co.th
- disabled building with jack audio
* Sun May 13 2007 - dougs@truemail.co.th
- Fixed typo
* Mon Apr 30 2007 - dougs@truemail.co.th
- Initial version
