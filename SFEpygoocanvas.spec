#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# Owner: halton
#
%define src_name pygoocanvas
%define python_version 2.4

%include Solaris.inc

Name:                SFEpygoocanvas
URL:                 http://developer.berlios.de/projects/pygoocanvas/
Summary:             pygoocanvas - GooCanvas python bindings
Version:             0.14.1
Source:              http://download.gnome.org/sources/%{src_name}/0.14/%{src_name}-%{version}.tar.bz2
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWPython-devel
BuildRequires: SUNWgnome-python-libs-devel
BuildRequires: SFEgoocanvas-devel
Requires: SUNWPython
Requires: SUNWgnome-python-libs
Requires: SFEgoocanvas

%package devel
Summary:                 %{summary} - development files
SUNW_BaseDir:            %{_basedir}
%include default-depend.inc
Requires: %name

%prep
%setup -q -n %{src_name}-%version


%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export PYTHON=/usr/bin/python%{python_version}
export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=%{_prefix}  \
	     %{gtk_doc_option}   \
            --sysconfdir=%{_sysconfdir}
make -j$CPUS

%install
make install DESTDIR=$RPM_BUILD_ROOT \
    pyexecdir=%{_libdir}/python%{python_version}/vendor-packages \
    pythondir=%{_libdir}/python%{python_version}/vendor-packages
find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.pyo" -exec rm -f {} ';'

%if %{!?_without_gtk_doc:0}%{?_without_gtk_doc:1}
rm -rf $RPM_BUILD_ROOT%{_datadir}/gtk-doc
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python?.?/vendor-packages

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/*
%if %{!?_without_gtk_doc:1}%{?_without_gtk_doc:0}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/gtk-doc
%endif


%changelog
* Mon Jun 15 2009 - halton.huo@sun.com
- Bump to 0.14.1
- Use GNOME download url
- Add dependency for python2.6
* Tue May 13 2008 - nonsea@users.sourceforge.net
- Bump to 0.10
- Update %files
* Mon Mar 17 2008 - jijun.yu@sun.com
- Correct the URL.
* Thu Jan 24 2008 - nonsea@users.sourceforge.net
- Add _without_gtk_doc control
* Tue Dec 11 2007 - nonsea@users.sourceforge.net
- Initial spec
