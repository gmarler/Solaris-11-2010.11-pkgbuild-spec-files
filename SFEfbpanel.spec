#
# spec file for package SFEfbpanel.spec
#
#
# spec file for package fbpanel
#
%include Solaris.inc

Name:		fbpanel
Version:	6.0
Summary:	A lightweight X11 desktop panel
Group:		User Interface/Desktops
License:	LGPLv2+ and GPLv2+
URL:		http://fbpanel.sourceforge.net
Source:		http://downloads.sourceforge.net/%{name}/%{name}-%{version}.tbz2
BuildRoot:  %{_tmppath}/%{name}-%{version}-build

%description
fbpanel is a lightweight X11 desktop panel. It works with any ICCCM / NETWM 
compliant window manager such as sawfish, metacity, openbox , xfwm4, or KDE.
It features tasklist, pager, launchbar, clock, menu and systray.

%prep
%setup -q


%build

./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \

make


%install
make install DESTDIR=$RPM_BUILD_ROOT

# desktop file stuff

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)
%doc CHANGELOG COPYING CREDITS README

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/%{name}

%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{name}

%dir %attr(0755, root, bin) %{_mandir}
%{_mandir}/man1/%{name}.1.*

%changelog
* Thu Jun 10 2010 - pradhap (at) gmail.com
- Initial SFEfbpanel spec file.
