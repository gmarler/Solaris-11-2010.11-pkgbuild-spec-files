#
# spec file for package giflib
#
# includes module(s): giflib
#

%define src_ver 1.2.1
%define src_name libssh2
%define src_url http://www.libssh2.org/download/

Name:		libssh2
Summary:	ssh2 library
Version:	%{src_ver}
Source:		%{src_url}/%{src_name}-%{version}.tar.gz
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

libtoolize -f -c
aclocal
autoconf -f
autoheader
automake -a -f

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --libexecdir=%{_libexecdir}	\
            --sysconfdir=%{_sysconfdir}	\
            --enable-shared		\
	    --disable-static

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_libdir}/lib*.*a

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Wed Nov  11 2009 - michal.bielicki@halokwadrat.de
- Initial base spec file
