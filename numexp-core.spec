%define	version	0.11.0
%define release	%mkrel 1

%define major	0
%define libname %mklibname numexp

Summary:	NumExp is a family of open-source applications for numeric computation
Name:		numexp-core
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Sciences/Mathematics
URL:		http://numexp.sourceforge.net/
Buildroot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source:		http://prdownloads.sourceforge.net/numexp/%{name}-%{version}.tar.bz2
Patch0:		%{name}-0.8.0-empty-config.patch
Patch1:		%{name}-0.10.0-db42.patch
Patch2:		%{name}-0.11.0-gcc40.patch

BuildRequires:	db4.2-devel >= 4.2.52
BuildRequires:	gmp-devel
BuildRequires:	gsl-devel >= 1.4
BuildRequires:	libbonobo2_x-devel
BuildRequires:	readline-devel
BuildRequires:	termcap-devel
BuildRequires:	popt-devel
BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	python-base
BuildRequires:	perl-XML-LibXML
BuildRequires:	perl-XML-DT >= 0.26
BuildRequires:	perl-DB_File >= 1.803
Requires:	%{libname}%{major} = %{version}

%description
This package is part of the NumExp project, which could be described as a
mathematical computation environment or even as a programming language.

It contains the backend kernel and a simple text client.
No GUI or graphics are available here.

%package	-n %{libname}%{major}
Summary:	NumExp is a family of open-source applications for numeric computation
Group:		Sciences/Mathematics
Provides:	%{libname} = %{version}-%{release}
Requires:	%{name} = %{version}

%description	-n %{libname}%{major}
This package is part of the NumExp project, which could be described as a
mathematical computation environment or even as a programming language.

It contains the core libraries, which are necessary for any application that
uses NumExp.

%package	-n %{libname}%{major}-devel
Summary:	NumExp is a family of open-source applications for numeric computation
Group:		Development/C
Provides:	%{libname}-devel = %{version}-%{release}
Provides:	%{name}-devel = %{version}-%{release}
Requires:	%{libname}%{major} = %{version}

%description	-n %{libname}%{major}-devel
This package contains header and development files of NumExp.
It is necessary only if you want to compile programs that uses NumExp.

%prep
%setup -q
%patch0 -p1 -b .emptyconfig
%patch1 -p1 -b .db42
%patch2 -p1 -b .gcc40

# needed for db4.2 patch
autoconf

%build
%configure2_5x \
%if %{?_enable_debug_package:1}%{!?_enable_debug_package:0}
	--enable-element-debug \
	--enable-namespace-debug
%endif

# (Abel) let it regenerate all DB files
find -name '*.db' -type f -print0 | xargs -r -0 rm -f

%make

# (Abel) bad threading behavior??
LD_ASSUME_KERNEL=2.4.20 make check

%install
rm -rf %{buildroot}
%makeinstall_std

%{find_lang} %{name}

# remove files not distributed
rm -f %{buildroot}%{_libdir}/orbit-2.0/*.la \
      %{buildroot}%{_libdir}/numexp/modules/*.la \

%clean
rm -rf %{buildroot}

%post -n %{libname}%{major} -p /sbin/ldconfig
%postun -n %{libname}%{major} -p /sbin/ldconfig

%files -f %{name}.lang
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_libexecdir}/numexp-kernel
%{_libdir}/bonobo/servers/*.server
%{_libdir}/numexp
%{_libdir}/orbit-2.0/*.so
%{_datadir}/idl/*.idl
%{_datadir}/%{name}

%files -n %{libname}%{major}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{libname}%{major}-devel
%defattr(-,root,root)
%doc ChangeLog
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/*
%{_includedir}/*


