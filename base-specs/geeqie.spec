#
# spec file for package geeqie 
#
# Copyright (c) 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
#Owner: jouby
#

Summary: Graphics file browser utility.
Name: geeqie 
Version: 1.0beta2 
Release: 0
License: GPL
Group: Applications/Multimedia
#Source:  http://sourceforge.net/projects/geeqie/files/geeqie/geeqie-%{version}/geeqie-%{version}.tar.gz/download  
Source:  http://surfnet.dl.sourceforge.net/sourceforge/geeqie/geeqie-%{version}.tar.gz
#owner:jouby date:2008-07-07 bugid:2024250 type:feature
Patch1:       gqview-01-editor.diff
#owner:jouby date:2008-07-29 type:branding
Patch2:       gqview-02-manpage.diff
#owner:jouby date:2008-08-21 bugid:2063964 type:bug
Patch3:       gqview-03-remote.diff
BuildRoot: %{_tmppath}/%{name}-%{version}-root
#BuildRoot: %{_tmppath}/%{name}-%{version}-root

URL: http://geeqie.sourceforge.net

Requires: gtk2 >= 2.4.0

%description
Geeqie is a browser for graphics files.Forked from Gqview project.
Offering single click viewing of your graphics files.
Includes thumbnail view, zoom and filtering features.
And external editor support.

%prep
%setup -q -n geeqie-%version
#%patch1 -p1
#%patch2 -p1
#%patch3 -p1
%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
    CPUS=1
fi

./configure --prefix=%{_prefix} --mandir=%{_mandir} --datadir=%{_datadir} 
make -j$CPUS 

mkdir html
cp doc/*.html doc/*.txt html/.

%install
rm -rf $RPM_BUILD_ROOT

#make DESTDIR=$RPM_BUILD_ROOT mandir=$RPM_BUILD_ROOT%{_mandir} bindir=$RPM_BUILD_ROOT%{_bindir} \
# prefix=$RPM_BUILD_ROOT%{_prefix} datadir=$RPM_BUILD_ROOT%{_datadir} \
# docdir=$RPM_BUILD_ROOT%{_docdir} install

make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, root)

#%doc README COPYING TODO html
#%{_bindir}/geeqie
#%{_datadir}/locale/*/*/*
##%{_datadir}/applications/gqview.desktop
#%{_datadir}/pixmaps/gqview.png
#%{_mandir}/man?/*

%changelog
* Mon Aug 24 2009 - yuntong.jin@sun.com
- Initial build.
