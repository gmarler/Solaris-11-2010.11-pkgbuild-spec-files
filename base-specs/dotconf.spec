# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
Summary:	Support for configuration file parsing
Name:		dotconf
Version:	1.0.13
License:	LGPL v2.1
Group:		Libraries
Source: 	http://www.azzit.de/dotconf/download/v1.0/%{name}-%{version}.tar.gz

%description
A configuration file parser library

%prep
%setup -q

%build
./configure --prefix=%{_prefix}
make

%install
make install DESTDIR=$RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, sys) %{_datadir}/

%changelog
* Mon Sep 14 2009 - Willie Walker
- Initial spec
