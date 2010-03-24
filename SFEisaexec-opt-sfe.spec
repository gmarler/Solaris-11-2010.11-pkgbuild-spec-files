#
# spec file for package: SFEisaexec
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

#%include Solaris.inc

Name:		SFEisaexec
Summary:	Invoke isa-specific executable
Version:	1.0
License:	CDDL
Group:		System/Core
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
SUNW_Basedir:	%{_basedir}
SUNW_Copyright:	%{name}.copyright

BuildRequires:	SUNWhea

# OpenSolaris IPS Manifest fields
#Meta(info.maintainer):	Laurent Blume

%description
isaexec is a wrapper to automatically run the binary most adequate to the architecture the system is running on.

%prep

mkdir -p %{name}-%{version}
cat << EOF >  %{name}-%{version}/isaexec.c
#include <unistd.h>
#include <stdlib.h>

int
main(int argc, char *argv[], char *envp[])
{
  return (isaexec(getexecname(), argv, envp));
}
EOF

cd %{name}-%{version}

%build

export PATH=/usr/ccs/bin:/usr/bin:$PATH
cd %{name}-%{version}
cc isaexec.c -o isaexec

# NOT todo: don't change /opt/SFE. Let this hard PATH
%install
rm -rf $RPM_BUILD_ROOT
cd %{name}-%{version}
mkdir -p $RPM_BUILD_ROOT/opt/SFE/lib
cp isaexec $RPM_BUILD_ROOT/opt/SFE/lib

%clean
rm -rf $RPM_BUILD_ROOT
rm -rf %{name}-%{version}


%files
%defattr (-, root, bin)
%dir %attr(0755, root, bin) /opt/SFE/lib
/opt/SFE/lib/isaexec

%changelog
* 2010/03/16 - laurent A elanor POINT org
  Initial version
