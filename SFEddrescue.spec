#
# Copyright (c) 2010 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc

%define src_name ddrescue

Name:                SFEddrescue
Summary:             GNU ddrescue - Data recovery tool
Version:             1.12
License:             GPLv3+
Source:              http://ftp.gnu.org/gnu/ddrescue/%{src_name}-%{version}.tar.gz
URL:                 http://www.gnu.org/software/ddrescue/ddrescue.html

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
Requires: SUNWlibC

%prep
%setup -q -n %{src_name}-%{version}

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

export CXX="$CXX -norunpath"
export CFLAGS="%{optflags}"
export CXXFLAGS="%{cxx_optflags}"
export LDFLAGS="%{_ldflags} -lCrun"

./configure --prefix=%{_prefix}		\
            --bindir=%{_bindir}		\
	    --mandir=%{_mandir}		\
	    --infodir=%{_infodir}	\
	    CXX="$CXX"			\
	    CFLAGS="$CFLAGS"		\
	    CXXFLAGS="$CXXFLAGS"	\
	    LDFLAGS="$LDFLAGS"

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
rm -f $RPM_BUILD_ROOT%{_infodir}/dir

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_infodir}
%{_infodir}/*
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/*

%changelog
* Sun Apr 18 2010 - Albert Lee <trisk@opensolaris.org>
- Initial spec
