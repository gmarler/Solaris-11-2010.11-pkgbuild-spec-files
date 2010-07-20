#
# spec file for package SFEpolyml 
#
# Copyright 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

%include Solaris.inc

%define cc_is_gcc 1
%include base.inc

%define src_name         polyml
%define src_ver          5.3

Name:                    SFEpolyml 
Summary:                 polyml - The Poly/ML implementation of Standard ML
Version:                 %{src_ver}
Release:                 1
License:                 LGPL
Group:                   Development/Languages/Polyml
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://www.polyml.org/
Source:                  http://downloads.sourceforge.net/project/polyml/polyml/5.3/%{src_name}.%{src_ver}.tar.gz
SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{src_name}.%{src_ver}

%description
Poly/ML is a full implementation of Standard ML available as open-source.

%include default-depend.inc

Requires: 	SFEgcc

if [ ! `which latex` ]
then
BuildRequires: 	SFEtexlive
fi

%prep
%setup -q -n %{src_name}.%{version}

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
%if %{cc_is_gcc}
export CC=gcc
export CXX=g++
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LD_OPTIONS="-L/usr/gnu/lib -R/usr/gnu/lib"
%else
# It does not compile with Sun Studio 12u1
sed -i -e 's, -Wall -fno-strict-aliasing,,' libpolymain/Makefile.am libpolymain/Makefile.in libpolyml/Makefile.am libpolyml/Makefile.in Makefile.am Makefile.in
sed -i -e 's, -Wall,,' libpolymain/Makefile.am libpolymain/Makefile.in libpolyml/Makefile.am libpolyml/Makefile.in Makefile.am Makefile.in
export check_cpp="yes"
export LDFLAGS="%_ldflags"
%endif

./configure --prefix=%{_prefix}                 \
            --bindir=%{_bindir}			\
            --sbindir=%{_sbindir}		\
            --libdir=%{_libdir}			\
            --libexecdir=%{_libexecdir}         \
            --datadir=%{_datadir}               \
            --mandir=%{_mandir}                 \
            --infodir=%{_infodir}               \
            --sysconfdir=%{_sysconfdir}         \
            --localstatedir=%{_localstatedir}

%build
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
%if %{cc_is_gcc}
export CC=gcc
export CXX=g++
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LD_OPTIONS="-L/usr/gnu/lib -R/usr/gnu/lib"
%else
export LDFLAGS="%_ldflags"
%endif
export LD_LIBRARY_PATH="${PWD}/kernel/byterun"
make VERBOSE=1

%install
rm -rf $RPM_BUILD_ROOT

export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"
%if %{cc_is_gcc}
export CC=gcc
export CXX=g++
export LDFLAGS="%_ldflags -L/usr/gnu/lib -R/usr/gnu/lib"
export LD_OPTIONS="-L/usr/gnu/lib -R/usr/gnu/lib"
%else
export LDFLAGS="%_ldflags"
%endif
make DESTDIR=$RPM_BUILD_ROOT install VERBOSE=1

# Prepare lists of files for packaging
touch SFEpolyml-all.files

find $RPM_BUILD_ROOT%{_prefix} \( -type f -o -type l \) -name "*" > SFEpolyml-all.files
sort SFEpolyml-all.files > SFEpolyml-all-sort.files
# Clean up syntax for %files section
sed -i -e 's:'"$RPM_BUILD_ROOT"'::' SFEpolyml-all-sort.files

%clean
rm -rf $RPM_BUILD_ROOT

%files -f SFEpolyml-all-sort.files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%dir %attr (0755, root, bin) %{_libdir}
%dir %attr (0755, root, sys) %{_datadir}

%changelog
* Tue July 20 2010 - markwright@internode.on.net
- Initial spec
