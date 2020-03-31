import ops
import iopc

pkg_path = ""
output_dir = ""
tarball = ""
src_def_config = ""
dst_def_config = ""
build_dir = ""
build_module_dir = ""
initramfs_name = "initramfs.cpio.gz"
initramfs_file = ""
build_arch = ""
build_format = ""
image_path = ""
image_output_name = "linux_image"
dtb_output_name = "linux_dtb"
LINUX_VERSION = ""
jobs_count = ""
#LINUX_VERSION_FULL_STR="linux-4.3"
#LINUX_VERSION_FULL_STR="linux-4.1.42"

def set_global(args):
    global pkg_path
    global output_dir 
    global tarball
    global src_def_config
    global dst_def_config 
    global build_dir 
    global build_module_dir 
    global initramfs_file
    global build_arch
    global build_format
    global image_path
    global LINUX_VERSION
    global jobs_count
    global dtb_path
    pkg_args = args["pkg_args"]
    def_cfg_version = "default_" + pkg_args["config"] + ".config"
    LINUX_VERSION = pkg_args["version"]
    LINUX_VERSION_FULL_STR = "linux-" + LINUX_VERSION
    build_format = pkg_args["format"]
    pkg_path = args["pkg_path"]
    output_dir = args["output_path"]
    arch = ops.getEnv("ARCH_ALT")
    build_arch = ops.getEnv("ARCH")
    jobs_count = ops.getEnv("BUILD_JOBS_COUNT")
    tarball = ops.path_join(pkg_path, LINUX_VERSION_FULL_STR + ".tar.xz")
    build_dir = ops.path_join(output_dir, LINUX_VERSION_FULL_STR)
    src_def_config = ops.path_join(pkg_path, def_cfg_version)

    image_dir = ""
    if arch == "armel":
        image_dir = "arch/arm/boot/"
        if build_format == "uImage":
            image_path = image_dir + "uImage"
        else:
            image_path = image_dir + "zImage"
    elif arch == "x86_64":
        image_dir = "arch/x86/boot/"
        build_arch = "x86"
        image_path = image_dir + "bzImage"
    else:
        sys.exit(1)

    dtb_path = ""
    if "dtb" in pkg_args :
        device_tree_binary = pkg_args["dtb"]
        dtb_path = image_dir + "dts/" + device_tree_binary

    dst_def_config = ops.path_join(build_dir, ".config")
    initramfs_file = ops.path_join(iopc.getOutputRootDir(), initramfs_name)
    build_module_dir = ops.path_join(ops.path_join(iopc.getOutputRootDir(), "kernel_modules"), LINUX_VERSION)
    if jobs_count == "":
        jobs_count = "2"

def MAIN_ENV(args):
    set_global(args)

    ops.exportEnv(ops.setEnv("LINUXKERNELROOT", build_dir))
    ops.exportEnv(ops.setEnv("LINUXKERNELMODULEROOT", build_module_dir))

    return False

def MAIN_EXTRACT(args):
    set_global(args)
    ops.unTarXz(tarball, output_dir)
    #iopc.make_initramfs(iopc.getTargetRootfs(), iopc.getOutputRootFile(""))
    return True

def MAIN_PATCH(args, patch_group_name):
    set_global(args)
    for patch in iopc.get_patch_list(pkg_path, patch_group_name):
        if iopc.apply_patch(build_dir, patch):
            continue
        else:
            sys.exit(1)

    return True

def MAIN_CONFIGURE(args):
    set_global(args)

    ops.copyto(src_def_config, dst_def_config)
    ops.kbuild_config_replace(dst_def_config, "CONFIG_INITRAMFS_SOURCE", initramfs_name)

    return True

def MAIN_BUILD(args):
    set_global(args)

    ops.copyto(initramfs_file, build_dir)
    opt_format = ""

    jobs_count = ops.getEnv("BUILD_JOBS_COUNT")
    extra_conf = []
    extra_conf.append("ARCH=" + build_arch)
    extra_conf.append("-j" + jobs_count)
    if build_format == "uImage":
        opt_format = "uImage"
        extra_conf.append(opt_format)
    iopc.make(build_dir, extra_conf)

    '''
    extra_conf = []
    extra_conf.append("modules")
    extra_conf.append("ARCH=" + build_arch)
    iopc.make(build_dir, extra_conf)
    '''
    '''
    extra_conf = []
    extra_conf.append("ARCH=" + ops.getEnv("ARCH"))
    extra_conf.append("tarxz-pkg")
    iopc.make(build_dir, extra_conf)
    '''

    return False

def MAIN_INSTALL(args):
    set_global(args)

    ops.copyto(ops.path_join(build_dir, image_path), ops.path_join(iopc.getOutputRootDir(), image_output_name))

    print dtb_path
    print "ADAM"
    if dtb_path != "" :
        if ops.isExist(ops.path_join(build_dir, dtb_path)) :
            ops.copyto(ops.path_join(build_dir, dtb_path), ops.path_join(iopc.getOutputRootDir(), dtb_output_name))

    ops.mkdir(build_module_dir)
    ops.touch(ops.path_join(build_module_dir, "modules.dep"))
    '''
    extra_conf = []
    extra_conf.append("modules_install")
    extra_conf.append("ARCH=" + ops.getEnv("ARCH"))
    extra_conf.append("INSTALL_MOD_PATH=" + output_dir)
    iopc.make(build_dir, extra_conf)

    extra_conf = []
    extra_conf.append("firmware_install")
    extra_conf.append("ARCH=" + ops.getEnv("ARCH"))
    extra_conf.append("INSTALL_MOD_PATH=" + output_dir)
    iopc.make(build_dir, extra_conf)
    '''
    return False

def MAIN_SDKENV(args):
    set_global(args)

    return False

def MAIN_CLEAN_BUILD(args):
    set_global(args)

    return False

def MAIN(args):
    set_global(args)
    print "linux kernel"

