#
# spec file for package SFEgargoyle.spec
#
# includes module(s): gargoyle
#
%include Solaris.inc

%define src_name	gargoyle
%define src_version     2009-08-25

Name:                   SFEgargoyle
URL:                    http://ccxvii.net/gargoyle/
Summary:                Interactive Fiction Player
Version:                2009.08.25
Source:                 http://garglk.googlecode.com/files/gargoyle-%{src_version}-sources.zip
Patch1:                 gargoyle-01-solaris.diff
Patch2:                 gargoyle-02-libexec.diff
Patch3:                 gargoyle-03-tads.diff
SUNW_BaseDir:           %{_basedir}
BuildRoot:              %{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires: SFEjam

%prep
%setup -q -c -n %{src_name}-%{version}
%patch1 -p1
%patch2 -p1
%patch3 -p1

%build
jam

%install
jam install

install -d $RPM_BUILD_ROOT/usr/bin
install -d $RPM_BUILD_ROOT/usr/lib/gargoyle
cp %{_builddir}/gargoyle-%{version}/build/dist/gargoyle $RPM_BUILD_ROOT/usr/bin
cp %{_builddir}/gargoyle-%{version}/build/dist/libgarglk.so $RPM_BUILD_ROOT/usr/lib

cp %{_builddir}/gargoyle-%{version}/build/dist/advsys $RPM_BUILD_ROOT/usr/lib/gargoyle
cp %{_builddir}/gargoyle-%{version}/build/dist/agility $RPM_BUILD_ROOT/usr/lib/gargoyle
cp %{_builddir}/gargoyle-%{version}/build/dist/alan2 $RPM_BUILD_ROOT/usr/lib/gargoyle
cp %{_builddir}/gargoyle-%{version}/build/dist/alan3 $RPM_BUILD_ROOT/usr/lib/gargoyle
cp %{_builddir}/gargoyle-%{version}/build/dist/frotz $RPM_BUILD_ROOT/usr/lib/gargoyle
cp %{_builddir}/gargoyle-%{version}/build/dist/geas $RPM_BUILD_ROOT/usr/lib/gargoyle
cp %{_builddir}/gargoyle-%{version}/build/dist/git $RPM_BUILD_ROOT/usr/lib/gargoyle
cp %{_builddir}/gargoyle-%{version}/build/dist/glulxe $RPM_BUILD_ROOT/usr/lib/gargoyle
cp %{_builddir}/gargoyle-%{version}/build/dist/hugo $RPM_BUILD_ROOT/usr/lib/gargoyle
cp %{_builddir}/gargoyle-%{version}/build/dist/jacl $RPM_BUILD_ROOT/usr/lib/gargoyle
cp %{_builddir}/gargoyle-%{version}/build/dist/level9 $RPM_BUILD_ROOT/usr/lib/gargoyle
cp %{_builddir}/gargoyle-%{version}/build/dist/magnetic $RPM_BUILD_ROOT/usr/lib/gargoyle
cp %{_builddir}/gargoyle-%{version}/build/dist/nitfol $RPM_BUILD_ROOT/usr/lib/gargoyle
cp %{_builddir}/gargoyle-%{version}/build/dist/scare $RPM_BUILD_ROOT/usr/lib/gargoyle
cp %{_builddir}/gargoyle-%{version}/build/dist/tadsr $RPM_BUILD_ROOT/usr/lib/gargoyle

chmod 775 $RPM_BUILD_ROOT/usr/lib/gargoyle/*
chmod 775 $RPM_BUILD_ROOT/usr/bin/gargoyle

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/lib*.so
%dir %attr (0755, root, bin) %{_libexecdir}/gargoyle
%{_libexecdir}/gargoyle/*

%changelog
%define src_version     2009-08-25
* Tue Aug 25 2009 - brian.cameron@sun.com
- Bump to 2009-08-25
* Tue Dec 30 2008 - brian.cameron@sun.com
- Initial version with 2008-12-25.
