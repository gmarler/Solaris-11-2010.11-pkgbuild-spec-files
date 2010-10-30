#!/usr/bin/perl -w

use strict 'vars';

# fetch the file from
# bug ID  ...
#22:13 < alanc> if you want to parse, you should use the text files richb made instead - that's
#               what he used to generate that page and make the changes to various gates
#22:13 < alanc> see the attachments on the "we should rename all the packages" bug:
#               http://defect.opensolaris.org/bz/show_bug.cgi?id=6186

# the attachment  "The final new package names sorted by new name."
# wget -O packagenames.sort_newnames.ts http://defect.opensolaris.org/bz/attachment.cgi?id=3635
# snippet:
# SUNWopenssl    <TAB>library/security/openssl    <TAB>'System/Security'    <TAB>OpenSSL Commands


# to get the exact build number when a package had been renamed
# write out a raw translation table which can be read in for packagenamemacros.inc 
# in spec-file-extra
# there are info files available specifying the exact build numer
#
# ##TODO## URL <place here>
#
# Idea: have a base packagenamemacros.inc and a additional include file
# with corrections to the official file. These are placed right after the
# offical include in packagenamemacros.inc to override the settings needed
# for special cases. E.g. SUNWopensslr and SUNWopensslu went to SUNWopenssl
# in that case, the name SUNWopenssl would be given back and would have to
# be re-checked that this is the final name

# Idea: package importer could help to detect the exact build number
# when a package got renamed

#NOTE: the package name -devel does not say, that there is such a package.
#      the spec file programmer has to take care about including the right
#      name, to meet old builds he wold use -devel only if that was present
#      on e.g. SXCE or S10 and not merged the -devel files into the regular
#      package (e.g. SUNWlibz)

my $TRUE = 1;
my $FALSE = 0;
my $packold = "";
my $packoldnoprefix = "";
my $packnew = "";
my $packnewhierarchical = "";
my $packgroup = "";
my $packdesc = "";


print "#Auto generated mappings for Packages in OpenSolaris IPS distrobutions\n";
print "#TODO# Add build numbers later in the include file, if the rename of a \n";
print "#specific package was performed with a specific other build number\n";
print "#Example: %if $( expr %{osbuild} '>=177' ) ... %else ... %endif \n";


while (<>) {

chomp;
next if /^ *$/;  #empty
next if /^#/;    #comments
s/ *\t/\t/g;     #strip  spaces before the <tab>
($packold, $packnew, $packgroup, $packdesc) = split (/\t/);
#print "$packold; $packnew; $packgroup; $packdesc\n";
$packnewhierarchical = $packnew;
#we hope, that there is no double name because auf the next changes of "/" and "-" and "\+" into "_"
$packnewhierarchical =~ s?/?_?g;  # replace all "/" with "_" to get a valid name for variable
$packnewhierarchical =~ s?-?_?g;  # replace all "-" with "_" to get a valid name for variable
$packnewhierarchical =~ s?\+?_?g;  # replace all "+" with "_" to get a valid name for variable
$packold =~ s/-/_/g;
print "\%define pnm_buildrequires_$packnewhierarchical $packnew\n";
print "\%define pnm_requires_$packnewhierarchical $packnew\n";
#special case, by suspicion just add -devel .. will fail the build if that name never existed
#but succeeds if automatic replacements in existing specs are done and -devel transforms into a pnm_*-devel
print "\%define pnm_buildrequires_".$packold."_devel $packnew\n";
print "\%define pnm_buildrequires_$packold $packnew\n";
print "\%define pnm_requires_$packold $packnew\n";
$packoldnoprefix = $packold;
$packoldnoprefix =~ s/^SUNW//;
print "\%define pnm_buildrequires_$packoldnoprefix $packnew\n";
print "\%define pnm_requires_$packoldnoprefix $packnew\n";

} # end while (<>)  for reading in the dump of the webpage performed\n";
