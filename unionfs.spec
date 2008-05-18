Summary:	Unionfs control tools
Summary(pl.UTF-8):	Stakowalny, unifikujący system plików
Name:		unionfs
Version:	0.2.1
Release:	1
Epoch:		1
License:	GPL v2
Group:		Base/Kernel
Source0:	ftp://ftp.fsl.cs.sunysb.edu/pub/unionfs/unionfs-utils-0.x/%{name}_utils-%{version}.tar.gz
# Source0-md5:	c88ba424a7eb196ac930ee41ef3b6f43
URL:		http://www.filesystems.org/project-unionfs.html
BuildRequires:	automake
BuildRequires:	libuuid-devel
# NB: tools do not require -libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_bindir	%{_sbindir}

%description
Unionfs is a stackable unification file system, which can appear to
merge the contents of several directories (branches), while keeping
their physical content separate. Unionfs is useful for unified source
tree management, merged contents of split CD-ROM, merged separate
software package directories, data grids, and more. Unionfs allows any
mix of read-only and read-write branches, as well as insertion and
deletion of branches anywhere in the fan-out.

%description -l pl.UTF-8
Unionfs to stakowalny, unifikujący system plików, potrafiący łączyć
zawartość kilku katalogów (gałęzi), zachowując oddzielnie ich fizyczną
zawartość. Unionfs jest przydatny do zarządzania połączonym drzewem
źródeł, połączoną zawartością podzielonych CD-ROM-ów, połączonymi
oddzielnymi katalogami z pakietami programów, tabelami danych itp.
Unionfs pozwala na dowolne mieszanie gałęzi tylko do odczytu oraz do
odczytu i zapisu, a także wstawianie i usuwanie gałęzi w dowolnym
miejscu.

%package libs
Summary:	Shared unionfs utils library
Group:		Libraries

%description libs
This package contains shared library used to control a unionfs mount.

%package devel
Summary:	Header files for unionfs library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki unionfs
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}

%description devel
Header files for unionfs library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki unionfs.

%package static
Summary:	Static unionfs library
Summary(pl.UTF-8):	Statyczna biblioteka unionfs
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static unionfs library.

%description static -l pl.UTF-8
Statyczna biblioteka unionfs.

%prep
%setup -q -n %{name}_utils-%{version}

%build
cp -f /usr/share/automake/config.sub .
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS INSTALL README
%attr(755,root,root) %{_bindir}/unionctl
%attr(755,root,root) %{_bindir}/uniondbg
%attr(755,root,root) %{_bindir}/unionimap
%{_mandir}/man8/*

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libunionfs_utils.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libunionfs_utils.so.0

%files devel
%defattr(644,root,root,755)
%{_includedir}/unionfs_utils.h
%{_libdir}/libunionfs_utils.la
%{_libdir}/libunionfs_utils.so
%{_mandir}/man3/*

%files static
%defattr(644,root,root,755)
%{_libdir}/libunionfs_utils.a
