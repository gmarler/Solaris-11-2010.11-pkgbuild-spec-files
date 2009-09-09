#
# spec file for package SFEmjpegtools
#
# includes module(s): SFEmjpegtools
#
%include Solaris.inc

%include base.inc

Name:                    SFEmjpegtools
Summary:                 mjpegtools - MPEG tools
Version:                 1.9.0
Source:                  %{sf_download}/mjpeg/mjpegtools-%{version}.tar.gz
Patch1:			 mjpegtools-01-progname.diff
Patch2:			 mjpegtools-02-alloca.diff
Patch4:                  mjpegtools-04-suncc.diff
Patch5:                  mjpegtools-05-shell.diff
Patch6:                  mjpegtools-06-gcc.diff
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC
Requires: SUNWgnome-base-libs
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWwxwidgets
BuildRequires: SFElibquicktime-devel
Requires: SFElibquicktime

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n mjpegtools-%version
%patch1 -p1
%patch2 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags -L/usr/X11/lib -L/usr/sfw/lib -R/usr/X11/lib -R/usr/sfw/lib"
export CPPFLAGS="-I/usr/X11/include -I/usr/sfw/include"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

# -fno-PIC is wrong
mv configure configure.orig
sed 's/PROGRAM_NOPIC="-fno-PIC"/PROGRAM_NOPIC=""/' configure.orig > configure

ksh ./configure --prefix=%{_prefix} --mandir=%{_mandir} \
            --libdir=%{_libdir}              \
            --libexecdir=%{_libexecdir}      \
            --sysconfdir=%{_sysconfdir}      \
	    --infodir=%{_datadir}/info       \
            --enable-shared		     \
	    --disable-static                 

perl -pi -e 's,-pthread,,' configure
# Parallel make spits dummy -j removed - Doug Scott
make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/lib*a

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so*
%dir %attr (0755, root, sys) %dir %{_datadir}
%{_datadir}/info
%{_datadir}/man

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%changelog
* Wed Sep 09 2009 - Milan Jurik
- update to 1.9.0
- switch to Sun CC
- SUNWwxwidgets used
* Fri Feb 16 2007 - dougs@truemail.co.th
- Removed -j from make
* Tue Nov 28 2006 - laca@sun.com
- make it work with either SFEwxwidgets or SFEwxGTK
* Thu Nov 22 2006 - dougs@truemail.co.th
- Initial version
