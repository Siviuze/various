from conans import ConanFile, CMake, tools


class ChibiosConan(ConanFile):
    name = "chibios"
    license = "GPL3/Apache2.0"
    author = "Giovanni Di Sirio  <And your email here>"
    url = "https://www.chibios.org"
    description = "ChibiOS is a complete development environment for embedded applications including RTOS, an HAL, peripheral drivers, support files and tools."
    topics = ("os", "hal")
    
    settings = "arch"
    options = {
        "board": [
            "arduino-nano", "arduino-uno", "arduino-mega", "arduino-mini", "digispark-attiny-167", "mt-db-x4",
            ""
            ],
        "familly": ["avr", "stm32"],
        "kernel": ["rt", "nil"]
        }
    default_options = {
        "kernel": "rt"
        }
    
    def export_sources(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            self.copy(patch["patch_file"])
    
    def config_options(self):
        pass
        
    def configure(self):
        familly = str(self.options.familly)
        board = str(self.options.board)
        kernel = str(self.options.kernel)
        self.board_path = ('demos/{familly}/{kernel}-{board}').format(familly=familly.upper(), kernel=kernel.upper(), board=board.upper())

    def source(self):
        tools.untargz('/home/leduc/Téléchargements/ChibiOS-ver21.11.2.tar.gz', strip_root=True, destination="sources")
        #tools.get(**self.conan_data['sources'][self.version], strip_root=True)

    def build(self):
        for patch in self.conan_data.get('patches', {}).get(self.version, []):
            print(patch)
            tools.patch(**patch)
            
        make_cmd = ('{make}' ' -j{cpucount}' ' -C sources/{board_path} USE_VERBOSE_COMPILE=yes lib').format(
                       make=tools.get_env('CONAN_MAKE_PROGRAM', tools.which('make')), cpucount=tools.cpu_count(), 
                       board_path=self.board_path)
        print(self.board_path)
        self.run(make_cmd)

        # Explicit way:
        # self.run('cmake %s/hello %s'
        #          % (self.source_folder, cmake.command_line))
        # self.run("cmake --build . %s" % cmake.build_config)

    def package(self):
        self.copy("*.h", dst="include", src="sources", excludes='*test*')
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["ch"]
        self.cpp_info.libdirs = ['lib']
        self.cpp_info.includedirs = [
            ('include/{board_path}/cfg').format(board_path=self.board_path),
            'include/os/license',
            'include/os/hal/include',
            
            'include/os/hal/boards/ARDUINO_NANO',
            
            'include/os/hal/ports/AVR/MEGA/ATMEGAxx',
            'include/os/hal/ports/AVR/MEGA/LLD/ADCv1',
            'include/os/hal/ports/AVR/MEGA/LLD/EXTv1',
            'include/os/hal/ports/AVR/MEGA/LLD/GPIOv1',
            'include/os/hal/ports/AVR/MEGA/LLD/I2Cv1',
            'include/os/hal/ports/AVR/MEGA/LLD/SPIv1',
            'include/os/hal/ports/AVR/MEGA/LLD/TIMv1',
            'include/os/hal/ports/AVR/MEGA/LLD/USARTv1',
            'include/os/hal/ports/AVR/MEGA/LLD/USBv1',

            'include/os/hal/osal/rt-nil',
            ('include/os/{kernel}/include').format(kernel=self.options.kernel),
            'include/os/oslib/include',
            'include/os/common/portability/GCC',

            'include/os/common/ports/AVR',
            'include/os/common/ports/AVR/compilers/GCC'
            ]
        print(self.cpp_info.includedirs)
