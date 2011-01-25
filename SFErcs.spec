#
# spec file for package SFErcs
#
# includes module: rcs
#

%include Solaris.inc
%define srcname rcs

Name:	        SFErcs
Summary:	GNU Revision Control System
URL:		http://www.cs.purdue.edu/homes/trinkle/RCS/
Vendor:		GNU Project
Version:        5.7
License:	GPLv2
Source:		http://www.cs.purdue.edu/homes/trinkle/RCS/%srcname-%version.tar.Z
SUNW_BaseDir:	%_basedir
BuildRoot:	%_tmppath/%name-%version-build
%include default-depend.inc


%prep
%setup -q -n %srcname-%version


%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

export CFLAGS="%optflags"
export LDFLAGS="%_ldflags"

./configure --prefix=$RPM_BUILD_ROOT%_prefix

gmake -j$CPUS


%install
rm -rf $RPM_BUILD_ROOT
gmake install

cd $RPM_BUILD_ROOT%_prefix
mkdir share
mv man share


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %_bindir
%_bindir/*
%dir %attr (0755, root, sys) %_datadir
%dir %attr (0755, root, bin) %_mandir
%dir %attr (0755, root, bin) %_mandir/man1
%_mandir/man1/*.1
%dir %attr (0755, root, bin) %_mandir/man5
%_mandir/man5/rcsfile.5


%changelog
* Tue Jan 18 2011 - Alex Viskovatoff
- Initial spec
