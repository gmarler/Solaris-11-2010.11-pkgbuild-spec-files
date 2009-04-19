#
# spec file for package SFEvagalume
#

%include Solaris.inc

Name:                    SFEvagalume
Summary:                 Last.fm client
Group:                   AudioVideo
Version:                 0.7.1
Source:                  http://vagalume.igalia.com/files/source/vagalume_%{version}.orig.tar.gz
BuildRoot:               %{_tmppath}/%{name}-%{version}
SUNW_Copyright:          %{name}.copyright

%include default-depend.inc

Requires:    SUNWgnome-libs
BuildRequires:    SUNWgnome-common-devel

%prep
%setup -q -n vagalume-%{version}.orig

%build
CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi

./configure --prefix=%{_prefix}		\
	    --bindir=%{_bindir}		\
	    --libdir=%{_libdir}		\
	    --includedir=%{_includedir}	\
	    --mandir=%{_mandir} 	\
	    --infodir=%{_infodir}	\
	    --sysconfdir=%{_sysconfdir}

make -j $CPUS


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%dir %attr (-, root, sys) /usr
%dir %attr (-, root, bin) %{_bindir}
%attr (-, root, bin) %{_bindir}/vagalume
%attr (-, root, bin) %{_bindir}/vagalumectl
%dir %attr (-, root, sys) %{_prefix}/share
%defattr (-, root, other)
%{_prefix}/share/icons
%{_prefix}/share/locale
%{_prefix}/share/pixmaps
%{_prefix}/share/applications
%{_prefix}/share/vagalume
%defattr (-, root, bin)
%{_prefix}/share/dbus-1
%attr (-, root, bin) %{_mandir}

%changelog
* Fri Apr 19 2009 - Sergio Schvezov <sergiusens@ieee.org>
- Initial spec
