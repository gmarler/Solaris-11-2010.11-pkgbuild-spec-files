#
# spec file for package SFEbdb
#
# includes module(s): bdb
#
%include Solaris.inc

#SUNWbdb is w/o db.h, we install in /usr/gnu/
%include usr-gnu.inc

Name:                    SFEbdb
Summary:                 Berkeley DB
Version:                 4.7.25
#Source:                  http://download-west.oracle.com/berkeley-db/db-%{version}.tar.gz
Source:			http://download.oracle.com/berkeley-db/db-%{version}.tar.gz
URL:                     http://www.oracle.com/technology/software/products/berkeley-db/index.html
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%prep
%setup -q -n db-%version

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
cd build_unix
../dist/configure                           \
        --prefix=%{_prefix}                 \
        --libexecdir=%{_libexecdir}         \
        --mandir=%{_mandir}                 \
        --datadir=%{_datadir}               \
        --infodir=%{_datadir}/info          \
        --enable-rpc			    \
	--enable-compat185		    \
        --disable-static                    \
        --enable-shared



make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT
cd build_unix
make install DESTDIR=$RPM_BUILD_ROOT
rm $RPM_BUILD_ROOT%{_libdir}/*.la
#rm $RPM_BUILD_ROOT%{_libdir}/*.a
mkdir -p $RPM_BUILD_ROOT%{_prefix}/share/doc
mv $RPM_BUILD_ROOT%{_prefix}/docs $RPM_BUILD_ROOT%{_prefix}/share/doc/bdb

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/db*
%{_bindir}/be*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/libdb*
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/doc
%{_datadir}/doc/*

%changelog
* Thr Apr 30 2009 - Thomas Wagner
- bump version to 4.7.25
- use usr-gnu.inc to avoid conflicts with SUNWbdb (which unfortunately doesn't provide db.h)
* Fri Jan 05 2007 - daymobrew@users.sourceforge.net
- Add URL.
* Tue Nov 07 2006 - glynn.foster@sun.com
- Initial spec file
