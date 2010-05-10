# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: trisk
#
%include Solaris.inc

# use the --with-opengl option to use opengl instead of agg
# use the --with-bzr-code option to use bzr code instead of the stable tarball
%define bzr_url      http://bzr.savannah.gnu.org/r/gnash/trunk
%define SUNWglib2    %(/usr/bin/pkginfo -q SUNWglib2 && echo 1 || echo 0)

Name:                SFEgnash
Summary:             Gnash - GNU Flash movie player
%if %{?_with_bzr_code:0}%{?!_with_bzr_code:1}
# stable tarball
Version:             0.8.6
Source:              http://ftp.gnu.org/pub/gnu/gnash/%{version}/gnash-%{version}.tar.bz2
Patch1:              gnash-01-stdc.diff
Patch2:              gnash-02-sunpro.diff
Patch3:              gnash-03-gnashrc.diff
Patch4:              gnash-04-plugin.diff
Patch5:              gnash-04-macros.diff
%else
# bzr code
Version:             0.8.6.999
%endif
Url:                 http://www.gnashdev.org/
License:             GPLv3+
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build

# cairo correctness/performance is poor
%if %{?_with_opengl:0}%{?!_with_opengl:1}
%define _with_agg 1
%endif

%include default-depend.inc
BuildRequires: SUNWgnome-common-devel
BuildRequires: SUNWgnu-gettext
BuildRequires: SFEboost-devel
Requires: SFEboost
Requires: SUNWlxml
Requires: SUNWlexpt
Requires: SUNWbzip
Requires: SUNWzlib
BuildRequires: SUNWjpg-devel
Requires: SUNWjpg
BuildRequires: SFEgiflib-devel
Requires: SFEgiflib
BuildRequires: SUNWpng-devel
Requires: SUNWpng
Requires: SUNWfontconfig
Requires: SUNWfreetype2
Requires: SUNWspeex
Requires: SUNWcurl

%if %{?_with_bzr_code:1}%{?!_with_bzr_code:0}
# bzr code
BuildRequires: SFEbzr
%endif

%if %{?_with_opengl:1}%{?!_with_opengl:0}
%define renderer ogl
Requires: SFEgtkglext
%else
%if %{?_with_agg:1}%{?!_with_agg:0}
%define renderer agg
BuildRequires: SFEagg-devel
%else
%define renderer cairo
%if %SUNWglib2
BuildRequires: SUNWcairo-devel
Requires: SUNWcairo
%endif
%endif
%endif

%if %SUNWglib2
BuildRequires: SUNWglib2-devel
Requires: SUNWglib2
BuildRequires: SUNWgtk2-devel
Requires: SUNWgtk2
%else
BuildRequires: SUNWgnome-base-libs-devel
Requires: SUNWgnome-base-libs
%endif

BuildRequires: SUNWgnome-media-devel
Requires: SUNWgnome-media
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
Requires: SUNWxorg-clientlibs

Requires: %{name}-root

%package root
Summary:                 %{summary} - root
SUNW_BaseDir:            /
%include default-depend.inc

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}

%if %build_l10n
%package l10n
Summary:                 %{summary} - l10n files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires:                %{name}
%endif

%prep
%if %{?_with_bzr_code:0}%{?!_with_bzr_code:1}
# stable tarball
%setup -q -n gnash-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%else
# bzr code
if [ ! -d "../SOURCES/gnash/.bzr" ]; then
	rm -rf gnash
	bzr branch %{bzr_url} ../SOURCES/gnash
else
	bzr update ../SOURCES/gnash
fi
rm -rf gnash
cp -rp ../SOURCES/gnash gnash
%endif

%build
%if %{?_with_bzr_code:1}%{?!_with_bzr_code:0}
# bzr code
cd gnash
%endif

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
# Necessary for mmap, clock_gettime, sigwait
export CPPFLAGS="-I%{xorg_inc} -D_XOPEN_SOURCE=500 -D__EXTENSIONS__"
export CFLAGS="%optflags -xlibmil"
# libtool strips -staticlib=stlport4
export CXXFLAGS="%cxx_optflags -xO4 -library=stlport4 -staticlib=stlport4 \
 -XCClinker -staticlib=stlport4 \
 -mt -xipo -xlibmil -xlibmopt -features=tmplife -features=tmplrefstatic"
export LDFLAGS="%_ldflags"
export MSGFMT="/usr/bin/msgfmt"

for dir in macros cygnal libltdl/m4; do
	[ -d "$dir" ] && aclocalincludes="-I $dir $aclocalincludes"
done
%if %{?_with_bzr_code:1}%{?!_with_bzr_code:0}
# bzr code
bash ./autogen.sh
%else
aclocal $aclocalincludes $ACLOCAL_FLAGS
automake -a -c -f
autoconf
%endif

./configure \
            --prefix=%{_prefix}		\
	    --sysconfdir=%{_sysconfdir}	\
            --mandir=%{_mandir}		\
	    --disable-jemalloc		\
	    --enable-avm2		\
	    --enable-gui=gtk		\
	    --enable-renderer=%{renderer}	\
	    --enable-media=gst		\
	    --disable-testsuite		\
	    --with-plugins-install=system

%if %{?_with_opengl:1}%{?!_with_opengl:0}
%else
%if %{?_with_agg:1}%{?!_with_agg:0}
# hack for AGG pod_vector heap corruption with -xO3 and higher
perl -pi -e 's,-xO[345],-xO2,g' backend/Makefile
%endif
%endif

gmake -j $CPUS

%install
%if %{?_with_bzr_code:1}%{?!_with_bzr_code:0}
# bzr code
cd gnash
%endif

rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT
gmake install-plugins DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'

%if %build_l10n
%else
rm -rf $RPM_BUILD_ROOT%{_localedir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, bin) %{_libdir}/gnash
%{_libdir}/gnash/*
%dir %attr (0755, root, bin) %{_libdir}/firefox
%dir %attr (0755, root, bin) %{_libdir}/firefox/plugins
%{_libdir}/firefox/plugins/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, sys) %{_datadir}/gnash
%{_datadir}/gnash/*
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, other) %{_docdir}/gnash
%{_docdir}/gnash/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*

%files root
%defattr (-, root, sys)
%attr (0755, root, sys) %dir %{_sysconfdir}
%{_sysconfdir}/gnash*rc

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*

%if %build_l10n
%files l10n
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_localedir}
%{_localedir}/*
%endif

%changelog
* Thu Jan 07 2009 - Albert Lee <trisk@opensolaris.org>
- Add --with-bzr-code option.
* Tue Dec 15 2009 - Albert Lee <trisk@opensolaris.org>
- Add OpenGL renderer.
- Add patch5.
* Mon Dec 14 2009 - Albert Lee <trisk@opensolaris.org>
- Fix file lists.
* Tue Dec 01 2009 - Albert Lee <trisk@opensolaris.org>
- Initial spec.
