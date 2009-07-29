#
# Copyright (c) 2006 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define realname scrot 

Name:                SFEscrot
Summary:             Commandline screen capture util like "import", but using imlib2. 
Version:             0.8
Source:              http://linuxbrit.co.uk/downloads/%{realname}-%{version}.tar.gz 

SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

Requires: SFEgcc
Requires: SFEimlib2
Requires: SFEgiblib

%prep
%setup -q -n %{realname}-%version


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CC="gcc"
export CXX="g++"

./configure --prefix=%{_prefix}

make -j$CPUS 

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT
rm -rf $RPM_BUILD_ROOT/%{_prefix}/doc
mkdir $RPM_BUILD_ROOT/%{_prefix}/share
mv $RPM_BUILD_ROOT/%{_prefix}/man $RPM_BUILD_ROOT/%{_prefix}/share

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, bin) %{_mandir}
%{_mandir}/*

%changelog
* Tue Jul 28 2009 - oliver.mauras@gmail.com
- Initial spec

