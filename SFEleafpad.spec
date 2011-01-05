#
# spec file for package SFEleafpad
#
# includes module(s): leafpad
#
%include Solaris.inc

Name:		SFEleafpad
Summary:	Leafpad - A GTK+ based text editor
Version:	0.8.18.1
Source:		http://savannah.nongnu.org/download/leafpad/leafpad-%{version}.tar.gz
URL:		http://tarot.freeshell.org/leafpad/
License:	GPLv2
Group:		Office/Editor
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc
BuildRequires:	SUNWgnome-common-devel

%if %build_l10n
%package l10n
Summary:                %{summary} - l10n files
SUNW_BaseDir:           %{_basedir}
%include default-depend.inc
Requires:               %{name}
%endif

%prep
%setup -q -n leafpad-%version

%build
./configure --prefix=%{_prefix} \
            --mandir=%{_mandir} \
            --libdir=%{_libdir} \
            --libexecdir=%{_libexecdir} \
            --infodir=%{_infodir} \
            --sysconfdir=%{_sysconfdir} \
            --datadir=%{_datadir} \
            --bindir=%{_bindir}

make

%install
make install DESTDIR=$RPM_BUILD_ROOT
%if %build_l10n
%else
rm -fr $RPM_BUILD_ROOT%{_datadir}/locale
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, sys)

%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*

%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_datadir}/applications
%{_datadir}/applications/*
%dir %attr (0755, root, other) %{_datadir}/pixmaps
%{_datadir}/pixmaps/*

%defattr (-, root, other)
%{_datadir}/icons

%if %build_l10n
%files l10n
%defattr (-, root, bin)
%dir %attr (0755, root, sys) %{_datadir}
%attr (-, root, other) %{_datadir}/locale
%endif

%changelog
* Wed Jan 05 2011 - Milan Jurik
- bump to 0.8.18.1
* Mon May 17 2010 - Milan Jurik
- bump to 0.8.17
* Sun Dec 25 2007 - Ananth Shrinivas <ananth@sun.com>
- Cleaned up spec file and fixed attributes
* Sat Dec 23 2007 - pradhap (at) gmail.com
- Initial leafpad spec file
