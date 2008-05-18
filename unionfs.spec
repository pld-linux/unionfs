# TODO
# - patch for vserver vfs_unlink
#
# Conditional build:
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_without	dist_kernel	# without distribution kernel
%bcond_with	verbose		# verbose build (V=1)
%bcond_without	vserver		# build with vserver patches

%ifarch sparc
%undefine	with_smp
%endif

%if %{without kernel}
%undefine	with_dist_kernel
%endif
%if "%{_alt_kernel}" != "%{nil}"
%undefine	with_userspace
%endif
%if %{without userspace}
# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0
%endif

#define		snap	20060916-2203
%define		rel    0.1
%define		pname	unionfs
Summary:	A Stackable Unification File System
Summary(pl.UTF-8):	Stakowalny, unifikujący system plików
Name:		%{pname}%{_alt_kernel}
Version:	1.3
Release:	%{?snap:0.%(echo %{snap} | tr - _).}%{rel}
License:	GPL v2
Group:		Base/Kernel
#Source0:	ftp://ftp.fsl.cs.sunysb.edu/pub/unionfs/snapshots/%{pname}-%{snap}.tar.gz
Source0:	ftp://ftp.fsl.cs.sunysb.edu/pub/unionfs/%{pname}-%{version}.tar.gz
# Source0-md5:	af5106f29fb0ddb12b028f522fa0463c
Patch0:		%{pname}-build.patch
#Patch1:		%{pname}-vserver.patch
URL:		http://www.filesystems.org/project-unionfs.html
%if %{with kernel} && %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.17
#BuildRequires:	kernel%{_alt_kernel}-module-build < 3:2.6.18
BuildRequires:	rpmbuild(macros) >= 1.330
%endif
BuildRequires:	libuuid-devel
BuildRoot:	%{tmpdir}/%{pname}-%{version}-root-%(id -u -n)

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

%package -n kernel%{_alt_kernel}-fs-unionfs
Summary:	Linux driver for unionfs
Summary(pl.UTF-8):	Sterownik Linuksa dla unionfs
Release:	%{rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel%{_alt_kernel}-fs-unionfs
Linux driver for unionfs.

%description -n kernel%{_alt_kernel}-fs-unionfs -l pl.UTF-8
Sterownik Linuksa dla unionfs.

%prep
%setup -q -n %{pname}-%{!?snap:%{version}}%{?snap:%{snap}}
%patch0 -p1
#%{?with_vserver:%patch1 -p1}

%build
%if %{with kernel}
%build_kernel_modules -m unionfs \
	EXTRACFLAGS="-DUNIONFS_NDEBUG -DUNIONFS_XATTR"
%endif

%if %{with userspace}
%{__make} utils \
	CC="%{__cc}" \
	UNIONFS_OPT_CFLAG="%{rpmcflags} %{rpmldflags}"
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with kernel}
%install_kernel_modules -m unionfs -d kernel/fs
%endif

%if %{with userspace}
%{__make} install-utils \
	PREFIX=$RPM_BUILD_ROOT%{_prefix} \
	MANDIR=$RPM_BUILD_ROOT%{_mandir}
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post -n kernel%{_alt_kernel}-fs-unionfs
%depmod %{_kernel_ver}

%postun -n kernel%{_alt_kernel}-fs-unionfs
%depmod %{_kernel_ver}

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS INSTALL README
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%endif

%if %{with kernel}
%files -n kernel%{_alt_kernel}-fs-unionfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/fs/*.ko*
%endif
