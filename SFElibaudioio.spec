#
# spec file for package SFElibaudioio
#
# includes module(s): libaudioio
#

%include Solaris.inc

Name:         SFElibaudioio
License:      Other
Group:        System/Libraries
Version:      0.6.1alpha
Summary:      LibAudioIO - audio foundation library
URL:          http://libaudioio.sourceforge.net/
Source:       http://trisk.acm.jhu.edu/libaudioio-%{version}.tar.gz
Patch1:       libaudioio-01-sunpro.diff
BuildRoot:    %{_tmppath}/%{name}-%{version}-build
Docdir:	      %{_defaultdocdir}/doc
SUNW_BaseDir: %{_basedir}
Autoreqprov:  on
%include default-depend.inc
Requires: SUNWlibC
Requires: SUNWlibms

%package devel
Summary:       %{summary} - development files
SUNW_BaseDir:  %{_basedir}
%include default-depend.inc
Requires:      %name

%prep
%setup -q -n libaudioio-%version
%patch1 -p1
for release in 2.10 2.11; do
	ln -s sys_i386solaris2.9.cc system/sys_%{base_arch}solaris$release.cc
	ln -s sys_i386solaris2.9.h system/sys_%{base_arch}solaris$release.h
done

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
  CPUS=1
fi

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
export LDFLAGS="%_ldflags -lCrun"

libtoolize --copy --force
aclocal $ACLOCAL_FLAGS
autoconf
./configure --prefix=%{_prefix} \
		--libdir=%{_libdir}
make -j $CPUS

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install
find $RPM_BUILD_ROOT%{_libdir} -type f -name "*.la" -exec rm -f {} ';'

%clean 
rm -rf $RPM_BUILD_ROOT

%files 
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_libdir}
%{_libdir}/*.so*

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %dir %{_includedir}
%{_includedir}/*

%changelog
* Mon Mar 10 2008 - trisk@acm.jhu.edu
- Initial spec
