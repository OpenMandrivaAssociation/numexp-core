%define	version	0.16.1
%define release	8

%define major	0
%define libname %mklibname numexp %major
%define develname %mklibname -d numexp

Summary:	Family of open-source applications for numeric computation
Name:		numexp-core
Version:	%{version}
Release:	%{release}
License:	GPL
Group:		Sciences/Mathematics
URL:		http://numexp.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Source:		http://prdownloads.sourceforge.net/numexp/%{name}-%{version}.tar.bz2
Patch0:		numexp-core-0.16.1-no-install-hook.patch
Patch1:		numexp-core-0.16.1-fix-format-errors.patch
Patch2:		numexp-core-0.16.1-fix-linking.patch
Patch3:		%{name}-0.16.0-Makefile-path.patch

BuildRequires:	gmp-devel
BuildRequires:	gsl-devel >= 1.4
BuildRequires:	libbonobo2_x-devel
BuildRequires:	readline-devel
BuildRequires:	termcap-devel
BuildRequires:	popt-devel
BuildRequires:	flex
BuildRequires:	python-base
BuildRequires:	perl-XML-LibXML
BuildRequires:	perl-XML-DT >= 0.26
BuildRequires:	perl-DB_File >= 1.803
BuildRequires:	mpfr-devel
Requires:	%{libname} = %{version}

%description
This package is part of the NumExp project, which could be described as a
mathematical computation environment or even as a programming language.

It contains the backend kernel and a simple text client.
No GUI or graphics are available here.

%package	-n %{libname}
Summary:	Family of open-source applications for numeric computation
Group:		Sciences/Mathematics
Provides:	libnumexp = %{version}-%{release}
Requires:	%{name} = %{version}

%description	-n %{libname}
This package is part of the NumExp project, which could be described as a
mathematical computation environment or even as a programming language.

It contains the core libraries, which are necessary for any application that
uses NumExp.

%package	-n %{develname}
Summary:	Family of open-source applications for numeric computation
Group:		Development/C
Provides:	%{name}-devel = %{version}-%{release}
Provides:	numexp-devel = %{version}-%{release}
Provides:	libnumexp-devel = %{version}-%{release}
Requires:	%{libname} = %{version}
Obsoletes:	%{libname}-devel

%description	-n %{develname}
This package contains header and development files of NumExp.
It is necessary only if you want to compile programs that uses NumExp.

%prep
%setup -q
%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p0

%build
autoreconf -fi
%configure2_5x
%make

%install
rm -rf %{buildroot}
%makeinstall_std

%{find_lang} %{name}

# remove files not distributed
rm -f %{buildroot}%{_libdir}/orbit-2.0/*.la \
      %{buildroot}%{_libdir}/numexp/modules/*.la \

%clean
rm -rf %{buildroot}

%if %mdkversion < 200900
%post -n %{libname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libname} -p /sbin/ldconfig
%endif

%files -f %{name}.lang
%defattr(-,root,root)
%doc README
%{_bindir}/*
%{_libexecdir}/numexp-kernel
%{_libdir}/bonobo/servers/*.server
%{_prefix}/lib/numexp
%{_libdir}/orbit-2.0/*.so
%{_datadir}/idl/*.idl
%{_datadir}/%{name}
%{_sysconfdir}/*

%files -n %{libname}
%defattr(-,root,root)
%{_libdir}/lib*.so.*

%files -n %{develname}
%defattr(-,root,root)
%doc ChangeLog
%{_libdir}/lib*.so
%{_libdir}/lib*.la
%{_libdir}/pkgconfig/*
%{_includedir}/*
