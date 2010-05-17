#
# spec file for package SFEopencity.spec
#
# includes module(s): opencity
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name opencity
%define src_version 0.0.6.2stable

Name:		SFEopencity
Summary:	opencity - OpenCity Game
Version:	0.0.6.2
Source:		%{sf_download}/%{src_name}/%{src_name}-%{src_version}.tar.bz2
Patch1:		opencity-01-errors.diff
URL:		http://www.opencity.info/
License:	GPLv2
Group:		Amusements/Game
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEsdl-ttf-devel
Requires: SFEsdl-ttf
BuildRequires: SFEsdl-mixer-devel
Requires: SFEsdl-mixer
BuildRequires: SFEsdl-net-devel
Requires: SFEsdl-net
BuildRequires: SFEsdl-image-devel
Requires: SFEsdl-image
BuildRequires: SUNWxorg-mesa
Requires: SUNWxorg-mesa
BuildRequires: SUNWgnome-common-devel

%package root
Summary:	%{summary} - / filesystem
SUNW_BaseDir:	/
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{src_version}
%patch1 -p1

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export CFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export MSGFMT="/usr/bin/msgfmt"

export CC=gcc
export CXX=g++
export CXXFLAGS="-O3 -Xlinker -i -fno-omit-frame-pointer -fpic -Dpic"
libtoolize --copy
aclocal
automake
autoconf --force
./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/pixmaps
mkdir -p $RPM_BUILD_ROOT%{_datadir}/applications
make install DESTDIR=$RPM_BUILD_ROOT

%post
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS_wait

%postun
test -x $BASEDIR/lib/postrun || exit 0
( echo 'test -x /usr/bin/update-desktop-database || exit 0';
  echo '/usr/bin/update-desktop-database'
) | $BASEDIR/lib/postrun -b -u -c JDS

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/pixmaps
%{_datadir}/%{src_name}
%{_datadir}/applications
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{src_name}/*
%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/man6/*

%files root
%defattr (-, root, bin)
%attr (0755, root, bin) %dir %{_sysconfdir}
%defattr (-, root, bin)
%attr (0755, root, bin) %dir %{_sysconfdir}/%{src_name}
%{_sysconfdir}/%{src_name}/*

%changelog
* Mon May 17 2010 - Milan Jurik
- update to 0.0.6.2stable
* Sun Apr 22 2007 - dougs@truemail.co.th
- Initial version
