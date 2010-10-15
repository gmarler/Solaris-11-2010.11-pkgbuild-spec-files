#
# spec file for package SFEhunspell
#
# includes module: hunspell
#

# To use, make sure that library/myspell/dictionary/en, for example, is
# installed, and that you have in .bashrc
# export DICPATH=/usr/share/spell/myspell
# export DICTIONARY=en_US

####			   USING WITH EMACS				    ####
#
# NOTE: To use Hunspell under Emacs, at least Emacs 23 is required.
# NOTE: For some reason, unless Emacs is started from the command line, hunspell
# WILL NOT FIND THE DICTIONARIES.  Also, for languages other than English,
# ispell often fails, complaining of "misalignment".
# It is necessary to redefine ispell's dictionary definitions, which are
# intended for aspell.  For example, place this in your .emacs file:
#
# (setq ispell-dictionary-base-alist
#   '((nil ; default
#      "[A-Za-z]" "[^A-Za-z]" "[']" t ("-d" "en_US") nil utf-8)
#     ("english" ; US English
#      "[A-Za-z]" "[^A-Za-z]" "[']" t ("-d" "en_US") nil utf-8)
#     ("german"  ; FRG German
#      "[A-Za-zäöüßA-ZÄÖÜ]" "[^A-Za-zäöüßA-ZÄÖÜ]" "[']" t ("-d" "de_DE") nil utf-8)
#     ("french"
#      "[A-Za-zÀÂÆÇÈÉÊËÎÏÔÙÛÜàâçèéêëîïôùûü]" "[^a-zÀÂÆÇÈÉÊËÎÏÔÙÛÜàâçèéêëîïôùûü]"
#      "[']" t ("-d" "fr_FR") nil utf-8)
#     ("portugese" ; Brazilian Portugese
#      "[a-zàáâãçéêíóôõúüA-ZÀÁÂÃÇÉÊÍÓÔÕÚÜ]" "[^a-zàáâãçéêíóôõúüA-ZÀÁÂÃÇÉÊÍÓÔÕÚÜ]"
#      "" nil ("-d" "pt_BR") nil utf-8)
#     ("russian"
#      "[А-Яа-яёЁ]" "[^А-Яа-яёЁ]" "[']" t ("-d" "ru_RU") nil utf-8)
# ))
#
# (eval-after-load "ispell"
#   '(setq ispell-dictionary "english"
# 	 ispell-extra-args '("-a")
# 	 ispell-silently-savep t))
#
# (setq-default ispell-program-name "hunspell")


%include Solaris.inc
%define srcname hunspell

Name:		SFEhunspell
Summary:	Spell checker
URL:		http://hunspell.sourceforge.net
Vendor:		László Németh
Version:	1.2.12
License:	MPL 1.1/GPL 2.0/LGPL 2.1
Source:		http://downloads.sourceforge.net/%{srcname}/%{srcname}-%{version}.tar.gz

%include default-depend.inc
SUNW_BaseDir:	%{_basedir}
BuildRoot:	%{_tmppath}/%{name}-%{version}-build
BuildRequires:	SUNWgmake
BuildRequires:	SUNWaconf
BuildRequires:	SUNWgnu-automake-19
Requires:	SFEncursesw
Requires:	library/readline

%package devel
Summary:	%{summary} - development files
SUNW_BaseDir:	%{_prefix}
%include default-depend.inc
Requires:	SFEhunspell


%prep
%setup -q -n %srcname-%version

%build

CPUS=`/usr/sbin/psrinfo | grep on-line | wc -l | tr -d ' '`
if test "x$CPUS" = "x" -o $CPUS = 0; then
     CPUS=1
fi
export CFLAGS="%optflags"

export CXXFLAGS="%cxx_optflags -I/usr/gnu/include/ncursesw"
export LIBS="-lsocket -lpthread -lCrun"
export LDFLAGS="-L/usr/gnu/lib -R/usr/gnu/lib"
./configure --prefix=%_prefix --enable-threads=solaris --with-ui --with-readline


gmake -j$CPUS

%install
rm -rf $RPM_BUILD_ROOT

gmake install DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr (-, root, bin)
%_bindir/*
%_libdir/*a
%_libdir/*.so*
%dir %attr (-, root, other) %_libdir/pkgconfig
%_libdir/pkgconfig/hunspell.pc
%dir %attr (-, root, sys) %_datadir
%dir %attr (-, root, other) %_datadir/locale
%attr (-, root, other) %_datadir/locale/*
%_mandir

%files devel
%defattr (-, root, bin)
%dir %attr (0755, root, bin) %{_includedir}
%{_includedir}/*

%changelog
* Thu Oct 14 2010 - Alex Viskovatoff
- Initial spec
