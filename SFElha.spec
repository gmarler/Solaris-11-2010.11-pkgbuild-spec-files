#
# spec file for package SFElha
#
# includes module(s): lha
#

%include Solaris.inc

%define src_name lha
%define src_version 1.14i-ac20040929

Name:		SFElha
Version:	1.14.9.1
Summary:	LHA/LZH archiver

Group:		Applications/Archiving
URL:		http://www2m.biglobe.ne.jp/~dolphin/%{src_name}/lha-unix.htm
Source:		http://dl.sourceforge.jp/%{src_name}/11617/%{src_name}-%{src_version}.tar.gz
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build

%include default-depend.inc

%description
LhA is an archiving and compression utility for LHarc format archive.
LhA is mostly used in the Amiga and in the DOS world, but can be used 
under Linux to extract files from .lha and .lzh archives. 

Install the LhA package if you need to extract files from .lha or .lzh
Amiga or DOS archives, or if you have to build LhA archives to
be read on the Amiga or DOS.

%prep
%setup -q -n %{src_name}-%{src_version}

%build
./configure --prefix=%{_prefix} --mandir=%{_mandir}

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,bin)
%{_bindir}/%{src_name}
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr(0755, root, bin) %{_mandir}
%dir %attr(0755, root, bin) %{_mandir}/mann
%{_mandir}/mann/*


%changelog
* Mon May 24 2010 - Milan Jurik
- initial import to SFE
