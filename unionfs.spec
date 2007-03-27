#
# Conditional build:
%bcond_without	kernel		# don't build kernel modules
%bcond_without	userspace	# don't build userspace programs
%bcond_without	dist_kernel	# without distribution kernel
%bcond_without	up		# don't build UP module
%bcond_without	smp		# don't build SMP module
%bcond_with	verbose		# verbose build (V=1)
%bcond_without	vserver		# build with vserver patches
%bcond_with	grsec_kernel	# build for kernel-grsecurity
#
%if %{without kernel}
%undefine	with_dist_kernel
%endif
#
%if %{with kernel} && %{with dist_kernel} && %{with grsec_kernel}
%define	alt_kernel	grsecurity
%endif
#
%ifarch sparc
%undefine	with_smp
%endif

#define		_snap	20060916-2203
%define         _rel    5
#
Summary:	A Stackable Unification File System
Summary(pl):	Stakowalny, unifikuj�cy system plik�w
Name:		unionfs
Version:	1.2
Release:	%{?_snap:0.%(echo %{_snap} | tr - _).}%{_rel}
License:	GPL v2
Group:		Base/Kernel
#Source0:	ftp://ftp.fsl.cs.sunysb.edu/pub/unionfs/snapshots/%{name}-%{_snap}.tar.gz
Source0:	ftp://ftp.fsl.cs.sunysb.edu/pub/unionfs/%{name}-%{version}.tar.gz
# Source0-md5:	2a8c6ef320efc43af91074ab47046f09
Patch0:		%{name}-build.patch
Patch1:		%{name}-vserver.patch
URL:		http://www.filesystems.org/project-unionfs.html
%if %{with kernel}
%if %{with dist_kernel}
BuildRequires:	kernel%{_alt_kernel}-module-build >= 3:2.6.16
BuildRequires:	kernel%{_alt_kernel}-module-build < 3:2.6.17
BuildRequires:	rpmbuild(macros) >= 1.326
%endif
BuildRequires:	libuuid-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Unionfs is a stackable unification file system, which can appear to
merge the contents of several directories (branches), while keeping
their physical content separate. Unionfs is useful for unified source
tree management, merged contents of split CD-ROM, merged separate
software package directories, data grids, and more. Unionfs allows any
mix of read-only and read-write branches, as well as insertion and
deletion of branches anywhere in the fan-out.

%description -l pl
Unionfs to stakowalny, unifikuj�cy system plik�w, potrafi�cy ��czy�
zawarto�� kilku katalog�w (ga��zi), zachowuj�c oddzielnie ich fizyczn�
zawarto��. Unionfs jest przydatny do zarz�dzania po��czonym drzewem
�r�de�, po��czon� zawarto�ci� podzielonych CD-ROM-�w, po��czonymi
oddzielnymi katalogami z pakietami program�w, tabelami danych itp.
Unionfs pozwala na dowolne mieszanie ga��zi tylko do odczytu oraz do
odczytu i zapisu, a tak�e wstawianie i usuwanie ga��zi w dowolnym
miejscu.

%package -n kernel%{_alt_kernel}-fs-unionfs
Summary:	Linux driver for unionfs
Summary(pl):	Sterownik Linuksa dla unionfs
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
Requires(post,postun):	/sbin/depmod
%if %{with dist_kernel}
%requires_releq_kernel_up
Requires(postun):	%releq_kernel_up
%endif

%description -n kernel%{_alt_kernel}-fs-unionfs
Linux driver for unionfs.

%description -n kernel%{_alt_kernel}-fs-unionfs -l pl
Sterownik Linuksa dla unionfs.

%package -n kernel%{_alt_kernel}-smp-fs-unionfs
Summary:	Linux SMP driver for unionfs
Summary(pl):	Sterownik Linuksa SMP dla unionfs
Release:	%{_rel}@%{_kernel_ver_str}
Group:		Base/Kernel
%if %{with dist_kernel}
%requires_releq_kernel_smp
Requires(postun):	%releq_kernel_smp
%endif
Provides:	kernel%{_alt_kernel}-unionfs = %{version}-%{_rel}@%{_kernel_ver_str}

%description -n kernel%{_alt_kernel}-smp-fs-unionfs
Linux SMP driver unionfs.

%description -n kernel%{_alt_kernel}-smp-fs-unionfs -l pl
Sterownik Linuksa SMP dla unionfs.

%prep
%setup -q %{?_snap:-n %{name}-%{_snap}}
%patch0 -p1
%{?with_vserver:%patch1 -p1}

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

%post -n kernel%{_alt_kernel}-smp-fs-unionfs
%depmod %{_kernel_ver}smp

%postun -n kernel%{_alt_kernel}-smp-fs-unionfs
%depmod %{_kernel_ver}smp

%if %{with userspace}
%files
%defattr(644,root,root,755)
%doc AUTHORS NEWS INSTALL README
%attr(755,root,root) %{_sbindir}/*
%{_mandir}/man?/*
%endif

%if %{with kernel}
%if %{with up} || %{without dist_kernel}
%files -n kernel%{_alt_kernel}-fs-unionfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}/kernel/fs/*.ko*
%endif

%if %{with smp} && %{with dist_kernel}
%files -n kernel%{_alt_kernel}-smp-fs-unionfs
%defattr(644,root,root,755)
/lib/modules/%{_kernel_ver}smp/kernel/fs/*.ko*
%endif
%endif
