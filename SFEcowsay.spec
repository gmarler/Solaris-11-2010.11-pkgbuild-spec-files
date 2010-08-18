#
# spec file for package SFEcowsay
#
# includes module(s): cowsay
#
%include Solaris.inc

%define src_name cowsay

Name:		SFEcowsay
Version:	3.03
Summary:	Configurable speaking/thinking cow
Group:		Amusements/Games
License:	GPLv2+ or Artistic
URL:		http://www.nog.net/~tony/warez/cowsay.shtml
Source:		http://www.nog.net/~tony/warez/%{src_name}-%{version}.tar.gz
Patch1:		cowsay-01-prefix.diff
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc

BuildRequires: SUNWgsed

%description
cowsay is a configurable talking cow, written in Perl.  It operates
much as the figlet program does, and it written in the same spirit
of silliness.
It generates ASCII pictures of a cow with a message. It can also generate
pictures of other animals.

%prep
%setup -q -n %{src_name}-%{version}
%patch1 -p1

gsed -e 's#PREFIX%%/share/cows#%{_datadir}/%{src_name}#' \
	-e 's#%%BANGPERL%%#!/usr/perl5/bin/perl#' -i %{src_name}
gsed -e 's#PREFIX%%/share/cows#%{_datadir}/%{src_name}#' \
	-e 's#/usr/local/share/cows#%{_datadir}/%{src_name}#' -i %{src_name}.1 

%build
echo No need to build anything

%install
rm -rf $RPM_BUILD_ROOT
# using install.sh is not a good idea so let's make the install manually
mkdir -p $RPM_BUILD_ROOT%{_bindir}
mkdir -p $RPM_BUILD_ROOT%{_mandir}/man1
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{src_name}
cp -p %{src_name} $RPM_BUILD_ROOT%{_bindir}
cp -p cows/* $RPM_BUILD_ROOT%{_datadir}/%{src_name}
cp -p %{src_name}.1 $RPM_BUILD_ROOT%{_mandir}/man1

ln -s %{src_name} $RPM_BUILD_ROOT%{_bindir}/cowthink
ln -s %{src_name}.1 $RPM_BUILD_ROOT%{_mandir}/man1/cowthink.1

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-, root, bin)
%doc ChangeLog LICENSE README
%{_bindir}/*
%{_mandir}/man1/cow*
%dir %attr (0755, root, sys) %{_datadir}
%dir %attr (0755, root, other) %{_docdir}
%{_datadir}/%{src_name}

%changelog
* Wed Aug 18 2010 - Milan Jurik
- Initial release based on Fedora spec
