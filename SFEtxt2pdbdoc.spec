#
# spec file for package txt2pdbdoc
#

%include Solaris.inc

Name:		SFEtxt2pdbdoc
Version:	1.4.4
Summary:	txt2pdbdoc is a Text-to-PalmDoc file conversion program
URL:		http://homepage.mac.com/pauljlucas/software/txt2pdbdoc/
Source:		http://homepage.mac.com/pauljlucas/software/txt2pdbdoc-%{version}.tar.gz
License:	GPLv2+
Group:		Utility
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWgawk

%prep
%setup -q -n txt2pdbdoc-%{version}

%build
export CFLAGS="%optflags"
export LDFLAGS="%{_ldflags}"
./configure  --prefix=%{_prefix}

make

%install
rm -rf $RPM_BUILD_ROOT
make install DESTDIR=$RPM_BUILD_ROOT


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%{_bindir}
%dir %attr (0755, root, sys) %{_datadir}
%{_mandir}

%changelog
* Sat Nov 27 2010 - Milan Jurik
- Initial spec
