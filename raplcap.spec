Summary:	C interface for getting/setting power caps with Intel RAPL
Summary(pl.UTF-8):	Interfejs C do odczytu/zapisu ograniczeń energii przy użyciu Intel RAPL
Name:		raplcap
Version:	0.5.0
Release:	1
License:	BSD
Group:		Applications/System
#Source0Download: https://github.com/powercap/raplcap/releases
Source0:	https://github.com/powercap/raplcap/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	1f8f6a5435e3311fe9f3b1678317f4aa
URL:		https://github.com/powercap/raplcap
BuildRequires:	cmake >= 2.8.12
BuildRequires:	pkgconfig
BuildRequires:	powercap-devel >= 0.3.0
Requires:	powercap >= 0.3.0
# so far only Intel CPUs are supported
ExclusiveArch:	i686 pentium4 x86_64 ia32e x32
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
This project provides the powercap library - a generic C interface to
the Linux power capping framework (sysfs interface). It includes an
implementation for working with Intel Running Average Power Limit
(RAPL).

%description -l pl.UTF-8
Ten projekt dostarcza bibliotekę powercap - ogólny interfejs C do
szkieletu Linuksa ograniczającego zużycie energii (przez interfejs
sysfs). Zawiera implementację działającą z Intel RAPL (Running Average
Power Limit).

%package devel
Summary:	Header files for raplcap libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek raplcap
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	powercap-devel >= 0.3.0

%description devel
Header files for raplcap libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek raplcap.

%prep
%setup -q

%build
install -d build
cd build
# .pc file generation expects relative CMAKE_INSTALL_{INCLUDE,LIB}DIR
%cmake .. \
	-DCMAKE_INSTALL_INCLUDEDIR=include \
	-DCMAKE_INSTALL_LIBDIR=%{_lib}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS LICENSE README.md RELEASES.md
%attr(755,root,root) %{_bindir}/rapl-configure-msr
%attr(755,root,root) %{_bindir}/rapl-configure-powercap
%attr(755,root,root) %{_libdir}/libraplcap-msr.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libraplcap-msr.so.0
%attr(755,root,root) %{_libdir}/libraplcap-powercap.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libraplcap-powercap.so.0
%{_mandir}/man1/rapl-configure-msr.1*
%{_mandir}/man1/rapl-configure-powercap.1*

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libraplcap-msr.so
%attr(755,root,root) %{_libdir}/libraplcap-powercap.so
%{_includedir}/raplcap
%{_pkgconfigdir}/raplcap-msr.pc
%{_pkgconfigdir}/raplcap-powercap.pc
