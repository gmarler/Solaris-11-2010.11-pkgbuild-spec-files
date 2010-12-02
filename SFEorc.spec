#
# spec file for package SFEorc
#

%include Solaris.inc
%include osdistro.inc

%ifarch amd64 sparcv9
%include arch64.inc
%use orc_64 = orc.spec
%endif

%if %arch_sse2
%define arch_opt --cpu=i686 --enable-mmx --enable-mmx2
%include x86_sse2.inc
%use orc_sse2 = orc.spec
%endif

%include base.inc

%use orc = orc.spec

%define src_name orc

Name:		%{orc.name}
Version:	%{orc.version}
Summary:	%{orc.summary}

Group:		%{orc.group}
License:	%{orc.license}
URL:		%{orc.url}
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%if %{os2nnn}
%if %(expr %{osbuild} '>=' 134)
buildRequires: library/desktop/gtk1
BuildRequires: developer/documentation-tool/gtk-doc
BuildRequires: developer/gnome/gettext
BuildRequires: data/docbook
%endif
%endif

%if %{os2nnn}
%if %(expr %{osbuild} '>=' 116)
%if %(expr %{osbuild} '<' 134)
#library/desktop/gtk1
# >=75 <= 133
BuildRequires: SUNWGtk 
#developer/documentation-tool/gtk-doc
# >=116 <=133
BuildRequires: SUNWgtk-doc
#developer/gnome/gettext
BuildRequires: SUNWgnome-common-devel
#data/docbook
BuildRequires: SUNWgnome-xml
%endif
%endif
%endif

# note build versions in %{os2nnn} before 116 aren't covered


#SXCE
%if %SXCE
%if %(expr %{osbuild} '<=' 130)
BuildRequires: SUNWGtku
BuildRequires: SUNWGtkr
BuildRequires: SUNWgtk-doc
# BuildRequires: data/docbook
BuildRequires: SUNWgnome-xml-root
BuildRequires: SUNWgnome-xml-share
%endif
%endif


%description
Orc is a library and set of tools for compiling and executing
very simple programs that operate on arrays of data.  The "language"
is a generic assembly language that represents many of the features
available in SIMD architectures, including saturated addition and
subtraction, and many arithmetic operations.

%package doc
Summary:	Documentation for Orc
Group:		Development/Languages
Requires:	%{name}

%description doc
Documentation for Orc.

%package devel
Summary:	Development files and static libraries for Orc
Group:		Development/Libraries
Requires:	%{name}

%prep
rm -rf %name-%version
mkdir %name-%version

%ifarch amd64 sparcv9
mkdir %name-%version/%_arch64
%orc_64.prep -d %name-%version/%_arch64
%endif

%if %arch_sse2
mkdir %name-%version/%sse2_arch
%orc_sse2.prep -d %name-%version/%sse2_arch
%endif

mkdir %name-%version/%base_arch
%orc.prep -d %name-%version/%base_arch

%build
%ifarch amd64 sparcv9
%orc_64.build -d %name-%version/%_arch64
%endif

%if %arch_sse2
%orc_sse2.build -d %name-%version/%sse2_arch
%endif

%orc.build -d %name-%version/%base_arch


%install
rm -rf $RPM_BUILD_ROOT

%ifarch amd64 sparcv9
%orc_64.install -d %name-%version/%_arch64
%endif

%if %arch_sse2
%orc_sse2.install -d %name-%version/%sse2_arch
%endif

%orc.install -d %name-%version/%base_arch


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,bin)
%{_bindir}/orc-bugreport
%{_libdir}/liborc-*.so.*
%if %arch_sse2
%{_libdir}/%{sse2_arch}/liborc-*.so.*
%endif
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/liborc-*.so.*
%endif


%files doc
%defattr(-,root,bin)
%dir %attr (0755, root, sys) %{_datadir}
%doc %{_datadir}/gtk-doc/html/orc/

%files devel
%defattr(-,root,bin)
%{_includedir}/*
%{_libdir}/liborc-*.so
%if %arch_sse2
%{_libdir}/%{sse2_arch}/liborc-*.so
%endif
%ifarch amd64 sparcv9
%dir %attr (0755, root, bin) %{_libdir}/%{_arch64}
%{_libdir}/%{_arch64}/liborc-*.so
%endif
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/orc-*.pc
%if %arch_sse2
%dir %attr (0755, root, other) %{_libdir}/%{sse2_arch}/pkgconfig
%{_libdir}/%{sse2_arch}/pkgconfig/*.pc
%endif
%ifarch amd64 sparcv9
%dir %attr (0755, root, other) %{_libdir}/%{_arch64}/pkgconfig
%{_libdir}/%{_arch64}/pkgconfig/*.pc
%endif
%{_bindir}/orcc


%changelog
* Thu Dec 02 2010 - Milan Jurik
- update to 0.4.11, enable only SSE backend because of Sun Studio
* Sat Oct 20 2010 - Thomas Wagner
- make (Build)Requires dependend of the osbuild version
* Fri Apr 09 2010 - Milan Jurik
- multiarch support
* Thu Apr 08 2010 - Milan Jurik
- update to 0.4.4 and integration to SFE
* Thu Mar 04 2010 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.3-1
- Updated to 0.4.3

* Sun Oct 18 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-4
- Removed unused libdir

* Sun Oct 18 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-3
- Specfile cleanup
- Removed tools subpackage
- Added docs subpackage

* Sat Oct 03 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-2
- Use orc as pakage name
- spec-file cleanup
- Added devel requirements
- Removed an rpath issue

* Fri Oct 02 2009 Fabian Deutsch <fabian.deutsch@gmx.de> - 0.4.2-1
- Initial release

