#
# spec file for package SFEextremetuxracer.spec
#
%include Solaris.inc

%define src_name extremetuxracer
%define SFEsdl      %(/usr/bin/pkginfo -q SFEsdl && echo 1 || echo 0)

Name:		SFEextremetuxracer
Summary:	Fork from the original tux-racer
Version:	0.4
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
URL:		http://extremetuxracer.com/
License:	GPLv2
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %SFEsdl
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%else
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%endif
BuildRequires:	SFEsdl-mixer-devel
Requires:	SFEsdl-mixer
Requires:	SUNWTcl
BuildRequires:	SUNWxorg-mesa
Requires:	SUNWxorg-mesa

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC="gcc"
export CXX="g++"
export CFLAGS="-I/usr/sfw/include"
export CXXFLAGS="-I/usr/sfw/include"
export LDFLAGS="%_ldflags -L/usr/sfw/lib -R/usr/sfw/lib -lsocket -lnsl"

./configure --prefix=%{_basedir}			\
            --bindir=%{_bindir}				\
            --datadir=%{_datadir}			\
            --mandir=%{_mandir}				\
            --libdir=%{_libdir}				\
            --with-localedir=%{_localedir}		\
	    --disable-static

make -j$CPUS 

%install
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, other)
%dir %attr (0755, root, sys) %{_basedir}
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%defattr (-, root, other)
%dir %attr (-, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/etracer
%{_datadir}/etracer/*

%changelog
* Sun May 09 2010 - Milan Jurik
- cleanup build dependencies
* Thu Aug 20 2009 - Milan Jurik
- update to 0.4
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWlibsdl or SFEsdl.
* Sat Oct 6 2007 Petr Sobotka <sobotkap@centrum.cz>
- Initial version
