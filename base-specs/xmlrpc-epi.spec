#
# spec file for package xmlrpc-epi
#
# includes module(s): xmlrpc-epi
#
%include Solaris.inc

Name:                   xmlrpc-epi
Summary:                A general purpose implementation of the xmlrpc specification in C
URL:                    http://xmlrpc-epi.sourceforge.net/
Version:                0.54.1
Source:                 http://downloads.sourceforge.net/project/xmlrpc-epi/xmlrpc-epi-base/%{version}/xmlrpc-epi-%{version}.tar.gz
BuildRoot:              %{_tmppath}/%{name}-%{version}-build

%prep
%setup -q -n xmlrpc

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export ACLOCAL_FLAGS="-I %{_datadir}/aclocal"
libtoolize --force
aclocal $ACLOCAL_FLAGS
autoconf
automake -a -c -f
./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
            --libdir=%{_libdir}		\
            --datadir=%{_datadir}	\
            --includedir=%{_prefix}/include/xmlrpc-epi \
            --libexecdir=%{_libexecdir} \
            --sysconfdir=%{_sysconfdir}

make -j1

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Jan 29 2010 - brian.cameron@sun.com
- Initial base spec with version 0.54.1.
