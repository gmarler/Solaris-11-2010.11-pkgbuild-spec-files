#
# spec file for package SFEunzoo
#
# includes module(s): unzoo
#

%include Solaris.inc

Name:		SFEunzoo
Version:	4.4
Summary:	ZOO archive extractor

Group:		Applications/Archiving
License:	Public Domain
URL:		http://archives.math.utk.edu/software/multi-platform/gap/util/unzoo.c
Source:		http://archives.math.utk.edu/software/multi-platform/gap/util/unzoo.c
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc


%description
'unzoo' is a zoo archive extractor.  A zoo archive is a file that
contains several files, called its members, usually in compressed form
to save space.  'unzoo' can list all or selected members or extract
all or selected members, i.e., uncompress them and write them to
files.  It cannot add new members or delete members.  For this you
need the zoo archiver, called 'zoo', written by Rahul Dhesi.


%prep
%setup -T -c -n %{name}-%{version}
cp -a %{SOURCE} .


%build
cc %{optflags} -o unzoo -DSYS_IS_UNIX unzoo.c

%install
rm -rf $RPM_BUILD_ROOT

# Install binaries
install -Dpm 755 unzoo $RPM_BUILD_ROOT%{_bindir}/unzoo
install -d $RPM_BUILD_ROOT%{_docdir}/unzoo
cat %{SOURCE} | sed -e '/SYNTAX/,/\*\//!d' | cut -c5- > $RPM_BUILD_ROOT%{_docdir}/unzoo/unzoo.txt


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,bin)
%{_bindir}/unzoo
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_docdir}/unzoo/unzoo.txt


%changelog
* Mon May 24 2010 - Milan Jurik
- initial import to SFE
