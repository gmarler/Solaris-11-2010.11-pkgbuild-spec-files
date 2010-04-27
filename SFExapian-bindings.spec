#
# spec file for package SFExapian-bindings
#
# includes module(s): xapian-bindings
#
%include Solaris.inc

%define cc_is_gcc 1
%define pythonver 2.6
%include base.inc

%define	src_name xapian-bindings
%define	src_url	http://www.oligarchy.co.uk/xapian/1.0.19

Name:                SFExapian-bindings
Summary:             Xapian bindings
Group:               System/Libraries
Version:             1.0.19
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:        %{_basedir}
SUNW_Copyright:       %{name}.copyright
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFExapian-core-devel
Requires: SFExapian-core
Requires: SUNWruby18u
BuildRequires: SUNWruby18u

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export PYTHON=/usr/bin/python%{pythonver}
export CC=gcc
export CXX=g++
export CXXFLAGS="%gcc_cxx_optflags"
export LDFLAGS="%_ldflags -lm"

aclocal
libtoolize --copy --force 
automake -a -f
autoconf -f 
./configure --prefix=%{_prefix}			\
            --bindir=%{_bindir}			\
            --libdir=%{_libdir}			\
            --sysconfdir=%{_sysconfdir}		\
            --includedir=%{_includedir} 	\
            --mandir=%{_mandir}			\
	    --infodir=%{_infodir}		\
	    --disable-static			\
	    --enable-shared

echo "#include <string.h>" >> config.h

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%{?pkgbuild_postprocess: %pkgbuild_postprocess -v -c "%{version}:%{jds_version}:%{name}:$RPM_ARCH:%(date +%%Y-%%m-%%d):%{support_level}" $RPM_BUILD_ROOT}

%files
%defattr (-, root, bin)
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%{_prefix}/ruby

%changelog
* Tue Apr 27 2010 - brian.cameron@sun.com
- Bump to 1.0.19.
* Wed Mar 10 2010 - brian.cameron@sun.com
- Bump to 1.0.18.
* Tue Feb 02 2010 - brian.cameron@sun.com
- Bump to 1.0.17.
* Tue Oct 21 2008  - Pradhap Devarajan <pradhap (at) gmail.com>
- Fix copyright 
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
