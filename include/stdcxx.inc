#
# spec file for package: [pkg name]
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#
# includes module(s): [pkg module(s)]
# 

# Definition of path to STDCXX

%define stdcxx_dir /usr/stdcxx 
%define stdcxx_lib %{stdcxx_dir}/lib/
%define stdcxx_include %{stdcxx_dir}/include
%define stdcxx_version 4.2.1

%define stdcxx_cxxflags "%{cxx_optflags} -library=%none -staticlib=%none -norunpath -features=tmplife -features=tmplrefstatic -L%{stdcxx_lib} -R%{stdcxx_lib} -I%{stdcxx_include} -lstd -lm"

%define stdcxx_ldflags "-library=%none -staticlib=%none -L%{stdcxx_dir} -R%{stdcxx_dir}"

