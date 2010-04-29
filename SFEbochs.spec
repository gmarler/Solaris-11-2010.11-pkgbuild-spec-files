#
# spec file for package SFEbochs.spec
#
# includes module(s): bochs
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name	bochs
%define src_url		http://%{src_name}.sourceforge.net/cvs-snapshot

Name:                   SFEbochs
Summary:                IA32 emulator
Version:                2.4.5
Source:                 %{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWwxwidgets-devel
Requires: SUNWwxwidgets
BuildRequires: SUNWlibsdl-devel
Requires: SUNWlibsdl

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
export CFLAGS="%{optflags}"
export LDFLAGS="%{_ldflags}"
export CC=gcc
export CXX=g++
export CXXFLAGS="-O3 -Xlinker -i -fno-omit-frame-pointer"

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoconf --force

./configure --prefix=%{_prefix}			\
	    --bindir=%{_bindir}			\
	    --mandir=%{_mandir}			\
            --libdir=%{_libdir}			\
            --datadir=%{_datadir}		\
            --localedir=%{_datadir}/locale	\
            --libexecdir=%{_libexecdir} 	\
            --sysconfdir=%{_sysconfdir} 	\
            --enable-shared			\
	    --disable-static			\
	    --enable-x86-64			\
	    --enable-ne2000			\
	    --enable-acpi			\
	    --enable-pci			\
	    --enable-x2apic			\
	    -with-sdl

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%{_mandir}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*
%{_datadir}/bochs

%changelog
* Thu Apr 29 2010 - Milan Jurik
- update to 2.4.5
* Tue Oct 21 2008  - Pradhap Devarajan <pradhap (at) gmail.com>
- Bump to 20080906
* Tue Feb 12 2008 <pradhap (at) gmail.com>
- Bumped up the version to 20080209
* Sat Apr 28 2006 - dougs@truemail.co.th
- Initial version
