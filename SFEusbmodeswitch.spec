#
# spec file for package SFEusbmodeswitch
#
# includes module(s): usbmodeswitch
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define	src_name	usb-modeswitch
%define	src_date	20101222

Name:		SFEusbmodeswitch
Version:	1.1.6
Summary:	A mode switching tool for controlling multiple-device USB gear
Group:		System/Utilities
License:	GPLv2+
URL:		http://www.draisberghof.de/usb_modeswitch/
Source:		http://www.draisberghof.de/usb_modeswitch/%{src_name}-%{version}.tar.bz2
Source1:	http://www.draisberghof.de/usb_modeswitch/%{src_name}-data-%{src_date}.tar.bz2
Source2:	http://www.draisberghof.de/usb_modeswitch/device_reference.txt.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires:	SUNWlibusb
Requires:	SUNWlibusb
Requires:	%{name}-root

%description
USB_ModeSwitch is a mode switching tool for controlling "flip flop"
(multiple device) USB gear. It allows so-called "Zero-CD" devices that
show up as USB storage initially to be switched into their more useful
"application mode". This is most common for UMTS/3G wireless WAN
devices.

%package root
SUNW_Basedir:   /
%include default-depend.inc

%prep
%setup -q -n %{src_name}-%{version}

%build
make CFLAGS="%{optflags}"

%install
rm -rf %{buildroot}
make DESTDIR=%{buildroot} install

rm %{buildroot}/lib/udev/usb_modeswitch
rmdir %{buildroot}/lib/udev
rmdir %{buildroot}/lib

mkdir -p %{buildroot}/%{_datadir}/%{src_name} && cp %{SOURCE1} %{buildroot}/%{_datadir}/%{src_name} && cp %{SOURCE2} %{buildroot}/%{_datadir}/%{src_name}

%clean
rm -rf %{buildroot}

%files
%defattr(-, root, bin)
%doc README COPYING ChangeLog
%{_sbindir}/usb_modeswitch
%{_sbindir}/usb_modeswitch_dispatcher
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr (0755, root, bin) %{_mandir}
%dir %attr (0755, root, bin) %{_mandir}/man1
%{_mandir}/man1/usb_modeswitch.1
%{_datadir}/%{src_name}

%files root
%defattr(-, root, sys)
%config %{_sysconfdir}/usb_modeswitch.conf

%changelog
* Mon Jan 24 2011 - Milan Jurik
- initial spec
