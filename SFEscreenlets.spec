Summary:	Small applications that are similar to OS X's widgets on the Dashboard

Name:		screenlets
Version:	0.1.2
Release:	1
License:	GPL
Group:		X11/Applications
Source0:	https://code.launchpad.net/screenlets/trunk/%{version}/+download/%{name}-%{version}.tar.bz2
		
URL:		http://www.screenlets.org/

Requires:	python-gnome-desktop-keyring
Requires:	python-gnome-desktop-libwnck
Requires:	python-pyxdg

%{?!pythonver:%define pythonver 2.6}

BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%description
Small applications that are similar to OS X's widgets on the
Dashboard.

%prep
%setup -q -n %{name}

%build
python%{pythonver} setup.py build

%install
rm -rf $RPM_BUILD_ROOT

python%{pythonver} setup.py install \
	--optimize=2 \
	--root $RPM_BUILD_ROOT \
	--prefix %{_prefix}


# move to vendor-packages
mkdir -p $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages
mv $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages/* \
   $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/vendor-packages/
rmdir $RPM_BUILD_ROOT%{_libdir}/python%{pythonver}/site-packages

find $RPM_BUILD_ROOT -name '*.pyo' -exec rm {} \;

%clean
rm -rf $RPM_BUILD_ROOT



%files
%defattr(644,root,root,755)
%doc CHANGELOG README TODO
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/screenlets*

%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/python%{pythonver}/vendor-packages/*

%{_datadir}/screenlets
%dir %{_datadir}/screenlets-manager
%attr(755,root,root) %{_datadir}/screenlets-manager/*.py

%{_datadir}/screenlets-manager/*.png
%{_datadir}/screenlets-manager/*.svg
%{_datadir}/screenlets-manager/prefs.js

%dir %{_datadir}/applications
%{_datadir}/applications/screenlets-manager.desktop	

%dir %{_datadir}/locale
%{_datadir}/locale/*	
%dir %{_datadir}/icons/screenlets.svg

%changelog
* Mon Oct 11 2010 - yun-tong.jin@oracle.com
- Init spec with version 0.1.2

