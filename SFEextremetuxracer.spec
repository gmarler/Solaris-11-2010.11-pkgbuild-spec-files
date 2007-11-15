#
# spec file for package SFEextremetuxracer.spec
#
%include Solaris.inc

%define src_name extreme-tuxracer
%define SUNWlibsdl      %(/usr/bin/pkginfo -q SUNWlibsdl && echo 1 || echo 0)

Name:                    	SFEextremetuxracer
Summary:                 	Fork from the original tux-racer
Version:                 	0.35
Source:                  	http://downloads.sourceforge.net/extremetuxracer/extreme-tuxracer-%{version}.tar.gz
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
%if %SUNWlibsdl
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
%else
BuildRequires: SFEsdl-devel
Requires: SFEsdl
%endif
BuildRequires:			SFEsdl-mixer-devel
Requires:			SFEsdl-mixer
Requires:			SUNWTcl

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
* Thu Nov 15 2007 - daymobrew@users.sourceforge.net
- Enable building with either SUNWlibsdl or SFEsdl.
* Sat Oct 6 2007 Petr Sobotka <sobotkap@centrum.cz>
- Initial version
