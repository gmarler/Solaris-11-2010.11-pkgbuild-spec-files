#
# spec file for package SFElibdevil.spec
#
# includes module(s): libdevil
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name	DevIL

Name:		SFElibdevil
Summary:	Cross-platform image library
Version:	1.7.8
Group:		Development/Libraries
URL:		http://openil.sourceforge.net/
Source:		%{sf_download}/openil/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SUNWlibmng
Requires: SUNWlibmng
BuildRequires: SUNWlcms
Requires: SUNWlcms
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl
BuildRequires: SUNWgawk

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_prefix}
%include default-depend.inc

%prep
%setup -q -n devil-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CXX=g++
export CFLAGS="-I/usr/include/libpng12 %{optflags}"
export LDFLAGS="%{_ldflags}"
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir} \
            --enable-shared		\
	    --disable-static		\
	    --enable-ILU=yes		\
	    --disable-release		\
	    --disable-debug

make -j$CPUS 

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
rm %{buildroot}%{_libdir}/lib*.*a

%clean
rm -rf %{buildroot}

%files
%defattr (-, root, bin)
%{_bindir}
%{_libdir}/*.so*

%files devel
%defattr (-, root, bin)
%{_includedir}
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/*

%changelog
* Thu Dec 16 2010 - Milan Jurik
- bump to 1.7.8
* Mon May  7 2007 - dougs@truemail.co.th
- Initial version
