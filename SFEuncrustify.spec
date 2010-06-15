#
# spec file for package SFEuncrustify.spec
#
# includes module(s): uncrustify
#
%include Solaris.inc
%define cc_is_gcc 1
%include base.inc

%define src_name	uncrustify

Name:		SFEuncrustify
Version:	0.56
Summary:	Reformat Source
Group:		Development/Tools
License:	GPLv2
URL:		http://uncrustify.sourceforge.net/
Source:		%{sf_download}/%{src_name}/%{src_name}-%{version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

%description
Source Code Beautifier for C, C++, C#, D, Java, and Pawn

%prep
%setup -q -n %{src_name}-%{version}

%build
export CC=gcc
export CXX=g++
export CFLAGS="%optflags"
export CXXFLAGS="%cxx_optflags"

./configure --prefix=%{_prefix}

make


%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT/%{_mandir}/man1
install -m644 man/%{src_name}.1 $RPM_BUILD_ROOT/%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT/%{_docdir}/%{src_name}
cp -r documentation/* $RPM_BUILD_ROOT/%{_docdir}/%{src_name}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, bin)
%doc COPYING AUTHORS README NEWS
%{_bindir}/%{src_name}
%dir %attr (0755, root, sys) %{_datadir}
%{_datadir}/%{src_name}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/%{src_name}
%{_mandir}/man1/%{src_name}.1


%changelog
* Tue Jun 15 2010 - Milan Jurik
- initial import to SFE
* Mon May 24 2010 Neal Becker <ndbecker2@gmail.com> - 0.56-2
- Remove 'BUGS'

* Mon May 24 2010 Neal Becker <ndbecker2@gmail.com> - 0.56-1
- Update to 0.56

* Sat Oct 17 2009 Neal Becker <ndbecker2@gmail.com> - 0.54-1
- Update to 0.54

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.52-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Sun Mar  8 2009 Neal Becker <ndbecker2@gmail.com> - 0.52-1
- Update to 0.52

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.50-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov  3 2008 Neal Becker <ndbecker2@gmail.com> - 0.50-2
- Documentation fixes

* Mon Nov  3 2008 Neal Becker <ndbecker2@gmail.com> - 0.50-1
- Update to 0.50

* Sun Jun 15 2008 Neal Becker <ndbecker2@gmail.com> - 0.47-1
- Update to 0.47

* Thu Apr 24 2008 Neal Becker <ndbecker2@gmail.com> - 0.46-1
- Update to 0.46

* Sun Mar  9 2008 Neal Becker <ndbecker2@gmail.com> - 0.45-1
- Update to 0.45

* Wed Feb 13 2008 Neal Becker <ndbecker2@gmail.com> - 0.44-1
- Update to 0.44

* Tue Jan 29 2008 Neal Becker <ndbecker2@gmail.com> - 0.43-2
- Remove explicit dep libstdc++

* Tue Jan 29 2008 Neal Becker <ndbecker2@gmail.com> - 0.43-1
- Update to 0.43

* Sun Nov 18 2007 Neal Becker <ndbecker2@gmail.com> - 0.41-1
- Update to 0.41

* Tue Nov  6 2007 Neal Becker <ndbecker2@gmail.com> - 0.40-2
- Increase release tag to satisfy cvs
- Bump tag

* Tue Nov  6 2007 Neal Becker <ndbecker2@gmail.com> - 0.40-1
- Update to 0.40

* Wed Aug 29 2007 Fedora Release Engineering <rel-eng at fedoraproject dot org> - 0.35-2
- Rebuild for selinux ppc32 issue.

* Fri Jul 20 2007 Neal Becker <ndbecker2@gmail.com> - 0.35-1
- 0.35

* Tue Jun 12 2007 Neal Becker <ndbecker2@gmail.com> - 0.34-1
- bump to 0.34

