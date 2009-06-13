#
# spec file for package SFEwildmidi
#
# includes module(s): wildmidi
#
%include Solaris.inc

Name:                    SFEwildmidi
Summary:                 wildmidi - software MIDI synthesizer
Version:                 0.2.2
Source0:                 %{sf_download}/wildmidi/wildmidi-%{version}.tar.gz
Source1:                 soundcard.h
Patch1:                  wildmidi-01-solaris.diff
Patch2:                  wildmidi-02-sunstudio.diff
URL:                     http://wildmidi.sourceforge.net/
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibms

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n wildmidi-%{version}
%patch1 -p1
%patch2 -p1
mkdir -p include/sys
cp %{SOURCE1} include/sys

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CPPFLAGS="-I${PWD}/include"
export CFLAGS="%optflags"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"

aclocal
libtoolize --copy --force 
automake -a -f
autoconf -f
./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
            --enable-shared		     \
	    --disable-static		     \
	    --disable-debug		     \
	    --disable-werror		     \
	    --enable-oss

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT%{_basedir}/info
rm -rf $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%doc README COPYING INSTALL TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/wildmidi
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Sat Jan 13 2009 - Milan Jurik
- workaround for missing __FUNCTION__ support
* Thu Dec 11 2008 - trisk@acm.jhu.edu
- Initial spec
