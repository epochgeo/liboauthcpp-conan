from conans import ConanFile, tools, CMake
from conan.tools.layout import cmake_layout


class LiboauthcppConan(ConanFile):
    name = "liboauthcpp"
    version = "0.1"

    # Optional metadata
    license = "MIT License"
    homepage = "https://github.com/sirikata/liboauthcpp"
    url = "https://github.com/conan-io/conan-center-index"
    description = "A pure C++ OAuth library"
    exports_sources = ["CMakeLists.txt", "src/*"]
    generators = "cmake"

    # Binary configuration
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False], "fPIC": [True, False]}
    default_options = {"shared": False, "fPIC": True}


    @property
    def _build_subfolder(self):
        return "build_subfolder"

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    def source(self):
        #self.run("git clone https://github.com/sirikata/liboauthcpp")
        url = "https://github.com/sirikata/liboauthcpp/archive/2893f1bf42e1dfd5acf0dd849519cf27ac9c7395.tar.gz"
        tools.get(url=url, strip_root=True, destination=self._source_subfolder)

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def build(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        cmake.build()

    def package(self):
        cmake = CMake(self)
        cmake.configure(build_folder=self._build_subfolder)
        cmake.install()
        # This is kind of a silly way to avoid distributing .so files but it works.
        if not self.options.shared:
            self.run(f"rm -f {self._build_subfolder}/lib/*.so*")

    def package_info(self):
        self.cpp_info.libs = ["oauthcpp"]
