#
# spec file for package SFEbvi
#

%include Solaris.inc
Name:                    SFEbvi
Summary:                 bvi - display-oriented editor for binary files (vi like)
URL:			 http://bvi.sourceforge.net/
Version:                 1.3.2
Source:                  %{sf_download}/bvi/bvi-%{version}.src.tar.gz


SUNW_BaseDir:            %{_basedir}
BuildRoot:               %{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%description
The bvi is a display-oriented editor for binary files, based on the vi 
texteditor. If you are familiar with vi, just start the editor and 
begin to edit! A bmore program is also included in the package.


%prep
%setup -q -n bvi-%version

%build

./configure --prefix=%{_prefix}  \
            --mandir=%{_mandir}   \
            --disable-static


make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

# for older pkgbuild/pkgtool
test -d $RPM_BUILD_ROOT%{_docdir} || mkdir $RPM_BUILD_ROOT%{_docdir}


%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-, root, bin)
%doc CHANGES COPYING CREDITS README
%dir %attr (0755, root, bin) %{_bindir}
%{_bindir}/*
%dir %attr (0755, root, bin) %{_libdir}
%{_libdir}/*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/*
%{_mandir}/*/*


%changelog
* Sun Jan 25 2009 - Thomas Wagner
- adjust %doc and %files permissions
* Wed Jan 07 2009  - Thomas Wagner
- Initial spec inspired by a tweet from davetong
