#
# spec file for package libnjp
#
# includes module(s): libnjp
#

Name:			 libnjp
Summary:	 	 libnjp - Creative Labs Nomad Jukebox library
Version:		 2.2.6
Release:                 1
License:                 BSD
Distribution:            Java Desktop System
Vendor:                  Sun Microsystems, Inc.
URL:                     http://libnjb.sourceforge.net/
Source:                  http://downloads.sourceforge.net/project/libnjb/libnjb/%{version}/libnjb-%{version}.tar.gz

BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%prep
#%setup -q -n libnjp-%version
#cd %{_builddir}/%name-%version
/usr/bin/gunzip < %SOURCE | tar xvf -


%build
# temporarily moved to SFElibnjp due to /usr/bin/cd issues


%install
cd libnjb-%version
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Fri Oct 23 2009 - jchoi42@pha.jhu.edu
- initial spec
