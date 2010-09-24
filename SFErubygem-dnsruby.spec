#
# spec file for package SFErubygem-dnsruby.spec
#
# includes module(s): rubygem-dnsruby
#
%include Solaris.inc

%define src_name        dnsruby

%define gemdir %(ruby -rubygems -e 'puts Gem::dir' 2>/dev/null) 

Name:		SFErubygem-dnsruby
URL:		http://rubyforge.org/projects/dnsruby
Summary:	Dnsruby is a pure Ruby DNS client library
Version:	1.50
Group:		Development/Languages/Ruby
License:	Apache
Source:		http://rubyforge.org/frs/download.php/72505/%{src_name}-%{version}.gem
SUNW_BaseDir:	/
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
%include default-depend.inc
BuildRequires:	SUNWruby18u
Requires:	SUNWruby18u

%prep

%build

%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{gemdir}

gem install --local --install-dir $RPM_BUILD_ROOT%{gemdir} -V --force %{SOURCE}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,bin)
%dir %attr (0755, root, sys)  %{_localstatedir}
%{gemdir}

%changelog
* Fri Sep 24 2010 - Milan Jurik
- bump to 1.50
* Thu Jan 10 2010 - Milan Jurik
- Initial version
