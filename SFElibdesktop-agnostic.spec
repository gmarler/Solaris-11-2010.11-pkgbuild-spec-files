#
# spec file for package SFESFElibdesktop-agnostic.spec
#
# includes module(s): libdesktop-agnostic
#
#
%include Solaris.inc

%define pythonver 2.6

Name:           libdesktop-agnostic
Version:        0.3.90
Summary:        Provides an extensible configuration API
Release:	  1
Group:          System Environment/Libraries
License:        GPLv2+ and LGPLv2+
URL:            https://launchpad.net/libdesktop-agnostic
Source0:        http://launchpad.net/libdesktop-agnostic/0.4/%{version}/+download/%{name}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-build

#BuildRequires:  waf
#BuildRequires:  gir-repository-devel
#BuildRequires:  pygtk2-devel
#BuildRequires:  python-devel
#BuildRequires:  gobject-introspection-devel
#BuildRequires:  GConf2-devel
#BuildRequires:  SUNWvala
#BuildRequires:  gtk+-devel
#BuildRequires:  gnome-desktop-devel
#BuildRequires:  glade3-libgladeui-devel
  
#Requires:       

%description
This library provides an extensible configuration API.
A unified virtual file system API, and a desktop item editor.


%package        bin
Summary:        Helper applications for %{name}
Group:          Applications/System
Requires:       %{name} = %{version}-%{release}

%description bin
This package contains helper applications for libdesktop-agnostic, such as a 
schema converter.


%package        -n python-desktop-agnostic
Summary:        Python bindings for %{name}
Group:		Development/Languages
Requires:       %{name} = %{version}-%{release}

%description    -n python-desktop-agnostic
This package contains the Python bindings for the core library.


%package        devel
Summary:        Development files for %{name}
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:	pkgconfig

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%prep
%setup -q



%build
export CFLAGS="%{optflags}"
PYTHONDIR=%{python_sitearch} ./waf configure \
      --prefix=%{_prefix} \
      --libdir=%{_libdir} \
      --sysconfdir=%{_sysconfdir} \
      --enable-debug \
      --config-backends=gconf \
      --vfs-backends=gio \
      --desktop-entry-backends=glib \
      --with-glade
./waf -v build

%install
rm -rf $RPM_BUILD_ROOT
DESTDIR=$RPM_BUILD_ROOT ./waf install

# install man files
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1/
install -D -p -m 0644 debian/lda*1 $RPM_BUILD_ROOT%{_mandir}/man1

# fix permissions so debuginfo is stripped from .so files
find $RPM_BUILD_ROOT%{_libdir} -name *.so -exec chmod 755 {} \;

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc COPYING COPYING.GPL-2 debian/changelog
%config %{_sysconfdir}/xdg/libdesktop-agnostic/desktop-agnostic.ini
%{_libdir}/*.so.*
%dir %{_libdir}/desktop-agnostic
%{_libdir}/desktop-agnostic/modules/libda-*.so
%{_libdir}/girepository-1.0/DesktopAgnostic*-1.0.typelib

%files bin
%defattr(-,root,root,-)
%{_bindir}/lda-desktop-entry-editor
%{_bindir}/lda-schema-to-gconf
%{_mandir}/man1/lda*1.gz

%files -n python-desktop-agnostic
%defattr(-,root,root,-)
%attr(755,root,root) %{_libdir}/python%{pythonver}/site-packages/desktopagnostic
 %{_libdir}/python%{pythonver}/site-packages/desktopagnostic/__init__.p*
 %{_libdir}/python%{pythonver}/site-packages/desktopagnostic/*.so


#%dir %{python_sitearch}/desktopagnostic
#%{python_sitearch}/desktopagnostic/__init__.p*
#%{python_sitearch}/desktopagnostic/*.so

%files devel
%defattr(-,root,root,-)
%{_includedir}/*
%{_datadir}/pygtk/2.0/defs/desktopagnostic*defs
%{_datadir}/vala/vapi/desktop-agnostic*
%{_datadir}/glade3/catalogs/desktop-agnostic.xml
%{_datadir}/gir-1.0/DesktopAgnostic*-1.0.gir
%{_libdir}/pkgconfig/desktop-agnostic.pc
%{_libdir}/*.so


%changelog
* Tue Mar 06 2010 simon jin <yuntong.jin@sun.com>
- inital spec, needed in awn 0.4.0

