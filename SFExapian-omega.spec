#
# spec file for package SFExapian-omega
#
# includes module(s): xapian-omega
#
%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define	src_name xapian-omega
%define	src_url	http://www.oligarchy.co.uk/xapian/1.0.19

Name:                SFExapian-omega
Summary:             Search Engine built on Xapian
Group:               System/Libraries
Version:             1.0.19
Source:              %{src_url}/%{src_name}-%{version}.tar.gz
SUNW_Copyright:      %{name}.copyright
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFExapian-core-devel
Requires: SFExapian-core

%package root
Summary:                 %{summary} - / filesystem
SUNW_BaseDir:            /
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

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
%{_bindir}
%{_libdir}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/omega
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%{_mandir}

%files root
%defattr (-, root, sys)
%{_sysconfdir}

%changelog
* Tue Arp 27 2010 - brian.cameron@sun.com
- Bump to 1.0.19.
* Tue Feb 02 2010 - brian.cameron@sun.com
- Bump to 1.0.17.
* Sun Jul 29 2007 - dougs@truemail.co.th
- Initial spec
