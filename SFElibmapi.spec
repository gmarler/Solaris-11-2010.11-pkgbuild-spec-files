#
# Copyright 2009 Sun Microsystems, Inc.
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.

%include Solaris.inc
%define major_version 0.9

Name:                SFElibmapi
Summary:             A client-side implementation of the MAPI protocol that is used by Microsoft Exchange and Outlook. 
Version:             0.9
Source:              http://downloads.sourceforge.net/openchange/openchange-%{version}-COCHRANE.tar.gz
SUNW_BaseDir:        %{_basedir}
BuildRoot:           %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

#####################################
##  Package Requirements Section   ##
#####################################
BuildRequires: SUNWgcc
    
%prep
%setup -q -n openchange-%{version}-COCHRANE

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

#export CFLAGS="%optflags"
export CFLAGS="-g -D__FUNCTION__=__func__"
export LDFLAGS="%_ldflags -ltevent"

./autogen.sh
./configure --prefix=%{_prefix}  \
            --with-moduelsdir=%{_libdir}/libmapi

make -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

make install DESTDIR=$RPM_BUILD_ROOT

find $RPM_BUILD_ROOT -type f -name "*.la" -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type f -name "*.a" -exec rm -f {} ';'


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/*.so*
%{_libdir}/mapistore_backends/*
%{_libdir}/python2.6
%{_libdir}/nagios
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/setup/*
/usr/modules/*

%changelog
* Wed Dec 02 2009 - brian.lu@sun.com
- Add a new patch libmapi-03-remove-gcc-options.diff
  Add a new patch libmapi-05-samba4alpha9.diff for Samba4 alpha9
* Mon Nov 02 2009 - brian.lu@sun.com
- Add patch libmapi-04-no-return-value.diff
  Add major_version
* Tue Aug 04 2009 - brian.lu@sun.com
- Bump to 0.8.2 
  Update the patch libmapi-01-solaris.diff
* Wed Feb 18 2009 - jedy.wang@sun.com
- Do not use optimization option for now.
* Tue Feb 17 2009 - jedy.wang@sun.com
- Fix file attribute problem.
* Thu Feb 12 2009 - jedy.wang@sun.com
- Initial spec
