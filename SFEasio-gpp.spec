#
# Copyright 2008 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define        major      1
%define        minor      4
%define        patchlevel 1

# Download manually
# %define src_url http://heanet.dl.sourceforge.net/project/asio/asio/%{major}.%{minor}.%{patchlevel}%20%28Stable%29

# If SFEasio is not install. Make sure all files are installed
%define SFEasio	%(/usr/bin/pkginfo -q SFEasio && echo 1 || echo 0)

Name:                SFEasio-gpp
Summary:             Asio is a cross-platform C++ library for network and low-level I/O programming (g++-built)
Version:             %{major}.%{minor}.%{patchlevel}
License:             Boost Software License 1.0
Source:              asio-%{major}.%{minor}.%{patchlevel}.zip
URL:                 https://sourceforge.net/projects/asio/

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SFEboost-gpp

%package devel
Summary:        %{summary} - development files
SUNW_BaseDir:   %{_basedir}
%include default-depend.inc

%prep
%setup -q -n asio-%{major}.%{minor}.%{patchlevel}
rm -rf ../boost*

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC=gcc
export CXX=g++
export CXXFLAGS="%gcc_cxx_optflags"
export LDFLAGS="%_ldflags -L/lib -R/lib -L%{_cxx_libdir} -R%{_cxx_libdir}"

./configure --prefix=%{_prefix}		\
            --mandir=%{_mandir}		\
            --includedir=%{_includedir}	\
            --datadir=%{_datadir}	\
            --libdir=%{_cxx_libdir}	\
            --sysconfdir=%{_sysconfdir}	

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT nobase_includeHEADERS_INSTALL='install -D -p -m644'

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%{_includedir}

%changelog
* Tue Sep 08 2009 - drdoug007@gmail.com
- Initial version
