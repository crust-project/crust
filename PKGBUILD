# Maintainer: Juraj Kollár <mostypc7@gmail.com>
pkgname=crust-git
pkgver=b01.0.g7b73b7a   # Will be auto-generated
pkgrel=1
pkgdesc="Crust - Python package installed via pip"
arch=('any')
url="https://github.com/mostypc123/crust"
license=('MIT')
depends=('python' 'python-pip')
makedepends=('git' 'python-build' 'python-installer' 'python-wheel' 'python-setuptools')
source=("git+$url")
sha256sums=('SKIP')

pkgver() {
  cd "$srcdir/crust"
  git describe --long --tags 2>/dev/null | sed 's/[-]/./g' || \
  echo "r$(git rev-list --count HEAD).$(git rev-parse --short HEAD)"
}

build() {
  cd "$srcdir/crust"
  python -m build --wheel --no-isolation
}

package() {
  cd "$srcdir/crust"
  python -m installer --destdir="$pkgdir" dist/*.whl
}
