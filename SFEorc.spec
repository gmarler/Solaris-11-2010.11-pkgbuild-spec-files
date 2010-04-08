#
# spec file for package SFEorc
#

%include Solaris.inc

%define src_name orc

Name:		SFEorc
Version:	0.4.4
Summary:	The Oil Run-time Compiler

Group:		System Environment/Libraries
License:	BSD
URL:		http://code.entropywave.com/projects/orc/
Source:		http://code.entropywave.com/download/orc/orc-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

BuildRequires: SUNWgtk-doc

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
%setup -q -n orc-%{version}

%build
LDFLAGS=-lm ./configure --prefix=%{_prefix} --disable-static --enable-gtk-doc

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# Remove unneeded files.
find $RPM_BUILD_ROOT/%{_libdir} -name \*.a -or -name \*.la -delete
rm -rf $RPM_BUILD_ROOT/%{_libdir}/orc


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,bin)
%{_libdir}/liborc-*.so.*

%files doc
%defattr(-,root,bin)
%dir %attr (0755, root, sys) %{_datadir}
%doc %{_datadir}/gtk-doc/html/orc/

%files devel
%defattr(-,root,bin)
%{_includedir}/%{src_name}-0.4/
%{_libdir}/liborc-*.so
%dir %attr (0755, root, other) %{_libdir}/pkgconfig
%{_libdir}/pkgconfig/orc-0.4.pc
%{_bindir}/orcc


%changelog
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

