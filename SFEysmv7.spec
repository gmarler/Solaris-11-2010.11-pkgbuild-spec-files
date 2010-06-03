#
# spec file for package SFEysmv7.spec
#
# includes module(s): ysmv7
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name	ysmv7
%define src_version	2_9_9_1

Name:		SFEysmv7
Summary:	console based ICQ client
Version:	2.9.9.1
License:	GPLv2
Group:		Applications/Internet
URL:		http://ysmv7.sourceforge.net/
Source:		%{sf_download}/%{src_name}/%{src_name}_%{src_version}.tar.bz2
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SFElibiconv-devel
Requires:	SFElibiconv
BuildRequires:	SUNWgnu-readline
Requires:	SUNWgnu-readline

%prep
%setup -q -n %{src_name}_%{src_version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CC=gcc
export CFLAGS="%{optflags} -I/usr/gnu/include"
export LDFLAGS="%{_ldflags} -L/usr/gnu/lib -R/usr/gnu/lib"

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --with-fribidi=no

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}/man1/ysm.1

%changelog
* Thu Jun 03 2010 -Milan Jurik
- Initial version
